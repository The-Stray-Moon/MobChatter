# 逐生物研究提示词模板

把 `<BATCH>` 替换为 `data/swarm_plan.json` 里的批次 id，把整个提示词交给一个子 Agent。

---

你在 `D:\work\MobChatter` 项目里做「模组 → 生物」的逐生物资料研究。你负责批次 `<BATCH>`。

## 先读计划

读 `data/swarm_plan.json`，找到 `id` 为 `<BATCH>` 的批次，里面有 `ranks` 列表。

## 每个模组

1. 运行 `python tools/mob_inventory.py --rank N`。它下载该版本的 jar 到 `data/jars/`，从 `assets/*/lang/en_us.json`、`zh_cn.json` 提取所有实体，输出 `data/inventory/N.json`。
2. 只处理 `projectile == false` 的实体。
3. 拉取失败或 jar 无实体时，记录错误并继续。

## 每个生物的资料优先级（严格，禁止使用 MC百科）

1. **模组正文**：`data/mod_bodies.json` 中该模组的 `body` 若提到该生物（英文名或中文名），摘出相关句子，压缩成中文介绍。`source=mod_body`，`source_url` 用模组链接。
2. **官方 wiki**：模组正文或 jar 里有 wiki/fandom 链接时，用 FetchURL 打开对应生物页。`source=wiki`，填实际 URL。
3. **jar 源码与数据文件**：
   - 解压 jar 到 `data/tmp/src_<rank>/`（只读）。
   - `javap -p -c` 读实体类的 `createAttributes` / `registerGoals`，取生命、攻击、护甲、移速、AI 目标。
   - 读 `data/<modid>/forge/biome_modifier/*.json` 取生成群系与权重。
   - 读 `data/<modid>/loot_tables/entities/*.json`（或 `loot_table/entities/`）取掉落。
   - `source=jar_data`，`confidence` 0.5–0.65，`notes` 注明“据 jar 源码与数据文件整理”。
4. 都拿不到：写“资料有限”，`confidence ≤ 0.5`，不得编造。

## 大名单

单个模组生物数 > 150 时写脚本批量处理，不要逐条手工。Pixelmon 用 PokéAPI（`https://pokeapi.co/api/v2/pokemon/<name>` 与 `pokemon-species`，语言 `zh-Hans`），`source=pokeapi`。

## 输出

每个模组写 `data/mobs/<rank>.json`：

```json
{"rank": 1, "mod": "Alex's Mobs", "mod_url": "https://modrinth.com/mod/alexs-mobs",
 "mobs": [{"mob_id": "alexsmobs:grizzly_bear", "name_en": "Grizzly Bear", "name_zh": "灰熊",
           "description_zh": "……", "source": "mod_body", "source_url": "…",
           "confidence": 0.9, "notes": ""}]}
```

约束：

- `mob_id` 用 `<modid>:<实体注册名>`；中文名缺失时 `name_zh` 留空字符串。
- 只写自己批次的 `data/mobs/<rank>.json`，不改其他文件。
- 不访问 mcmod.cn，不引用其内容。

完成后回复：批次 id、处理模组数、生物总数、各 source 计数、失败/跳过项。
