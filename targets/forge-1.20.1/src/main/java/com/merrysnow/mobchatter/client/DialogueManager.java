package com.merrysnow.mobchatter.client;

import com.google.gson.Gson;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;
import com.merrysnow.mobchatter.dialogue.DialoguePatch;
import com.merrysnow.mobchatter.dialogue.DialoguePatch.Line;
import com.mojang.logging.LogUtils;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;
import org.tukaani.xz.XZInputStream;

import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class DialogueManager extends SimplePreparableReloadListener<Map<String, Map<String, List<Line>>>> {
    private static final ResourceLocation RESOURCE = new ResourceLocation("mobchatter", "dialogue.json.xz");
    private static final String DIRECTORY = "mobchatter/dialogue/";
    private static final Gson GSON = new Gson();
    private static final Type RAW_TYPE =
            new TypeToken<Map<String, Map<String, List<List<String>>>>>() { }.getType();
    private static final Logger LOGGER = LogUtils.getLogger();
    private static volatile Map<String, Map<String, List<Line>>> data = Map.of();

    @Override
    protected Map<String, Map<String, List<Line>>> prepare(ResourceManager manager, ProfilerFiller profiler) {
        long started = System.nanoTime();
        Map<String, Map<String, List<Line>>> merged = new HashMap<>();
        Resource base = manager.getResource(RESOURCE)
                .orElseThrow(() -> new IllegalStateException("Missing dialogue base: " + RESOURCE));
        try (InputStreamReader reader = new InputStreamReader(
                new XZInputStream(base.open()), StandardCharsets.UTF_8)) {
            Map<String, Map<String, List<List<String>>>> raw = GSON.fromJson(reader, RAW_TYPE);
            if (raw == null || raw.isEmpty()) {
                throw new IllegalArgumentException("Empty dialogue base");
            }
            for (var mob : raw.entrySet()) {
                if (!ResourceLocation.isValidResourceLocation(mob.getKey())) {
                    throw new IllegalArgumentException("Invalid entity ID: " + mob.getKey());
                }
                Map<String, List<Line>> scenarios = new HashMap<>();
                for (var scenario : mob.getValue().entrySet()) {
                    if (!DialoguePatch.SCENARIOS.contains(scenario.getKey())) {
                        throw new IllegalArgumentException("Unknown scenario: " + scenario.getKey());
                    }
                    List<Line> lines = new ArrayList<>();
                    for (List<String> pair : scenario.getValue()) {
                        if (pair == null || pair.size() != 2 || pair.get(0) == null || pair.get(1) == null
                                || pair.get(0).isBlank() || pair.get(1).isBlank()) {
                            throw new IllegalArgumentException("Invalid line for " + mob.getKey() + "/" + scenario.getKey());
                        }
                        lines.add(new Line(pair.get(0), pair.get(1)));
                    }
                    scenarios.put(scenario.getKey(), List.copyOf(lines));
                }
                merged.put(mob.getKey(), Map.copyOf(scenarios));
            }
        } catch (Exception exception) {
            throw new IllegalStateException("Failed to load " + RESOURCE + " from " + base.sourcePackId(), exception);
        }
        int loaded = 0;
        int failed = 0;
        var stacks = manager.listResourceStacks("mobchatter/dialogue", id -> id.getPath().endsWith(".json"));
        for (var entry : stacks.entrySet()) {
            ResourceLocation location = entry.getKey();
            String path = location.getPath();
            String entity = location.getNamespace() + ":" + path.substring(DIRECTORY.length(), path.length() - 5);
            for (Resource resource : entry.getValue()) {
                try (var reader = resource.openAsReader()) {
                    if (!ResourceLocation.isValidResourceLocation(entity)) {
                        throw new IllegalArgumentException("Invalid entity ID: " + entity);
                    }
                    DialoguePatch patch = DialoguePatch.parse(JsonParser.parseReader(reader));
                    merged.put(entity, patch.apply(merged.getOrDefault(entity, Map.of())));
                    loaded++;
                } catch (Exception exception) {
                    failed++;
                    LOGGER.warn("Skipping dialogue patch {} from {}: {}", location, resource.sourcePackId(),
                            exception.getMessage());
                }
            }
        }
        long lines = merged.values().stream().flatMap(m -> m.values().stream()).mapToLong(List::size).sum();
        LOGGER.info("Dialogue prepared: {} entities, {} lines, {} patches, {} failed, {} ms",
                merged.size(), lines, loaded, failed, (System.nanoTime() - started) / 1_000_000);
        return Map.copyOf(merged);
    }

    @Override
    protected void apply(Map<String, Map<String, List<Line>>> prepared, ResourceManager manager,
                         ProfilerFiller profiler) {
        data = prepared;
        DialogueController.clear();
    }

    public static String[] pick(String entityId, String scenario, long seed) {
        Map<String, List<Line>> scenarios = data.get(entityId);
        if (scenarios == null) {
            return null;
        }
        List<Line> lines = DialoguePatch.lines(scenarios, scenario);
        if (lines.isEmpty()) {
            return null;
        }
        Line line = lines.get(Math.floorMod(seed, lines.size()));
        return new String[]{line.zh(), line.en()};
    }

    public static boolean isSupported(String entityId) {
        return data.containsKey(entityId);
    }

    public static int size() {
        return data.size();
    }
}
