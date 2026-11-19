package com.merrysnow.mobchatter;

import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.network.DialogueNetwork;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;

@Mod(MobChatterForge.MOD_ID)
public final class MobChatterForge {
    public static final String MOD_ID = "mobchatter";

    public MobChatterForge() {
        ModLoadingContext.get().registerConfig(
                ModConfig.Type.COMMON, CommonConfig.SPEC, "mobchatter-common.toml");
        DialogueNetwork.register();
    }
}
