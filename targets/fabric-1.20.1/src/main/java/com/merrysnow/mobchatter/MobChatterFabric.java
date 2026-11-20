package com.merrysnow.mobchatter;

import com.merrysnow.mobchatter.item.FabricRadioReceiverItem;
import com.merrysnow.mobchatter.item.ModItems;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.world.item.CreativeModeTabs;
import com.merrysnow.mobchatter.platform.FabricPlatform;
import com.merrysnow.mobchatter.platform.Platforms;
import com.merrysnow.mobchatter.server.ServerDialogueController;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.EntityTrackingEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.core.Registry;

public final class MobChatterFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Platforms.install(new FabricPlatform());
        Item receiver = Registry.register(BuiltInRegistries.ITEM,
                ResourceLocation.tryParse(MobChatterCommon.MOD_ID + ":radio_receiver"),
                new FabricRadioReceiverItem(new Item.Properties().stacksTo(1)));
        ModItems.setRadioReceiver(() -> receiver);
        ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.TOOLS_AND_UTILITIES)
                .register(entries -> entries.accept(receiver));

        ServerEntityEvents.ENTITY_LOAD.register((entity, world) ->
                ServerDialogueController.onJoin(entity, world, false));
        ServerEntityEvents.ENTITY_UNLOAD.register(ServerDialogueController::onLeave);
        EntityTrackingEvents.START_TRACKING.register(ServerDialogueController::onStartTracking);
        EntityTrackingEvents.STOP_TRACKING.register(ServerDialogueController::onStopTracking);
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) ->
                ServerDialogueController.onLogout(handler.player));
        ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
            if (amount > 0) {
                ServerDialogueController.onDamage(entity, source, amount);
            }
            return true;
        });
        ServerTickEvents.END_SERVER_TICK.register(ServerDialogueController::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> ServerDialogueController.clear());
    }
}
