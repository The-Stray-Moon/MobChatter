package com.merrysnow.mobchatter.client;

import com.google.common.reflect.TypeToken;
import com.merrysnow.mobchatter.MobChatterCommon;
import com.merrysnow.mobchatter.platform.Platforms;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.AddClientReloadListenersEvent;
import net.neoforged.neoforge.client.renderstate.RegisterRenderStateModifiersEvent;

@EventBusSubscriber(modid = MobChatterCommon.MOD_ID, value = Dist.CLIENT)
public final class NeoForgeClientSetup {
    private NeoForgeClientSetup() {
    }

    @SubscribeEvent
    public static void addReloadListeners(AddClientReloadListenersEvent event) {
        event.addListener(Identifier.fromNamespaceAndPath(MobChatterCommon.MOD_ID, "dialogue"),
                new DialogueManager());
    }

    @SubscribeEvent
    public static void registerRenderStateModifiers(RegisterRenderStateModifiersEvent event) {
        event.registerEntityModifier(
                new TypeToken<LivingEntityRenderer<LivingEntity, LivingEntityRenderState, ?>>() { },
                NeoForgeClientSetup::extractBubble);
    }

    private static void extractBubble(LivingEntity entity, LivingEntityRenderState state) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null || !ClientDialogueController.canSee()) {
            return;
        }
        DialogueState dialogue = ClientDialogueController.stateOf(entity);
        if (dialogue == null || dialogue.current == null) {
            return;
        }
        BubbleLayout.View view = BubbleLayout.view(dialogue, minecraft.level.getGameTime(),
                entity.distanceToSqr(minecraft.player), Platforms.get().config());
        if (view != null) {
            state.setRenderData(DialogueRenderer.BUBBLE, view);
        }
    }
}
