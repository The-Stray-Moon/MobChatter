package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.dialogue.DialogueLoader;
import cc.sighs.mobchatter.dialogue.DialogueResource;
import cc.sighs.mobchatter.dialogue.DialogueResourceSource;
import cc.sighs.mobchatter.dialogue.DialogueStore;
import com.mojang.logging.LogUtils;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public final class DialogueManager extends SimplePreparableReloadListener<DialogueLoader.Result> {
    private static final ResourceLocation RESOURCE =
            ResourceLocation.fromNamespaceAndPath("mobchatter", "dialogue.json.xz");
    private static final String DIRECTORY = "mobchatter/dialogue/";
    private static final Logger LOGGER = LogUtils.getLogger();

    @Override
    protected DialogueLoader.Result prepare(ResourceManager manager, ProfilerFiller profiler) {
        long started = System.nanoTime();
        DialogueLoader.Result result;
        try {
            result = DialogueLoader.load(new ManagerSource(manager),
                    message -> LOGGER.warn(message));
        } catch (IOException exception) {
            throw new IllegalStateException("Failed to read dialogue resources", exception);
        }
        LOGGER.info("Dialogue prepared: {} entities, {} lines, {} patches, {} failed, {} ms",
                result.data().size(), result.lines(), result.patches(), result.failed(),
                (System.nanoTime() - started) / 1_000_000);
        return result;
    }

    @Override
    protected void apply(DialogueLoader.Result prepared, ResourceManager manager, ProfilerFiller profiler) {
        DialogueStore.publish(prepared.data());
        ClientDialogueController.clear();
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
                                new String(stream.readAllBytes(), java.nio.charset.StandardCharsets.UTF_8)));
                    } catch (IOException exception) {
                        LOGGER.warn("Skipping unreadable dialogue patch {}: {}", location, exception.getMessage());
                    }
                }
            }
            return patches;
        }
    }
}
