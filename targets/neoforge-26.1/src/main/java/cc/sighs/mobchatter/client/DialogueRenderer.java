package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.MobChatterCommon;
import cc.sighs.mobchatter.platform.Platforms;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.util.context.ContextKey;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RenderLivingEvent;

/**
 * Draws up to two stacked lines above a living entity using the 26.1 submit
 * pipeline. The shared layout is computed while the entity render state is
 * extracted, because render events no longer expose the entity itself.
 */
@EventBusSubscriber(modid = MobChatterCommon.MOD_ID, value = Dist.CLIENT)
public final class DialogueRenderer {
    public static final ContextKey<BubbleLayout.View> BUBBLE = new ContextKey<>(
            Identifier.fromNamespaceAndPath(MobChatterCommon.MOD_ID, "bubble"));

    private DialogueRenderer() {
    }

    @SubscribeEvent
    public static void onRenderLiving(RenderLivingEvent.Post<?, ?, ?> event) {
        LivingEntityRenderState state = event.getRenderState();
        BubbleLayout.View view = state.getRenderData(BUBBLE);
        if (view == null) {
            return;
        }
        Minecraft minecraft = Minecraft.getInstance();
        PoseStack pose = event.getPoseStack();
        SubmitNodeCollector collector = event.getSubmitNodeCollector();

        pose.pushPose();
        pose.translate(0.0D, state.boundingBoxHeight + 0.62D, 0.0D);
        pose.mulPose(minecraft.gameRenderer.getMainCamera().rotation());
        pose.scale(-0.025F, -0.025F, -0.025F);

        int topColor = 0xFFFFFF | (BubbleLayout.alpha(view.topAlpha()) << 24);
        draw(collector, minecraft.font, pose, state.lightCoords, view.top(), 0.0F, topColor);

        if (view.bottom() != null && !view.bottom().isEmpty()) {
            float bottomAlpha = view.bottomAlpha() * (float) Platforms.get().config().bottomAlpha();
            pose.pushPose();
            pose.translate(0.0F, view.lineSpacing(), 0.0F);
            pose.scale(view.bottomScale(), view.bottomScale(), view.bottomScale());
            int bottomColor = 0xFFFFFF | (BubbleLayout.alpha(bottomAlpha) << 24);
            draw(collector, minecraft.font, pose, state.lightCoords, view.bottom(), 0.0F, bottomColor);
            pose.popPose();
        }
        pose.popPose();
    }

    private static void draw(SubmitNodeCollector collector, Font font, PoseStack pose, int light,
                             String text, float y, int color) {
        collector.submitText(pose, -font.width(text) / 2.0F, y,
                Component.literal(text).getVisualOrderText(), true,
                Font.DisplayMode.NORMAL, light, color, 0, 0);
    }
}
