package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.MobChatterCommon;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterClientReloadListenersEvent;

@EventBusSubscriber(modid = MobChatterCommon.MOD_ID, value = Dist.CLIENT)
public final class DialogueReloadRegistration {
    private DialogueReloadRegistration() {
    }

    @SubscribeEvent
    public static void register(RegisterClientReloadListenersEvent event) {
        event.registerReloadListener(new DialogueManager());
    }
}
