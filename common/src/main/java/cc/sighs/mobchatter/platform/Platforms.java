package cc.sighs.mobchatter.platform;

import java.util.Objects;

/**
 * Explicit service registration performed by each loader entry point.
 *
 * <p>No reflection, version sniffing or classpath override is involved: a
 * target either installs its platform during mod construction or the shared
 * code fails loudly.</p>
 */
public final class Platforms {
    private static volatile MobChatterPlatform platform;

    private Platforms() {
    }

    public static void install(MobChatterPlatform installed) {
        Objects.requireNonNull(installed, "platform");
        if (platform != null && platform != installed) {
            throw new IllegalStateException("MobChatter platform already installed: " + platform.getClass());
        }
        platform = installed;
    }

    public static MobChatterPlatform get() {
        MobChatterPlatform current = platform;
        if (current == null) {
            throw new IllegalStateException("MobChatter platform has not been installed");
        }
        return current;
    }

    public static boolean isInstalled() {
        return platform != null;
    }
}
