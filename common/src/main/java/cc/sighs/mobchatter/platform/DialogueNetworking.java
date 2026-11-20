package cc.sighs.mobchatter.platform;

import cc.sighs.mobchatter.network.DialogueSignal;
import net.minecraft.server.level.ServerPlayer;

/** Loader-specific delivery of server-authoritative dialogue signals. */
public interface DialogueNetworking {
    String PROTOCOL_VERSION = "1";

    /** Sends one already-finalised signal to a single player. */
    void send(ServerPlayer player, DialogueSignal signal);
}
