package cc.sighs.mobchatter.network;

import cc.sighs.mobchatter.MobChatterCommon;
import cc.sighs.mobchatter.client.ForgeClientEvents;
import cc.sighs.mobchatter.platform.DialogueNetworking;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.DistExecutor;
import net.minecraftforge.network.NetworkDirection;
import net.minecraftforge.network.NetworkRegistry;
import net.minecraftforge.network.PacketDistributor;
import net.minecraftforge.network.simple.SimpleChannel;

public final class DialogueNetwork implements DialogueNetworking {
    private static final String PROTOCOL = DialogueNetworking.PROTOCOL_VERSION;
    private static SimpleChannel channel;

    public static boolean accepts(String version) {
        return PROTOCOL.equals(version);
    }

    public static void register() {
        channel = NetworkRegistry.newSimpleChannel(
                new ResourceLocation(MobChatterCommon.MOD_ID, "dialogue"), () -> PROTOCOL,
                DialogueNetwork::accepts, DialogueNetwork::accepts);
        channel.messageBuilder(DialogueSignal.class, 0, NetworkDirection.PLAY_TO_CLIENT)
                .encoder(DialogueSignal::encode)
                .decoder(DialogueSignal::decode)
                .consumer((signal, context) -> {
                    context.get().enqueueWork(() -> DistExecutor.unsafeRunWhenOn(Dist.CLIENT,
                            () -> () -> ForgeClientEvents.receive(signal)));
                    context.get().setPacketHandled(true);
                })
                .add();
    }

    @Override
    public void send(ServerPlayer player, DialogueSignal signal) {
        channel.send(PacketDistributor.PLAYER.with(() -> player), signal);
    }
}
