package cc.sighs.mobchatter.compat;

import cc.sighs.mobchatter.item.ModItems;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

/** Loaded only when Curios is present. */
public final class CuriosBridge {
    private CuriosBridge() {
    }

    public static void register() {
        CuriosApi.registerCurio(ModItems.radioReceiver(), new ICurioItem() {
            @Override
            public boolean canEquip(SlotContext context, ItemStack stack) {
                return "head".equals(context.identifier());
            }
        });
    }

    public static boolean isWearing(Player player) {
        return CuriosApi.getCuriosHelper()
                .findFirstCurio(player, ModItems.radioReceiver())
                .isPresent();
    }
}
