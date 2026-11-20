package com.merrysnow.mobchatter.item;

import com.merrysnow.mobchatter.platform.Platforms;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;

import java.util.List;

/** Shared tooltip text; each target only adapts the version-specific append signature. */
public final class RadioReceiverTooltip {
    public static final String SLOT_KEY = "item.mobchatter.radio_receiver.tooltip.slot";
    public static final String ENABLED_KEY = "item.mobchatter.radio_receiver.tooltip.enabled";
    public static final String DISABLED_KEY = "item.mobchatter.radio_receiver.tooltip.disabled";

    private RadioReceiverTooltip() {
    }

    public static List<String> keys() {
        if (!Platforms.isInstalled()) {
            return List.of();
        }
        return List.of(SLOT_KEY, Platforms.get().config().requireReceiver() ? ENABLED_KEY : DISABLED_KEY);
    }

    public static List<Component> lines() {
        return keys().stream()
                .<Component>map(key -> Platforms.get().translatable(key).withStyle(ChatFormatting.GRAY))
                .toList();
    }
}
