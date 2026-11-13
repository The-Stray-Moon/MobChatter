package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.config.CommonConfig;
import net.minecraft.client.Minecraft;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

/**
 * Client-side trigger detection. Picks a scenario, asks {@link DialogueManager}
 * for a line, and pushes it into the entity's bubble slot.
 */
@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class DialogueController {
    private static final Map<UUID, DialogueState> STATES = new HashMap<>();
    private static final Random RANDOM = new Random();

    private DialogueController() {
    }

    @SubscribeEvent
    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null) {
            STATES.clear();
            return;
        }
        if (!CommonConfig.ENABLED.get()) {
            return;
        }

        long now = minecraft.level.getGameTime();
        double maxDistance = CommonConfig.MAX_DISTANCE.get();
        double maxSqr = maxDistance * maxDistance;
        Player player = minecraft.player;

        for (Entity entity : minecraft.level.entitiesForRendering()) {
            if (!(entity instanceof LivingEntity living) || living == player) {
                continue;
            }
            if (living.distanceToSqr(player) > maxSqr) {
                continue;
            }
            DialogueState state = STATES.computeIfAbsent(living.getUUID(), key -> new DialogueState());
            if (!state.initialized) {
                state.initialized = true;
                state.lastHealth = living.getHealth();
                state.lastX = living.getX();
                state.lastY = living.getY();
                state.lastZ = living.getZ();
                state.lastTarget = living instanceof Mob mob ? idOf(mob.getTarget()) : null;
                state.lastMainCount = handCount(living);
                state.lastOffCount = living.getOffhandItem().getCount();
                trigger(living, state, "spawn", now, 0.7D);
                continue;
            }
            update(living, state, player, minecraft, now);
        }
    }

    private static void update(LivingEntity entity, DialogueState state, Player player,
                               Minecraft minecraft, long now) {
        float health = entity.getHealth();
        if (health < state.lastHealth - 0.05F) {
            trigger(entity, state, "hurt." + damageType(entity.getLastDamageSource()), now, 1.0D);
            state.lastHealth = health;
        } else {
            state.lastHealth = health;
        }

        if (entity instanceof Mob mob) {
            UUID targetId = idOf(mob.getTarget());
            if (targetId != null && !targetId.equals(state.lastTarget)) {
                trigger(entity, state, "target_acquire", now, 1.0D);
            } else if (targetId != null) {
                trigger(entity, state, "targeting", now, ambient(0.7D));
            }
            state.lastTarget = targetId;

            int mainCount = handCount(entity);
            int offCount = entity.getOffhandItem().getCount();
            if (mainCount > state.lastMainCount || offCount > state.lastOffCount) {
                trigger(entity, state, "pickup", now, 0.9D);
            }
            state.lastMainCount = mainCount;
            state.lastOffCount = offCount;
        }

        if (entity instanceof Animal animal) {
            if (animal.isInLove()) {
                trigger(entity, state, "mate", now, 0.6D);
            }
            ItemStack held = player.getMainHandItem();
            if (animal.isFood(held) && entity.distanceToSqr(player) < 64.0D) {
                trigger(entity, state, "tempted", now, 0.45D);
            }
        }

        if (player.getBoundingBox().inflate(0.08D).intersects(entity.getBoundingBox())) {
            trigger(entity, state, "collide", now, 0.35D);
        }

        if (entity.swinging && !state.lastSwinging) {
            trigger(entity, state, "melee_attack", now, 0.9D);
        }
        state.lastSwinging = entity.swinging;

        if (minecraft.crosshairPickEntity == entity) {
            trigger(entity, state, "look_player", now, ambient(0.6D));
        }

        double dx = entity.getX() - state.lastX;
        double dy = entity.getY() - state.lastY;
        double dz = entity.getZ() - state.lastZ;
        double movedSqr = dx * dx + dy * dy + dz * dz;
        if (movedSqr > 2.5E-4D && entity.onGround()) {
            state.stillTicks = 0;
            trigger(entity, state, "walk", now, ambient(0.3D));
        } else {
            state.stillTicks++;
            if (state.stillTicks > 60) {
                trigger(entity, state, "idle", now, ambient(0.3D));
            }
        }
        state.lastX = entity.getX();
        state.lastY = entity.getY();
        state.lastZ = entity.getZ();
    }

    public static DialogueState stateOf(LivingEntity entity) {
        return STATES.get(entity.getUUID());
    }

    private static double ambient(double factor) {
        return CommonConfig.CHANCE.get() * factor;
    }

    private static void trigger(LivingEntity entity, DialogueState state, String scenario,
                                long now, double chance) {
        long last = state.lastByScenario.getOrDefault(scenario, Long.MIN_VALUE / 4);
        if (now - last < CommonConfig.SCENARIO_COOLDOWN.get()) {
            return;
        }
        if (chance < 1.0D && RANDOM.nextDouble() > chance) {
            return;
        }
        String entityId = String.valueOf(ForgeRegistries.ENTITY_TYPES.getKey(entity.getType()));
        String[] line = DialogueManager.pick(entityId, scenario);
        if (line == null) {
            return;
        }
        if (state.current != null) {
            state.previous = state.current;
        }
        state.current = new Bubble(line[0], line[1], now);
        state.lastByScenario.put(scenario, now);
    }

    private static int handCount(LivingEntity entity) {
        return entity.getMainHandItem().getCount() + entity.getOffhandItem().getCount();
    }

    private static UUID idOf(Entity entity) {
        return entity == null ? null : entity.getUUID();
    }

    private static String damageType(DamageSource source) {
        if (source == null) {
            return "generic";
        }
        return switch (source.getMsgId()) {
            case "inFire", "onFire", "lava", "hotFloor" -> "fire";
            case "fall" -> "fall";
            case "drown" -> "drown";
            case "explosion", "player_explosion", "badRespawnPoint" -> "explosion";
            case "arrow", "trident", "mob_projectile", "fireball", "thrown", "witherSkull" -> "projectile";
            case "magic", "indirectMagic", "wither" -> "magic";
            case "starve" -> "starvation";
            case "lightningBolt" -> "lightning";
            case "outOfWorld", "fell_out_of_world" -> "void";
            default -> "generic";
        };
    }
}
