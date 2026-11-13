package com.merrysnow.mobchatter.config;

import net.minecraftforge.common.ForgeConfigSpec;

/**
 * Common config. Written to {@code config/mobchatter-common.toml}.
 */
public final class CommonConfig {
    public static final ForgeConfigSpec SPEC;

    public static final ForgeConfigSpec.BooleanValue ENABLED;
    public static final ForgeConfigSpec.IntValue DISPLAY_DURATION;
    public static final ForgeConfigSpec.IntValue FADE_OUT;
    public static final ForgeConfigSpec.DoubleValue MAX_DISTANCE;
    public static final ForgeConfigSpec.DoubleValue LINE_SPACING;
    public static final ForgeConfigSpec.DoubleValue BOTTOM_SCALE;
    public static final ForgeConfigSpec.DoubleValue BOTTOM_ALPHA;
    public static final ForgeConfigSpec.IntValue SCENARIO_COOLDOWN;
    public static final ForgeConfigSpec.DoubleValue CHANCE;
    public static final ForgeConfigSpec.ConfigValue<String> LANGUAGE;

    static {
        ForgeConfigSpec.Builder builder = new ForgeConfigSpec.Builder();

        builder.comment("Chatter bubble display").push("display");
        ENABLED = builder.comment("Master switch for chatter bubbles.").define("enabled", true);
        DISPLAY_DURATION = builder
                .comment("How long a bubble stays fully visible, in ticks.")
                .defineInRange("displayDurationTicks", 80, 20, 1200);
        FADE_OUT = builder
                .comment("Fade-out time at the end of the bubble lifetime, in ticks.")
                .defineInRange("fadeOutTicks", 20, 1, 200);
        MAX_DISTANCE = builder
                .comment("Only entities within this distance of the local player can chatter.")
                .defineInRange("maxDistance", 32.0D, 4.0D, 128.0D);
        LINE_SPACING = builder
                .comment("Vertical gap between the top and bottom line, in font pixels.")
                .defineInRange("lineSpacing", 10.0D, 6.0D, 24.0D);
        BOTTOM_SCALE = builder
                .comment("Scale of the second line relative to the first.")
                .defineInRange("bottomLineScale", 0.8D, 0.4D, 1.0D);
        BOTTOM_ALPHA = builder
                .comment("Opacity of the second line, 0..1.")
                .defineInRange("bottomLineAlpha", 0.55D, 0.1D, 1.0D);
        LANGUAGE = builder
                .comment("Bubble language: zh or en.")
                .defineInList("language", "zh", java.util.List.of("zh", "en"));
        builder.pop();

        builder.comment("How often bubbles can trigger").push("trigger");
        SCENARIO_COOLDOWN = builder
                .comment("Minimum ticks before the same scenario can trigger again for one entity.")
                .defineInRange("scenarioCooldownTicks", 160, 20, 2400);
        CHANCE = builder
                .comment("Probability for ambient scenarios (walk, idle, look, targeting).")
                .defineInRange("ambientChance", 0.35D, 0.0D, 1.0D);
        builder.pop();

        SPEC = builder.build();
    }

    private CommonConfig() {
    }
}
