package com.merrysnow.mobchatter.platform;

import com.merrysnow.mobchatter.compat.CuriosBridge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.item.ModItems;
import com.merrysnow.mobchatter.network.NeoForgeDialogueNetwork;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.neoforged.fml.ModList;

public final class NeoForgePlatform implements MobChatterPlatform {
    private final NeoForgeDialogueNetwork networking = new NeoForgeDialogueNetwork();

    @Override
    public DialogueConfig config() {
        return CommonConfig.ADAPTER;
    }

    @Override
    public DialogueNetworking networking() {
        return networking;
    }

    @Override
    public Level levelOf(Entity entity) {
        return entity.level();
    }

    @Override
    public String entityTypeId(Entity entity) {
        ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType());
        return id == null ? null : id.toString();
    }

    @Override
    public String dimensionId(Level level) {
        return level.dimension().location().toString();
    }

    @Override
    public String damageScenario(DamageSource source) {
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

    @Override
    public boolean onGround(Entity entity) {
        return entity.onGround();
    }

    @Override
    public boolean isWearingReceiver(Player player) {
        if (player.getItemBySlot(EquipmentSlot.HEAD).is(ModItems.radioReceiver())) {
            return true;
        }
        return ModList.get().isLoaded("curios") && CuriosBridge.isWearing(player);
    }
}
