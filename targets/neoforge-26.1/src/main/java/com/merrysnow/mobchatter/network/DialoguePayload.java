package com.merrysnow.mobchatter.network;

import com.merrysnow.mobchatter.MobChatterCommon;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

public record DialoguePayload(DialogueSignal signal) implements CustomPacketPayload {
    public static final Type<DialoguePayload> TYPE = new Type<>(
            Identifier.fromNamespaceAndPath(MobChatterCommon.MOD_ID, "dialogue"));

    public static final StreamCodec<RegistryFriendlyByteBuf, DialoguePayload> STREAM_CODEC =
            StreamCodec.of((RegistryFriendlyByteBuf buffer, DialoguePayload payload) -> payload.signal().encode(buffer),
                    buffer -> new DialoguePayload(DialogueSignal.decode(buffer)));

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
