package cc.sighs.mobchatter.client;

import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.CommandSourceStack;
import net.minecraftforge.client.event.RegisterClientCommandsEvent;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MobChatterClientCommandsTest {
    @Test
    void registersCopyCommandWithoutPermissionRequirement() {
        CommandDispatcher<CommandSourceStack> dispatcher = new CommandDispatcher<>();
        MobChatterClientCommands.register(new RegisterClientCommandsEvent(dispatcher, null));
        var parsed = dispatcher.parse("mobchatterunsupported", (CommandSourceStack) null);
        assertTrue(parsed.getExceptions().isEmpty());
        assertTrue(!parsed.getReader().canRead());
        assertNotNull(parsed.getContext().getCommand());
    }
}
