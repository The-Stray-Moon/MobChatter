package cc.sighs.mobchatter.network;

import cc.sighs.mobchatter.dialogue.DialogueIds;
import cc.sighs.mobchatter.dialogue.DialoguePatch;
import net.minecraft.network.FriendlyByteBuf;

import java.util.UUID;

/**
 * Server-authoritative dialogue broadcast.
 *
 * <p>Ids travel as strings rather than {@code ResourceLocation}, because 26.1
 * renamed that type to {@code Identifier}. All random and lifetime decisions
 * happen on the server; clients receive the same seed, sequence and original
 * start tick and only select the line locally.</p>
 */
public record DialogueSignal(String dimension, int entityId, UUID entityUuid,
                             String entityType, String scenario, long seed, long sequence,
                             long startTick, int duration, int fadeTicks, double range) {
    public DialogueSignal {
        if (!DialogueIds.isValid(dimension) || !DialogueIds.isValid(entityType)
                || !DialoguePatch.SCENARIOS.contains(scenario) || entityId < 0 || sequence < 0
                || duration < 20 || duration > 1200 || fadeTicks < 1 || fadeTicks > 200
                || !Double.isFinite(range) || range < 4 || range > 128) {
            throw new IllegalArgumentException("Invalid dialogue signal");
        }
    }

    public void encode(FriendlyByteBuf buffer) {
        buffer.writeUtf(dimension, 256);
        buffer.writeVarInt(entityId);
        buffer.writeUUID(entityUuid);
        buffer.writeUtf(entityType, 256);
        buffer.writeUtf(scenario, 32);
        buffer.writeLong(seed);
        buffer.writeLong(sequence);
        buffer.writeLong(startTick);
        buffer.writeVarInt(duration);
        buffer.writeVarInt(fadeTicks);
        buffer.writeDouble(range);
    }

    public static DialogueSignal decode(FriendlyByteBuf buffer) {
        return new DialogueSignal(buffer.readUtf(256), buffer.readVarInt(), buffer.readUUID(),
                buffer.readUtf(256), buffer.readUtf(32), buffer.readLong(), buffer.readLong(),
                buffer.readLong(), buffer.readVarInt(), buffer.readVarInt(), buffer.readDouble());
    }

    public boolean expired(long now) {
        return now - startTick >= duration;
    }

    public boolean inRange(double distanceSquared) {
        return distanceSquared >= 0 && distanceSquared <= range * range;
    }
}
