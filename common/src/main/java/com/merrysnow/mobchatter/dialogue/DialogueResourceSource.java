package com.merrysnow.mobchatter.dialogue;

import java.io.IOException;
import java.util.List;

/**
 * Loader-side view of loaded client resources.
 *
 * <p>Targets read the base XZ file and the ordered patch stack with their
 * version's resource-manager API, then hand the bytes to
 * {@link DialogueLoader}. The shared layer never touches version-specific
 * resource-manager signatures.</p>
 */
public interface DialogueResourceSource {
    /** Raw XZ bytes of {@code assets/mobchatter/dialogue.json.xz}. */
    byte[] base() throws IOException;

    /** Pack id of the base resource, for diagnostics. */
    String baseSource();

    /** Patch files in low-to-high pack order. */
    List<DialogueResource> patches() throws IOException;
}
