package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.platform.DialogueConfig;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BubbleLayoutTest {
    private static final DialogueConfig CONFIG = new DialogueConfig() {
        public boolean enabled() { return true; }
        public double maxDistance() { return 32.0D; }
        public int displayDuration() { return 80; }
        public int fadeOut() { return 20; }
        public int scenarioCooldown() { return 160; }
        public double chance() { return 0.35D; }
        public double lineSpacing() { return 10.0D; }
        public double bottomScale() { return 0.8D; }
        public double bottomAlpha() { return 0.55D; }
        public String language() { return "en"; }
        public boolean requireReceiver() { return false; }
    };

    @Test
    void keepsTheCurrentLineFullyOpaqueUntilTheFadeWindow() {
        DialogueState state = new DialogueState();
        state.current = new Bubble("甲", "A", 100, 80, 20, 32);
        assertEquals(1.0F, BubbleLayout.fade(state.current, 100));
        assertEquals(1.0F, BubbleLayout.fade(state.current, 160));
        assertEquals(0.5F, BubbleLayout.fade(state.current, 170));
        assertEquals(0.0F, BubbleLayout.fade(state.current, 180));
    }

    @Test
    void showsThePreviousLineInTheConfiguredLanguageAndClearsExpiredOnes() {
        DialogueState state = new DialogueState();
        state.current = new Bubble("甲", "A", 100, 80, 20, 32);
        state.previous = new Bubble("乙", "B", 60, 80, 20, 32);
        BubbleLayout.View view = BubbleLayout.view(state, 110, 4.0D, CONFIG);
        assertNotNull(view);
        assertEquals("A", view.top());
        assertEquals("B", view.bottom());
        assertEquals(1.0F, view.topAlpha());
        assertEquals(1.0F, view.bottomAlpha());
        assertEquals(10.0F, view.lineSpacing());
        assertEquals(0.8F, view.bottomScale());
        assertNull(BubbleLayout.view(state, 200, 4.0D, CONFIG));
        assertNull(state.current);
    }

    @Test
    void hidesEverythingOutsideTheServerProvidedRange() {
        DialogueState state = new DialogueState();
        state.current = new Bubble("甲", "A", 100, 80, 20, 32);
        assertNull(BubbleLayout.view(state, 110, 33 * 33, CONFIG));
        assertEquals(0x00, BubbleLayout.alpha(0.0F));
        assertEquals(0xFF, BubbleLayout.alpha(1.0F));
        assertEquals(0x7F, BubbleLayout.alpha(0.5F));
    }
}
