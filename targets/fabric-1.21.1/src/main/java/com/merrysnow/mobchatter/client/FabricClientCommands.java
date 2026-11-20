package com.merrysnow.mobchatter.client;

import com.mojang.brigadier.CommandDispatcher;
import net.fabricmc.fabric.api.client.command.v2.FabricClientCommandSource;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;

import java.util.Set;

import static net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal;

public final class FabricClientCommands {
    private FabricClientCommands() {
    }

    public static void register(CommandDispatcher<FabricClientCommandSource> dispatcher) {
        dispatcher.register(literal("mobchatterunsupported").executes(context -> copyUnsupported(context.getSource())));
    }

    private static int copyUnsupported(FabricClientCommandSource source) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null) {
            source.sendError(Component.translatable("commands.mobchatter.no_level"));
            return 0;
        }
        Set<String> unsupported = UnsupportedScanner.collect(minecraft.level);
        minecraft.keyboardHandler.setClipboard(UnsupportedScanner.joined(unsupported));
        if (unsupported.isEmpty()) {
            source.sendFeedback(Component.translatable("commands.mobchatter.unsupported.none"));
        } else {
            source.sendFeedback(Component.translatable(
                    "commands.mobchatter.unsupported.copied", unsupported.size()));
        }
        return unsupported.size();
    }
}
