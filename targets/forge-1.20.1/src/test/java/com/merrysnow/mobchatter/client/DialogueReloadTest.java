package com.merrysnow.mobchatter.client;

import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.PathPackResources;
import net.minecraft.server.packs.resources.MultiPackResourceManager;
import net.minecraft.util.profiling.InactiveProfiler;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.tukaani.xz.LZMA2Options;
import org.tukaani.xz.XZOutputStream;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DialogueReloadTest {
    @TempDir
    Path directory;

    private PathPackResources pack(String name) throws Exception {
        Path root = directory.resolve(name);
        Files.createDirectories(root);
        return new PathPackResources(name, root, false);
    }

    private void write(String pack, String resource, String content) throws Exception {
        Path path = directory.resolve(pack).resolve("assets").resolve(resource);
        Files.createDirectories(path.getParent());
        Files.writeString(path, content);
    }

    @Test
    void loadsActualResourceStacksAndRestoresBaseAfterPackRemoval() throws Exception {
        var base = pack("base");
        var low = pack("low");
        var high = pack("high");
        var broken = pack("broken");
        Path compressed = directory.resolve("base/assets/mobchatter/dialogue.json.xz");
        Files.createDirectories(compressed.getParent());
        try (var output = new XZOutputStream(Files.newOutputStream(compressed), new LZMA2Options())) {
            output.write("{\"minecraft:cow\":{\"walk\":[[\"原句\",\"Base\"]],\"hurt\":[[\"疼\",\"Ouch\"]]}}"
                    .getBytes(StandardCharsets.UTF_8));
        }
        String path = "minecraft/mobchatter/dialogue/cow.json";
        write("low", path, """
                {"format_version":1,"scenarios":{"walk":{"operation":"append","lines":[
                {"zh":"追加","en":"Added"}]}}}
                """);
        write("high", path, """
                {"format_version":1,"scenarios":{"walk":{"operation":"replace","lines":[
                {"zh":"覆盖","en":"Override"}]},"hurt.fire":{"operation":"disable"}}}
                """);
        write("high", "example/mobchatter/dialogue/nested/new_mob.json", """
                {"format_version":1,"scenarios":{"spawn":{"operation":"append","lines":[
                {"zh":"新增","en":"New"}]}}}
                """);
        write("broken", path, "{broken");
        var listener = new DialogueManager();
        try (var manager = new MultiPackResourceManager(PackType.CLIENT_RESOURCES, List.of(base, low))) {
            var prepared = listener.prepare(manager, InactiveProfiler.INSTANCE);
            assertEquals(2, prepared.get("minecraft:cow").get("walk").size());
        }
        try (var manager = new MultiPackResourceManager(PackType.CLIENT_RESOURCES, List.of(base, low, high, broken))) {
            var prepared = listener.prepare(manager, InactiveProfiler.INSTANCE);
            listener.apply(prepared, manager, InactiveProfiler.INSTANCE);
            assertArrayEquals(new String[]{"覆盖", "Override"}, DialogueManager.pick("minecraft:cow", "walk", 0));
            assertNull(DialogueManager.pick("minecraft:cow", "hurt.fire", 0));
            assertArrayEquals(new String[]{"疼", "Ouch"}, DialogueManager.pick("minecraft:cow", "hurt.fall", 0));
            assertArrayEquals(new String[]{"新增", "New"}, DialogueManager.pick("example:nested/new_mob", "spawn", 0));
        }
        try (var manager = new MultiPackResourceManager(PackType.CLIENT_RESOURCES, List.of(base))) {
            listener.apply(listener.prepare(manager, InactiveProfiler.INSTANCE), manager, InactiveProfiler.INSTANCE);
            assertEquals(1, DialogueManager.size());
            assertTrue(DialogueManager.isSupported("minecraft:cow"));
            assertFalse(DialogueManager.isSupported("example:nested/new_mob"));
            assertArrayEquals(new String[]{"原句", "Base"}, DialogueManager.pick("minecraft:cow", "walk", 0));
            assertNull(DialogueManager.pick("example:nested/new_mob", "spawn", 0));
        }
        Files.writeString(compressed, "not xz");
        try (var manager = new MultiPackResourceManager(PackType.CLIENT_RESOURCES, List.of(base))) {
            assertThrows(IllegalStateException.class, () -> listener.prepare(manager, InactiveProfiler.INSTANCE));
            assertEquals(1, DialogueManager.size());
        }
    }

    @Test
    void serverSeedSelectsSameLineAcrossReloadsAndUnrelatedCalls() {
        var lines = List.of(
                new com.merrysnow.mobchatter.dialogue.DialoguePatch.Line("甲", "A"),
                new com.merrysnow.mobchatter.dialogue.DialoguePatch.Line("乙", "B"),
                new com.merrysnow.mobchatter.dialogue.DialoguePatch.Line("丙", "C"));
        var snapshot = java.util.Map.of("minecraft:cow", java.util.Map.of("walk", lines, "hurt", lines));
        var listener = new DialogueManager();
        var manager = net.minecraft.server.packs.resources.ResourceManager.Empty.INSTANCE;
        for (long seed : new long[]{0, 1, 2, -1, Long.MIN_VALUE, Long.MAX_VALUE}) {
            listener.apply(snapshot, manager, InactiveProfiler.INSTANCE);
            String[] firstClient = DialogueManager.pick("minecraft:cow", "walk", seed);
            DialogueManager.pick("minecraft:cow", "hurt", 93);
            listener.apply(snapshot, manager, InactiveProfiler.INSTANCE);
            String[] secondClient = DialogueManager.pick("minecraft:cow", "walk", seed);
            assertArrayEquals(firstClient, secondClient);
            assertEquals(lines.get(Math.floorMod(seed, lines.size())).zh(), firstClient[0]);
            assertArrayEquals(firstClient, DialogueManager.pick("minecraft:cow", "hurt.fire", seed));
        }
    }
}
