package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.dialogue.DialogueStore;
import com.merrysnow.mobchatter.network.DialogueSignal;
import com.merrysnow.mobchatter.platform.Platforms;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Applies server signals to client state. It never rolls randomness or
 * re-triggers chatter: the seed, sequence and start tick all come from the
 * server.
 */
public final class ClientDialogueController {
    private static final Map<UUID, DialogueState> STATES = new HashMap<>();
    private static ClientLevel level;

    private ClientDialogueController() {
    }

    public static void clear() {
        STATES.clear();
    }

    /** Visibility gate shared by all renderers. */
    public static boolean canSee() {
        if (!Platforms.get().config().requireReceiver()) {
            return true;
        }
        Minecraft minecraft = Minecraft.getInstance();
        return minecraft.player != null && Platforms.get().isWearingReceiver(minecraft.player);
    }

    public static void receive(DialogueSignal signal) {
        updateLevel();
        ClientLevel current = level;
        if (current == null || !Platforms.get().config().enabled()
                || !Platforms.get().dimensionId(current).equals(signal.dimension())
                || signal.expired(current.getGameTime())) {
            return;
        }
        Entity entity = current.getEntity(signal.entityId());
        if (!(entity instanceof LivingEntity) || entity instanceof Player
                || !entity.getUUID().equals(signal.entityUuid())
                || !signal.entityType().equals(Platforms.get().entityTypeId(entity))) {
            return;
        }
        UUID uuid = entity.getUUID();
        DialogueState state = STATES.get(uuid);
        if (state != null && state.sequence >= signal.sequence()) {
            return;
        }
        String[] line = DialogueStore.pick(signal.entityType(), signal.scenario(), signal.seed());
        if (line == null) {
            return;
        }
        if (state == null) {
            state = new DialogueState();
            STATES.put(uuid, state);
        }
        state.previous = state.current;
        state.current = new Bubble(line[0], line[1], signal.startTick(), signal.duration(),
                signal.fadeTicks(), signal.range());
        state.sequence = signal.sequence();
    }

    public static void tick() {
        updateLevel();
        ClientLevel current = level;
        if (current != null) {
            long now = current.getGameTime();
            STATES.values().removeIf(state -> state.current == null
                    || now - state.current.startTick >= state.current.duration);
        }
    }

    public static void onEntityLeave(Entity entity) {
        STATES.remove(entity.getUUID());
    }

    public static DialogueState stateOf(LivingEntity entity) {
        return STATES.get(entity.getUUID());
    }

    private static void updateLevel() {
        ClientLevel current = Minecraft.getInstance().level;
        if (level != current) {
            clear();
            level = current;
        }
    }
}
