package com.merrysnow.mobchatter.network;

import com.merrysnow.mobchatter.MobChatterCommon;
import com.merrysnow.mobchatter.client.ClientDialogueController;
import com.merrysnow.mobchatter.platform.DialogueNetworking;
import io.netty.buffer.Unpooled;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

public final class FabricDialogueNetwork implements DialogueNetworking {
    public static final ResourceLocation CHANNEL =
            ResourceLocation.tryParse(MobChatterCommon.MOD_ID + ":dialogue");

    @Override
    public void send(ServerPlayer player, DialogueSignal signal) {
        if (!ServerPlayNetworking.canSend(player, CHANNEL)) {
            return;
        }
        FriendlyByteBuf buffer = new FriendlyByteBuf(Unpooled.buffer());
        try {
            signal.encode(buffer);
            ServerPlayNetworking.send(player, CHANNEL, buffer);
        } finally {
            buffer.release();
        }
    }

    public static void registerClientReceiver() {
        ClientPlayNetworking.registerGlobalReceiver(CHANNEL, (client, handler, buffer, responseSender) -> {
            DialogueSignal signal = DialogueSignal.decode(buffer);
            client.execute(() -> ClientDialogueController.receive(signal));
        });
    }
}
