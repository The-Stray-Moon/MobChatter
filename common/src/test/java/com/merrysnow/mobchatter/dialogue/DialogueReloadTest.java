package com.merrysnow.mobchatter.dialogue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.tukaani.xz.LZMA2Options;
import org.tukaani.xz.XZOutputStream;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

class DialogueReloadTest {
    @TempDir
    Path directory;

    private byte[] compressed(String json) throws IOException {
        Path file = directory.resolve("dialogue.json.xz");
        Files.createDirectories(file.getParent());
        try (var output = new XZOutputStream(Files.newOutputStream(file), new LZMA2Options())) {
            output.write(json.getBytes(StandardCharsets.UTF_8));
        }
        return Files.readAllBytes(file);
    }

    private static DialogueResource patch(String entity, String pack, String json) {
        return new DialogueResource(entity, pack, json);
    }

    private static DialogueResourceSource source(String baseSource, byte[] base, List<DialogueResource> patches) {
        return new DialogueResourceSource() {
            @Override
            public byte[] base() {
                return base;
            }

            @Override
            public String baseSource() {
                return baseSource;
            }

            @Override
            public List<DialogueResource> patches() {
                return patches;
            }
        };
    }

    @Test
    void mergesOrderedPatchesAndRestoresTheBaseAfterPackRemoval() throws Exception {
        byte[] base = compressed("{\"minecraft:cow\":{\"walk\":[[\"原句\",\"Base\"]],"
                + "\"hurt\":[[\"疼\",\"Ouch\"]]}}");
        List<DialogueResource> lowAndHigh = List.of(
                patch("minecraft:cow", "low", """
                        {"format_version":1,"scenarios":{"walk":{"operation":"append","lines":[
                        {"zh":"追加","en":"Added"}]}}}
                        """),
                patch("minecraft:cow", "high", """
                        {"format_version":1,"scenarios":{"walk":{"operation":"replace","lines":[
                        {"zh":"覆盖","en":"Override"}]},"hurt.fire":{"operation":"disable"}}}
                        """),
                patch("example:nested/new_mob", "high", """
                        {"format_version":1,"scenarios":{"spawn":{"operation":"append","lines":[
                        {"zh":"新增","en":"New"}]}}}
                        """),
                patch("minecraft:cow", "broken", "{broken"));
        AtomicInteger warnings = new AtomicInteger();
        DialogueLoader.Result loaded = DialogueLoader.load(
                source("base", base, lowAndHigh), message -> warnings.incrementAndGet());
        DialogueStore.publish(loaded.data());
        assertEquals(3, loaded.patches());
        assertEquals(1, loaded.failed());
        assertEquals(1, warnings.get());
        assertEquals(1, DialogueStore.snapshot().get("minecraft:cow").get("walk").size());
        assertArrayEquals(new String[]{"覆盖", "Override"}, DialogueStore.pick("minecraft:cow", "walk", 0));
        assertNull(DialogueStore.pick("minecraft:cow", "hurt.fire", 0));
        assertArrayEquals(new String[]{"疼", "Ouch"}, DialogueStore.pick("minecraft:cow", "hurt.fall", 0));
        assertArrayEquals(new String[]{"新增", "New"}, DialogueStore.pick("example:nested/new_mob", "spawn", 0));

        DialogueLoader.Result restored = DialogueLoader.load(source("base", base, List.of()), message -> { });
        DialogueStore.publish(restored.data());
        assertEquals(1, DialogueStore.size());
        assertTrue(DialogueStore.isSupported("minecraft:cow"));
        assertFalse(DialogueStore.isSupported("example:nested/new_mob"));
        assertArrayEquals(new String[]{"原句", "Base"}, DialogueStore.pick("minecraft:cow", "walk", 0));
        assertNull(DialogueStore.pick("example:nested/new_mob", "spawn", 0));
    }

    @Test
    void brokenBaseFailsWithoutPublishingPartialData() throws Exception {
        DialogueStore.publish(java.util.Map.of("minecraft:cow", java.util.Map.of("walk", List.of(
                new DialoguePatch.Line("原句", "Base")))));
        assertThrows(IllegalStateException.class, () -> DialogueLoader.load(
                source("base", "not xz".getBytes(StandardCharsets.UTF_8), List.of()), message -> { }));
        assertEquals(1, DialogueStore.size());
    }

    @Test
    void serverSeedSelectsSameLineAcrossReloadsAndUnrelatedCalls() throws Exception {
        var lines = List.of(
                new DialoguePatch.Line("甲", "A"),
                new DialoguePatch.Line("乙", "B"),
                new DialoguePatch.Line("丙", "C"));
        DialogueStore.publish(java.util.Map.of("minecraft:cow",
                java.util.Map.of("walk", lines, "hurt", lines)));
        List<String[]> results = new ArrayList<>();
        for (long seed : new long[]{0, 1, 2, -1, Long.MIN_VALUE, Long.MAX_VALUE}) {
            String[] firstClient = DialogueStore.pick("minecraft:cow", "walk", seed);
            DialogueStore.pick("minecraft:cow", "hurt", 93);
            String[] secondClient = DialogueStore.pick("minecraft:cow", "walk", seed);
            assertArrayEquals(firstClient, secondClient);
            assertEquals(lines.get(Math.floorMod(seed, lines.size())).zh(), firstClient[0]);
            assertArrayEquals(firstClient, DialogueStore.pick("minecraft:cow", "hurt.fire", seed));
            results.add(firstClient);
        }
        assertEquals(6, results.size());
    }
}
