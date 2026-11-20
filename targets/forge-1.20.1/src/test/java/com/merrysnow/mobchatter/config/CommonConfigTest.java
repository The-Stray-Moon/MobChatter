package com.merrysnow.mobchatter.config;

import net.minecraftforge.common.ForgeConfigSpec;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

class CommonConfigTest {
    @Test
    void containsAllServerAndClientOptionsInOneSpec() {
        for (ForgeConfigSpec.ConfigValue<?> value : List.of(
                CommonConfig.ENABLED, CommonConfig.MAX_DISTANCE, CommonConfig.DISPLAY_DURATION,
                CommonConfig.FADE_OUT, CommonConfig.SCENARIO_COOLDOWN, CommonConfig.CHANCE,
                CommonConfig.LINE_SPACING, CommonConfig.BOTTOM_SCALE, CommonConfig.BOTTOM_ALPHA,
                CommonConfig.LANGUAGE, CommonConfig.REQUIRE_RECEIVER)) {
            assertSame(value, CommonConfig.SPEC.getValues().get(value.getPath()));
        }
        assertEquals(List.of("display", "maxDistance"), CommonConfig.MAX_DISTANCE.getPath());
        assertEquals(32.0D, CommonConfig.MAX_DISTANCE.getDefault());
        assertEquals(80, CommonConfig.DISPLAY_DURATION.getDefault());
        assertEquals(20, CommonConfig.FADE_OUT.getDefault());
        assertEquals(160, CommonConfig.SCENARIO_COOLDOWN.getDefault());
        assertEquals(0.35D, CommonConfig.CHANCE.getDefault());
        assertEquals("zh", CommonConfig.LANGUAGE.getDefault());
        assertEquals(false, CommonConfig.REQUIRE_RECEIVER.getDefault());
    }
}
