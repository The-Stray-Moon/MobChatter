package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.platform.DialogueConfig;
import cc.sighs.mobchatter.platform.Platforms;

/**
 * Shared layout maths: which two texts are visible, their opacity, and the
 * second-line scale and spacing. Targets only translate this view into their
 * version's text drawing API.
 */
public final class BubbleLayout {
    public record View(String top, float topAlpha, String bottom, float bottomAlpha,
                       float lineSpacing, float bottomScale) {
    }

    private BubbleLayout() {
    }

    public static View view(DialogueState state, long now, double distanceSquared, DialogueConfig config) {
        if (state.current == null) {
            return null;
        }
        float currentAlpha = fade(state.current, now);
        if (currentAlpha <= 0.0F) {
            state.current = null;
            return null;
        }
        if (distanceSquared > state.current.range * state.current.range) {
            return null;
        }
        float previousAlpha = 0.0F;
        if (state.previous != null) {
            previousAlpha = distanceSquared > state.previous.range * state.previous.range
                    ? 0.0F : fade(state.previous, now);
            if (previousAlpha <= 0.0F) {
                state.previous = null;
            }
        }

        boolean chinese = useChinese(config.language(), selectedLanguage());
        String top = chinese ? state.current.zh : state.current.en;
        String bottom = state.previous == null ? null : (chinese ? state.previous.zh : state.previous.en);
        if (top == null || top.isEmpty()) {
            return null;
        }
        return new View(top, currentAlpha, bottom, previousAlpha,
                (float) config.lineSpacing(), (float) config.bottomScale());
    }

    static boolean useChinese(String configured, String selected) {
        if ("zh".equalsIgnoreCase(configured)) {
            return true;
        }
        if ("en".equalsIgnoreCase(configured)) {
            return false;
        }
        return selected != null && selected.toLowerCase(java.util.Locale.ROOT).contains("zh");
    }

    private static String selectedLanguage() {
        return Platforms.isInstalled() ? Platforms.get().gameLanguage() : null;
    }

    public static float fade(Bubble bubble, long now) {
        long age = Math.max(0, now - bubble.startTick);
        if (age >= bubble.duration) {
            return 0.0F;
        }
        int fadeStart = Math.max(0, bubble.duration - bubble.fadeTicks);
        if (age <= fadeStart) {
            return 1.0F;
        }
        return 1.0F - (age - fadeStart) / (float) Math.max(1, bubble.fadeTicks);
    }

    public static int alpha(float value) {
        return Math.max(0, Math.min(255, (int) (value * 255.0F)));
    }
}
