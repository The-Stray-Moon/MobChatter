package cc.sighs.mobchatter.network;

import net.minecraftforge.network.NetworkRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DialogueNetworkTest {
    @Test
    void requiresTheChannelOnBothEnds() {
        assertTrue(DialogueNetwork.accepts("1"));
        assertFalse(DialogueNetwork.accepts("0"));
        assertFalse(DialogueNetwork.accepts(NetworkRegistry.ABSENT.version()));
        assertFalse(DialogueNetwork.accepts(NetworkRegistry.ACCEPTVANILLA));
    }
}
