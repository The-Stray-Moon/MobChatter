package cc.sighs.mobchatter.network;

import cc.sighs.mobchatter.MobChatterCommon;
import cc.sighs.mobchatter.client.ClientDialogueController;
import cc.sighs.mobchatter.platform.DialogueNetworking;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

@EventBusSubscriber(modid = MobChatterCommon.MOD_ID)
public final class NeoForgeNetworkRegistration {
    private NeoForgeNetworkRegistration() {
    }

    @SubscribeEvent
    public static void register(RegisterPayloadHandlersEvent event) {
        event.registrar(DialogueNetworking.PROTOCOL_VERSION)
                .playToClient(DialoguePayload.TYPE, DialoguePayload.STREAM_CODEC,
                        (payload, context) -> ClientDialogueController.receive(payload.signal()));
    }
}
