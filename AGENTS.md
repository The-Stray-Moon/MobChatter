# MobChatter 开发规范

项目 mod id 为 mobchatter，Java 包名 / Gradle group 为 cc.sighs.mobchatter。功能与目标配置见 [README](README.md)。本工程已完成初始化；不得再次运行初始化脚本覆盖维护者编辑的文档。初始化不是构建、兼容性或运行行为验证，禁止编造已通过的测试和功能。

## 架构与修改边界

- 默认将没有确证 loader / Minecraft 版本差异的代码与资源放在 `common/`，允许引用 Minecraft 和 loader 类型；平台类型依赖本身不是拆分理由。
- 只有阅读实际源码/API 确证差异后，才将相应实现移到 target；差异记录在 target 的 `commonJava { exclude 'path/to/File.java' }`，只排除共享来源文件，不排除 target 的替代实现。
- 跨版本差异统一通过 common 的 `platform.MobChatterPlatform` 契约收敛：各 loader 入口显式 `Platforms.install(...)`，禁止反射、ServiceLoader 猜测或按运行时版本分支。已确证的差异包括：1.18.2/1.19.2 使用 `Entity.level` 字段与 `isOnGround()`；1.20+ 使用 `level()`/`onGround()`；`ResourceLocation` 在 26.1 更名 `Identifier`、`ResourceKey#location()` 更名 `identifier()`（共享信号与选句使用字符串 ID）；1.18.2/1.19.2 伤害分类用 `DamageSource#getMsgId` 与谓词，1.20+ 用 `DamageTypeTags`；Fabric 1.20.1 的 API 没有受伤后事件，只能监听 `ALLOW_DAMAGE`（结算前），1.21.1/26.1 使用 `AFTER_DAMAGE`；Forge/NeoForge 用各自 config spec，Fabric 用 `FileDialogueConfig`；网络分别为 SimpleChannel、`CustomPacketPayload` 与 Fabric payload；资源重载与渲染入口按版本 API 实装。
- `shared.gradle` 直接将 common 原文件接入 target 源码集。禁止复制源码到 build、依赖 common jar、重复添加 common 源码根或使用 `project(':common')`。
- 不以运行时版本判断、反射分发或 classpath 同名类覆盖隐藏兼容性问题。每个产物只对应一个 loader 和 Minecraft 版本，不发布 universal jar。
- 单 target 改动限定在该目标；common 改动需验证所有受影响目标。不得顺手修改其他版本或未经验证统一 API。
- Forge 1.20.1 头顶文字沿用 `Font.drawInBatch(..., shadow=true, NORMAL)` 原版 GUI 阴影；billboard 局部 Z 需朝向相机，使 `Font` 的正文 `+0.03` 深度偏移在阴影前方，不手绘反向阴影。构建与源码推导不能代替 AutoJS 运行及视觉验证。
- Forge 1.20.1 要求双端安装，严格校验 `mobchatter:dialogue` 协议。原始触发、概率、冷却与范围只由服务端决定，按追踪关系、同维度及距离广播单份带 seed/sequence/startTick 的 S2C 信号；客户端仅按 `floorMod(seed, lines.size())` 选句，禁止客户端再次随机或触发。同台词库、同顺序时选句一致；资源包或语言不同可能显示不同。所有配置只注册一份 `ModConfig.Type.COMMON`，文件为双端各自的 `config/mobchatter-common.toml`。服务端读取触发及范围/时长，客户端读取本地语言/样式/显示开关；COMMON 不自动同步，权威显示参数随信号下发，客户端同名参数不得覆盖。单人共用同一份配置，禁止重新拆分 CLIENT/SERVER 配置文件。
- Forge 1.20.1 客户端指令 `/mobchatterunsupported` 只扫描客户端当前已加载的非玩家 LivingEntity，按当前资源包合并快照的实体键判断是否已有记录；去重排序后逐行复制剪贴板，不扫描未加载区块、不向服务器发送指令。显式禁用的实体仍算有记录。
- 对话资源包规范见 `docs/DIALOGUE_RESOURCE_PACKS.md`；共享补丁解析/合并位于 common，各 target 在资源重载 prepare 阶段读取基础库及低到高的完整 JSON 资源栈，apply 阶段一次性发布快照并清理气泡。禁止将显式禁用当成缺失而触发 hurt 回退；坏 JSON 按文件原子跳过，坏基础库使重载失败。1.18.2 使用 `getResources`/`listResources(String, Predicate<String>)`，1.19.2+ 使用 `getResource`/`listResourceStacks`，26.1 使用新的 `PreparableReloadListener.SharedState` 签名，均由 target 适配。只有客户端安装对话资源包读取；服务端只负责触发与广播。
- 对话资源使用 `dialogue.json.xz`（XZ preset 6），由 `tools/build_mod_dialogue.py` 生成，禁止同时打包旧 gzip。所有 target 都显式配置 `org.tukaani:xz:1.10` 并内嵌（Forge/NeoForge 使用 Jar-in-Jar，Fabric 使用 Loom `include`），不假定 loader 自带。
- 电波接收器（`mobchatter:radio_receiver`）的物品逻辑与可见性门控在 common，注册和装备入口在 target。物品注册后用 `ModItems.setRadioReceiver(...)` 安装 supplier，禁止在 common 直接持有 loader registry。Curios 是可选依赖：Forge 1.18.2/1.19.2 在 Curios 存在时注册 `CuriosRadioReceiverItem`（实现 `ICurioItem`），其他 Forge/NeoForge 版本通过 `compileOnly` + `compat/CuriosBridge` 在 `ModList` 检测后 `registerCurio`；`CuriosBridge` 只能在 Curios 存在时加载。Fabric 没有 Curios，使用原版头盔槽。1.18.2–1.21.1 的右键装备回退由 target 的 `RadioReceiverItem` 子类实现；26.1 使用原版 `DataComponents.EQUIPPABLE` 组件，不再 override `use`。`display.requireReceiver` 只控制客户端渲染可见性，不得改变服务端触发、冷却或广播；所有渲染入口必须调用 `ClientDialogueController.canSee()`，摘下饰品后立即隐藏。物品 tooltip 必须通过 `RadioReceiverTooltip` 输出装备位置及当前启用/未启用状态，使用 `.tooltip.slot` / `.enabled` / `.disabled` 翻译键；各 target 只适配 `appendHoverText` 签名（1.18.2–1.20.1 用 `Level`，1.21.1 用 `Item.TooltipContext`，26.1 用 `TooltipDisplay + Consumer`）。
- 共享资源放 common；metadata、Mixin 配置、access widener / transformer 和版本专属资源放 target。同路径资源明确唯一归属，不依赖覆盖顺序。
- 共用模组元数据放根 `gradle.properties`，版本、loader、JDK 和 `debug_*` 放 target 属性。普通本地 jar 放目标 `libs/`，不假定存在传递依赖。
- 插件和运行配置归 target；通用源码接入、热调试、发布逻辑分别复用 `gradle/target-conventions/shared.gradle`、`hot-debug.gradle`、`publish.gradle`。

## IDE 与构建

- 单版本开发独立打开目标目录，使用其 wrapper 与 `ci.properties` 指定的 JDK。
- 全版本浏览打开 `idea-workspace/`，当前配置主版本为 neoforge-1.21.1（JDK 21）；修改主版本以工作区属性为准。主模块唯一管理 common，浏览模块覆盖文档、根配置、脚本和其他 target，不承诺非主版本 API 补全。
- 不额外关联独立 common、根构建或其他完整 target；浏览根排除主 target、common/src、缓存及运行产物。common 内容修改应直接反映到目标索引，构建配置与排除规则修改后重新加载 Gradle。
- 工作区 composite build 共用工作区 Gradle/JVM，不使用被包含目标的 wrapper；切换前检查兼容性，非主版本用独立 wrapper 验证。
- 根和 CI 自动扫描 targets，禁止维护固定版本名单。`ci.enabled` 是验证配置，不是兼容性证据。新增目标遵循 [自动发现指南](docs/CI_TARGET_DISCOVERY.md)。
- 标准验证：target 目录执行 `clean build`；共享层可执行根 `./gradlew -p common build`，但单独 common 成功不代表目标矩阵通过。产物需检查 metadata、共享类、资源及版本范围。涉及启动期注册、配置、网络、资源重载或渲染的改动，还必须在对应 target 实际启动 `runServer`（出现 `Done (`）与 `runClient`（出现 `Sound engine started`），并用 AutoJS `status`/`eval_js` 回读真实状态；不能以编译通过代替。
- 运行差异记录：1.18.2/1.19.2 需要 `pack.mcmeta`；1.19.2 固定 forgespi `6.0.0`、typetools `0.8.3`，Rhino 使用 Modrinth 坐标，且不要在调试运行启用会崩溃的 KubeJS `1902.6.2-build.74`；NeoForge 1.21.1/26.1 需要把热调试运行时接入 run classpath，并固定 KubeJS 浮动传递依赖；26.1 的物品注册必须通过带 `setId(...)` 的重载；Fabric 1.21.1 的 API 版本需满足 AutoJS 的 `>=0.116.17+1.21.1` 约束。

## 必须使用 AutoJS 热调试

- 游戏运行时调试与行为验证必须用 AutoJS：先 `verifyHotDebug` 解析依赖，再启动实例，通过 `status` 确认可用 side 和模式，用 `eval_js` 触发行为并回读真实状态、执行可重复断言。
- 每次检查 `isError`、`ok`、`diagnostics`；不能以无异常、构建成功或静态推测代替运行验证。记录 target、引擎、side、脚本和实际返回结果。
- server side 负责权威世界状态；client side 负责 UI/输入。需要后台调试时使用 `AutoJS.background(true)`，结束后恢复。
- 修改脚本使用 `reload_scripts`；有 KubeJS 时配合 `kubejs_log`，仅 Rhino 时重建作用域后重新注入脚本，不假定存在 KubeJS 事件。配方、标签、战利品表按需另做 `/reload`。
- Java/Mixin 改动和新增启动期注册内容需重新构建、重启，再用 AutoJS 验证；脚本重载不是 Java 热替换。
- AutoJS、Rhino、可用的 KubeJS 仅进入开发游戏运行配置，不进入 common 编译依赖、发布 jar 或玩家必需 metadata。Forge 生产 jar 使用重映射配置并显式补齐依赖，不直接加入普通 runtimeOnly。Forge 1.20.1 运行类路径必须继承 `hotDebugRuntime`（带 named 约束），并从每个 run 的 additionalRuntimeClasspath 移除同一配置，保证 Forge 发现且只加载一份重映射模组；不得改为直接继承不带约束的 `modHotDebugRuntime`。
- 默认端点 `http://127.0.0.1:25585/mcp`，`/health` 探活；配置在游戏目录 `config/autojs.json`，多实例使用 `AUTOJS_PORT`。从 AutoJS jar 提取 `SKILL.md` 查详细用法，不依赖维护者机器上的绝对路径。
- 任意代码执行端点只供本机开发，禁止暴露公网或玩家生产环境；共享环境设置 token，不提交凭据，不操作无关世界/文件。首次 Minecraft EULA 必须由用户阅读并接受。
- 仓库不可访问、依赖缺失、游戏或端点不能启动时记录具体阻塞，不能静默改用本地替代物或伪称验证完成。

## 发布、文档与交付

- 发布前逐目标完成构建与对应 client/server 行为验证，检查最终 jar；发布平台 ID 和凭据按 [发布指南](docs/PUBLISHING.md) 配置，token 只用环境变量。
- `mod_license` 元数据声明不自动替换 LICENSE 正文，维护者需核对正文、依赖和素材授权。不凭许可证参数声称完成法律授权检查。
- 修改功能、支持范围、依赖、工具链或工作区配置后同步 README、AGENTS.md 与相关 docs；文档归维护者管理，不自动重写整个文件。
- 不提交密钥、IDE 缓存、运行世界和构建输出。交付说明区分已验证、未验证和阻塞；不要将模板历史测试作为本项目的验证记录。
- 日常维护与迁移流程见 [维护指南](docs/MAINTENANCE_WORKFLOW.md)；版本/API 差异见 [迁移参考](docs/version-differences/README.md)。
