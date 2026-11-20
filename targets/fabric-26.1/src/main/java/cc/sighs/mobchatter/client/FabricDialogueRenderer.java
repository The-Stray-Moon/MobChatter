package cc.sighs.mobchatter.client;

import cc.sighs.mobchatter.platform.Platforms;
import com.mojang.blaze3d.vertex.PoseStack;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelRenderEvents;
import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.network.chat.Component;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;

/**
 * Submits dialogue text during the 26.1 level submit-collection stage. The
 * shared layout still decides text, opacity and scale.
 */
public final class FabricDialogueRenderer {
    private static final int FULL_BRIGHT = 15728880;

    private FabricDialogueRenderer() {
    }

    public static void register() {
        LevelRenderEvents.COLLECT_SUBMITS.register(FabricDialogueRenderer::collectSubmits);
    }

    private static void collectSubmits(LevelRenderContext context) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null || !Platforms.get().config().enabled()
                || !ClientDialogueController.canSee()) {
            return;
        }
        SubmitNodeCollector collector = context.submitNodeCollector();
        Camera camera = minecraft.gameRenderer.getMainCamera();
        Vec3 cameraPos = camera.position();
        float delta = minecraft.getDeltaTracker().getGameTimeDeltaPartialTick(false);
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
            draw(collector, minecraft.font, pose, view.top(), 0.0F, topColor);

            if (view.bottom() != null && !view.bottom().isEmpty()) {
                float bottomAlpha = view.bottomAlpha() * (float) Platforms.get().config().bottomAlpha();
                PoseStack bottomPose = new PoseStack();
                bottomPose.translate(x - cameraPos.x, y - cameraPos.y, z - cameraPos.z);
                bottomPose.mulPose(camera.rotation());
                bottomPose.scale(-0.025F, -0.025F, -0.025F);
                bottomPose.translate(0.0F, view.lineSpacing(), 0.0F);
                bottomPose.scale(view.bottomScale(), view.bottomScale(), view.bottomScale());
                int bottomColor = 0xFFFFFF | (BubbleLayout.alpha(bottomAlpha) << 24);
                draw(collector, minecraft.font, bottomPose, view.bottom(), 0.0F, bottomColor);
            }
        }
    }

    private static void draw(SubmitNodeCollector collector, Font font, PoseStack pose,
                             String text, float y, int color) {
        collector.submitText(pose, -font.width(text) / 2.0F, y,
                Component.literal(text).getVisualOrderText(), true,
                Font.DisplayMode.NORMAL, FULL_BRIGHT, color, 0, 0);
    }
}
