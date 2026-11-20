package cc.sighs.mobchatter;

import cc.sighs.mobchatter.network.DialoguePayload;
import cc.sighs.mobchatter.item.ModItems;
import cc.sighs.mobchatter.item.Fabric261RadioReceiverItem;
import cc.sighs.mobchatter.platform.FabricPlatform;
import cc.sighs.mobchatter.platform.Platforms;
import cc.sighs.mobchatter.server.ServerDialogueController;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.Registry;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.Equippable;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.EntityTrackingEvents;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;

public final class MobChatterFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Platforms.install(new FabricPlatform());
        ResourceKey<Item> receiverKey = ResourceKey.create(Registries.ITEM,
                Identifier.fromNamespaceAndPath(MobChatterCommon.MOD_ID, "radio_receiver"));
        Item receiver = Registry.register(BuiltInRegistries.ITEM, receiverKey,
                new Fabric261RadioReceiverItem(new Item.Properties()
                        .setId(receiverKey)
                        .stacksTo(1)
                        .component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.HEAD)
                                .setSwappable(true)
                                .setEquipSound(SoundEvents.ARMOR_EQUIP_GENERIC)
                                .build())));
        ModItems.setRadioReceiver(() -> receiver);
        PayloadTypeRegistry.clientboundPlay().register(DialoguePayload.TYPE, DialoguePayload.STREAM_CODEC);

        ServerEntityEvents.ENTITY_LOAD.register((entity, world) ->
                ServerDialogueController.onJoin(entity, world, false));
        ServerEntityEvents.ENTITY_UNLOAD.register(ServerDialogueController::onLeave);
        EntityTrackingEvents.START_TRACKING.register(ServerDialogueController::onStartTracking);
        EntityTrackingEvents.STOP_TRACKING.register(ServerDialogueController::onStopTracking);
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) ->
                ServerDialogueController.onLogout(handler.player));
        ServerLivingEntityEvents.AFTER_DAMAGE.register((entity, source, baseAmount, amount, blocked) -> {
            if (amount > 0) {
                ServerDialogueController.onDamage(entity, source, amount);
            }
        });
        ServerTickEvents.END_SERVER_TICK.register(ServerDialogueController::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> ServerDialogueController.clear());
    }
}
