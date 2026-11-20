package cc.sighs.mobchatter.compat;

import cc.sighs.mobchatter.item.CuriosRadioReceiverItem;
import cc.sighs.mobchatter.item.ModItems;
import net.minecraft.world.item.Item;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

/** Loaded only when Curios is present. */
public final class CuriosRegistration {
    private CuriosRegistration() {
    }

    public static RegistryObject<Item> register(DeferredRegister<Item> items) {
        return items.register(ModItems.RADIO_RECEIVER,
                () -> new CuriosRadioReceiverItem(new Item.Properties().stacksTo(1)));
    }
}
