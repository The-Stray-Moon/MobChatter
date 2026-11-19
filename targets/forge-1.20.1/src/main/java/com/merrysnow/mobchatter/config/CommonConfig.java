package com.merrysnow.mobchatter.config;

import net.minecraftforge.common.ForgeConfigSpec;

public final class CommonConfig {
    public static final ForgeConfigSpec SPEC;
    public static final ForgeConfigSpec.BooleanValue ENABLED;
    public static final ForgeConfigSpec.DoubleValue MAX_DISTANCE;
    public static final ForgeConfigSpec.IntValue DISPLAY_DURATION;
    public static final ForgeConfigSpec.IntValue FADE_OUT;
    public static final ForgeConfigSpec.IntValue SCENARIO_COOLDOWN;
    public static final ForgeConfigSpec.DoubleValue CHANCE;
    public static final ForgeConfigSpec.DoubleValue LINE_SPACING;
    public static final ForgeConfigSpec.DoubleValue BOTTOM_SCALE;
    public static final ForgeConfigSpec.DoubleValue BOTTOM_ALPHA;
    public static final ForgeConfigSpec.ConfigValue<String> LANGUAGE;

    static {
        ForgeConfigSpec.Builder builder = new ForgeConfigSpec.Builder();
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
        LANGUAGE = builder.comment("Bubble language: zh or en.")
                .defineInList("language", "zh", java.util.List.of("zh", "en"));
        builder.pop();
        builder.push("trigger");
        SCENARIO_COOLDOWN = builder.comment("Server-controlled minimum ticks between the same scenario for one entity.")
                .defineInRange("scenarioCooldownTicks", 160, 20, 2400);
        CHANCE = builder.comment("Server-controlled ambient probability multiplier.")
                .defineInRange("ambientChance", 0.35D, 0.0D, 1.0D);
        builder.pop();
        SPEC = builder.build();
    }

    private CommonConfig() {
    }
}
