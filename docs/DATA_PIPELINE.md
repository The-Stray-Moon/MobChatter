# MobChatter — Minecraft 1.20.1 Forge「新增生物」模组榜单

收集 **Minecraft 1.20.1 + Forge 可用 + 新增了原版没有的生物** 的模组，按热度降序输出全部命中（当前 308 条）。

实现原则：**API 负责拉全量候选和热度排序，AI 只负责"这条描述是否新增生物"的判定**。所有中间结果、原始响应、日志、判定理由都落在本地，可重跑、可审计。

---

## 1. 口径（先定死的规则）

| 项 | 定义 |
|---|---|
| 目标版本 | 游戏版本包含 `1.20.1`，且该版本有 **Forge** 构建（不是"项目支持过 1.20.1"或"项目有 Forge 版"就算，必须两者同时满足） |
| 收录标准 | 新增至少 1 个非原版生物/实体（怪物、动物、Boss、NPC、神话生物等） |
| 排除 | 只改原版生物（换皮、改数值、加变种）；只加方块/物品/装备/武器/结构/法术/维度但无新生物 |
| `primary_type` | 模组核心就是加生物 → `纯生物模组`；生物群系/维度/科技/魔法类顺带加生物 → `混合/顺带新增生物` |
| 热度 | 项目总下载量（total downloads）。跨平台取两平台的 **最大值**，不求和，并记录 `popularity_source` |
| 排序 | `downloads_total` 降序 |

已知偏差（这是数据源本身的限制，不是实现问题）：

- CurseForge 和 Modrinth 都**不提供"单个 1.20.1 文件"的下载量**，只有项目总下载量，所以热度天然混入了其它版本/其它加载器的历史下载。
- Modrinth 有 `downloads_1_20_1_forge` 字段（按版本统计的下载量之和），可作为 1.20.1 视角的参考；CurseForge 无对应数据，该列留空。
- 跨平台下载量不可直接比较，取最大值只是排序近似。

---

## 2. 当前状态（2026-11-12）

| 环节 | 状态 |
|---|---|
| Modrinth 拉取 + 1.20.1 Forge 校验 | **已完成**：广度池前 3000 + `mobs` 分类前 1500，去重后 **3990 条候选**，逐项目校验 1.20.1 Forge 文件 |
| CurseForge 拉取 | **未执行** — `.env` 里的 `CURSEFORGE_TOKEN` 是发布 token，官方数据 API 返回 403；网页接口被 Cloudflare 拦截 |
| 判定 | **已完成**：按下载量顺序人工/Agent 逐条判定前 750 条，命中 **309 个新增生物模组**，`method=agent-manual` |
| 去重 / 排序 / 导出 | **已完成**：309 个命中，导出 **308 条**，末位下载量 43,462 |
| 逐生物资料表 | **已完成**：308 个模组 + Minecraft 26.1 原版，**6,598 个生物**（见第 10 节） |
| 逐生物台词表 | **已完成**：6,598 个生物 × 12 个情景，**1,156,546 句**中英对照（见第 11 节） |

榜单第 1 名 `Alex's Mobs`（15.7M），末位 `Arachnids`（43.5k）；共 308 条，排名沿用采集编号，中间存在空号。全部是 `agent-manual` 判定，逐条 URL 抽检可用。

几点说明：

- 广度池（前 3000）密度低，`mobs` 分类池（前 1500）密度高得多，两者合并后 750 条人工判定里出了 309 个正例，全部导出（不再截断到 200）。
- 判定过程中实测并修正了 6 条边界误判：`Nullscape`（纯世界生成）、`Alien Evolution`（玩家变身）、`When Dungeons Arise: Seven Seas`（船只结构）、`Spider Caves`（仅生物群系+装备）、`Under the Moon`（仅生物群系）、`Create: Biotech`（把原版生物接进机器，不加新生物）。判断依据都写进了各自标签的 `evidence`。
- 队列第 750 条之后的候选没有逐条人工判定，`all_candidates.csv` 只含已判定正例；继续往下挖还能补出更多（下载量更低）。

要接 CurseForge 的话：到 https://console.curseforge.com/ 申请数据 API Key，填到 `config.json` 的 `curseforge.api_key`（会覆盖 `.env` 里的发布 token），再跑 `python -m mobchat.run all`。

---

## 3. 凭据

**优先读项目根目录的 `.env`**，其次读 `config.json`。`.env` 支持的变量：

| 变量 | 用途 |
|---|---|
| `CURSEFORGE_TOKEN` / `CURSEFORGE_API_KEY` | CurseForge 数据 API 的 `x-api-key` |
| `MODRINTH_TOKEN` | Modrinth 个人 token，放 `Authorization` 头，提高限速额度 |
| `LLM_API_KEY`（或 `OPENAI_API_KEY` / `MOONSHOT_API_KEY` / `DEEPSEEK_API_KEY`） | 外部 LLM 判定 |
| `LLM_BASE_URL` / `LLM_MODEL` | 配合上面的 Key 使用 |

值只加载、不打印；`data/run_meta.json` 里记录的是打码后的配置。

> 本项目 `.env` 里的 `CURSEFORGE_TOKEN` 是**发布用 token**（配合 `SIGHS_PUBLISH_USER/PASSWORD` 上传模组用），官方数据 API 会返回 `403 Forbidden: API Key missing or invalid`。要跑 CurseForge 数据抓取，需要到 https://console.curseforge.com/ 单独申请 API Key。
>
> CurseForge 网页端接口（`www.curseforge.com/api/v1/...`）和第三方代理（`api.curse.tools`）都被 Cloudflare 拦截，不可用。

不配 LLM 也可以：用第 6 节的"人工/Agent 判定"流程，结果标记为 `method=agent-manual`。


`config.json` 已被 `.gitignore` 忽略，Key 不会进版本库。

全部默认值（可直接覆盖）：

| 配置项 | 默认 | 说明 |
|---|---|---|
| `modrinth.max_projects` | 3000 | 按下载量顺序取前 N 个项目做校验（本次实跑 3000） |
| `modrinth.page_size` | 100 | Modrinth 搜索单页上限 |
| `curseforge.max_mods` | 2000 | 按下载量顺序取前 N 个 mod |
| `curseforge.page_size` | 50 | CurseForge 搜索单页上限 |
| `curseforge.max_verify` | 1200 | 逐 mod 校验文件的前 N 条（控制请求量） |
| `llm.batch_size` | 20 | 每次请求送多少条给模型 |
| `llm.concurrency` | 4 | 并发请求数 |
| `llm.max_body_fetch` | 150 | 低置信度条目补抓全文的预算 |
| `http.min_interval` | 0.2 | 全局请求最小间隔（秒），限速用 |
| `http.cache_ttl_hours` | 168 | 缓存有效期 |
| `output.top_n` | 0 | 导出条数，`0` = 全部 |
| `output.exclude` | `[]` | 按名称精确排除的模组 |
| `output.min_confidence` | 0.5 | LLM 判定低于此置信度的正例丢弃 |

---

## 4. 运行

零第三方依赖，只用标准库。需要 Python 3.10+。

```bash
python -m mobchat.run all                      # 拉取 -> 判定 -> 导出
python -m mobchat.run all --sources modrinth   # 只用 Modrinth
python -m mobchat.run fetch --max-modrinth 3000 --max-curseforge 3000
python -m mobchat.run classify                 # 只跑判定（支持断点续跑）
python -m mobchat.run classify --no-ai         # 强制用关键词启发式
python -m mobchat.run build                    # 只重跑去重/排序/导出
```

- **可断点续跑**：所有 HTTP 响应按 URL 哈希缓存在 `data/cache/`（默认 7 天）；已判定的条目记录在 `data/classified.json`，重跑只处理新增部分。
- **日志**：每次运行写 `data/logs/run-YYYYmmdd-HHMMSS.log`，同时输出到控制台。
- **`--no-ai` 的产物是草稿**：启发式只看标题/摘要关键词，`method` 字段会标成 `heuristic`，用于先把链路跑通，不能当结论。

---

## 5. 数据源与接口（实现细节）

### Modrinth（无需 Key）

```text
GET https://api.modrinth.com/v2/search
    ?facets=[["project_type:mod"],["versions:1.20.1"],["categories:forge"]]
    &index=downloads&limit=100&offset=0
```

facet 数组之间是 AND，数组内是 OR。按 `downloads` 排序分页。

关键坑：`versions:1.20.1` 只保证"项目有 1.20.1 版本"，`categories:forge` 只保证"项目有 Forge 版本"，**不保证 1.20.1 有 Forge 构建**。所以必须逐项目二次校验：

```text
GET https://api.modrinth.com/v2/project/{project_id}/version
    ?game_versions=["1.20.1"]&loaders=["forge"]
```

返回非空才算通过；同时把返回的每个 version 的 `downloads` 求和，得到 `downloads_1_20_1_forge`。

### CurseForge（需 Key，请求头 `x-api-key`）

```text
GET https://api.curseforge.com/v1/mods/search
    ?gameId=432&classId=6&gameVersion=1.20.1&modLoaderType=1
    &sortField=6&sortOrder=desc&pageSize=50&index=0
```

- `gameId=432` = Minecraft，`classId=6` = Mods（不含资源包/光影/整合包），`modLoaderType=1` = Forge
- `sortField=6` = TotalDownloads
- 搜索分页上限：`index + pageSize <= 10000`，代码到了会停
- 逐 mod 校验 1.20.1 Forge 文件：

```text
GET https://api.curseforge.com/v1/mods/{modId}/files
    ?gameVersion=1.20.1&modLoaderType=1&pageSize=50
```

返回非空才算通过。CurseForge 搜索接口本身也接受版本+加载器过滤，但历史上存在返回"项目在别的版本有 Forge 构建"的情况，所以仍逐条校验。

### 跨平台去重

1. 名称规范化（NFKD、小写、`&`→`and`、只保留字母/数字，中日韩字符保留）后做精确分桶；
2. **只合并来自不同平台的记录**：同一平台内即使名称完整相同也保持独立（Modrinth 上同名项目可能是不同模组，误合并会让一条直接从榜单消失）；
3. 不同平台且精确同名 → 直接合并；
4. 其余按规范化名称前 2 个字符分块，块内用 `difflib.SequenceMatcher` 比较：
   - 跨平台且 `>= 0.92` → 自动合并（`action=merged`）
   - `0.85 ~ 0.92`，或一方是另一方的前缀（副标题式命名）→ 不合并，写入 `output/merge_review.csv` 供人工确认（`action=review`）
5. 合并时保留双方 URL、来源、下载量，下载量取大者决定 `popularity_source` 和主 URL。

名称规范化为空（纯符号/emoji）的记录不会参与匹配，但会原样保留在结果里，不会被丢弃。

---

## 6. AI 判定怎么做的

- 输入：名称、摘要（≤600 字符）、分类；低置信度负例再补抓全文（Modrinth 用 `body`，CurseForge 用 `description` 去 HTML），预算 `llm.max_body_fetch`。
- 提示词约束模型：只依据给定文本、禁止使用记忆补充事实、`evidence` 必须逐字摘自原文、证据不足时给低置信度。
- 输出严格 JSON：`{adds_new_mob, primary, mobs[], evidence, confidence}`。
- 解析容错：去 ```json 围栏、提取首个 JSON 对象；批次失败自动二分重试；最终失败的条目退回关键词标注并标 `method=heuristic-fallback`。
- 只有 `adds_new_mob=true` 且（LLM 时）`confidence >= min_confidence` 才进入榜单。

`evidence` 字段是人工抽检的抓手：它能直接验证模型不是编的。

### 没有 LLM 时：人工 / Agent 判定

外部模型不是必须的。流程是把候选压成人能读完的队列，逐条判定后写回：

```bash
python tools/make_review_queue.py --limit 900 --chunk 250   # 生成 data/review/queue_*.txt
# 逐块阅读 queue_*.txt，输出 data/review/labels.jsonl
python tools/apply_labels.py                                 # 写回 data/classified.json
python -m mobchat.run build
```

- 队列预筛：名称/摘要里出现生物类关键词，或 Modrinth 分类含 `mobs`，并按下载量降序；无关键词的模组仍可通过 `--limit` 放大覆盖面。
- 标签格式（每行一个 JSON）：
  `{"key":"modrinth:xxxx","adds_new_mob":true,"primary":true,"mobs":["X"],"evidence":"摘要原文","confidence":0.9}`
- 写入后 `method=agent-manual`，与 `llm` 同级参与 `min_confidence` 过滤和导出。
- `data/review/queue_map.json` 保存 `#编号 -> source:source_id` 的映射，便于核对。

---

## 7. 产物

| 文件 | 内容 |
|---|---|
| `output/top308_mob_mods.csv` | 最终榜单（UTF-8 BOM，Excel 可直接打开；文件名里的数字是实际条数） |
| `output/top308_mob_mods.json` | 同上，结构化版本（列表字段保留为数组） |
| `output/all_candidates.csv` | 所有判定通过的模组（排除名单生效后），与榜单同序 |
| `output/mob_descriptions.csv` | 逐生物资料表：模组 × 生物 × 中文介绍 × 来源（6,598 行） |
| `output/mob_descriptions.json` | 同上，结构化版本 |
| `output/mod_mob_summary.csv` | 每个模组的生物数量与各来源计数（关系映射的汇总视图） |
| `output/mob_index.json` | `模组排名 → 生物 id 列表` 的关系映射 |
| `output/merge_review.csv` | 去重审计：自动合并的配对 + 需人工确认的近似名 |
| `output/summary.json` | 各阶段数量统计 |
| `data/candidates.json` | 已通过 1.20.1 Forge 校验的候选池 |
| `data/classified.json` | 逐条判定结果（按 `source:source_id` 索引，可续跑） |
| `data/intro_zh.json` | 模组名 → 完整中文简介（按项目正文逐条撰写，`build` 时写入榜单） |
| `data/mod_bodies.json` | 308 个模组的项目正文快照（清洗后保留 4000 字），简介的事实来源 |
| `data/raw/*.json` | 原始 API 响应快照（搜索页、校验结果） |
| `data/cache/` | 按 URL 哈希的响应缓存，可安全删除以强制刷新 |
| `data/run_meta.json` | 最近一次运行的命令、时间、脱敏后的配置、各阶段计数 |
| `data/logs/` | 运行日志 |

### 字段字典

| 字段 | 含义 |
|---|---|
| `rank` | 排名（1 起） |
| `name` / `slug` | 模组名 / 平台 slug |
| `summary` | 平台原始英文摘要 |
| `intro_zh` | 完整中文简介（约 3–5 句），依据 Modrinth 项目正文逐条撰写 |
| `primary_type` | `纯生物模组` 或 `混合/顺带新增生物` |
| `mobs` | 描述中明确提到的生物名（`;` 分隔，可能为空） |
| `mob_count_named` | 上述名称的数量 |
| `downloads_total` | 总下载量（跨平台取最大） |
| `downloads_1_20_1_forge` | Modrinth 上 1.20.1 Forge 版本的下载量之和；CurseForge 为空 |
| `popularity_source` | 下载量取自哪个平台 |
| `sources` | 收录来源（`modrinth; curseforge`） |
| `url` / `url_modrinth` / `url_curseforge` | 模组页链接 |
| `confidence` | AI 判定置信度 |
| `method` | `llm` / `heuristic` / `heuristic-fallback` |
| `evidence` | 支撑判定的原文片段 |
| `categories` / `authors` | 平台分类 / 作者 |
| `last_updated` | 平台上的最后更新时间 |
| `verified_1_20_1_forge` | 是否通过逐文件校验（当前只导出通过的） |

---

## 8. 已知限制 / 下一步

1. **单平台覆盖有限**：本次只用 Modrinth（`.env` 里的 CurseForge token 无权访问数据 API）。1.20.1 Forge 的主力生态在 CurseForge，接入正式 API Key 后榜单会更接近真实热度分布，Top 200 的下限也会抬高。
2. **召回盲区**：广度池只扫下载量前 3000，`mobs` 分类池只扫前 1500；人工判定只覆盖前 750 条队列。归到冷门分类、或摘要完全没提生物的模组可能被漏掉。可补的召回手段（尚未实现）：
   - 关键词检索 `mob / creature / boss / animal` 并入候选；
   - 抓热门 1.20.1 Forge 整合包（如 ATM9、Better MC）的 manifest 依赖清单反查；
   - CurseForge `/v1/mods/{id}/related` 关联图扩展。
3. **判定粒度**：本次为逐条人工判定，主要依据名称 + 摘要，边界条目（约 60 条）额外抓了正文核对。标注置信度 0.6 的非核心模组建议优先复核。
4. **下载量口径**：见第 1 节"已知偏差"。

### 交付前的抽检建议

- 随机抽 40 条（含 top 20 全部），逐条打开链接确认：1.20.1 有 Forge 文件、确实新增生物、`evidence` 与描述一致；
- 检查 `output/merge_review.csv` 里 `action=review` 的行，确认没有漏合并；
- 确认 `output/all_candidates.csv` 行数 > 200，否则说明候选池不够，需要加大 `max_projects` / 开 CurseForge。

---

## 9. 目录结构

```text
MobChatter/
├── .env                     # 凭据（已被 gitignore）
├── config.json              # 参数（已被 gitignore）
├── mobchat/
│   ├── config.py            # 默认配置、.env 加载、路径、日志 tee
│   ├── http.py              # 带缓存/限速/重试的 JSON GET
│   ├── sources.py           # Modrinth / CurseForge 拉取、逐文件校验、字段归一化
│   ├── classify.py          # LLM 批量判定 + 关键词回退
│   ├── build.py             # 去重、筛选、排序、CSV/JSON 导出
│   └── run.py               # CLI：fetch / classify / build / all
├── tools/
│   ├── make_review_queue.py   # 生成人工判定队列（分块可读）
│   ├── decisions_to_labels.py # 紧凑决策文件转标签 JSONL
│   ├── apply_labels.py        # 把人工标签合并进 classified.json
│   ├── fetch_bodies.py        # 抓取 308 个模组的项目正文（简介事实来源）
│   ├── mob_inventory.py       # 下载 jar 并从语言文件提取生物清单
│   ├── build_vanilla.py       # 26.1 原版生物表（客户端 jar + 中文 wiki）
│   ├── build_dialogue.py      # 按类别模板与权重合成逐生物台词
│   └── build_mob_table.py     # 合并逐生物资料，生成关系映射与汇总
├── data/                    # 缓存、原始快照、候选池、判定结果、日志、复核队列
│   ├── jars/                # 309 个 1.20.1 Forge jar（只读，可删）
│   ├── inventory/           # 每个模组的实体清单（语言文件提取）
│   ├── mobs/                # 每个模组的逐生物资料（批次产出）
│   ├── dialogue/            # 类别定义、模板句库、逐模组台词
│   └── swarm_plan.json      # 逐生物研究的批次划分
└── output/                  # 最终榜单与审计文件
```

---

## 10. 逐生物资料表（mob_descriptions）

### 产物

| 文件 | 内容 |
|---|---|
| `output/mob_descriptions.csv` | 6,598 行，一行一个（模组, 生物）关系 |
| `output/mob_descriptions.json` | 同上，JSON |
| `output/mob_index.json` | `模组 rank → {mod, url, mob_count, mob_ids[]}` 关系映射 |
| `output/mod_mob_summary.csv` | 每个模组的生物数，以及 mod_body / wiki / jar_data 各来源计数（另含历史 `mcmod` 列） |
| `data/mobs/<rank>.json` | 每个模组的原始研究结果（可单独重跑） |

字段：`mod_rank, mod_name, mod_url, mob_id, name_en, name_zh, description_zh, source, source_url, confidence, notes`。

### 生物清单怎么来的

用 `tools/mob_inventory.py` 下载对应 1.20.1 Forge jar，读 `assets/*/lang/en_us.json` 与 `zh_cn.json` 里所有 `entity.*` 键。这是模组实际注册的实体清单，包含投掷物（用 `projectile` 标记，最终表里排除）。中文名直接取 `zh_cn.json`，没有中文语言文件的模组 `name_zh` 留空，不翻译、不编造。

### 介绍的资料优先级

1. `mod_body`：Modrinth 项目正文里提到该生物时，摘取并压缩。
2. `wiki`：正文或 jar 里有官方 wiki 链接时，抓取对应生物页。
3. `jar_data`：以上都没有时读源码与数据文件——`javap` 解析 `createAttributes` / `registerGoals`，解析 `forge/biome_modifier/*.json` 的生成群系、`loot_tables/entities/*.json` 的掉落、实体碰撞箱。`confidence` 0.5–0.65，`notes` 注明“据 jar 源码与数据文件整理”。

不使用 MC百科（mcmod.cn）；`build_mob_table.py` 只接受上述三种来源。已有的 609 条 `mcmod` 是历史数据，合并脚本按 legacy 放行，新流程不会产生。

### 覆盖情况（2026-11-12）

- 308 个模组 + Minecraft 26.1 原版（90 个生物）全部处理；**6,598 个生物条目**，无空介绍。
- `jar_data` 4,137（55%）、`mod_body` 1,419、`wiki` 353；另有 609 条 `mcmod` 为历史数据（早期版本采集，新流程不再使用，保留不动）。
- 20 个模组没有新实体（0 条），如 `The Hordes`（只做入侵机制）、`Bad Dreams`、`Lost Souls`；它们在 `mod_mob_summary.csv` 中 `mob_count=0`，属正常。
- 大名单：DragonMine Z 370、Advent Of Ascension 290、The Digimod 273、Bok's Banging Butterflies 230、Terra Entity 195。

### 已知限制

- `name_zh` 有 3,100+ 条为空：模组 jar 不含 `zh_cn.json`，保持空白而不是机器翻译。
- `jar_data` 条目来自字节码与数据文件，能确认属性、AI 目标、生成群系与掉落，但无法还原作者未写进代码的设定文案。
- 拆分自同一模组的变体（如各颜色骑士）会各占一行，`mob_id` 不同但共享模板化描述。

---

## 11. 逐生物台词表（mob_dialogue）

为每个生物（含 26.1 原版）写 12 个情景的台词，中英对照，结构化存储，便于批量导入对话系统。

### 产物

| 文件 | 内容 |
|---|---|
| `output/mob_dialogue.csv` | 1,156,546 行扁平表，一行一句（191 MB） |
| `data/dialogue/mods/<rank>.json` | 每个模组的嵌套结构，一个生物一份情景树 |
| `output/mob_dialogue_index.json` | 每个模组的生物数与台词数 |
| `data/dialogue/banks/<archetype>.json` | 25 类生物的模板句库（每类 262 句） |
| `data/dialogue/archetypes.json` | 类别定义、情景列表、各情景权重 |
| `dialogue-pack/` | 按资源包格式摊开的逐实体台词源，社区 PR 直接编辑这里 |

### 情景

`walk` 常态行走、`idle` 呆立、`look_player` 看向玩家、`hurt` 受伤、`tempted` 被吸引、`collide` 与生物碰撞、`mate` 交配、`pickup` 拾取物品、`target_acquire` 锁定目标瞬间、`targeting` 索敌进行时、`melee_attack` 触发近战攻击、`spawn` 生成时。

`hurt` 额外拆分：`generic` 通用受伤，以及 `fire / fall / drown / explosion / projectile / magic / starvation / lightning / void` 九种伤害类型。

### 数量规则

- 每个情景先取 10 句基础台词（`kind=base`）。
- 再按该类别的出现频率权重追加：`extra = round(10 × (weight − 1))`，最高加到 20 句（`kind=extra`）。
- `hurt` 为 10 句通用 + 每种伤害类型 1 句，权重高时继续追加通用句。
- 权重定义在 `data/dialogue/archetypes.json`：例如食草动物 `walk/idle/tempted` 权重 1.6，近战怪 `targeting/melee_attack` 权重 2.0，首领 `spawn` 权重 2.0。

### 结构

```json
{
  "mob_key": "0:minecraft:cow",
  "mob_id": "minecraft:cow",
  "name_en": "Cow",
  "name_zh": "牛",
  "archetype": "passive_herbivore",
  "scenarios": {
    "walk": {"weight": 1.6, "lines": [{"zh": "绕一圈，再绕一圈。", "en": "One more lap, then another.", "kind": "base", "weight": 1.6}]},
    "hurt": {"weight": 1.0, "generic": [...], "by_damage": {"fire": [...], "fall": [...]}}
  }
}
```

CSV 列：`mod_rank, mod_name, mob_key, mob_id, name_en, name_zh, archetype, scenario, damage_type, line_index, kind, weight, text_zh, text_en`。

`mob_key = <mod_rank>:<mob_id>` 是全局唯一键。`mob_id` 单独不唯一（例如 Alex's Mobs 与 Alex's Mobs Continued 共用 `alexsmobs:` 命名空间）。

### 生成方式

1. 25 类生物各写一份模板句库（`banks`），每类 12 情景 × 20 句 + 伤害子句。
2. 每个生物按名称/简介关键词归入一个类别；The Digimod 归 `digimon`，原版按实体 id 手工映射。
   模组简介（`intro_zh`）会识别出主题（恐怖、魔法、机械、史前、水生、下界、末地、亡灵、战争、自然、龙、史莱姆）：189 个模组命中主题，影响 178 个模组里生物的归类、栖息地、标志物与权重。
3. 合成器按 `mob_key` 做确定性抽样（同一生物每次生成结果一致），把 `{name}`、`{name_en}`、`{sound}`、`{habitat}`、`{food}`、`{prey}`、`{motif}` 按中英文分别填充。`{motif}` 优先取生物简介里出现的具体名词（鳞片、骨头、齿轮、符文等，4,224 个生物命中），再退回主题/类别默认值。
4. 权重决定追加句数；同一情景内不重复抽样。

重跑：`python tools/build_dialogue.py`。

资源包增量台词无需改动采集数据或重建基础库，直接提供按实体 ID 分文件的 JSON；格式、优先级及重载规则见 [对话资源包指南](DIALOGUE_RESOURCE_PACKS.md)。

运行时资源以资源包格式摊开在 `dialogue-pack/`（每个实体一个 JSON，格式见 [对话资源包指南](DIALOGUE_RESOURCE_PACKS.md)）。各 target 与 common 的 `processResources` 依赖 `buildDialoguePack`，构建时会自动调用 `python tools/build_mod_dialogue.py` 打包为 `common/src/main/resources/assets/mobchatter/dialogue.json.xz`；也可手动运行该脚本。流水线重新生成 `data/dialogue/mods/*.json` 后，先运行 `python tools/export_dialogue_pack.py --source mods` 刷新目录再打包；不带参数的 `export_dialogue_pack.py` 则从当前 XZ 反向重建目录。打包保留全部中英对照和场景，紧凑 JSON 使用 Python 标准库 XZ preset 6 压缩；不再发布旧 `dialogue.json.gz`。Forge 1.20.1 使用内嵌的 `org.tukaani:xz:1.10` 解码，修改压缩格式后需检查数据一致性、最终 jar 的嵌套依赖，并重启游戏验证加载。

### 已知限制

- 台词按“生物类别 + 个体画像”生成，同一类别内不同生物会共享部分句式；每个生物的名称、栖息地、食物、标志物会替换进句子。
- 原版生物以 26.1 客户端 jar 的实体清单为准（90 个），不含投掷物、船、矿车等非生物实体。
- `text_en` 里可能有 77 条保留中文专名（模组本身没有英文名），未做强制翻译。