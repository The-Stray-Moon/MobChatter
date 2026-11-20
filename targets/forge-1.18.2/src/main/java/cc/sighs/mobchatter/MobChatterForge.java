package cc.sighs.mobchatter;

import cc.sighs.mobchatter.config.CommonConfig;
import cc.sighs.mobchatter.compat.CuriosRegistration;
import cc.sighs.mobchatter.item.ForgeRadioReceiverItem;
import cc.sighs.mobchatter.item.ModItems;
import cc.sighs.mobchatter.network.DialogueNetwork;
import cc.sighs.mobchatter.platform.ForgePlatform;
import cc.sighs.mobchatter.platform.Platforms;
import net.minecraft.world.item.Item;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

@Mod(MobChatterForge.MOD_ID)
public final class MobChatterForge {
    public static final String MOD_ID = MobChatterCommon.MOD_ID;

    private static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, MOD_ID);
    private static RegistryObject<Item> radioReceiver;

    public MobChatterForge() {
        Platforms.install(new ForgePlatform());
        ModLoadingContext.get().registerConfig(
                ModConfig.Type.COMMON, CommonConfig.SPEC, "mobchatter-common.toml");
        radioReceiver = registerReceiver();
        ModItems.setRadioReceiver(radioReceiver);
        ITEMS.register(FMLJavaModLoadingContext.get().getModEventBus());
        DialogueNetwork.register();
    }

    private static RegistryObject<Item> registerReceiver() {
        if (ModList.get().isLoaded("curios")) {
            return CuriosRegistration.register(ITEMS);
        }
        return ITEMS.register(ModItems.RADIO_RECEIVER,
                () -> new ForgeRadioReceiverItem(new Item.Properties().stacksTo(1)));
    }
}
