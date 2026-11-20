package com.merrysnow.mobchatter.dialogue;

/**
 * One resource-pack patch file, already resolved to its entity and read as
 * text by the target's resource manager.
 *
 * @param entityId entity id encoded by the resource path
 * @param source   pack id used for diagnostics
 * @param json     raw JSON contents
 */
public record DialogueResource(String entityId, String source, String json) {
}
