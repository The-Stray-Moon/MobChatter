package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.network.DialogueSignal;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityLeaveLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class DialogueController {
    private static final Map<UUID, DialogueState> STATES = new HashMap<>();
    private static ClientLevel level;

    private DialogueController() {
    }

    public static void clear() {
        STATES.clear();
    }

    private static void updateLevel() {
        ClientLevel current = Minecraft.getInstance().level;
        if (level != current) {
            clear();
            level = current;
        }
    }

    public static void receive(DialogueSignal signal) {
        updateLevel();
        if (level == null || !CommonConfig.ENABLED.get()
                || !level.dimension().location().equals(signal.dimension())
                || signal.expired(level.getGameTime())) {
            return;
        }
        var entity = level.getEntity(signal.entityId());
        if (!(entity instanceof LivingEntity) || entity instanceof Player
                || !entity.getUUID().equals(signal.entityUuid())
                || !signal.entityType().equals(ForgeRegistries.ENTITY_TYPES.getKey(entity.getType()))) {
            return;
        }
        DialogueState state = STATES.get(entity.getUUID());
        if (state != null && state.sequence >= signal.sequence()) {
            return;
        }
        String[] line = DialogueManager.pick(signal.entityType().toString(), signal.scenario(), signal.seed());
        if (line == null) {
            return;
        }
        if (state == null) {
            state = new DialogueState();
            STATES.put(entity.getUUID(), state);
        }
        state.previous = state.current;
        state.current = new Bubble(line[0], line[1], signal.startTick(), signal.duration(), signal.fadeTicks(), signal.range());
        state.sequence = signal.sequence();
    }

    @SubscribeEvent
    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
        updateLevel();
        if (level != null) {
            long now = level.getGameTime();
            STATES.values().removeIf(state -> state.current == null || now - state.current.startTick >= state.current.duration);
        }
    }

    @SubscribeEvent
    public static void onLeave(EntityLeaveLevelEvent event) {
        if (event.getLevel().isClientSide()) {
            STATES.remove(event.getEntity().getUUID());
        }
    }

    public static DialogueState stateOf(LivingEntity entity) {
        return STATES.get(entity.getUUID());
    }
}
