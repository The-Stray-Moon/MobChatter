# 对话资源包

当前全部客户端 target（Forge 1.18.2/1.19.2/1.20.1、NeoForge 1.21.1/26.1、Fabric 1.20.1/1.21.1/26.1）均已接入对话资源加载。资源包无需压缩或复制整个台词库，可以用普通 UTF-8 JSON 新增实体台词、追加、覆盖或禁用场景。

## 内置台词源

模组自带的 6,507 个实体台词按本页格式摊开在仓库 [`dialogue-pack/`](../dialogue-pack/)：

- 路径与运行时资源包一致：`dialogue-pack/assets/<实体命名空间>/mobchatter/dialogue/<实体路径>.json`，每个实体一个文件。
- 每个文件使用 `mode: "replace"` 与 `operation: "replace"`，即该实体的完整台词；增删或改写句子直接编辑对应文件。
- 构建时 `processResources` 依赖 `buildDialoguePack`，会先自动重新生成 `common/src/main/resources/assets/mobchatter/dialogue.json.xz`；也可手动运行 `python tools/build_mod_dialogue.py`。贡献者只需提交 JSON，无需处理 XZ。
- `python tools/export_dialogue_pack.py` 可从当前 XZ 反向重建整棵目录；数据流水线更新后也可用 `python tools/export_dialogue_pack.py --source mods` 从 `data/dialogue/mods/` 重建。XZ 是生成物，不要手工编辑。
- `dialogue-pack/pack.mcmeta` 只用于把该目录压缩成临时资源包进游戏验收；`pack_format` 按目标版本调整，打包脚本不读取它。
- 当前目录与内置 XZ 内容一致：6,507 个实体、998,401 句。字段错误的文件会被 `build_mod_dialogue.py` 拒绝并指出位置。

## 目录

```text
我的资源包/
├── pack.mcmeta
└── assets/
    ├── minecraft/mobchatter/dialogue/cow.json
    └── examplemod/mobchatter/dialogue/some_mob.json
```

Forge 1.20.1 的 `pack.mcmeta`：

```json
{"pack":{"pack_format":15,"description":"我的生物对话"}}
```

路径 `assets/<实体命名空间>/mobchatter/dialogue/<实体路径>.json` 唯一对应一个实体 ID。实体 ID 为 `examplemod:group/mob` 时文件为 `assets/examplemod/mobchatter/dialogue/group/mob.json`。未安装对应模组不会报错；资源包只提供台词，不注册实体或新触发器。

将目录或 zip 放到游戏的 `resourcepacks/`，在资源包菜单启用。切换资源包或 `F3+T` 后重新加载全部台词并清理客户端已有气泡，不改变服务端的触发冷却。服务端不解析客户端台词库，只发送实体、情景、统一随机种子及服务端显示参数。各客户端对相同有序台词列表使用 `floorMod(seed, 台词数量)` 选句；一致的模组版本、资源包内容及加载顺序保证同一条台词。不同资源包可能选到不同文字，客户端语言不同则显示同一对照台词的不同语言。重载后等待下一次服务端信号显示，不由客户端重触发。

## 文件格式

```json
{
  "format_version": 1,
  "mode": "merge",
  "scenarios": {
    "walk": {
      "operation": "append",
      "lines": [
        {"zh": "这边的草好像更香。", "en": "The grass smells better over here."}
      ]
    },
    "look_player": {
      "operation": "replace",
      "lines": [
        {"zh": "你带小麦了吗？", "en": "Did you bring any wheat?"}
      ]
    },
    "hurt.fire": {"operation": "disable"}
  }
}
```

- `format_version` 必须为数字 `1`。
- `mode` 可省略，默认 `merge`：保留未声明的场景。`replace` 先清除该实体此前所有场景，再处理本文件。
- `scenarios` 必须是对象，允许空对象。`mode: replace` 加空对象可以禁用该实体的全部台词。
- `operation` 必须显式指定：`append` 追加、`replace` 替换当前场景、`disable` 禁用当前场景。
- `append` 和 `replace` 必须有非空 `lines`；每句必须有非空字符串 `zh`、`en`。追加和替换均按完整中英文对去重，保持顺序。
- `disable` 不允许包含 `lines`，同时阻止受伤场景回退。更高层仍可通过追加或替换重新启用。
- 未知字段、场景、操作和不支持的版本均视为错误，防止拼写错误悄悄生效。

支持的场景：

`walk`、`idle`、`look_player`、`hurt`、`tempted`、`collide`、`mate`、`pickup`、`target_acquire`、`targeting`、`melee_attack`、`spawn`。

受伤细分：`hurt.fire`、`hurt.fall`、`hurt.drown`、`hurt.explosion`、`hurt.projectile`、`hurt.magic`、`hurt.starvation`、`hurt.lightning`、`hurt.void`。

缺少细分场景时回退到 `hurt`；细分场景被显式禁用时不回退。

## 优先级与错误

加载顺序为：最高优先级的基础 XZ → 低优先级 JSON 资源包 → 高优先级 JSON 资源包。同一路径的每一层 JSON 都会参与合并，这与普通资源的整文件替换不同。游戏资源包菜单中位于上方的包优先级更高。

例如基础 `walk` 有 10 句，低层追加 2 句后有 12 句，高层替换为 3 句后最终只有 3 句。不同实体文件互不影响。每次重载都从基础库重新构建，关闭资源包不会残留追加内容。

高级用法仍可在 `assets/mobchatter/dialogue.json.xz` 提供完整基础库替换；其结构必须与生成脚本一致，不是本页的 JSON 补丁格式。全部 JSON 层都应用在选中的基础库之上。

单个 JSON 文件校验失败时整个文件跳过，保留此前各层结果，日志包含资源包名、文件路径及字段位置；JSON 语法错误使用解析器提供的位置。基础 XZ 缺失、损坏或内容格式错误会使重载失败，不能静默退为空库。失败准备阶段不会发布新快照。

日志搜索 `Dialogue prepared` 查看实体数、台词数、补丁成功/失败数和准备耗时；搜索 `Skipping dialogue patch` 定位错误文件。

## 验证状态

2026-11-21：`buildDialoguePack` 接入 `common` 与各 target 的 `processResources`、`sourcesJar`。`common` 与 neoforge-1.21.1 实际执行通过；neoforge-1.21.1 的 `jar` 包含由 `dialogue-pack/` 重新生成的 XZ，内容与旧库一致（6,507 个实体、998,401 句）。其余 target 未逐一重跑。

2026-11-20：共享补丁解析/合并迁移到 `common` 后，全部 8 个 target 的 `build` 通过；common 自动化测试覆盖合并规则、资源包优先级、新实体嵌套路径、错误文件跳过、禁用与回退、移除资源包恢复，以及基础库损坏不替换旧快照。2026-11-19 的 Forge 1.20.1 真实 `MultiPackResourceManager` 测试保留为历史记录。

共享解析器同时通过 Fabric 1.20.1 / 1.21.1、Forge 1.18.2 / 1.19.2、NeoForge 1.21.1 的干净构建及共享测试；两个 26.1 目标因未配置 JDK 25 未验证。这些目标仍没有对话客户端适配层。

早期验证仅记录 `Dialogue prepared: 6507 entities, 998401 lines, 0 patches, 0 failed, 2691 ms`，当时 AutoJS 不可用。2026-11-19 已修复 Forge 1.20.1 调试模组发现与映射链；两个真实客户端及专用服务器均通过 AutoJS `status` / `eval_js`（KubeJS 模式），客户端确认 6,507 个实体，服务端火焰/摔落伤害广播的台词、序号、开始时间和范围在两个客户端完全一致，范围外玩家不收新信号，回到范围内补收原信号且不重置寿命。具体脚本调用及实际返回见 README 的 AutoJS / 多人验证记录。真实资源包切换、`F3+T` 和气泡阴影视觉仍未专项验收，不能以这些测试替代。
