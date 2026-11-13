package com.merrysnow.mobchatter.client;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Per-entity client state for bubble stacking and trigger cooldowns.
 */
public final class DialogueState {
    public Bubble current;
    public Bubble previous;

    public final Map<String, Long> lastByScenario = new HashMap<>();

    public boolean initialized;
    public float lastHealth;
    public UUID lastTarget;
    public boolean lastSwinging;
    public double lastX;
    public double lastY;
    public double lastZ;
    public int stillTicks;
    public int lastMainCount;
    public int lastOffCount;
}
