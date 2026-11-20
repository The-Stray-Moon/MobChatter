package cc.sighs.mobchatter;

import cc.sighs.mobchatter.client.ClientDialogueController;
import cc.sighs.mobchatter.client.FabricClientCommands;
import cc.sighs.mobchatter.client.FabricDialogueRenderer;
import cc.sighs.mobchatter.client.FabricDialogueReloadListener;
import cc.sighs.mobchatter.network.FabricDialogueNetwork;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientEntityEvents;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.resource.ResourceManagerHelper;
import net.minecraft.server.packs.PackType;

public final class MobChatterFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> ClientDialogueController.tick());
        ClientEntityEvents.ENTITY_UNLOAD.register((entity, world) ->
                ClientDialogueController.onEntityLeave(entity));
        ClientCommandRegistrationCallback.EVENT.register((dispatcher, access) ->
                FabricClientCommands.register(dispatcher));
        ResourceManagerHelper.get(PackType.CLIENT_RESOURCES)
                .registerReloadListener(new FabricDialogueReloadListener());
        FabricDialogueRenderer.register();
        FabricDialogueNetwork.registerClientReceiver();
    }
}
