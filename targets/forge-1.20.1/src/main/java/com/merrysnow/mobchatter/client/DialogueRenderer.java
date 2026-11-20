package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.platform.Platforms;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RenderLivingEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import org.joml.Matrix4f;

/**
 * Draws up to two stacked lines above a living entity.
 */
@Mod.EventBusSubscriber(modid = MobChatterForge.MOD_ID, value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class DialogueRenderer {
    private DialogueRenderer() {
    }

    @SubscribeEvent
    @SuppressWarnings("rawtypes")
    public static void onRenderLiving(RenderLivingEvent.Post event) {
        if (!Platforms.get().config().enabled() || !ClientDialogueController.canSee()) {
            return;
        }
        LivingEntity entity = event.getEntity();
        if (entity == null) {
            return;
        }
        DialogueState state = ClientDialogueController.stateOf(entity);
        if (state == null || state.current == null) {
            return;
        }

        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null) {
            return;
        }
        long now = minecraft.level.getGameTime();
        BubbleLayout.View view = BubbleLayout.view(state, now,
                entity.distanceToSqr(minecraft.player), Platforms.get().config());
        if (view == null) {
            return;
        }

        Font font = minecraft.font;
        PoseStack pose = event.getPoseStack();
        MultiBufferSource buffer = event.getMultiBufferSource();
        int light = event.getPackedLight();

        pose.pushPose();
        pose.translate(0.0D, entity.getBbHeight() + 0.62D, 0.0D);
        pose.mulPose(minecraft.gameRenderer.getMainCamera().rotation());
        pose.scale(-0.025F, -0.025F, -0.025F);

        int topColor = 0xFFFFFF | (BubbleLayout.alpha(view.topAlpha()) << 24);
        draw(font, pose, buffer, view.top(), 0.0F, topColor, light);

        if (view.bottom() != null && !view.bottom().isEmpty()) {
            float bottomAlpha = view.bottomAlpha() * (float) Platforms.get().config().bottomAlpha();
            pose.pushPose();
            pose.translate(0.0F, view.lineSpacing(), 0.0F);
            pose.scale(view.bottomScale(), view.bottomScale(), view.bottomScale());
            int bottomColor = 0xFFFFFF | (BubbleLayout.alpha(bottomAlpha) << 24);
            draw(font, pose, buffer, view.bottom(), 0.0F, bottomColor, light);
            pose.popPose();
        }
        pose.popPose();
    }

    private static void draw(Font font, PoseStack pose, MultiBufferSource buffer,
                             String text, float y, int color, int light) {
        Matrix4f matrix = pose.last().pose();
        float x = -font.width(text) / 2.0F;
        // Same as GuiGraphics#drawString(font, text, x, y, color, true):
        // let Font draw the shadow with its own offset.
        font.drawInBatch(text, x, y, color, true, matrix, buffer,
                Font.DisplayMode.NORMAL, 0, light);
    }
}
