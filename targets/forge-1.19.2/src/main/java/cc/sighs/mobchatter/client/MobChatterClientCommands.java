package cc.sighs.mobchatter.client;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.context.CommandContext;
import net.minecraft.client.Minecraft;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.network.chat.Component;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RegisterClientCommandsEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

import java.util.Set;

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
        Set<String> unsupported = UnsupportedScanner.collect(minecraft.level);
        minecraft.keyboardHandler.setClipboard(UnsupportedScanner.joined(unsupported));
        if (unsupported.isEmpty()) {
            context.getSource().sendSuccess(
                    Component.translatable("commands.mobchatter.unsupported.none"), false);
        } else {
            context.getSource().sendSuccess(
                    Component.translatable("commands.mobchatter.unsupported.copied", unsupported.size()), false);
        }
        return unsupported.size();
    }
}
