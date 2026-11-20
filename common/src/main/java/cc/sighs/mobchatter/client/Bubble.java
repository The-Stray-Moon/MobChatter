package cc.sighs.mobchatter.client;

/** One locally selected dialogue line pair with its server-provided lifetime. */
public final class Bubble {
    public final String zh;
    public final String en;
    public final long startTick;
    public final int duration;
    public final int fadeTicks;
    public final double range;

    public Bubble(String zh, String en, long startTick, int duration, int fadeTicks, double range) {
        this.zh = zh;
        this.en = en;
        this.startTick = startTick;
        this.duration = duration;
        this.fadeTicks = fadeTicks;
        this.range = range;
    }
}
