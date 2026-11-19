---
name: mob-collector
description: 采集 Minecraft 模组榜单并生成逐生物资料表（模组×生物×中文介绍×来源），数据来自 Modrinth/CurseForge、模组正文、官方 wiki 与 jar 源码
type: prompt
whenToUse: 当用户要求收集 Minecraft 模组、整理某个模组/榜单的生物清单，或生成逐生物中文介绍表时
arguments:
  - game_version
  - loader
---

# MobCollector：模组榜单 + 逐生物资料

目标：给定游戏版本与加载器（默认 `1.20.1` / `forge`），产出两张表：

1. **模组榜**：新增了生物的模组，按下载量排序。
2. **逐生物表**：一行一个「模组 × 生物」，含英文名、中文名、中文介绍、来源 URL、置信度。

工作目录假定为项目根（本 Skill 所在项目的根目录）。所有中间数据落本地，可断点续跑。

## 环境与凭据

- Python 3.10+，零第三方依赖；jar 解析需要 `javap`（JDK 8+ 均可，1.20.1 类文件建议 JDK 17+）。
- `.env`（项目根）或 `config.json`：
  - `CURSEFORGE_API_KEY` —— 可选，不填则只用 Modrinth；
  - `MODRINTH_TOKEN` —— 可选，提高限速；
  - `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` —— 可选，用于批量判定；不填走人工判定。
- 严禁使用 MC百科（mcmod.cn）作为信息来源。本流程不包含任何 mcmod 步骤。

## 步骤 1：拉取候选模组

```bash
python -m mobchat.run fetch --sources modrinth
python -m mobchat.run fetch --sources curseforge
```

- Modrinth 按下载量取前 N 个 `game_version + loader` 项目，并逐项目校验该版本确有对应加载器的文件。
- 同时跑 `mobs` 分类池补召回（`config.json` 的 `modrinth.category` / `category_max`）。
- 结果写 `data/candidates.json`，原始响应在 `data/raw/`，缓存 `data/cache/`。

## 步骤 2：判定“是否新增生物”

两种方式，二选一：

**A. LLM 批量判定**（配置了 LLM 时）

```bash
python -m mobchat.run classify
```

**B. 人工/Agent 判定**（无 LLM 时）

```bash
python tools/make_review_queue.py --limit 900 --chunk 250
# 逐块阅读 data/review/queue_*.txt，写 data/review/decisions_*.txt
python tools/decisions_to_labels.py
python tools/apply_labels.py
```

判定口径：新增了原版没有的可交互生物才算；只改原版生物（换皮、调数值、加变种）不算；只加方块/物品/结构/维度不算。`primary=true` 表示模组核心就是加生物。

## 步骤 3：导出模组榜

```bash
python -m mobchat.run build
```

输出 `output/top<N>_mob_mods.csv` / `.json`，含 `summary`（英文摘要）与 `intro_zh`（完整中文简介）。
排除名单在 `config.json` 的 `output.exclude`（按名称精确匹配）。

## 步骤 4：抓模组正文

```bash
python tools/fetch_bodies.py
```

用 Modrinth 项目正文生成 `data/mod_bodies.json`（每个模组最多 4000 字），是逐生物介绍的第一优先来源。

## 步骤 5：提取生物清单

```bash
python tools/mob_inventory.py --rank 12
python tools/mob_inventory.py --range 12-20
```

- 下载对应版本的 jar 到 `data/jars/<project_id>.jar`（只读缓存）。
- 读 `assets/*/lang/en_us.json` 与 `zh_cn.json` 的 `entity.*` 键，得到模组真实注册的实体，输出 `data/inventory/<rank>.json`。
- 投掷物/船/矿车等用 `projectile` 标记，最终表排除。
- 大型整合型模组可能只有一个实体类型，物种写在 `data/<modid>/...` 里，需要单独枚举。

## 步骤 6：逐生物研究（可并行）

按 `data/swarm_plan.json` 的批次分给并行 Agent，每个 Agent 处理一批模组。研究提示词见 `references/research-prompt.md`。

资料优先级（严格）：

1. **模组正文**（`data/mod_bodies.json`）提到该生物 → 提取、压缩。
2. **官方 wiki**：正文或 jar 里有 wiki/fandom 链接时，抓对应页面。
3. **jar 源码与数据文件**：`javap` 读 `createAttributes` / `registerGoals`；读 `forge/biome_modifier/*.json` 的生成群系；读 `loot_tables/entities/*.json` 的掉落；读实体碰撞箱与刷怪蛋。
4. 没有资料时写“资料有限”，`confidence ≤ 0.5`，不得编造。

大名单（>150 个生物）必须写脚本批量处理。

每个模组输出 `data/mobs/<rank>.json`：

```json
{"rank": 1, "mod": "Alex's Mobs", "mod_url": "https://modrinth.com/mod/alexs-mobs",
 "mobs": [{"mob_id": "alexsmobs:grizzly_bear", "name_en": "Grizzly Bear", "name_zh": "灰熊",
           "description_zh": "……", "source": "mod_body", "source_url": "…",
           "confidence": 0.9, "notes": ""}]}
```

`source` 只能是 `mod_body` / `wiki` / `jar_data`。

## 步骤 7：合并与校验

```bash
python tools/build_mob_table.py
```

输出：

| 文件 | 内容 |
|---|---|
| `output/mob_descriptions.csv` | 逐生物表，UTF-8 BOM |
| `output/mob_descriptions.json` | 同上 |
| `output/mob_index.json` | 模组 rank → 生物 id 列表 |
| `output/mod_mob_summary.csv` | 每个模组的生物数与来源计数 |

校验：`(mod_rank, mob_id)` 唯一、无空介绍、数量与 summary 一致。

## 质量规则

- 中文介绍 1–3 句，写具体事实：属性、AI 行为、生成环境、掉落、驯服/骑乘等。
- 中文名优先取 jar 的 `zh_cn.json`；没有就留空，不做机器翻译。
- 每条必须有 `source` 与 `source_url`；`jar_data` 的 `notes` 注明“据 jar 源码与数据文件整理”。
- 不写没有依据的设定、数值或玩法。

## 已知限制

- 依赖 jar 的语言文件：模组若不给实体 lang 键，清单会缺项，需要用数据文件或 wiki 补。
- 源码只能还原代码里的事实，作者未写进代码的设定文案无法还原。
- 跨平台下载量不可直接比较，热度口径见 `README.md` 第 1 节。

## 可选：加入 Minecraft 26.1 原版生物

```bash
python tools/build_vanilla.py
```

下载 26.1 客户端 jar，取 `entity.*` 清单（过滤投掷物/船/矿车），再用中文 Minecraft Wiki API 取中文名与简介，写入 `data/mobs/0.json`（rank 0）。

## 可选：逐生物台词

```bash
python tools/build_dialogue.py
```

- 先按 `data/dialogue/archetypes.json` 的 25 个类别写模板句库到 `data/dialogue/banks/`（每类 12 情景 × 20 句 + 伤害子句，中英对照）。
- 合成器按 `mob_key = <rank>:<mob_id>` 确定性抽样，基础 10 句/情景，再按权重追加额外句。
- 输出 `output/mob_dialogue.csv`、`data/dialogue/mods/<rank>.json`、`output/mob_dialogue_index.json`。
- `hurt` 拆 `generic` + 9 种伤害类型（fire/fall/drown/explosion/projectile/magic/starvation/lightning/void）。

台词同样是本地生成，不依赖 MC百科。
