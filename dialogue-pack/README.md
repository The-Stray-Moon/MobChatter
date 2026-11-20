# MobChatter 内置台词源

这里按对话资源包格式保存模组自带的全部台词，每个实体一个文件：

```text
assets/<实体命名空间>/mobchatter/dialogue/<实体路径>.json
```

`minecraft:cow` 对应 `assets/minecraft/mobchatter/dialogue/cow.json`，`examplemod:group/mob` 对应 `assets/examplemod/mobchatter/dialogue/group/mob.json`。文件内 `zh` / `en` 必须成对存在且非空；支持的情景和严格字段规则见 [对话资源包指南](../docs/DIALOGUE_RESOURCE_PACKS.md)。

## 贡献台词

1. 只编辑对应实体的 JSON；每个文件使用 `mode: "replace"`，代表该实体的完整台词。
2. 提交 JSON 即可。构建 target 或 common 时，`buildDialoguePack` 会在 `processResources` 前自动重新生成 `common/src/main/resources/assets/mobchatter/dialogue.json.xz`；也可手动运行 `python tools/build_mod_dialogue.py`。XZ 是生成物，不要手工编辑。
3. 需要验收时，可把整个目录压缩成资源包放进 `resourcepacks/`，并按目标版本调整 `pack.mcmeta` 的 `pack_format`。

`python tools/export_dialogue_pack.py` 可从当前 XZ 反向重建本目录；流水线更新后使用 `--source mods` 从 `data/dialogue/mods/` 重建。
