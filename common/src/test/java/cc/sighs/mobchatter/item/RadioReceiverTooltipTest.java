package cc.sighs.mobchatter.item;

import cc.sighs.mobchatter.platform.DialogueConfig;
import cc.sighs.mobchatter.platform.DialogueNetworking;
import cc.sighs.mobchatter.platform.MobChatterPlatform;
import cc.sighs.mobchatter.platform.Platforms;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RadioReceiverTooltipTest {
    private static final class Config implements DialogueConfig {
        boolean requireReceiver;

        Config(boolean requireReceiver) {
            this.requireReceiver = requireReceiver;
        }

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
        public boolean requireReceiver() { return requireReceiver; }
    }

    private static final class Platform implements MobChatterPlatform {
        final Config config = new Config(false);

        public DialogueConfig config() { return config; }
        public DialogueNetworking networking() { return null; }
        public Level levelOf(Entity entity) { return null; }
        public String entityTypeId(Entity entity) { return null; }
        public String dimensionId(Level level) { return null; }
        public String damageScenario(DamageSource source) { return "hurt"; }
        public boolean onGround(Entity entity) { return true; }
        public boolean isWearingReceiver(Player player) { return false; }
        public MutableComponent translatable(String key) { return null; }
        public String gameLanguage() { return "en_us"; }
    }

    @Test
    void describesTheCurrentReceiverSetting() {
        Platform platform = new Platform();
        Platforms.install(platform);

        assertEquals(2, RadioReceiverTooltip.keys().size());
        assertEquals(RadioReceiverTooltip.SLOT_KEY, RadioReceiverTooltip.keys().get(0));
        assertEquals(RadioReceiverTooltip.DISABLED_KEY, RadioReceiverTooltip.keys().get(1));

        platform.config.requireReceiver = true;
        assertEquals(RadioReceiverTooltip.ENABLED_KEY, RadioReceiverTooltip.keys().get(1));
    }
}
