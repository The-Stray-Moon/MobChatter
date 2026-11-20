package com.merrysnow.mobchatter.config;

import com.merrysnow.mobchatter.platform.DialogueConfig;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Minimal TOML-style configuration used by loaders without a built-in config
 * API. The file keeps the same keys, ranges and defaults as the Forge COMMON
 * config so server operators see one format across targets.
 */
public final class FileDialogueConfig implements DialogueConfig {
    public static final String FILE_NAME = "mobchatter-common.toml";

    private static final String TEMPLATE = """
            # MobChatter shared configuration. Server side: triggering, ranges, durations.
            # Client side: language and text layout. Restart the game after editing.

            [display]
            enabled = true
            maxDistance = 32.0
            displayDurationTicks = 80
            fadeOutTicks = 20
            lineSpacing = 10.0
            bottomLineScale = 0.8
            bottomLineAlpha = 0.55
            language = "zh"
            requireReceiver = false

            [trigger]
            scenarioCooldownTicks = 160
            ambientChance = 0.35
            """;

    private final boolean enabled;
    private final double maxDistance;
    private final int displayDuration;
    private final int fadeOut;
    private final int scenarioCooldown;
    private final double chance;
    private final double lineSpacing;
    private final double bottomScale;
    private final double bottomAlpha;
    private final String language;
    private final boolean requireReceiver;

    private FileDialogueConfig(Map<String, String> values) {
        enabled = bool(values, "display.enabled", true);
        maxDistance = clampDouble(values, "display.maxDistance", 32.0D, 4.0D, 128.0D);
        displayDuration = clampInt(values, "display.displayDurationTicks", 80, 20, 1200);
        fadeOut = clampInt(values, "display.fadeOutTicks", 20, 1, 200);
        lineSpacing = clampDouble(values, "display.lineSpacing", 10.0D, 6.0D, 24.0D);
        bottomScale = clampDouble(values, "display.bottomLineScale", 0.8D, 0.4D, 1.0D);
        bottomAlpha = clampDouble(values, "display.bottomLineAlpha", 0.55D, 0.1D, 1.0D);
        String languageValue = values.getOrDefault("display.language", "zh").replace("\"", "").trim();
        language = "en".equalsIgnoreCase(languageValue) ? "en" : "zh";
        requireReceiver = bool(values, "display.requireReceiver", false);
        scenarioCooldown = clampInt(values, "trigger.scenarioCooldownTicks", 160, 20, 2400);
        chance = clampDouble(values, "trigger.ambientChance", 0.35D, 0.0D, 1.0D);
    }

    public static FileDialogueConfig load(Path file) {
        try {
            if (Files.notExists(file)) {
                Files.createDirectories(file.getParent());
                Files.writeString(file, TEMPLATE, StandardCharsets.UTF_8);
            }
            return new FileDialogueConfig(parse(Files.readAllLines(file, StandardCharsets.UTF_8)));
        } catch (IOException exception) {
            return new FileDialogueConfig(Map.of());
        }
    }

    public static FileDialogueConfig defaults() {
        return new FileDialogueConfig(Map.of());
    }

    private static Map<String, String> parse(List<String> lines) {
        Map<String, String> values = new LinkedHashMap<>();
        String section = "";
        for (String raw : lines) {
            String line = raw.trim();
            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }
            if (line.startsWith("[") && line.endsWith("]")) {
                section = line.substring(1, line.length() - 1).trim();
                continue;
            }
            int separator = line.indexOf('=');
            if (separator < 1) {
                continue;
            }
            String key = line.substring(0, separator).trim();
            String value = stripComment(line.substring(separator + 1));
            if (key.isEmpty() || value.isEmpty()) {
                continue;
            }
            values.put(section.isEmpty() ? key : section + "." + key, value);
        }
        return values;
    }

    private static String stripComment(String value) {
        boolean quoted = false;
        for (int index = 0; index < value.length(); index++) {
            char current = value.charAt(index);
            if (current == '"') {
                quoted = !quoted;
            } else if (current == '#' && !quoted) {
                return value.substring(0, index).trim();
            }
        }
        return value.trim();
    }

    private static boolean bool(Map<String, String> values, String key, boolean fallback) {
        String value = values.get(key);
        if (value == null) {
            return fallback;
        }
        String normalized = value.toLowerCase(Locale.ROOT);
        return normalized.equals("true") || normalized.equals("false") ? Boolean.parseBoolean(normalized) : fallback;
    }

    private static int clampInt(Map<String, String> values, String key, int fallback, int min, int max) {
        try {
            return Math.max(min, Math.min(max, Integer.parseInt(values.getOrDefault(key, Integer.toString(fallback)))));
        } catch (NumberFormatException exception) {
            return fallback;
        }
    }

    private static double clampDouble(Map<String, String> values, String key, double fallback,
                                      double min, double max) {
        try {
            double value = Double.parseDouble(values.getOrDefault(key, Double.toString(fallback)));
            return Double.isFinite(value) ? Math.max(min, Math.min(max, value)) : fallback;
        } catch (NumberFormatException exception) {
            return fallback;
        }
    }

    @Override
    public boolean enabled() {
        return enabled;
    }

    @Override
    public double maxDistance() {
        return maxDistance;
    }

    @Override
    public int displayDuration() {
        return displayDuration;
    }

    @Override
    public int fadeOut() {
        return fadeOut;
    }

    @Override
    public int scenarioCooldown() {
        return scenarioCooldown;
    }

    @Override
    public double chance() {
        return chance;
    }

    @Override
    public double lineSpacing() {
        return lineSpacing;
    }

    @Override
    public double bottomScale() {
        return bottomScale;
    }

    @Override
    public double bottomAlpha() {
        return bottomAlpha;
    }

    @Override
    public String language() {
        return language;
    }

    @Override
    public boolean requireReceiver() {
        return requireReceiver;
    }
}
