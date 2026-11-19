package com.merrysnow.mobchatter.server;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.network.DialogueNetwork;
import com.merrysnow.mobchatter.network.DialogueSignal;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.event.entity.EntityLeaveLevelEvent;
import net.minecraftforge.event.entity.living.LivingDamageEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.server.ServerStoppedEvent;
import net.minecraftforge.eventbus.api.EventPriority;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;

@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class ServerDialogueController {
    private static final Map<LivingEntity, State> STATES = new HashMap<>();
    private static final Random RANDOM = new Random();
    private static long sequence;

    private ServerDialogueController() {
    }

    @SubscribeEvent
    public static void onJoin(EntityJoinLevelEvent event) {
        if (event.getLevel() instanceof ServerLevel level && eligible(event.getEntity()) && !event.loadedFromDisk()) {
            LivingEntity entity = (LivingEntity) event.getEntity();
            level.getServer().execute(() -> {
                if (!entity.isRemoved()) {
                    STATES.computeIfAbsent(entity, State::new).spawn = true;
                }
            });
        }
    }

    @SubscribeEvent
    public static void onLeave(EntityLeaveLevelEvent event) {
        if (event.getLevel() instanceof ServerLevel level) {
            level.getServer().execute(() -> STATES.remove(event.getEntity()));
        }
    }

    @SubscribeEvent
    public static void onStartTracking(PlayerEvent.StartTracking event) {
        if (event.getEntity() instanceof ServerPlayer player && eligible(event.getTarget())) {
            LivingEntity entity = (LivingEntity) event.getTarget();
            STATES.computeIfAbsent(entity, State::new).tracking.add(player.getUUID());
        }
    }

    @SubscribeEvent
    public static void onStopTracking(PlayerEvent.StopTracking event) {
        State state = STATES.get(event.getTarget());
        if (state != null && event.getEntity() instanceof ServerPlayer player) {
            state.tracking.remove(player.getUUID());
            state.delivered.remove(player.getUUID());
        }
    }

    @SubscribeEvent
    public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        for (State state : STATES.values()) {
            state.tracking.remove(event.getEntity().getUUID());
            state.delivered.remove(event.getEntity().getUUID());
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void onDamage(LivingDamageEvent event) {
        LivingEntity entity = event.getEntity();
        if (entity.level() instanceof ServerLevel && eligible(entity) && event.getAmount() > 0
                && CommonConfig.ENABLED.get()) {
            State state = STATES.computeIfAbsent(entity, State::new);
            offer(entity, state, damageScenario(event.getSource()), 1.0D, 100);
        }
    }

    @SubscribeEvent
    public static void onTick(TickEvent.ServerTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
        if (!CommonConfig.ENABLED.get()) {
            STATES.values().forEach(state -> {
                state.pending = null;
                state.spawn = false;
                state.active = null;
                state.delivered.clear();
            });
            return;
        }
        Set<UUID> lookedAt = new HashSet<>();
        for (ServerPlayer player : event.getServer().getPlayerList().getPlayers()) {
            if (player.isSpectator()) {
                continue;
            }
            double range = CommonConfig.MAX_DISTANCE.get();
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
        var iterator = STATES.entrySet().iterator();
        while (iterator.hasNext()) {
            var entry = iterator.next();
            LivingEntity entity = entry.getKey();
            State state = entry.getValue();
            if (entity.isRemoved()) {
                iterator.remove();
                continue;
            }
            ServerLevel level = (ServerLevel) entity.level();
            long now = level.getGameTime();
            List<ServerPlayer> audience = new ArrayList<>();
            for (UUID uuid : state.tracking) {
                ServerPlayer player = event.getServer().getPlayerList().getPlayer(uuid);
                if (player != null && player.level() == level
                        && entity.distanceToSqr(player) <= CommonConfig.MAX_DISTANCE.get() * CommonConfig.MAX_DISTANCE.get()) {
                    audience.add(player);
                }
            }
            if (!audience.isEmpty()) {
                update(entity, state, audience, lookedAt.contains(entity.getUUID()));
                if (state.pending != null) {
                    Candidate candidate = state.pending;
                    state.active = new DialogueSignal(level.dimension().location(), entity.getId(), entity.getUUID(),
                            ForgeRegistries.ENTITY_TYPES.getKey(entity.getType()), candidate.scenario(),
                            RANDOM.nextLong(), sequence++, now, CommonConfig.DISPLAY_DURATION.get(),
                            CommonConfig.FADE_OUT.get(), CommonConfig.MAX_DISTANCE.get());
                    state.lastByScenario.put(candidate.scenario(), now);
                    state.delivered.clear();
                }
                if (state.active != null && !state.active.expired(now)) {
                    for (ServerPlayer player : audience) {
                        if (state.active.inRange(entity.distanceToSqr(player)) && state.delivered.add(player.getUUID())) {
                            DialogueNetwork.send(player, state.active);
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
            state.sample(entity);
            if (state.tracking.isEmpty() && state.active == null) {
                iterator.remove();
            }
        }
    }

    private static void update(LivingEntity entity, State state, List<ServerPlayer> audience, boolean lookedAt) {
        if (state.spawn) {
            offer(entity, state, "spawn", 0.7D, 90);
        }
        if (entity instanceof Mob mob) {
            UUID target = mob.getTarget() == null ? null : mob.getTarget().getUUID();
            if (target != null) {
                offer(entity, state, target.equals(state.lastTarget) ? "targeting" : "target_acquire",
                        target.equals(state.lastTarget) ? ambient(0.7D) : 1.0D, 80);
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
            if (audience.stream().anyMatch(player -> !player.isSpectator() && entity.distanceToSqr(player) < 64.0D
                    && (animal.isFood(player.getMainHandItem()) || animal.isFood(player.getOffhandItem())))) {
                offer(entity, state, "tempted", 0.45D, 40);
            }
        }
        if (audience.stream().anyMatch(player -> !player.isSpectator()
                && player.getBoundingBox().inflate(0.08D).intersects(entity.getBoundingBox()))) {
            offer(entity, state, "collide", 0.35D, 30);
        }
        if (lookedAt) {
            offer(entity, state, "look_player", ambient(0.6D), 20);
        }
        double moved = entity.position().distanceToSqr(state.position);
        if (moved > 2.5E-4D && entity.onGround()) {
            state.stillTicks = 0;
            offer(entity, state, "walk", ambient(0.3D), 10);
        } else if (++state.stillTicks > 60) {
            offer(entity, state, "idle", ambient(0.3D), 10);
        }
    }

    private static void offer(LivingEntity entity, State state, String scenario, double chance, int priority) {
        long now = entity.level().getGameTime();
        if (state.pending != null && state.pending.priority() >= priority
                || now - state.lastByScenario.getOrDefault(scenario, Long.MIN_VALUE / 4) < CommonConfig.SCENARIO_COOLDOWN.get()
                || chance < 1.0D && RANDOM.nextDouble() > chance) {
            return;
        }
        state.pending = new Candidate(scenario, priority);
    }

    public static String damageScenario(DamageSource source) {
        if (source.is(DamageTypes.LIGHTNING_BOLT)) return "hurt.lightning";
        if (source.is(DamageTypes.FELL_OUT_OF_WORLD)) return "hurt.void";
        if (source.is(DamageTypes.DROWN)) return "hurt.drown";
        if (source.is(DamageTypes.STARVE)) return "hurt.starvation";
        if (source.is(DamageTypeTags.IS_FIRE)) return "hurt.fire";
        if (source.is(DamageTypeTags.IS_FALL)) return "hurt.fall";
        if (source.is(DamageTypeTags.IS_EXPLOSION)) return "hurt.explosion";
        if (source.is(DamageTypeTags.IS_PROJECTILE)) return "hurt.projectile";
        if (source.is(DamageTypes.MAGIC) || source.is(DamageTypes.INDIRECT_MAGIC)
                || source.is(DamageTypes.WITHER) || source.is(DamageTypes.DRAGON_BREATH)) return "hurt.magic";
        return "hurt";
    }

    private static boolean eligible(Entity entity) {
        return entity instanceof LivingEntity && !(entity instanceof Player);
    }

    private static double ambient(double factor) {
        return CommonConfig.CHANCE.get() * factor;
    }

    private static int handCount(LivingEntity entity) {
        return entity.getMainHandItem().getCount() + entity.getOffhandItem().getCount();
    }

    @SubscribeEvent
    public static void onStopped(ServerStoppedEvent event) {
        STATES.clear();
        sequence = 0;
    }

    private record Candidate(String scenario, int priority) { }

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
            sample(entity);
        }

        void sample(LivingEntity entity) {
            position = entity.position();
            lastTarget = entity instanceof Mob mob && mob.getTarget() != null ? mob.getTarget().getUUID() : null;
            lastSwinging = entity.swinging;
            lastHandCount = handCount(entity);
        }
    }
}
