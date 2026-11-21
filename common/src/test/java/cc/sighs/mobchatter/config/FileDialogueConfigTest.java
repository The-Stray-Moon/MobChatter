package cc.sighs.mobchatter.config;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

class FileDialogueConfigTest {
    @TempDir
    Path directory;

    @Test
    void writesAndReadsTheSharedDefaults() {
        Path file = directory.resolve("config").resolve(FileDialogueConfig.FILE_NAME);
        FileDialogueConfig config = FileDialogueConfig.load(file);
        assertTrue(Files.isRegularFile(file));
        assertTrue(config.enabled());
        assertEquals(32.0D, config.maxDistance());
        assertEquals(80, config.displayDuration());
        assertEquals(20, config.fadeOut());
        assertEquals(160, config.scenarioCooldown());
        assertEquals(0.35D, config.chance());
        assertEquals(10.0D, config.lineSpacing());
        assertEquals(0.8D, config.bottomScale());
        assertEquals(0.55D, config.bottomAlpha());
        assertEquals("auto", config.language());
        assertFalse(config.requireReceiver());
    }

    @Test
    void parsesValuesAndClampsThemToTheForgeRanges() throws Exception {
        Path file = directory.resolve(FileDialogueConfig.FILE_NAME);
        Files.writeString(file, """
                [display]
                enabled = false
                maxDistance = 999
                displayDurationTicks = 5
                fadeOutTicks = 500
                lineSpacing = 12.5
                bottomLineScale = 0.6
                bottomLineAlpha = 0.4
                language = "en"

                requireReceiver = true

                [trigger]
                scenarioCooldownTicks = 5
                ambientChance = 2
                """);
        FileDialogueConfig config = FileDialogueConfig.load(file);
        assertFalse(config.enabled());
        assertEquals(128.0D, config.maxDistance());
        assertEquals(20, config.displayDuration());
        assertEquals(200, config.fadeOut());
        assertEquals(12.5D, config.lineSpacing());
        assertEquals(0.6D, config.bottomScale());
        assertEquals(0.4D, config.bottomAlpha());
        assertEquals("en", config.language());
        assertTrue(config.requireReceiver());
        assertEquals(20, config.scenarioCooldown());
        assertEquals(1.0D, config.chance());
    }

    @Test
    void fallsBackToDefaultsForMissingOrMalformedValues() throws Exception {
        Path file = directory.resolve(FileDialogueConfig.FILE_NAME);
        Files.writeString(file, "display.enabled = maybe\n[display]\nlanguage = \"fr\"\n");
        FileDialogueConfig config = FileDialogueConfig.load(file);
        assertTrue(config.enabled());
        assertEquals("auto", config.language());
        assertEquals(32.0D, config.maxDistance());
    }
}
