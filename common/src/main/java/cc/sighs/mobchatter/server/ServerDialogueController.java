package cc.sighs.mobchatter.server;

import cc.sighs.mobchatter.network.DialogueSignal;
import cc.sighs.mobchatter.platform.DialogueConfig;
import cc.sighs.mobchatter.platform.Platforms;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative trigger state machine.
 *
 * <p>Loaders only forward join/leave/tracking/damage/tick events and deliver
 * the resulting signals. Trigger arbitration, cooldowns, audience selection
 * and the random seed live here so every target behaves identically.</p>
 */
public final class ServerDialogueController {
    private static final Map<LivingEntity, State> STATES = new HashMap<>();
    private static final Random RANDOM = new Random();
    private static long sequence;

    private ServerDialogueController() {
    }

    public static void onJoin(Entity entity, Level level, boolean loadedFromDisk) {
        if (level instanceof ServerLevel serverLevel && eligible(entity) && !loadedFromDisk) {
            LivingEntity living = (LivingEntity) entity;
            serverLevel.getServer().execute(() -> {
                if (!living.isRemoved()) {
                    STATES.computeIfAbsent(living, State::new).spawn = true;
                }
            });
        }
    }

    public static void onLeave(Entity entity, Level level) {
        if (level instanceof ServerLevel serverLevel) {
            serverLevel.getServer().execute(() -> STATES.remove(entity));
        }
    }

    public static void onStartTracking(Entity target, ServerPlayer player) {
        if (eligible(target)) {
            STATES.computeIfAbsent((LivingEntity) target, State::new).tracking.add(player.getUUID());
        }
    }

    public static void onStopTracking(Entity target, ServerPlayer player) {
        State state = STATES.get(target);
        if (state != null) {
            state.tracking.remove(player.getUUID());
            state.delivered.remove(player.getUUID());
        }
    }

    public static void onLogout(ServerPlayer player) {
        for (State state : STATES.values()) {
            state.tracking.remove(player.getUUID());
            state.delivered.remove(player.getUUID());
        }
    }

    public static void onDamage(LivingEntity entity, DamageSource source, float amount) {
        if (Platforms.get().levelOf(entity) instanceof ServerLevel
                && eligible(entity) && amount > 0 && Platforms.get().config().enabled()) {
            State state = STATES.computeIfAbsent(entity, State::new);
            offer(entity, state, Platforms.get().damageScenario(source), 1.0D, 100);
        }
    }

    public static void tick(MinecraftServer server) {
        DialogueConfig config = Platforms.get().config();
        if (!config.enabled()) {
            STATES.values().forEach(state -> {
                state.pending = null;
                state.spawn = false;
                state.active = null;
                state.delivered.clear();
            });
            return;
        }
        Set<UUID> lookedAt = lookedAt(server, config);
        Iterator<Map.Entry<LivingEntity, State>> iterator = STATES.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<LivingEntity, State> entry = iterator.next();
            LivingEntity entity = entry.getKey();
            State state = entry.getValue();
            if (entity.isRemoved()) {
                iterator.remove();
                continue;
            }
            Level level = Platforms.get().levelOf(entity);
            if (!(level instanceof ServerLevel serverLevel)) {
                iterator.remove();
                continue;
            }
            long now = level.getGameTime();
            List<ServerPlayer> audience = audience(server, entity, serverLevel, state, config);
            if (!audience.isEmpty()) {
                update(entity, state, audience, config, lookedAt.contains(entity.getUUID()));
                if (state.pending != null) {
                    Candidate candidate = state.pending;
                    state.active = new DialogueSignal(Platforms.get().dimensionId(level), entity.getId(), entity.getUUID(),
                            Platforms.get().entityTypeId(entity), candidate.scenario(),
                            RANDOM.nextLong(), sequence++, now, config.displayDuration(),
                            config.fadeOut(), config.maxDistance());
                    state.lastByScenario.put(candidate.scenario(), now);
                    state.delivered.clear();
                }
                if (state.active != null && !state.active.expired(now)) {
                    for (ServerPlayer player : audience) {
                        if (state.active.inRange(entity.distanceToSqr(player))
                                && state.delivered.add(player.getUUID())) {
                            Platforms.get().networking().send(player, state.active);
                        }
                    }
                }
            }
            state.pending = null;
            state.spawn = false;
            if (state.active != null && state.active.expired(now)) {
                state.active = null;
                state.delivered.clear();
            }
            state.sample(entity, config);
            if (state.tracking.isEmpty() && state.active == null) {
                iterator.remove();
            }
        }
    }

    public static void clear() {
        STATES.clear();
        sequence = 0;
    }

    public static boolean eligible(Entity entity) {
        return entity instanceof LivingEntity && !(entity instanceof Player);
    }

    private static Set<UUID> lookedAt(MinecraftServer server, DialogueConfig config) {
        Set<UUID> lookedAt = new HashSet<>();
        for (ServerPlayer player : server.getPlayerList().getPlayers()) {
            if (player.isSpectator()) {
                continue;
            }
            double range = config.maxDistance();
            Vec3 from = player.getEyePosition();
            Vec3 delta = player.getLookAngle().scale(range);
            HitResult block = player.pick(range, 1.0F, false);
            double limit = block.getType() == HitResult.Type.MISS ? range * range
                    : from.distanceToSqr(block.getLocation());
            var hit = ProjectileUtil.getEntityHitResult(player, from, from.add(delta),
                    player.getBoundingBox().expandTowards(delta).inflate(1.0D),
                    entity -> eligible(entity) && entity.isPickable() && !entity.isSpectator(), limit);
            if (hit != null) {
                lookedAt.add(hit.getEntity().getUUID());
            }
        }
        return lookedAt;
    }

    private static List<ServerPlayer> audience(MinecraftServer server, LivingEntity entity, ServerLevel level,
                                               State state, DialogueConfig config) {
        List<ServerPlayer> audience = new ArrayList<>();
        double max = config.maxDistance();
        for (UUID uuid : state.tracking) {
            ServerPlayer player = server.getPlayerList().getPlayer(uuid);
            if (player != null && Platforms.get().levelOf(player) == level
                    && entity.distanceToSqr(player) <= max * max) {
                audience.add(player);
            }
        }
        return audience;
    }

    private static void update(LivingEntity entity, State state, List<ServerPlayer> audience,
                               DialogueConfig config, boolean lookedAt) {
        if (state.spawn) {
            offer(entity, state, "spawn", 0.7D, 90);
        }
        if (entity instanceof Mob mob) {
            UUID target = mob.getTarget() == null ? null : mob.getTarget().getUUID();
            if (target != null) {
                offer(entity, state, target.equals(state.lastTarget) ? "targeting" : "target_acquire",
                        target.equals(state.lastTarget) ? ambient(config, 0.7D) : 1.0D, 80);
            }
            if (handCount(entity) > state.lastHandCount) {
                offer(entity, state, "pickup", 0.9D, 60);
            }
        }
        if (entity.swinging && !state.lastSwinging) {
            offer(entity, state, "melee_attack", 0.9D, 70);
        }
        if (entity instanceof Animal animal) {
            if (animal.isInLove()) {
                offer(entity, state, "mate", 0.6D, 50);
            }
            if (audience.stream().anyMatch(player -> !player.isSpectator()
                    && entity.distanceToSqr(player) < 64.0D
                    && (animal.isFood(player.getMainHandItem()) || animal.isFood(player.getOffhandItem())))) {
                offer(entity, state, "tempted", 0.45D, 40);
            }
        }
        if (audience.stream().anyMatch(player -> !player.isSpectator()
                && player.getBoundingBox().inflate(0.08D).intersects(entity.getBoundingBox()))) {
            offer(entity, state, "collide", 0.35D, 30);
        }
        if (lookedAt) {
            offer(entity, state, "look_player", ambient(config, 0.6D), 20);
        }
        double moved = entity.position().distanceToSqr(state.position);
        if (moved > 2.5E-4D && Platforms.get().onGround(entity)) {
            state.stillTicks = 0;
            offer(entity, state, "walk", ambient(config, 0.3D), 10);
        } else if (++state.stillTicks > 60) {
            offer(entity, state, "idle", ambient(config, 0.3D), 10);
        }
    }

    private static void offer(LivingEntity entity, State state, String scenario, double chance, int priority) {
        long now = Platforms.get().levelOf(entity).getGameTime();
        if (state.pending != null && state.pending.priority() >= priority
                || now - state.lastByScenario.getOrDefault(scenario, Long.MIN_VALUE / 4)
                < Platforms.get().config().scenarioCooldown()
                || chance < 1.0D && RANDOM.nextDouble() > chance) {
            return;
        }
        state.pending = new Candidate(scenario, priority);
    }

    private static double ambient(DialogueConfig config, double factor) {
        return config.chance() * factor;
    }

    private static int handCount(LivingEntity entity) {
        return entity.getMainHandItem().getCount() + entity.getOffhandItem().getCount();
    }

    private record Candidate(String scenario, int priority) {
    }

    private static final class State {
        final Set<UUID> tracking = new HashSet<>();
        final Set<UUID> delivered = new HashSet<>();
        final Map<String, Long> lastByScenario = new HashMap<>();
        Vec3 position;
        UUID lastTarget;
        boolean lastSwinging;
        int lastHandCount;
        int stillTicks;
        boolean spawn;
        Candidate pending;
        DialogueSignal active;

        State(LivingEntity entity) {
            sample(entity, Platforms.get().config());
        }

        void sample(LivingEntity entity, DialogueConfig config) {
            position = entity.position();
            lastTarget = entity instanceof Mob mob && mob.getTarget() != null ? mob.getTarget().getUUID() : null;
            lastSwinging = entity.swinging;
            lastHandCount = handCount(entity);
        }
    }
}
