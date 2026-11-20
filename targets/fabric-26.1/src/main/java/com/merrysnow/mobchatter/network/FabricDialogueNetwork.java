package com.merrysnow.mobchatter.network;

import com.merrysnow.mobchatter.client.ClientDialogueController;
import com.merrysnow.mobchatter.platform.DialogueNetworking;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.level.ServerPlayer;

public final class FabricDialogueNetwork implements DialogueNetworking {
    @Override
    public void send(ServerPlayer player, DialogueSignal signal) {
        if (!ServerPlayNetworking.canSend(player, DialoguePayload.TYPE)) {
            return;
        }
        ServerPlayNetworking.send(player, new DialoguePayload(signal));
    }

    public static void registerClientReceiver() {
        ClientPlayNetworking.registerGlobalReceiver(DialoguePayload.TYPE, (payload, context) ->
                context.client().execute(() -> ClientDialogueController.receive(payload.signal())));
    }
}
