package cc.sighs.mobchatter.config;

import cc.sighs.mobchatter.platform.DialogueConfig;
import net.neoforged.neoforge.common.ModConfigSpec;

public final class CommonConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue ENABLED;
    public static final ModConfigSpec.DoubleValue MAX_DISTANCE;
    public static final ModConfigSpec.IntValue DISPLAY_DURATION;
    public static final ModConfigSpec.IntValue FADE_OUT;
    public static final ModConfigSpec.IntValue SCENARIO_COOLDOWN;
    public static final ModConfigSpec.DoubleValue CHANCE;
    public static final ModConfigSpec.DoubleValue LINE_SPACING;
    public static final ModConfigSpec.DoubleValue BOTTOM_SCALE;
    public static final ModConfigSpec.DoubleValue BOTTOM_ALPHA;
    public static final ModConfigSpec.ConfigValue<String> LANGUAGE;
    public static final ModConfigSpec.BooleanValue REQUIRE_RECEIVER;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        builder.push("display");
        ENABLED = builder.comment("Server: enable chatter triggers. Client: show received chatter bubbles.")
                .define("enabled", true);
        MAX_DISTANCE = builder.comment("Server-controlled broadcast and display radius in blocks.")
                .defineInRange("maxDistance", 32.0D, 4.0D, 128.0D);
        DISPLAY_DURATION = builder.comment("Server-controlled bubble lifetime in ticks.")
                .defineInRange("displayDurationTicks", 80, 20, 1200);
        FADE_OUT = builder.comment("Server-controlled fade-out time in ticks.")
                .defineInRange("fadeOutTicks", 20, 1, 200);
        LINE_SPACING = builder.comment("Vertical line gap in font pixels.")
                .defineInRange("lineSpacing", 10.0D, 6.0D, 24.0D);
        BOTTOM_SCALE = builder.comment("Second line scale.")
                .defineInRange("bottomLineScale", 0.8D, 0.4D, 1.0D);
        BOTTOM_ALPHA = builder.comment("Second line opacity.")
                .defineInRange("bottomLineAlpha", 0.55D, 0.1D, 1.0D);
        LANGUAGE = builder.comment("Bubble language: auto (follow game language), zh, or en.")
                // Arrays.asList tolerates the null probe NeoForge 26.1 runs while correcting a fresh config; List.of throws.
                .defineInList("language", "auto", java.util.Arrays.asList("auto", "zh", "en"));
        REQUIRE_RECEIVER = builder.comment("Only show chatter for players wearing the radio receiver.")
                .define("requireReceiver", false);
        builder.pop();
        builder.push("trigger");
        SCENARIO_COOLDOWN = builder.comment("Server-controlled minimum ticks between the same scenario for one entity.")
                .defineInRange("scenarioCooldownTicks", 160, 20, 2400);
        CHANCE = builder.comment("Server-controlled ambient probability multiplier.")
                .defineInRange("ambientChance", 0.35D, 0.0D, 1.0D);
        builder.pop();
        SPEC = builder.build();
    }

    public static final DialogueConfig ADAPTER = new DialogueConfig() {
        @Override
        public boolean enabled() {
            return ENABLED.get();
        }

        @Override
        public double maxDistance() {
            return MAX_DISTANCE.get();
        }

        @Override
        public int displayDuration() {
            return DISPLAY_DURATION.get();
        }

        @Override
        public int fadeOut() {
            return FADE_OUT.get();
        }

        @Override
        public int scenarioCooldown() {
            return SCENARIO_COOLDOWN.get();
        }

        @Override
        public double chance() {
            return CHANCE.get();
        }

        @Override
        public double lineSpacing() {
            return LINE_SPACING.get();
        }

        @Override
        public double bottomScale() {
            return BOTTOM_SCALE.get();
        }

        @Override
        public double bottomAlpha() {
            return BOTTOM_ALPHA.get();
        }

        @Override
        public String language() {
            return LANGUAGE.get();
        }

        @Override
        public boolean requireReceiver() {
            return REQUIRE_RECEIVER.get();
        }
    };

    private CommonConfig() {
    }
}
