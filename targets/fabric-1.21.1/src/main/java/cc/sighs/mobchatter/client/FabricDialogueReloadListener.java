package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.MobChatterCommon;
import cc.sighs.mobchatter.dialogue.DialogueLoader;
import cc.sighs.mobchatter.dialogue.DialogueResource;
import cc.sighs.mobchatter.dialogue.DialogueResourceSource;
import cc.sighs.mobchatter.dialogue.DialogueStore;
import com.mojang.logging.LogUtils;
import net.fabricmc.fabric.api.resource.IdentifiableResourceReloadListener;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.PreparableReloadListener;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.Executor;

public final class FabricDialogueReloadListener implements IdentifiableResourceReloadListener {
    private static final ResourceLocation ID =
            ResourceLocation.tryParse(MobChatterCommon.MOD_ID + ":dialogue");
    private static final ResourceLocation RESOURCE =
            ResourceLocation.tryParse(MobChatterCommon.MOD_ID + ":dialogue.json.xz");
    private static final String DIRECTORY = "mobchatter/dialogue/";
    private static final Logger LOGGER = LogUtils.getLogger();

    @Override
    public ResourceLocation getFabricId() {
        return ID;
    }

    @Override
    public CompletableFuture<Void> reload(PreparableReloadListener.PreparationBarrier barrier,
                                          ResourceManager manager, ProfilerFiller prepareProfiler,
                                          ProfilerFiller applyProfiler, Executor prepareExecutor,
                                          Executor applyExecutor) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return DialogueLoader.load(new ManagerSource(manager), LOGGER::warn);
            } catch (IOException exception) {
                throw new CompletionException(exception);
            }
        }, prepareExecutor).thenCompose(barrier::wait).thenAcceptAsync(result -> {
            DialogueStore.publish(result.data());
            ClientDialogueController.clear();
            LOGGER.info("Dialogue prepared: {} entities, {} lines, {} patches, {} failed",
                    result.data().size(), result.lines(), result.patches(), result.failed());
        }, applyExecutor);
    }

    private record ManagerSource(ResourceManager manager) implements DialogueResourceSource {
        @Override
        public byte[] base() throws IOException {
            Resource resource = manager.getResource(RESOURCE)
                    .orElseThrow(() -> new IllegalStateException("Missing dialogue base: " + RESOURCE));
            try (var stream = resource.open()) {
                return stream.readAllBytes();
            }
        }

        @Override
        public String baseSource() {
            return manager.getResource(RESOURCE)
                    .orElseThrow(() -> new IllegalStateException("Missing dialogue base: " + RESOURCE))
                    .sourcePackId();
        }

        @Override
        public List<DialogueResource> patches() {
            List<DialogueResource> patches = new ArrayList<>();
            var stacks = manager.listResourceStacks("mobchatter/dialogue", id -> id.getPath().endsWith(".json"));
            for (var entry : stacks.entrySet()) {
                ResourceLocation location = entry.getKey();
                String path = location.getPath();
                String entity = location.getNamespace() + ":" + path.substring(DIRECTORY.length(), path.length() - 5);
                for (Resource resource : entry.getValue()) {
                    try (var stream = resource.open()) {
                        patches.add(new DialogueResource(entity, resource.sourcePackId(),
                                new String(stream.readAllBytes(), StandardCharsets.UTF_8)));
                    } catch (IOException exception) {
                        LOGGER.warn("Skipping unreadable dialogue patch {}: {}", location, exception.getMessage());
                    }
                }
            }
            return patches;
        }
    }
}
