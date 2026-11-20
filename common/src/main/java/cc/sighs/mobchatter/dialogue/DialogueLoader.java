package cc.sighs.mobchatter.dialogue;

import com.google.gson.Gson;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;
import cc.sighs.mobchatter.dialogue.DialoguePatch.Line;
import org.tukaani.xz.XZInputStream;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Parses the base XZ dialogue library and applies the ordered resource-pack
 * patch stack.
 *
 * <p>A broken patch is skipped atomically; a broken base library aborts the
 * whole reload. Both behaviours are part of the documented resource-pack
 * contract.</p>
 */
public final class DialogueLoader {
    private static final Gson GSON = new Gson();
    private static final Type RAW_TYPE =
            new TypeToken<Map<String, Map<String, List<List<String>>>>>() { }.getType();

    private DialogueLoader() {
    }

    public static Result load(DialogueResourceSource source, Consumer<String> warning) throws IOException {
        byte[] baseBytes = source.base();
        Map<String, Map<String, List<Line>>> merged = parseBase(baseBytes, source.baseSource());
        int loaded = 0;
        int failed = 0;
        for (DialogueResource resource : source.patches()) {
            try {
                if (!DialogueIds.isValid(resource.entityId())) {
                    throw new IllegalArgumentException("Invalid entity ID: " + resource.entityId());
                }
                DialoguePatch patch = DialoguePatch.parse(JsonParser.parseString(resource.json()));
                merged.put(resource.entityId(),
                        patch.apply(merged.getOrDefault(resource.entityId(), Map.of())));
                loaded++;
            } catch (Exception exception) {
                failed++;
                warning.accept("Skipping dialogue patch " + resource.entityId()
                        + " from " + resource.source() + ": " + exception.getMessage());
            }
        }
        Map<String, Map<String, List<Line>>> snapshot = immutable(merged);
        long lines = snapshot.values().stream()
                .flatMap(scenarios -> scenarios.values().stream())
                .mapToLong(List::size)
                .sum();
        return new Result(snapshot, loaded, failed, lines);
    }

    private static Map<String, Map<String, List<Line>>> parseBase(byte[] bytes, String source) {
        try (InputStreamReader reader = new InputStreamReader(
                new XZInputStream(new ByteArrayInputStream(bytes)), StandardCharsets.UTF_8)) {
            Map<String, Map<String, List<List<String>>>> raw = GSON.fromJson(reader, RAW_TYPE);
            if (raw == null || raw.isEmpty()) {
                throw new IllegalArgumentException("Empty dialogue base");
            }
            Map<String, Map<String, List<Line>>> merged = new HashMap<>();
            for (Map.Entry<String, Map<String, List<List<String>>>> mob : raw.entrySet()) {
                if (!DialogueIds.isValid(mob.getKey())) {
                    throw new IllegalArgumentException("Invalid entity ID: " + mob.getKey());
                }
                if (mob.getValue() == null) {
                    throw new IllegalArgumentException("Missing scenarios for " + mob.getKey());
                }
                Map<String, List<Line>> scenarios = new HashMap<>();
                for (Map.Entry<String, List<List<String>>> scenario : mob.getValue().entrySet()) {
                    if (!DialoguePatch.SCENARIOS.contains(scenario.getKey())) {
                        throw new IllegalArgumentException("Unknown scenario: " + scenario.getKey());
                    }
                    List<Line> lines = new ArrayList<>();
                    for (List<String> pair : scenario.getValue()) {
                        if (pair == null || pair.size() != 2 || pair.get(0) == null || pair.get(1) == null
                                || pair.get(0).isBlank() || pair.get(1).isBlank()) {
                            throw new IllegalArgumentException("Invalid line for "
                                    + mob.getKey() + "/" + scenario.getKey());
                        }
                        lines.add(new Line(pair.get(0), pair.get(1)));
                    }
                    scenarios.put(scenario.getKey(), List.copyOf(lines));
                }
                merged.put(mob.getKey(), Map.copyOf(scenarios));
            }
            return merged;
        } catch (Exception exception) {
            throw new IllegalStateException("Failed to load dialogue base from " + source, exception);
        }
    }

    private static Map<String, Map<String, List<Line>>> immutable(Map<String, Map<String, List<Line>>> merged) {
        Map<String, Map<String, List<Line>>> copy = new HashMap<>();
        merged.forEach((entity, scenarios) -> copy.put(entity, Map.copyOf(scenarios)));
        return Map.copyOf(copy);
    }

    public record Result(Map<String, Map<String, List<Line>>> data,
                         int patches, int failed, long lines) {
    }
}
