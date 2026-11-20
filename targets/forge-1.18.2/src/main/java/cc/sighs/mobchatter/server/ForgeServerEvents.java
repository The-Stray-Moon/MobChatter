package cc.sighs.mobchatter.server;

import cc.sighs.mobchatter.MobChatterForge;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.event.entity.EntityLeaveWorldEvent;
import net.minecraftforge.event.entity.living.LivingDamageEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.server.ServerStoppedEvent;
import net.minecraftforge.eventbus.api.EventPriority;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.server.ServerLifecycleHooks;

@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class ForgeServerEvents {
    private ForgeServerEvents() {
    }

    @SubscribeEvent
    public static void onJoin(EntityJoinWorldEvent event) {
        ServerDialogueController.onJoin(event.getEntity(), event.getWorld(), event.loadedFromDisk());
    }

    @SubscribeEvent
    public static void onLeave(EntityLeaveWorldEvent event) {
        ServerDialogueController.onLeave(event.getEntity(), event.getWorld());
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
        ServerDialogueController.onDamage((LivingEntity) event.getEntity(), event.getSource(), event.getAmount());
    }

    @SubscribeEvent
    public static void onTick(TickEvent.ServerTickEvent event) {
        if (event.phase == TickEvent.Phase.END) {
            var server = ServerLifecycleHooks.getCurrentServer();
            if (server != null) {
                ServerDialogueController.tick(server);
            }
        }
    }

    @SubscribeEvent
    public static void onStopped(ServerStoppedEvent event) {
        ServerDialogueController.clear();
    }
}
