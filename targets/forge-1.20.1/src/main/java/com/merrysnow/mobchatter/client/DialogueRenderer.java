package com.merrysnow.mobchatter.client;

import com.merrysnow.mobchatter.MobChatterForge;
import com.merrysnow.mobchatter.config.CommonConfig;
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
        if (!CommonConfig.ENABLED.get()) {
            return;
        }
        LivingEntity entity = event.getEntity();
        if (entity == null) {
            return;
        }
        DialogueState state = DialogueController.stateOf(entity);
        if (state == null || state.current == null) {
            return;
        }

        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null
                || entity.distanceToSqr(minecraft.player) > state.current.range * state.current.range) {
            return;
        }
        long now = minecraft.level.getGameTime();

        float currentAlpha = fade(state.current, now, state.current.duration, state.current.fadeTicks);
        if (currentAlpha <= 0.0F) {
            state.current = null;
            return;
        }
        float previousAlpha = state.previous == null ? 0.0F
                : entity.distanceToSqr(minecraft.player) > state.previous.range * state.previous.range ? 0.0F
                : fade(state.previous, now, state.previous.duration, state.previous.fadeTicks);
        if (previousAlpha <= 0.0F) {
            state.previous = null;
        }

        boolean english = "en".equals(CommonConfig.LANGUAGE.get());
        String top = english ? state.current.en : state.current.zh;
        String bottom = state.previous == null ? null : (english ? state.previous.en : state.previous.zh);
        if (top == null || top.isEmpty()) {
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

        int topColor = 0xFFFFFF | (alpha(currentAlpha) << 24);
        draw(font, pose, buffer, top, 0.0F, topColor, light);

        if (bottom != null && !bottom.isEmpty()) {
            float spacing = CommonConfig.LINE_SPACING.get().floatValue();
            float scale = CommonConfig.BOTTOM_SCALE.get().floatValue();
            float bottomAlpha = previousAlpha * CommonConfig.BOTTOM_ALPHA.get().floatValue();

            pose.pushPose();
            pose.translate(0.0F, spacing, 0.0F);
            pose.scale(scale, scale, scale);
            int bottomColor = 0xFFFFFF | (alpha(bottomAlpha) << 24);
            draw(font, pose, buffer, bottom, 0.0F, bottomColor, light);
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

    private static float fade(Bubble bubble, long now, int duration, int fadeTicks) {
        long age = Math.max(0, now - bubble.startTick);
        if (age >= duration) {
            return 0.0F;
        }
        int fadeStart = Math.max(0, duration - fadeTicks);
        if (age <= fadeStart) {
            return 1.0F;
        }
        return 1.0F - (age - fadeStart) / (float) Math.max(1, fadeTicks);
    }

    private static int alpha(float value) {
        return Math.max(0, Math.min(255, (int) (value * 255.0F)));
    }
}
