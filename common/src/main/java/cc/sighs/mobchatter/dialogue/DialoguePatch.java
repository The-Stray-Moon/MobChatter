package cc.sighs.mobchatter.dialogue;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public record DialoguePatch(boolean replace, Map<String, Change> scenarios) {
    public static final Set<String> SCENARIOS = Set.of(
            "walk", "idle", "look_player", "hurt", "tempted", "collide", "mate", "pickup",
            "target_acquire", "targeting", "melee_attack", "spawn", "hurt.fire", "hurt.fall",
            "hurt.drown", "hurt.explosion", "hurt.projectile", "hurt.magic", "hurt.starvation",
            "hurt.lightning", "hurt.void");

    public record Line(String zh, String en) { }

    public record Change(String operation, List<Line> lines) { }

    public static DialoguePatch parse(JsonElement json) {
        JsonObject root = object(json, "$", Set.of("format_version", "mode", "scenarios"));
        JsonElement version = root.get("format_version");
        if (version == null || !version.isJsonPrimitive() || !version.getAsJsonPrimitive().isNumber()
                || !version.getAsString().equals("1")) {
            throw new IllegalArgumentException("$.format_version: expected 1");
        }
        String mode = root.has("mode") ? text(root.get("mode"), "$.mode") : "merge";
        if (!mode.equals("merge") && !mode.equals("replace")) {
            throw new IllegalArgumentException("$.mode: expected merge or replace");
        }
        JsonObject scenarios = object(root.get("scenarios"), "$.scenarios", SCENARIOS);
        Map<String, Change> changes = new HashMap<>();
        for (Map.Entry<String, JsonElement> entry : scenarios.entrySet()) {
            String path = "$.scenarios." + entry.getKey();
            JsonObject value = object(entry.getValue(), path, Set.of("operation", "lines"));
            String operation = text(value.get("operation"), path + ".operation");
            List<Line> lines = new ArrayList<>();
            if (operation.equals("disable")) {
                if (value.has("lines")) {
                    throw new IllegalArgumentException(path + ".lines: not allowed for disable");
                }
            } else if (operation.equals("append") || operation.equals("replace")) {
                JsonElement array = value.get("lines");
                if (array == null || !array.isJsonArray() || array.getAsJsonArray().size() == 0) {
                    throw new IllegalArgumentException(path + ".lines: expected non-empty array");
                }
                int index = 0;
                for (JsonElement line : array.getAsJsonArray()) {
                    String linePath = path + ".lines[" + index++ + "]";
                    JsonObject pair = object(line, linePath, Set.of("zh", "en"));
                    lines.add(new Line(text(pair.get("zh"), linePath + ".zh"),
                            text(pair.get("en"), linePath + ".en")));
                }
            } else {
                throw new IllegalArgumentException(path + ".operation: expected append, replace or disable");
            }
            changes.put(entry.getKey(), new Change(operation, List.copyOf(lines)));
        }
        return new DialoguePatch(mode.equals("replace"), Map.copyOf(changes));
    }

    public Map<String, List<Line>> apply(Map<String, List<Line>> previous) {
        Map<String, List<Line>> result = replace ? new HashMap<>() : new HashMap<>(previous);
        scenarios.forEach((scenario, change) -> {
            LinkedHashSet<Line> lines = new LinkedHashSet<>();
            if (change.operation().equals("append")) {
                lines.addAll(result.getOrDefault(scenario, List.of()));
            }
            lines.addAll(change.lines());
            result.put(scenario, List.copyOf(lines));
        });
        return Map.copyOf(result);
    }

    public static List<Line> lines(Map<String, List<Line>> scenarios, String scenario) {
        List<Line> lines = scenarios.get(scenario);
        if (lines == null && scenario.startsWith("hurt.")) {
            lines = scenarios.get("hurt");
        }
        return lines == null ? List.of() : lines;
    }

    private static JsonObject object(JsonElement value, String path, Set<String> allowed) {
        if (value == null || !value.isJsonObject()) {
            throw new IllegalArgumentException(path + ": expected object");
        }
        JsonObject object = value.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!allowed.contains(key)) {
                throw new IllegalArgumentException(path + "." + key + ": unknown field or scenario");
            }
        }
        return object;
    }

    private static String text(JsonElement value, String path) {
        if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString()
                || value.getAsString().isBlank()) {
            throw new IllegalArgumentException(path + ": expected non-empty string");
        }
        return value.getAsString();
    }
}
