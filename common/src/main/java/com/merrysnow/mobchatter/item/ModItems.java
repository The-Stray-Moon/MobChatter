package com.merrysnow.mobchatter.item;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.Objects;
import java.util.function.Supplier;

/**
 * Loader-independent handle to the mod item. Targets register the item with
 * their own registry and install the supplier here.
 */
public final class ModItems {
    public static final String RADIO_RECEIVER = "radio_receiver";

    private static Supplier<Item> radioReceiver = () -> Items.AIR;

    private ModItems() {
    }

    public static void setRadioReceiver(Supplier<Item> supplier) {
        radioReceiver = Objects.requireNonNull(supplier, "supplier");
    }

    public static Item radioReceiver() {
        return radioReceiver.get();
    }

    public static boolean isRadioReceiver(ItemStack stack) {
        return stack.is(radioReceiver());
    }
}
