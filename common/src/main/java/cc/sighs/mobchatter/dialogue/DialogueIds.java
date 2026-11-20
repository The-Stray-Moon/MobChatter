package cc.sighs.mobchatter.dialogue;

import java.util.regex.Pattern;

/**
 * Version-independent resource id syntax.
 *
 * <p>Minecraft calls this type {@code ResourceLocation} through 1.21.11 and
 * {@code Identifier} from 26.1. The shared layer keeps ids as strings and
 * validates them with the same namespace/path grammar.</p>
 */
public final class DialogueIds {
    private static final Pattern VALID = Pattern.compile("[a-z0-9_.-]+:[a-z0-9_./-]+");

    private DialogueIds() {
    }

    public static boolean isValid(String id) {
        return id != null && VALID.matcher(id).matches();
    }
}
