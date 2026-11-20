package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.MobChatterForge;
import cc.sighs.mobchatter.network.DialogueSignal;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityLeaveWorldEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class ForgeClientEvents {
    private ForgeClientEvents() {
    }

    public static void receive(DialogueSignal signal) {
        ClientDialogueController.receive(signal);
    }

    @SubscribeEvent
    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase == TickEvent.Phase.END) {
            ClientDialogueController.tick();
        }
    }

    @SubscribeEvent
    public static void onLeave(EntityLeaveWorldEvent event) {
        if (event.getWorld().isClientSide()) {
            ClientDialogueController.onEntityLeave(event.getEntity());
        }
    }
}
