package com.merrysnow.mobchatter.platform;

import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * The only loader and Minecraft-version boundary used by the shared code.
 *
 * <p>Every member represents a confirmed difference between targets: Minecraft
 * renamed accessors, loader registries differ, id types were renamed from
 * {@code ResourceLocation} to {@code Identifier} in 26.1, and damage
 * classification moved from {@code DamageSource} predicates to damage type
 * tags. The shared logic stays in {@code common}; each target supplies an
 * implementation in its own entry point.</p>
 */
public interface MobChatterPlatform {
    DialogueConfig config();

    DialogueNetworking networking();

    /** {@code Entity#level()} on 1.19.4+, the {@code level} field on 1.18.2/1.19.2. */
    Level levelOf(Entity entity);

    /** {@code ResourceLocation} in 1.18-1.21.11, {@code Identifier} from 26.1. */
    String entityTypeId(Entity entity);

    /** Dimension id, using the version's key accessor. */
    String dimensionId(Level level);

    /** Maps a damage source to a shared scenario id; tag support differs by version. */
    String damageScenario(DamageSource source);

    /** {@code onGround()} on 1.20+, {@code isOnGround()} on 1.18.2/1.19.2. */
    boolean onGround(Entity entity);

    /** True when the receiver is in the vanilla head slot or the optional Curios head slot. */
    boolean isWearingReceiver(Player player);
}
