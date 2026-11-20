package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.MobChatterCommon;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.context.CommandContext;
import net.minecraft.client.Minecraft;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.network.chat.Component;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterClientCommandsEvent;

import java.util.Set;

import static net.minecraft.commands.Commands.literal;

@EventBusSubscriber(modid = MobChatterCommon.MOD_ID, value = Dist.CLIENT)
public final class NeoForgeClientCommands {
    private NeoForgeClientCommands() {
    }

    @SubscribeEvent
    public static void register(RegisterClientCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
        dispatcher.register(literal("mobchatterunsupported")
                .executes(NeoForgeClientCommands::copyUnsupported));
    }

    private static int copyUnsupported(CommandContext<CommandSourceStack> context) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null) {
            context.getSource().sendFailure(Component.translatable("commands.mobchatter.no_level"));
            return 0;
        }
        Set<String> unsupported = UnsupportedScanner.collect(minecraft.level);
        minecraft.keyboardHandler.setClipboard(UnsupportedScanner.joined(unsupported));
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
