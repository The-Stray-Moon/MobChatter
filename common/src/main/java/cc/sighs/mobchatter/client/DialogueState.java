package cc.sighs.mobchatter.client;

/** Current and previous bubble for one entity, plus the last accepted sequence. */
public final class DialogueState {
    public Bubble current;
    public Bubble previous;
    public long sequence = -1;
}
