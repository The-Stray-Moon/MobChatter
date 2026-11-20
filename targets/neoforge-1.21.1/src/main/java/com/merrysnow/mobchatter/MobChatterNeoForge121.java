package com.merrysnow.mobchatter;

import com.merrysnow.mobchatter.compat.CuriosBridge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.item.ModItems;
import com.merrysnow.mobchatter.item.NeoForgeRadioReceiverItem;
import com.merrysnow.mobchatter.platform.NeoForgePlatform;
import com.merrysnow.mobchatter.platform.Platforms;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(MobChatterNeoForge121.MOD_ID)
public final class MobChatterNeoForge121 {
    public static final String MOD_ID = MobChatterCommon.MOD_ID;

    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);
    private static final DeferredItem<Item> RADIO_RECEIVER = ITEMS.register(
            ModItems.RADIO_RECEIVER,
            () -> new NeoForgeRadioReceiverItem(new Item.Properties().stacksTo(1)));

    public MobChatterNeoForge121(IEventBus modBus, ModContainer container) {
        Platforms.install(new NeoForgePlatform());
        container.registerConfig(ModConfig.Type.COMMON, CommonConfig.SPEC, "mobchatter-common.toml");
        ModItems.setRadioReceiver(RADIO_RECEIVER);
        ITEMS.register(modBus);
        modBus.addListener((BuildCreativeModeTabContentsEvent event) -> {
            if (event.getTabKey() == CreativeModeTabs.TOOLS_AND_UTILITIES) {
                event.accept(RADIO_RECEIVER.get());
            }
        });
        modBus.addListener((FMLCommonSetupEvent event) -> {
            if (ModList.get().isLoaded("curios")) {
                CuriosBridge.register();
            }
        });
    }
}
