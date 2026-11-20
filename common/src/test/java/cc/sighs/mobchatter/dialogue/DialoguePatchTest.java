package cc.sighs.mobchatter.dialogue;

import com.google.gson.JsonParser;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class DialoguePatchTest {
    private static final DialoguePatch.Line BASE = new DialoguePatch.Line("原句", "Base");

    private static DialoguePatch patch(String body) {
        return DialoguePatch.parse(JsonParser.parseString(body));
    }

    @Test
    void appendsDeduplicatesAndReplacesInLayerOrder() {
        Map<String, List<DialoguePatch.Line>> base = Map.of("walk", List.of(BASE), "idle", List.of(BASE));
        var appended = patch("""
                {"format_version":1,"scenarios":{"walk":{"operation":"append","lines":[
                {"zh":"原句","en":"Base"},{"zh":"追加","en":"Added"}]}}}
                """).apply(base);
        assertEquals(2, appended.get("walk").size());
        assertEquals(List.of(BASE), appended.get("idle"));
        var replaced = patch("""
                {"format_version":1,"scenarios":{"walk":{"operation":"replace","lines":[
                {"zh":"替换","en":"Replacement"}]}}}
                """).apply(appended);
        assertEquals(List.of(new DialoguePatch.Line("替换", "Replacement")), replaced.get("walk"));
        assertEquals(1, base.get("walk").size());
    }

    @Test
    void supportsNewEntitiesAndWholeEntityReplacement() {
        var added = patch("""
                {"format_version":1,"scenarios":{"spawn":{"operation":"append","lines":[
                {"zh":"你好","en":"Hello"}]}}}
                """).apply(Map.of());
        assertEquals(1, added.get("spawn").size());
        var cleared = patch("""
                {"format_version":1,"mode":"replace","scenarios":{}}
                """).apply(added);
        assertTrue(cleared.isEmpty());
    }

    @Test
    void disableBlocksFallbackAndHigherLayerCanReenable() {
        var base = Map.of("hurt", List.of(BASE));
        assertEquals(List.of(BASE), DialoguePatch.lines(base, "hurt.fire"));
        var disabled = patch("""
                {"format_version":1,"scenarios":{"hurt.fire":{"operation":"disable"}}}
                """).apply(base);
        assertTrue(DialoguePatch.lines(disabled, "hurt.fire").isEmpty());
        assertEquals(List.of(BASE), DialoguePatch.lines(disabled, "hurt.fall"));
        var enabled = patch("""
                {"format_version":1,"scenarios":{"hurt.fire":{"operation":"append","lines":[
                {"zh":"原句","en":"Base"}]}}}
                """).apply(disabled);
        assertEquals(List.of(BASE), DialoguePatch.lines(enabled, "hurt.fire"));
    }

    @Test
    void rejectsInvalidFilesBeforeApplyingAnyChanges() {
        for (String invalid : List.of(
                "{}", "null", "{\"format_version\":2,\"scenarios\":{}}",
                "{\"format_version\":\"1\",\"scenarios\":{}}",
                "{\"format_version\":1,\"mode\":\"unknown\",\"scenarios\":{}}",
                "{\"format_version\":1,\"scenarios\":{\"typo\":{\"operation\":\"disable\"}}}",
                "{\"format_version\":1,\"scenarios\":{\"walk\":{\"operation\":\"replace\",\"lines\":[]}}}",
                "{\"format_version\":1,\"scenarios\":{\"walk\":{\"operation\":\"disable\",\"lines\":[]}}}",
                "{\"format_version\":1,\"scenarios\":{\"walk\":{\"operation\":\"append\",\"lines\":[{\"zh\":\"好\"}]}}}")) {
            assertThrows(IllegalArgumentException.class, () -> patch(invalid), invalid);
        }
        var base = Map.of("walk", List.of(BASE));
        assertThrows(IllegalArgumentException.class, () -> patch("""
                {"format_version":1,"mode":"replace","scenarios":{
                "idle":{"operation":"disable"},"walk":{"operation":"wrong"}}}
                """));
        assertEquals(List.of(BASE), base.get("walk"));
    }
}
