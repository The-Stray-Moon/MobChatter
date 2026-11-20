package cc.sighs.mobchatter.client;

import com.mojang.blaze3d.vertex.PoseStack;
import cc.sighs.mobchatter.platform.Platforms;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;
import org.joml.Matrix4f;

public final class FabricDialogueRenderer implements WorldRenderEvents.AfterEntities {
    @Override
    public void afterEntities(WorldRenderContext context) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null || !Platforms.get().config().enabled()
                || !ClientDialogueController.canSee()) {
            return;
        }
        MultiBufferSource buffer = context.consumers();
        if (buffer == null) {
            return;
        }
        Camera camera = context.camera();
        Vec3 cameraPos = camera.getPosition();
        float delta = context.tickCounter().getGameTimeDeltaPartialTick(false);
        long now = minecraft.level.getGameTime();
        for (Entity entity : minecraft.level.entitiesForRendering()) {
            if (!(entity instanceof LivingEntity living) || entity instanceof Player) {
                continue;
            }
            DialogueState state = ClientDialogueController.stateOf(living);
            if (state == null || state.current == null) {
                continue;
            }
            BubbleLayout.View view = BubbleLayout.view(state, now,
                    living.distanceToSqr(minecraft.player), Platforms.get().config());
            if (view == null) {
                continue;
            }
            double x = Mth.lerp(delta, living.xo, living.getX());
            double y = Mth.lerp(delta, living.yo, living.getY()) + living.getBbHeight() + 0.62D;
            double z = Mth.lerp(delta, living.zo, living.getZ());
            PoseStack pose = new PoseStack();
            pose.translate(x - cameraPos.x, y - cameraPos.y, z - cameraPos.z);
            pose.mulPose(camera.rotation());
            pose.scale(-0.025F, -0.025F, -0.025F);

            int topColor = 0xFFFFFF | (BubbleLayout.alpha(view.topAlpha()) << 24);
            draw(minecraft.font, pose, buffer, view.top(), topColor);

            if (view.bottom() != null && !view.bottom().isEmpty()) {
                float bottomAlpha = view.bottomAlpha() * (float) Platforms.get().config().bottomAlpha();
                pose.pushPose();
                pose.translate(0.0F, view.lineSpacing(), 0.0F);
                pose.scale(view.bottomScale(), view.bottomScale(), view.bottomScale());
                int bottomColor = 0xFFFFFF | (BubbleLayout.alpha(bottomAlpha) << 24);
                draw(minecraft.font, pose, buffer, view.bottom(), bottomColor);
                pose.popPose();
            }
        }
    }

    private static void draw(Font font, PoseStack pose, MultiBufferSource buffer, String text, int color) {
        Matrix4f matrix = pose.last().pose();
        float x = -font.width(text) / 2.0F;
        font.drawInBatch(text, x, 0.0F, color, true, matrix, buffer,
                Font.DisplayMode.NORMAL, 0, LightTexture.FULL_BRIGHT);
    }
}
