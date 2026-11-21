package cc.sighs.mobchatter.platform;

import cc.sighs.mobchatter.config.FileDialogueConfig;
import cc.sighs.mobchatter.item.ModItems;
import cc.sighs.mobchatter.network.FabricDialogueNetwork;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

public final class FabricPlatform implements MobChatterPlatform {
    private final DialogueConfig config = FileDialogueConfig.load(
            FabricLoader.getInstance().getConfigDir().resolve(FileDialogueConfig.FILE_NAME));
    private final DialogueNetworking networking = new FabricDialogueNetwork();

    @Override
    public DialogueConfig config() {
        return config;
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
        Identifier id = BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType());
        return id == null ? null : id.toString();
    }

    @Override
    public String dimensionId(Level level) {
        return level.dimension().identifier().toString();
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
        return player.getItemBySlot(EquipmentSlot.HEAD).is(ModItems.radioReceiver());
    }

    @Override
    public net.minecraft.network.chat.MutableComponent translatable(String key) {
        return Component.translatable(key);
    }

    @Override
    public String gameLanguage() {
        return net.minecraft.client.Minecraft.getInstance().getLanguageManager().getSelected();
    }
}
