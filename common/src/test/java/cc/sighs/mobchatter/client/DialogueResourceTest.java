package cc.sighs.mobchatter.client;

import org.junit.jupiter.api.Test;
import org.tukaani.xz.XZInputStream;

import java.io.InputStream;
import java.io.OutputStream;

import static org.junit.jupiter.api.Assertions.*;

class DialogueResourceTest {
    @Test
    void decodesCompleteDialogueLibrary() throws Exception {
        assertNull(getClass().getResource("/assets/mobchatter/dialogue.json.gz"));
        try (InputStream resource = getClass().getResourceAsStream("/assets/mobchatter/dialogue.json.xz")) {
            assertNotNull(resource);
            try (XZInputStream decoded = new XZInputStream(resource)) {
                long size = decoded.transferTo(OutputStream.nullOutputStream());
                assertTrue(size > 70_000_000L, "Dialogue library is unexpectedly small: " + size);
            }
        }
    }
}
