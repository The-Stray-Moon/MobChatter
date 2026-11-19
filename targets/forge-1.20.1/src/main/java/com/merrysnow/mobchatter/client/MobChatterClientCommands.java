package com.merrysnow.mobchatter.client;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.context.CommandContext;
import net.minecraft.client.Minecraft;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RegisterClientCommandsEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.Set;
import java.util.TreeSet;

import static net.minecraft.commands.Commands.literal;

@Mod.EventBusSubscriber(modid = "mobchatter", value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class MobChatterClientCommands {
    private MobChatterClientCommands() {
    }

    @SubscribeEvent
    public static void register(RegisterClientCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
        dispatcher.register(literal("mobchatterunsupported")
                .executes(MobChatterClientCommands::copyUnsupported));
    }

    private static int copyUnsupported(CommandContext<CommandSourceStack> context) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null) {
            context.getSource().sendFailure(Component.translatable("commands.mobchatter.no_level"));
            return 0;
        }
        Set<String> unsupported = new TreeSet<>();
        for (Entity entity : minecraft.level.entitiesForRendering()) {
            if (!(entity instanceof LivingEntity) || entity instanceof Player) {
                continue;
            }
            ResourceLocation id = ForgeRegistries.ENTITY_TYPES.getKey(entity.getType());
            if (id != null && !DialogueManager.isSupported(id.toString())) {
                unsupported.add(id.toString());
            }
        }
        String copied = String.join("\n", unsupported);
        minecraft.keyboardHandler.setClipboard(copied);
        if (unsupported.isEmpty()) {
            context.getSource().sendSuccess(
                    () -> Component.translatable("commands.mobchatter.unsupported.none"), false);
        } else {
            context.getSource().sendSuccess(
                    () -> Component.translatable("commands.mobchatter.unsupported.copied", unsupported.size()), false);
        }
        return unsupported.size();
    }
}
