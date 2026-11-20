package com.merrysnow.mobchatter;

import com.merrysnow.mobchatter.compat.CuriosBridge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.item.ForgeRadioReceiverItem;
import com.merrysnow.mobchatter.item.ModItems;
import com.merrysnow.mobchatter.network.DialogueNetwork;
import com.merrysnow.mobchatter.platform.ForgePlatform;
import com.merrysnow.mobchatter.platform.Platforms;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

@Mod(MobChatterForge.MOD_ID)
public final class MobChatterForge {
    public static final String MOD_ID = MobChatterCommon.MOD_ID;

    private static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, MOD_ID);
    private static final RegistryObject<Item> RADIO_RECEIVER = ITEMS.register(
            ModItems.RADIO_RECEIVER,
            () -> new ForgeRadioReceiverItem(new Item.Properties().stacksTo(1)));

    public MobChatterForge() {
        Platforms.install(new ForgePlatform());
        ModLoadingContext.get().registerConfig(
                ModConfig.Type.COMMON, CommonConfig.SPEC, "mobchatter-common.toml");
        ModItems.setRadioReceiver(RADIO_RECEIVER);
        ITEMS.register(FMLJavaModLoadingContext.get().getModEventBus());
        FMLJavaModLoadingContext.get().getModEventBus().addListener((BuildCreativeModeTabContentsEvent event) -> {
            if (event.getTabKey() == CreativeModeTabs.TOOLS_AND_UTILITIES) {
                event.accept(RADIO_RECEIVER.get());
            }
        });
        FMLJavaModLoadingContext.get().getModEventBus().addListener((FMLCommonSetupEvent event) -> {
            if (ModList.get().isLoaded("curios")) {
                CuriosBridge.register();
            }
        });
        DialogueNetwork.register();
    }
}
