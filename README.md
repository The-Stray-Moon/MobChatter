# MobChatter

Creature chatter bubbles rendered above mobs.

- mod id：mobchatter
- Java 包名 / Gradle group：cc.sighs.mobchatter
- 作者：MerrySnow
- 声明的许可证：GPL-3.0-only

## 功能

生物头顶对话气泡（客户端渲染）：

- 每个生物在不同时机冒出一句台词，最多两行。
- 第一行正常白色；新台词进入时，上一句被挤到第二行，缩小到 0.8 倍并降到 55% 不透明度。
- **客户端和服务端都必须安装**。Forge 1.20.1 的 SimpleChannel 严格拒绝缺失模组或协议不匹配的连接；其他 target 依赖各自 loader 的 payload 通道检查，原版客户端不会收到气泡包。服务端判定触发并统一生成随机种子，客户端只从本地资源包选句、渲染，不再自行触发。单人游戏由集成服务器负责触发。
- 服务端显示范围默认 32 格；同维度、正在追踪实体且处于范围内的全部玩家收到相同信号。进入范围或新开始追踪的玩家会补收尚未过期的当前信号，不重置寿命。客户端移出范围会隐藏气泡。
- Forge/NeoForge 只注册一份 `ModConfig.Type.COMMON`；Fabric 读取相同键的 `config/mobchatter-common.toml`（启动时加载，修改后需重启）。双端各自使用本机文件。服务端读取范围、显示时长、淡出、触发开关、冷却及概率，客户端读取本机语言、排版及显示开关。COMMON 文件不会自动同步，但服务端权威参数随台词信号下发，客户端同名范围/时长参数不参与判定。单人集成服务器与客户端共用同一份配置。拆分版本的 `mobchatter-client.toml` / `mobchatter-server.toml` 不再读取，如曾使用需手动合并到 common 文件。
- 新增头部饰品 **电波接收器**（`mobchatter:radio_receiver`）。配置 `display.requireReceiver`（默认 `false`）打开后，只有佩戴者才能看见生物台词；摘下后已在显示的气泡立即隐藏，重新戴上会恢复剩余寿命内的气泡。
  - Forge/NeoForge 安装 Curios 时可放入 `head` 槽；Curios 是可选依赖，不安装也能用。无 Curios 时右键把接收器放入原版头盔槽（1.18.2–1.21.1）；26.1 使用原版 `Equippable` 组件，右键直接换装。
  - Fabric 没有 Curios，使用原版头盔槽；26.1 同样走 `Equippable`。
  - Forge 1.20.1、NeoForge 1.21.1/26.1、Fabric 1.20.1/1.21.1 会出现在“工具与实用物品”创造模式页；Fabric 26.1 与 Forge 1.18.2/1.19.2 可用 `/give mobchatter:radio_receiver` 获取。
  - Tooltip 会显示装备位置，并根据 `display.requireReceiver` 实时说明当前状态：启用时提示“只有佩戴者能看见生物台词”，未启用时提示“所有玩家都能看见”及如何开启。翻译键为 `item.mobchatter.radio_receiver.tooltip.slot` / `.enabled` / `.disabled`。
- 触发情景：行走、呆立、看向玩家、受伤（含 9 种伤害类型）、被食物吸引、与玩家碰撞、交配、拾取物品、锁定目标瞬间、索敌中、近战挥击、生成。Fabric 1.20.1 的伤害触发发生在结算前（`ALLOW_DAMAGE`），其余 target 使用结算后事件；被完全吸收或取消的伤害判定因此略有差异。
- 台词资源来自 `common/src/main/resources/assets/mobchatter/dialogue.json.xz`，覆盖 6,507 个实体、约 100 万句中英对照；默认显示中文，可在配置中改为英文。使用 XZ preset 6 无损压缩，通过 `python tools/build_mod_dialogue.py` 生成；原有 gzip 资源不再打包。所有 target 都内嵌 `org.tukaani:xz:1.10` 解码库（Forge/NeoForge Jar-in-Jar，Fabric `include`），玩家无需另装依赖。自定义资源包需提供同路径的 XZ 文件，旧 `.gz` 文件不再读取。

客户端指令：

```text
/mobchatterunsupported
```

在当前已加载世界中收集已加载的生物实体，排除玩家和已有台词数据的实体，按实体 ID 排序后复制到系统剪贴板；聊天栏会显示复制数量。没有进入世界时指令会提示错误；没有未支持生物时会复制空文本并提示无结果。资源包显式禁用的实体仍视为已有记录，不会误报为缺失。此指令不枚举整合包内所有注册类型，也不加载区块。

2026-11-20：共享层及全部 8 个 target 的 `build`/测试通过，且每个 target 的 `runServer` 与 `runClient` 均实际启动到 `Done (` / `Sound engine started`；AutoJS 端点可用时均通过 `status` 与物品注册检查（Forge 1.18.2/1.19.2/1.20.1 使用 JDK 21，NeoForge 1.21.1/Fabric 1.20.1/1.21.1 使用 JDK 21，26.1 目标使用 JDK 25）。common 测试覆盖对话补丁合并、资源包分层与坏文件跳过、XZ 语料校验、信号编解码、配置解析和气泡布局；Forge 1.20.1 另有指令树、COMMON 配置和网络协议测试。全部 target 已完成启动级验证；完整的多人台词同步、资源包切换、剪贴板写入、聊天反馈和视觉验收仍只在 Forge 1.20.1 有历史记录，未逐一重跑。

主要配置项：

| 配置端 | 键 | 默认 | 说明 |
| --- | --- | --- | --- |
| 服务端 | `display.enabled` | true | 触发总开关 |
| 服务端 | `display.displayDurationTicks` | 80 | 显示寿命（tick，原始服务端时间） |
| 服务端 | `display.fadeOutTicks` | 20 | 淡出时长（tick） |
| 服务端 | `display.maxDistance` | 32 | 广播及显示半径（格），还受实体追踪距离限制 |
| 服务端 | `trigger.scenarioCooldownTicks` | 160 | 每实体同情景冷却，不按玩家分别计算 |
| 服务端 | `trigger.ambientChance` | 0.35 | 环境类触发概率乘数 |
| 客户端 | `display.enabled` | true | 本地显示开关 |
| 客户端 | `display.lineSpacing` | 10 | 两行间距 |
| 客户端 | `display.bottomLineScale` | 0.8 | 第二行缩放 |
| 客户端 | `display.bottomLineAlpha` | 0.55 | 第二行不透明度 |
| 客户端 | `display.language` | zh | `zh` / `en` |
| 客户端 | `display.requireReceiver` | false | 仅佩戴电波接收器时显示台词；Fabric 文件配置同名键 |

服务端每实体每 tick 最多发送一条新台词，按受伤、生成、锁定/索敌、挥击、拾取等优先级仲裁，不随观察玩家数量重复随机。受伤使用服务端 `LivingDamageEvent` 的最终正伤害和伤害类型/标签；全被吸收或取消的伤害不触发。行走、呆立、挥击、手持物品数量增加和动物状态由服务端采样；`look_player` 根据服务端玩家朝向射线及方块遮挡判定。生成只针对新加入世界的实体，不把磁盘加载或玩家首次看到旧实体当成生成。

同一信号包含相同的情景、随机种子、序号和开始 tick，客户端按 `floorMod(seed, 台词数量)` 选句；要求各客户端台词库内容和顺序一致。语言不同会显示同一对照句的不同语言，自定义资源包不同则不保证文字一致。

共享触发、信号、选句、资源合并、指令和布局位于 `common/`，通过 `MobChatterPlatform` SPI 组合；各 `targets/<loader>-<version>` 只保留确证差异：配置系统、网络通道、事件注册、资源重载入口、伤害分类、实体/维度 ID 访问和渲染管线。Forge 1.18.2/1.19.2、Forge 1.20.1、NeoForge 1.21.1/26.1、Fabric 1.20.1/1.21.1/26.1 均已接入。

支持资源包在 `assets/<实体命名空间>/mobchatter/dialogue/<实体路径>.json` 新增、追加、覆盖和禁用台词。同路径按资源包从低到高分层合并，支持整实体或单场景覆盖；切换资源包或 `F3+T` 重载后发布新快照并清理客户端气泡，不改变服务端冷却。普通 JSON 无需 XZ 工具，格式与示例见 [对话资源包指南](docs/DIALOGUE_RESOURCE_PACKS.md)。

头顶文字使用原版 GUI 的 `Font.drawInBatch(..., shadow=true, NORMAL)` 阴影。局部 Z 缩放为负值，让正文 `+0.03` 偏移朝向相机；不手绘阴影、不关闭全局深度测试。白字、右下阴影、双行和淡出的视觉验收仍未完成，数据回读不代表视觉正确。

XZ 体积优化：资源从约 26 MiB 降至 16.4 MiB，解压后与原 gzip 逐字节一致。Java 测试固定校验当前语料的长度与 SHA-256，更新语料时需同步基准；真实客户端通过 AutoJS 回读确认已加载 6,507 个实体。

AutoJS / 多人验证（2026-11-19，Forge 1.20.1）：已修复开发模组发现和映射链，完整 KubeJS `2001.6.5-build.26`＋Rhino `2001.2.2-build.17`＋AutoJS `1.0.1` 可启动。必须让运行类路径继承带 named 映射约束的 `hotDebugRuntime`，同时从额外类路径移除同一配置，不能直接继承未带约束的 `modHotDebugRuntime` 或同时加载原始/转换 jar。修复只针对此 target，其他 target 未按此方式验证。

按用户授权，开发实例 `run/eula.txt` 已接受 EULA（忽略文件，不提交）。测试使用隔离的本机服务器 `127.0.0.1:25591` 和两名真实客户端 Dev / AutoJsObserver；AutoJS 端口为客户端 `25588` / `25590`、服务端 `25589`，均绑定 loopback。三个实例均通过 `status` 确认可用 side 和 KubeJS 模式，成功断言均为 `ok:true`、无 `isError`、无错误 diagnostics：

- 客户端 `DialogueManager.size()` 返回 `6507`。
- 服务端 `/damage @e[tag=mobchatter_autojs_test,limit=1] 1 minecraft:in_fire` 后，两个客户端 `DialogueController.stateOf(cow)` 均读到“毛烧起来了，我闻得到。” / `My hide's burning. I can smell it.`，序号 `2`、开始 tick `9473`、时长 `1200`、范围 `32` 全部一致。
- 观察者移到 `x=40.5`（范围外），服务端触发摔落伤害后仅近处玩家获得新信号；观察者返回范围内后，两边均读到“从坡上滚下来，摔得不轻。”、序号 `4`、原始开始 tick `13723`，没有重新随机或重置寿命。测试时长 `1200` 仅写入临时服务器配置，正式默认值仍为 `80`。
- 测试结束通过 AutoJS 恢复后台调试模式并正常退出两个客户端、停止服务器；临时世界和运行参数清理，不碰现有存档。

实际缺少模组时的连接拒绝、资源包切换 / `F3+T` 和阴影视觉仍待专项实测；已有协议与资源合并自动化测试不代替这些验收。

### 构建注意

`maven.neoforged.net` 在当前网络不可达。Forge 1.20.1 将 `net.jodah:typetools`、`log4j`、`cpw.mods:modlauncher` 的超范围版本固定为可从 Maven Central / Forge Maven 解析的具体版本，并缩短了 Gradle HTTP 超时；Forge 1.18.2/1.19.2 同样固定 `typetools`、`eventbus`、`coremods`、`modlauncher`，避免 NeoForm 解析动态版本时访问不可达仓库。Curios 仅用于 `compileOnly`，不会打入发布 jar；1.18.2/1.19.2/1.20.1 从 Modrinth Maven 解析，NeoForge 1.21.1/26.1 的上游 Maven 当前不可达，API jar 放在对应 `libs/` 供编译使用。玩家端 Curios 仍是可选安装。

运行级修复记录：1.18.2/1.19.2 使用 `pack.mcmeta`；1.19.2 固定 forgespi `6.0.0`、typetools `0.8.3`（`gradle/local-repo`），Rhino 改用 Modrinth 坐标并关闭会在专用服崩溃的 KubeJS `1902.6.2-build.74`；NeoForge 1.21.1/26.1 固定 KubeJS 浮动传递依赖并把热调试运行时接入 run classpath；26.1 物品注册使用带 `setId(...)` 的注册重载。

## 开发与构建

开发规范见 [AGENTS.md](AGENTS.md)。共享业务与资源位于 `common/`；loader / Minecraft 差异位于 `targets/<loader>-<version>/`。所有 target 直接编译 common 原源码，不引用共享 jar，也不等待复制到 build 目录。

- 单版本：IDEA 打开对应 target 目录，使用该目录的 wrapper 和矩阵声明的 JDK。
- 全版本：IDEA 打开 `idea-workspace/`；当前主版本为 **neoforge-1.21.1**，配置的 Gradle JVM 为 **JDK 21**。该值来自 target 描述文件，仍须核对工作区 wrapper 与所用 JDK 的兼容性。
- 工作区只完整导入主 target。其他版本、文档、脚本及根配置作为仓库浏览内容展示，不承诺非主版本的 API 补全。common 源码只归属主 target，不额外关联根工程、common 或其他完整 target。
- 切换主版本修改 `idea-workspace/gradle.properties` 的 `workspace_main_target` 后重新加载 Gradle。composite build 共用工作区的 Gradle/JVM，不使用被包含 target 的 wrapper；若不兼容，独立打开 target 或调整工作区工具链。
- 普通 common 内容修改无需运行源码同步任务；变更 Gradle 配置或 `commonJava` 排除规则后需重新加载 Gradle。

在所选 target 目录执行：

```powershell
.\gradlew.bat clean build
.\gradlew.bat verifyHotDebug
.\gradlew.bat runClient
# 或 runServer；Minecraft EULA 必须由用户阅读并接受
```

在仓库根可执行 `./gradlew -p common build` 单独检查共享层，但不能替代目标矩阵验证。根 `-Ptarget=<目录名> build` 调用该 target 的独立 wrapper；`-PallTargets=true build` 自动选择已启用且 `ci.java` 不高于当前 Gradle JVM 的目标，并打印跳过项。最低 JDK 筛选不保证旧 wrapper 支持任意新版 JDK，必要时分别构建。根 `build` 默认只验证 common。

## AutoJS 热调试与热执行

运行时调试必须使用 AutoJS，不得仅凭源码推断、临时日志或构建成功宣称游戏行为正确。

每个 target 的 `debug_*` 属性声明来自 Sighs Maven 的 AutoJS、Rhino 及可用的 KubeJS。具体版本和模式以该 target 配置为准；没有 `debug_kubejs` 时仅用 Rhino，不假设存在 KubeJS 事件或 `kubejs_log`。调试依赖仅用于开发游戏运行，不嵌入发布 jar，不成为玩家端必需依赖。

1. 使用相应 JDK 执行 `verifyHotDebug`，再启动 target 的游戏实例。
2. 默认 `GET http://127.0.0.1:25585/health` 探活，通过 MCP 客户端连接 `http://127.0.0.1:25585/mcp`，先调用 `status` 确认 side 和引擎模式。
3. 用 `eval_js` 执行短脚本，例如 server side 的 `AutoJS.snapshot()`；检查 `isError`、`ok`、`diagnostics`，触发行为后回读状态并形成断言。界面和输入用 client，权威世界修改用 server。
4. 修改脚本用 `reload_scripts`；KubeJS 模式结合 `kubejs_log` 检查错误，Rhino 模式重建作用域后重新注入验证脚本。配方、标签等按需另做 `/reload`。
5. Java、Mixin 和启动期注册内容不能靠脚本热重载替换，需构建重启后再用 AutoJS 验证。

配置位于游戏目录 `config/autojs.json`；多实例用 `AUTOJS_PORT` 分配不同端口。端点默认可执行任意 Java，只用于本机开发，不得暴露公网或玩家生产环境。共享机器配置 token，请求带 `Authorization: Bearer <token>`，不提交凭据。完整操作手册可从 AutoJS 发布 jar 提取 `SKILL.md`。仓库或端点不可用时明确记录阻塞，不用本地替代 jar 冒充远端验证。

## 发布与维护

- curseforge: project ID not configured in root gradle.properties; environment overrides and credentials remain unverified.
- modrinth: project ID not configured in root gradle.properties; environment overrides and credentials remain unverified.

发布前验证承诺支持的每个 target：构建、检查 jar 的 metadata/共享类/资源、使用 AutoJS 做最小 client 和 dedicated server 行为验证，并记录实际范围。初始化没有运行这些验证，不得把上表的待验证状态当作兼容性承诺。

- [发布指南](docs/PUBLISHING.md)
- [维护流程](docs/MAINTENANCE_WORKFLOW.md)
- [自动发现与新增 target](docs/CI_TARGET_DISCOVERY.md)
- [版本迁移参考](docs/version-differences/README.md)

工程来源：[开发框架](https://github.com/Tower-of-Sighs/SighsTemple)。本 README 与 AGENTS.md 已转为项目文档，后续由项目维护者更新，不再运行初始化脚本覆盖。
