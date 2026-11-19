package com.merrysnow.mobchatter.network;

import com.merrysnow.mobchatter.dialogue.DialoguePatch;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;

import java.util.UUID;

public record DialogueSignal(ResourceLocation dimension, int entityId, UUID entityUuid,
                             ResourceLocation entityType, String scenario, long seed, long sequence,
                             long startTick, int duration, int fadeTicks, double range) {
    public DialogueSignal {
        if (!DialoguePatch.SCENARIOS.contains(scenario) || entityId < 0 || sequence < 0
                || duration < 20 || duration > 1200 || fadeTicks < 1 || fadeTicks > 200
                || !Double.isFinite(range) || range < 4 || range > 128) {
            throw new IllegalArgumentException("Invalid dialogue signal");
        }
    }

    public void encode(FriendlyByteBuf buffer) {
        buffer.writeResourceLocation(dimension);
        buffer.writeVarInt(entityId);
        buffer.writeUUID(entityUuid);
        buffer.writeResourceLocation(entityType);
        buffer.writeUtf(scenario, 32);
        buffer.writeLong(seed);
        buffer.writeLong(sequence);
        buffer.writeLong(startTick);
        buffer.writeVarInt(duration);
        buffer.writeVarInt(fadeTicks);
        buffer.writeDouble(range);
    }

    public static DialogueSignal decode(FriendlyByteBuf buffer) {
        return new DialogueSignal(buffer.readResourceLocation(), buffer.readVarInt(), buffer.readUUID(),
                buffer.readResourceLocation(), buffer.readUtf(32), buffer.readLong(), buffer.readLong(),
                buffer.readLong(), buffer.readVarInt(), buffer.readVarInt(), buffer.readDouble());
    }

    public boolean expired(long now) {
        return now - startTick >= duration;
    }

    public boolean inRange(double distanceSquared) {
        return distanceSquared >= 0 && distanceSquared <= range * range;
    }
}
