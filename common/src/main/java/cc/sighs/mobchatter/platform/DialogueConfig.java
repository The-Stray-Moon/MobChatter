package cc.sighs.mobchatter.platform;

/**
 * Server and client settings shared by every loader.
 *
 * <p>The server side owns triggering, ranges, durations and cooldowns. The
 * client side owns language and text layout. Loaders may expose the same
 * values through their native config system, but the dialogue code only reads
 * through this contract.</p>
 */
public interface DialogueConfig {
    boolean enabled();

    double maxDistance();

    int displayDuration();

    int fadeOut();

    int scenarioCooldown();

    double chance();

    double lineSpacing();

    double bottomScale();

    double bottomAlpha();

    String language();

    /** When true, dialogue is only rendered while the player wears the radio receiver. */
    boolean requireReceiver();
}
