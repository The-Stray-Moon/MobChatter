package com.merrysnow.mobchatter.client;

import org.junit.jupiter.api.Test;
import org.tukaani.xz.XZInputStream;

import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;

import static org.junit.jupiter.api.Assertions.*;

class DialogueResourceTest {
    @Test
    void decodesCompleteDialogueWithoutChangingContent() throws Exception {
        assertNull(getClass().getResource("/assets/mobchatter/dialogue.json.gz"));
        try (InputStream resource = getClass().getResourceAsStream("/assets/mobchatter/dialogue.json.xz")) {
            assertNotNull(resource);
            try (XZInputStream decoded = new XZInputStream(resource)) {
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] buffer = new byte[8192];
                long size = 0;
                int count;
                while ((count = decoded.read(buffer)) != -1) {
                    digest.update(buffer, 0, count);
                    size += count;
                }
                assertEquals(74296757L, size);
                assertEquals("ddd6fad5aca8fa3867efce6d43ceee7761075d856d72d0c7b6e5e12232e5ba10",
                        HexFormat.of().formatHex(digest.digest()));
            }
        }
    }
}
