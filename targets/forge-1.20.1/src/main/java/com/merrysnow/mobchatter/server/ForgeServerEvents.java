package com.merrysnow.mobchatter.server;

import com.merrysnow.mobchatter.MobChatterForge;
import net.minecraft.server.level.ServerPlayer;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.event.entity.EntityLeaveLevelEvent;
import net.minecraftforge.event.entity.living.LivingDamageEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.server.ServerStoppedEvent;
import net.minecraftforge.eventbus.api.EventPriority;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class ForgeServerEvents {
    private ForgeServerEvents() {
    }

    @SubscribeEvent
    public static void onJoin(EntityJoinLevelEvent event) {
        ServerDialogueController.onJoin(event.getEntity(), event.getLevel(), event.loadedFromDisk());
    }

    @SubscribeEvent
    public static void onLeave(EntityLeaveLevelEvent event) {
        ServerDialogueController.onLeave(event.getEntity(), event.getLevel());
    }

    @SubscribeEvent
    public static void onStartTracking(PlayerEvent.StartTracking event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            ServerDialogueController.onStartTracking(event.getTarget(), player);
        }
    }

    @SubscribeEvent
    public static void onStopTracking(PlayerEvent.StopTracking event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            ServerDialogueController.onStopTracking(event.getTarget(), player);
        }
    }

    @SubscribeEvent
    public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            ServerDialogueController.onLogout(player);
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void onDamage(LivingDamageEvent event) {
        ServerDialogueController.onDamage(event.getEntity(), event.getSource(), event.getAmount());
    }

    @SubscribeEvent
    public static void onTick(TickEvent.ServerTickEvent event) {
        if (event.phase == TickEvent.Phase.END) {
            ServerDialogueController.tick(event.getServer());
        }
    }

    @SubscribeEvent
    public static void onStopped(ServerStoppedEvent event) {
        ServerDialogueController.clear();
    }
}
