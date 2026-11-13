package com.merrysnow.mobchatter.client;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;

import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Random;
import java.util.zip.GZIPInputStream;

/**
 * Loads the generated dialogue resource and serves random lines per entity/scenario.
 */
public final class DialogueManager {
    private static final ResourceLocation RESOURCE = new ResourceLocation("mobchatter", "dialogue.json.gz");
    private static final Gson GSON = new Gson();
    private static final Type RAW_TYPE =
            new TypeToken<Map<String, Map<String, List<List<String>>>>>() { }.getType();
    private static final Random RANDOM = new Random();

    private static Map<String, Map<String, List<String[]>>> data;

    private DialogueManager() {
    }

    public static void ensureLoaded() {
        if (data != null) {
            return;
        }
        Minecraft minecraft = Minecraft.getInstance();
        Optional<Resource> resource = minecraft.getResourceManager().getResource(RESOURCE);
        if (resource.isEmpty()) {
            data = Collections.emptyMap();
            return;
        }
        try (InputStreamReader reader = new InputStreamReader(
                new GZIPInputStream(resource.get().open()), StandardCharsets.UTF_8)) {
            Map<String, Map<String, List<List<String>>>> raw = GSON.fromJson(reader, RAW_TYPE);
            Map<String, Map<String, List<String[]>>> parsed = new HashMap<>();
            if (raw != null) {
                for (Map.Entry<String, Map<String, List<List<String>>>> mob : raw.entrySet()) {
                    Map<String, List<String[]>> scenarios = new HashMap<>();
                    for (Map.Entry<String, List<List<String>>> scenario : mob.getValue().entrySet()) {
                        List<String[]> lines = new ArrayList<>();
                        for (List<String> pair : scenario.getValue()) {
                            if (pair != null && pair.size() >= 2) {
                                lines.add(new String[]{pair.get(0), pair.get(1)});
                            }
                        }
                        if (!lines.isEmpty()) {
                            scenarios.put(scenario.getKey(), lines);
                        }
                    }
                    if (!scenarios.isEmpty()) {
                        parsed.put(mob.getKey(), scenarios);
                    }
                }
            }
            data = parsed;
        } catch (Exception exception) {
            data = Collections.emptyMap();
        }
    }

    public static String[] pick(String entityId, String scenario) {
        ensureLoaded();
        Map<String, List<String[]>> scenarios = data.get(entityId);
        if (scenarios == null) {
            return null;
        }
        List<String[]> lines = scenarios.get(scenario);
        if (lines == null && scenario.startsWith("hurt.")) {
            lines = scenarios.get("hurt");
        }
        if (lines == null || lines.isEmpty()) {
            return null;
        }
        return lines.get(RANDOM.nextInt(lines.size()));
    }

    public static int size() {
        ensureLoaded();
        return data.size();
    }
}
