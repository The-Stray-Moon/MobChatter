# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("_tmp_u0326_gen.py")
src = p.read_text(encoding="utf-8")

R = [
("你打量我，我数你几根骨头。", "You size me up; I count your bones.", "你看我，我也在看你。"),
("你的目光一碰我就缩回去。", "Your gaze shrinks back the moment it meets mine.", "你的眼睛在躲我。"),
("举到崖边来，别在下面晃。", "Raise it to the ledge instead of waving it below.", "你举那么高，我够不着。"),
("离开我的爪距，我不习惯贴着人。", "Get out of my claw reach; I dislike being close.", "你退后，我不喜欢被贴着。"),
("这种分量，爪尖一挑就起来。", "One flick of my claw lifts something this light.", "轻得很，一只手就够。"),
("我算着它颈侧那处空隙。", "I am measuring the gap at the side of its neck.", "我盯着它的喉咙。"),
("风从它背后吹，我的味道送不过去。", "The wind is at its back, so my scent never reaches it.", "风向对我有利。"),
("我留了三分力，怕把石头打裂。", "I held back a third of my strength to spare the stone.", "这一下只用了一半力。"),
("崖还在上面，我随时能走。", "The cliff is still above me; I can leave anytime.", "别以为这样就能留住我。"),
("被人盯着，我的叶子会发紧。", "Under a stare, my leaves go tight.", "我不喜欢被盯着看。"),
("我一呼一吸，跟着日影走。", "I breathe in and out with the moving shadow.", "我数着自己的呼吸。"),
("看在这片叶子够嫩的份上。", "Only because this leaf is tender enough.", "我可以勉强尝一口。"),
("尾尖被你踩进泥里了。", "You pressed my tail tip into the mud.", "你踩到我的尾巴了。"),
("你的膝盖正好撞在我额角。", "Your knee landed right on the ridge of my brow.", "你的膝盖撞到我的头。"),
("我只让开这一步，记住。", "I yield this single step; remember it.", "我退了一步，就一步。"),
("尾巴一卷，东西就离了地。", "One curl of my tail lifts it off the ground.", "我用尾巴卷起来。"),
("我半拖半衔，草叶都乱了。", "Half dragging, half carrying, I scatter the grass.", "我拖着它走了几步。"),
("它踩断枯枝，声音替我报了位置。", "It snapped a dead twig, and that sound told me where.", "它踩断了一根枯枝。"),
("风从它那边来，它闻不到我。", "The wind comes from it, so it cannot smell me.", "风从它那边吹过来。"),
("这片草有生土的味道，是新的。", "This grass smells of raw soil; it is new ground.", "这里的气味我不熟。"),
("雷落在附近，我的藤全缩了。", "The bolt struck nearby and every vine recoiled.", "雷劈下来，我全身发麻。"),
("雪压在我壳上，也不化。", "Snow piles on my shell without melting.", "雪落在我背上，不化。"),
("我没躲，是懒得挪这几寸。", "I did not hide; I was too lazy to shift an inch.", "我不怕你，只是不想动。"),
("放到雪面上，我够不着那么高。", "Set it on the snow; I cannot reach that high.", "放低一点，我够不着。"),
("这段路够我爬一整个下午。", "That stretch would take me a whole afternoon.", "太远了，我爬过去要很久。"),
("我一口就饱，别多给。", "One bite fills me; do not give more.", "我只吃一点点。"),
("你的靴跟擦过我的壳。", "Your boot heel scraped across my shell.", "你差点踩到我。"),
("这重量我拖三步就得歇。", "At this weight I rest after three steps.", "太重了，我拖不动。"),
("这是我先看见的，放下。", "I saw it first; put it down.", "别抢，我先看见的。"),
("它还在翻树皮，没看我。", "It is still prying bark and has not looked my way.", "它还没发现我。"),
("我把冷气含在嘴里不出。", "I hold the cold air in my mouth.", "我屏住呼吸。"),
("我把冷气吐在它眼睛里。", "I breathe the cold air straight into its eyes.", "一口冷气喷在它脸上。"),
("壳响个不停，我压不住。", "My shell keeps rattling and I cannot steady it.", "我抖了很久才停。"),
("我落脚的地方，草都贴地了。", "Where I step, the grass lies flat.", "地面在我脚下陷下去。"),
("我慢，可我不改方向。", "Slow, but I never change direction.", "我走得很慢，但不会停。"),
("有片叶子蹭得我鼻子痒。", "A leaf is tickling my nose.", "鼻子有点痒。"),
("仰头看你，我这身肉不轻松。", "Looking up at you is hard work for my bulk.", "我抬头看你，脖子有点酸。"),
("甜的，是谁在附近藏了果子。", "Sweet. Someone nearby is hiding fruit.", "我闻到甜味了。"),
("你撞进我肚子，又滑回去了。", "You sank into my belly and slid back out.", "你撞在我肚子上，弹开了。"),
("我先把两条腿撑起来。", "First I push my two legs up under me.", "我慢慢站起来。"),
("我把肚子挪正，对着它。", "I shift my belly around to face it.", "我把身子转正。"),
("它站着没动，那我也不急。", "It has not moved, so I am in no rush.", "它还在原地。"),
("我张嘴打了个震耳朵的哈欠。", "I open my mouth for an ear-ringing yawn.", "我打了个很长的哈欠。"),
("我撑起身，肩上的骨头响了。", "I push up and the bones in my shoulders crack.", "我伸了个懒腰，骨头响。"),
("我正做梦吃果子，被打断了。", "I was dreaming of fruit, and you interrupted.", "这一下把我打醒了。"),
("火贴上来，毛尖噼啪地卷。", "Fire touches me and my fur tips curl, crackling.", "火燎到我的毛，焦味很冲。"),
("我顺着坡滚，压平一路的草。", "I roll down the slope, flattening the grass.", "我从坡上滚下来，停不住。"),
]

for new_zh, new_en, old_zh in R:
    old = '("%s",' % old_zh
    assert old in src, old_zh
    src = src.replace(old, '("%s",' % new_zh, 1)
    i = src.index('("%s",' % new_zh)
    j = src.index(")", src.index('", "', i))
    seg = src[i:j + 1]
    old_en = seg[seg.index('", "') + 4:seg.rindex('"')]
    src = src[:i] + seg.replace(old_en, new_en) + src[j + 1:]

p.write_text(src, encoding="utf-8")
print("patched", len(R))
