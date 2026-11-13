package com.merrysnow.mobchatter.client;

/**
 * One rendered speech bubble line pair.
 */
public final class Bubble {
    public final String zh;
    public final String en;
    public final long startTick;

    public Bubble(String zh, String en, long startTick) {
        this.zh = zh;
        this.en = en;
        this.startTick = startTick;
    }
}
