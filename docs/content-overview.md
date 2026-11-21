# 喋喋不休

很多模组都尝试过让玩家和生物对话，有预制的，也有 AI 的，本模组带来了另一种形式，AI 预制。

本模组提前用 AI 生成了大量主流模组中的生物台词并内置，在合适的时机播放，每种情景准备了十句以上随机切换，共约**一百万**句。

首先，本模组收集了下载量最高的 **308** 个包含生物的模组，提取了包含原版共 **6507** 种生物的信息，详见 [模组支持清单](https://github.com/The-Stray-Moon/MobChatter/blob/main/docs/supported-mods.md) 和 [生物支持清单](https://github.com/The-Stray-Moon/MobChatter/blob/main/docs/supported-mobs.md) 。

接着，针对 21 种常见通用生物行为场景，按出现权重分别为每种生物生成 10 句以上的台词，场景包括：

普通行为（11 种），walk 行走、idle 呆立、look_player 看向玩家、tempted 被食物吸引、collide 与玩家碰撞、mate 交配、pickup 拾取物品、target_acquire 锁定目标、targeting 索敌中、melee_attack 近战挥击、spawn 生成。

受伤（10 种），通用 hurt，以及 9 种细分，hurt.fire、hurt.fall、hurt.drown、hurt.explosion、hurt.projectile、hurt.magic、hurt.starvation、hurt.lightning、hurt.void。

构建资源一共包含 **998401** 组原始台词，逐实体台词源见 [`dialogue-pack/`](../dialogue-pack/)，运行时资源为 dialogue.json.xz。

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

本模组还提供了一个饰品叫电波接收器，配置文件中打开requireReceiver后，只有戴上电波接收器才可以看见生物说话。

内置资源由DeepSeek生成，味道较大，欢迎向仓库贡献新的台词。