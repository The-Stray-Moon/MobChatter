package com.merrysnow.mobchatter.compat;

import com.merrysnow.mobchatter.item.ModItems;
import net.minecraft.world.entity.player.Player;
import top.theillusivec4.curios.api.CuriosApi;

/** Loaded only when Curios is present. */
public final class CuriosBridge {
    private CuriosBridge() {
    }

    public static boolean isWearing(Player player) {
        return CuriosApi.getCuriosHelper()
                .findFirstCurio(player, ModItems.radioReceiver())
                .isPresent();
    }
}
