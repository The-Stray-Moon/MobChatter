package cc.sighs.mobchatter.network;

import cc.sighs.mobchatter.platform.DialogueNetworking;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.network.PacketDistributor;

public final class NeoForgeDialogueNetwork implements DialogueNetworking {
    @Override
    public void send(ServerPlayer player, DialogueSignal signal) {
        PacketDistributor.sendToPlayer(player, new DialoguePayload(signal));
    }
}
