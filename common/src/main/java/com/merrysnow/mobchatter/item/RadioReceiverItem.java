package com.merrysnow.mobchatter.item;

import net.minecraft.world.item.Item;

/**
 * Head-mounted receiver that can gate dialogue visibility.
 *
 * <p>Targets either register a subclass with their version's right-click
 * equip hook or attach the 26.1 {@code Equippable} data component. The Curios
 * registration is optional and lives in the loader target.</p>
 */
public class RadioReceiverItem extends Item {
    public RadioReceiverItem(Properties properties) {
        super(properties);
    }
}
