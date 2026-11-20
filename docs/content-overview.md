# MobChatter 内容简介

MobChatter 为生物添加情境化的头顶对话气泡。当前实际实现目标为 **Minecraft 1.20.1 Forge**：客户端与服务端都需要安装。服务端观察生物行为及真实伤害事件，在行走、待机、受伤、看向玩家、攻击、生成等情境中生成触发信号和统一随机种子，并按服务端配置的显示范围广播给正在追踪该生物的玩家；客户端从本地资源包确定性选句并显示。默认资源包一致时，各玩家选择同一条中英对照台词（显示语言仍由各客户端选择）。气泡支持中英文显示、双行过渡、缩放、淡出与距离/触发配置；台词可由资源包按实体和场景新增、追加、覆盖或禁用，切换资源包或按 `F3+T` 后重新加载。详细资源包格式见 [对话资源包指南](DIALOGUE_RESOURCE_PACKS.md)。

## 内容规模

- **运行时台词库：6,507 个实体 ID**，其中 `minecraft:` 原版实体 90 个、模组实体 ID 6,417 个。
- **台词：约 100 万组中英文对照**；构建资源包含 998,401 组原始台词，具体版本以本仓库 `dialogue.json.xz` 为准。
- **资料榜单：308 个** Minecraft 1.20.1 Forge 候选模组；其中 291 个榜单条目有逐生物资料/台词记录，另 17 个当前无对应生物条目。模组候选并不等同于模组作者或加载器兼容性认证。
- 逐生物资料表记录 6,598 行关系（含 90 行 Minecraft 26.1 原版资料）；实体 ID 跨模组重复时，运行时按实体 ID 合并。

## 支持范围说明

“模组清单”表示项目资料及对话数据覆盖情况，不表示已对 308 个模组逐一进行联机、行为或版本兼容性测试。当前游戏功能适配位于 `common/` 及全部 8 个 target；共享层构建/测试通过，运行行为仅 Forge 1.20.1 完成 AutoJS 验证。完整台词清单以实际打包的运行时资源为准，来源与已知限制见 [模组支持清单](supported-mods.md) 和 [生物支持清单](supported-mobs.md)。

项目目前只读取客户端资源包，不会下载或安装清单里的模组。清单数据按仓库现有输出生成，资源和游戏支持状态会随项目版本变化。


很多作者都尝试过让玩家和生物对话，有预制的，也有 AI 的，本模组带来了另一种形式，AI 预制。

首先，本模组收集了下载量最高的 **308** 个包含生物的模组，提取了包含原版共 **6507** 个生物的信息，详见[模组支持清单](https://github.com/The-Stray-Moon/MobChatter/blob/main/docs/supported-mods.md)和[生物支持清单](https://github.com/The-Stray-Moon/MobChatter/blob/main/docs/supported-mobs.md)。

接着，针对 21 种常见通用生物行为场景，按出现权重分别生成 10 句以上的台词，场景包括：

普通行为（11 种），walk 行走、idle 呆立、look_player 看向玩家、tempted 被食物吸引、collide 与玩家碰撞、mate 交配、pickup 拾取物品、target_acquire 锁定目标、targeting 索敌中、melee_attack 近战挥击、spawn 生成。

受伤（10 种），通用 hurt，以及 9 种细分，hurt.fire、hurt.fall、hurt.drown、hurt.explosion、hurt.projectile、hurt.magic、hurt.starvation、hurt.lightning、hurt.void。

构建资源一共包含 **998401** 组原始台词，详见本模组资源包中的 dialogue.json.xz 压缩文件。

服务端监听生物行为，随机选取符合条件的台词，并广播给一定范围内的所有玩家，每个玩家都可以看见某个生物头顶上冒出了同一句台词。

![showcase](https://resource-api.xyeidc.com//client/members/pics/2af9d9e9)

每种情景十句以上，常规状态下已经足够丰富，如果还觉得不够，可以通过资源包自行添加，如assets/alexsmobs/mobchatter/dialogue/grizzly_bear.json：
```
{
  "format_version": 1,
  "mode": "merge",
  "scenarios": {
    "walk": {
      "operation": "append",
      "lines": [
        {
          "zh": "这边的草好像更香。",
          "en": "The grass smells better over here."
        }
      ]
    },
    "look_player": {
      "operation": "replace",
      "lines": [
        {
          "zh": "你带小麦了吗？",
          "en": "Did you bring any wheat?"
        }
      ]
    }
  }
}

```