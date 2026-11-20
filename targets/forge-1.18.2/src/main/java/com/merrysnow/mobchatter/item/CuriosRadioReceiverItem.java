package com.merrysnow.mobchatter.item;

import net.minecraft.world.item.ItemStack;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

/** Item class chosen only when Curios is loaded. */
public final class CuriosRadioReceiverItem extends ForgeRadioReceiverItem implements ICurioItem {
    public CuriosRadioReceiverItem(Properties properties) {
        super(properties);
    }

    @Override
    public boolean canEquip(SlotContext context, ItemStack stack) {
        return "head".equals(context.identifier());
    }
}
