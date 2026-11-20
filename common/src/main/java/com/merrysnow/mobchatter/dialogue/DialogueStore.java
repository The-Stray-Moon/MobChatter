package com.merrysnow.mobchatter.dialogue;

import com.merrysnow.mobchatter.dialogue.DialoguePatch.Line;

import java.util.List;
import java.util.Map;

/**
 * Immutable client snapshot of merged dialogue data.
 *
 * <p>Selection is deterministic for a server-provided seed: clients with the
 * same line library and order show the same line and never roll their own
 * random values.</p>
 */
public final class DialogueStore {
    private static volatile Map<String, Map<String, List<Line>>> data = Map.of();

    private DialogueStore() {
    }

    public static void publish(Map<String, Map<String, List<Line>>> snapshot) {
        data = Map.copyOf(snapshot);
    }

    public static Map<String, Map<String, List<Line>>> snapshot() {
        return data;
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
