package com.merrysnow.mobchatter.network;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.client.DialogueController;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.DistExecutor;
import net.minecraftforge.network.NetworkDirection;
import net.minecraftforge.network.NetworkRegistry;
import net.minecraftforge.network.PacketDistributor;
import net.minecraftforge.network.simple.SimpleChannel;

public final class DialogueNetwork {
    private static final String PROTOCOL = "1";
    private static SimpleChannel channel;

    private DialogueNetwork() {
    }

    public static boolean accepts(String version) {
        return PROTOCOL.equals(version);
    }

    public static void register() {
        channel = NetworkRegistry.newSimpleChannel(
                new ResourceLocation(MobChatterForge.MOD_ID, "dialogue"), () -> PROTOCOL,
                DialogueNetwork::accepts, DialogueNetwork::accepts);
        channel.messageBuilder(DialogueSignal.class, 0, NetworkDirection.PLAY_TO_CLIENT)
                .encoder(DialogueSignal::encode)
                .decoder(DialogueSignal::decode)
                .consumerMainThread((signal, context) -> DistExecutor.unsafeRunWhenOn(Dist.CLIENT,
                        () -> () -> DialogueController.receive(signal)))
                .add();
    }

    public static void send(ServerPlayer player, DialogueSignal signal) {
        channel.send(PacketDistributor.PLAYER.with(() -> player), signal);
    }
}
