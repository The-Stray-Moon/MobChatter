package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.dialogue.DialogueStore;
import cc.sighs.mobchatter.platform.Platforms;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;

import java.util.Set;
import java.util.TreeSet;

/**
 * Collects entity ids that are loaded on this client but have no dialogue
 * entry. Explicitly disabled entries still count as present because the
 * merged snapshot keeps their scenario map.
 */
public final class UnsupportedScanner {
    private UnsupportedScanner() {
    }

    public static Set<String> collect(ClientLevel level) {
        Set<String> unsupported = new TreeSet<>();
        for (Entity entity : level.entitiesForRendering()) {
            if (!(entity instanceof LivingEntity) || entity instanceof Player) {
                continue;
            }
            String id = Platforms.get().entityTypeId(entity);
            if (id != null && !DialogueStore.isSupported(id)) {
                unsupported.add(id);
            }
        }
        return unsupported;
    }

    public static String joined(Set<String> unsupported) {
        return String.join("\n", unsupported);
    }
}
