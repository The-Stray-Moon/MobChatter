# MobChatter

Creature chatter bubbles rendered above mobs.

- mod id：mobchatter
- Java 包名 / Gradle group：com.merrysnow.mobchatter
- 作者：MerrySnow
- 声明的许可证：MIT

## 项目状态

项目已完成工程初始化。功能清单、安装说明、截图和发布说明由维护者补充；此文件不代表已有业务功能或已经完成任何构建、游戏启动和兼容性验证。

以下矩阵在初始化时从实际 target 目录及 `ci.properties` 生成。CI 启用仅表示会参与验证，不等于已验证支持；后续增删版本或改变工具链时同步维护本表。

| Target | Gradle JVM | CI 配置 | 项目验证状态 |
| --- | --- | --- | --- |
| fabric-1.20.1 | JDK 17 | true | Pending verification |
| fabric-1.21.1 | JDK 21 | true | Pending verification |
| fabric-26.1 | JDK 25 | true | Pending verification |
| forge-1.18.2 | JDK 21 | true | Pending verification |
| forge-1.19.2 | JDK 21 | true | Pending verification |
| forge-1.20.1 | JDK 21 | true | `build verifyHotDebug` 通过；`clean` 因工件占用失败；阴影视觉验证未完成（本次客户端未加载 AutoJS，专用端口拒绝连接） |
| neoforge-1.21.1 | JDK 21 | true | Pending verification |
| neoforge-26.1 | JDK 25 | true | Pending verification |

## 功能

生物头顶对话气泡（客户端渲染）：

- 每个生物在不同时机冒出一句台词，最多两行。
- 第一行正常白色；新台词进入时，上一句被挤到第二行，缩小到 0.8 倍并降到 55% 不透明度。
- 每句有固定显示时长和淡出时间，均在 `config/mobchatter-common.toml` 的 `[display]` 中调整。
- 触发情景：行走、呆立、看向玩家、受伤（含 9 种伤害类型）、被食物吸引、与玩家碰撞、交配、拾取物品、锁定目标瞬间、索敌中、近战挥击、生成。
- 台词资源来自 `common/src/main/resources/assets/mobchatter/dialogue.json.gz`，覆盖 7,527 个实体、约 115 万句中英对照；默认显示中文，可在配置中改为英文。

主要配置项：

| 键 | 默认 | 说明 |
| --- | --- | --- |
| `display.enabled` | true | 总开关 |
| `display.displayDurationTicks` | 80 | 显示时长（tick） |
| `display.fadeOutTicks` | 20 | 淡出时长（tick） |
| `display.maxDistance` | 32 | 触发距离 |
| `display.lineSpacing` | 10 | 两行间距 |
| `display.bottomLineScale` | 0.8 | 第二行缩放 |
| `display.bottomLineAlpha` | 0.55 | 第二行不透明度 |
| `display.language` | zh | `zh` / `en` |
| `trigger.scenarioCooldownTicks` | 160 | 同情景冷却 |
| `trigger.ambientChance` | 0.35 | 环境类情景触发概率 |

当前实现位于 `targets/forge-1.20.1`。其他 target 尚未实现该功能的适配层。

头顶文字使用原版 GUI 的 `Font.drawInBatch(..., shadow=true, NORMAL)` 阴影。局部 Z 缩放改为负值，让原版给白色正文施加的 `+0.03` 偏移朝向相机；不手绘阴影、不关闭全局深度测试。源码确认原先正 Z 会让正文位于阴影后方，名牌的无阴影绘制不能直接证明该深度方向适用于 GUI 阴影。此次 `build verifyHotDebug` 与现有 1 项共享模块测试通过，但不构成视觉验证。`clean` 因既有进程占用工件失败；本项目 `runClient` 启动后未发现 AutoJS 模组加载，专用 `25587` 端口 `/health` 返回连接拒绝，因此未执行 `status` / `eval_js`，尚需重启可用的 AutoJS 客户端验证白字、右下阴影、双行和淡出。

### 构建注意

`maven.neoforged.net` 在当前网络不可达，`targets/forge-1.20.1/build.gradle` 已将 `net.jodah:typetools`、`log4j`、`cpw.mods:modlauncher` 的超范围版本固定为可从 Maven Central / Forge Maven 解析的具体版本，并缩短了 Gradle HTTP 超时。

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
