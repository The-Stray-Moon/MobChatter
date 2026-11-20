package com.merrysnow.mobchatter.platform;

import com.merrysnow.mobchatter.compat.CuriosBridge;
import com.merrysnow.mobchatter.config.CommonConfig;
import com.merrysnow.mobchatter.item.ModItems;
import com.merrysnow.mobchatter.network.DialogueNetwork;
import net.minecraft.network.chat.TranslatableComponent;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.registries.ForgeRegistries;

public final class ForgePlatform implements MobChatterPlatform {
    private final DialogueNetwork networking = new DialogueNetwork();

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
        return entity.level;
    }

    @Override
    public String entityTypeId(Entity entity) {
        ResourceLocation id = ForgeRegistries.ENTITIES.getKey(entity.getType());
        return id == null ? null : id.toString();
    }

    @Override
    public String dimensionId(Level level) {
        return level.dimension().location().toString();
    }

    @Override
    public String damageScenario(DamageSource source) {
        String id = source.getMsgId();
        if (id.equals("lightningBolt")) return "hurt.lightning";
        if (id.equals("outOfWorld")) return "hurt.void";
        if (id.equals("drown")) return "hurt.drown";
        if (id.equals("starve")) return "hurt.starvation";
        if (source.isFire()) return "hurt.fire";
        if (source.isFall()) return "hurt.fall";
        if (source.isExplosion()) return "hurt.explosion";
        if (source.isProjectile()) return "hurt.projectile";
        if (source.isMagic()) return "hurt.magic";
        return "hurt";
    }

    @Override
    public boolean onGround(Entity entity) {
        return entity.isOnGround();
    }

    @Override
    public boolean isWearingReceiver(Player player) {
        if (player.getItemBySlot(EquipmentSlot.HEAD).is(ModItems.radioReceiver())) {
            return true;
        }
        return ModList.get().isLoaded("curios") && CuriosBridge.isWearing(player);
    }

    @Override
    public net.minecraft.network.chat.MutableComponent translatable(String key) {
        return new TranslatableComponent(key);
    }
}
