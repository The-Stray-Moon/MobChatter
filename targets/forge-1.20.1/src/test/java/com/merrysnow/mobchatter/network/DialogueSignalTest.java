package com.merrysnow.mobchatter.network;

import io.netty.buffer.Unpooled;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.network.NetworkRegistry;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class DialogueSignalTest {
    private DialogueSignal signal(long seed, double range) {
        return new DialogueSignal(new ResourceLocation("minecraft", "overworld"), 42,
                UUID.fromString("12345678-1234-1234-1234-123456789abc"),
                new ResourceLocation("minecraft", "cow"), "hurt.fire", seed, 7, 1000, 80, 20, range);
    }

    @Test
    void roundTripsTheSameSignalForMultipleClients() {
        for (long seed : new long[]{0, -1, Long.MIN_VALUE, Long.MAX_VALUE}) {
            DialogueSignal sent = signal(seed, 32);
            FriendlyByteBuf buffer = new FriendlyByteBuf(Unpooled.buffer());
            try {
                sent.encode(buffer);
                buffer.markReaderIndex();
                DialogueSignal firstClient = DialogueSignal.decode(buffer);
                buffer.resetReaderIndex();
                DialogueSignal secondClient = DialogueSignal.decode(buffer);
                assertEquals(sent, firstClient);
                assertEquals(firstClient, secondClient);
                assertEquals(1000, firstClient.startTick());
            } finally {
                buffer.release();
            }
        }
    }

    @Test
    void enforcesRangeAndOriginalExpiryForLateObservers() {
        DialogueSignal signal = signal(0, 32);
        assertTrue(signal.inRange(32 * 32));
        assertFalse(signal.inRange(32 * 32 + 0.01));
        assertFalse(signal.inRange(Double.NaN));
        assertFalse(signal.expired(1079));
        assertTrue(signal.expired(1080));
        assertThrows(IllegalArgumentException.class, () -> signal(0, Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> signal(0, 129));
    }

    @Test
    void requiresTheChannelOnBothEnds() {
        assertTrue(DialogueNetwork.accepts("1"));
        assertFalse(DialogueNetwork.accepts("0"));
        assertFalse(DialogueNetwork.accepts(NetworkRegistry.ABSENT.version()));
        assertFalse(DialogueNetwork.accepts(NetworkRegistry.ACCEPTVANILLA));
    }
}
