package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.dialogue.DialogueLoader;
import com.merrysnow.mobchatter.dialogue.DialogueResource;
import com.merrysnow.mobchatter.dialogue.DialogueResourceSource;
import com.merrysnow.mobchatter.dialogue.DialogueStore;
import com.mojang.logging.LogUtils;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public final class DialogueManager extends SimplePreparableReloadListener<DialogueLoader.Result> {
    private static final ResourceLocation RESOURCE = new ResourceLocation("mobchatter", "dialogue.json.xz");
    private static final String DIRECTORY = "mobchatter/dialogue/";
    private static final Logger LOGGER = LogUtils.getLogger();

    @Override
    protected DialogueLoader.Result prepare(ResourceManager manager, ProfilerFiller profiler) {
        long started = System.nanoTime();
        DialogueLoader.Result result;
        try {
            result = DialogueLoader.load(new ManagerSource(manager), message -> LOGGER.warn(message));
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
            List<Resource> resources = manager.getResources(RESOURCE);
            if (resources.isEmpty()) {
                throw new IllegalStateException("Missing dialogue base: " + RESOURCE);
            }
            Resource resource = resources.get(resources.size() - 1);
            try (var stream = resource.getInputStream()) {
                return stream.readAllBytes();
            }
        }

        @Override
        public String baseSource() {
            try {
                List<Resource> resources = manager.getResources(RESOURCE);
                return resources.isEmpty() ? "unknown"
                        : resources.get(resources.size() - 1).getSourceName();
            } catch (IOException exception) {
                return "unknown";
            }
        }

        @Override
        public List<DialogueResource> patches() throws IOException {
            List<DialogueResource> patches = new ArrayList<>();
            for (ResourceLocation location : manager.listResources(
                    "mobchatter/dialogue", path -> path.endsWith(".json"))) {
                String path = location.getPath();
                String entity = location.getNamespace() + ":" + path.substring(DIRECTORY.length(), path.length() - 5);
                for (Resource resource : manager.getResources(location)) {
                    try (var stream = resource.getInputStream()) {
                        patches.add(new DialogueResource(entity, resource.getSourceName(),
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
