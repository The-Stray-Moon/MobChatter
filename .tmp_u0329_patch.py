import json

PATH = 'data/dialogue/unique/u0329.json'
d = json.load(open(PATH, encoding='utf-8'))

# (mob_id, scenario, old_en_or_zh, new_zh, new_en)
FIX = [
("pixelmon:spectrier", "pickup", "我闻了闻，不是吃的。", "我嗅过一遍，这不能吃。", "I sniffed it once; it is not food."),
("pixelmon:spectrier", "melee_attack", "我转身，后蹄扫过去。", "我扭身，后蹄横着扫出。", "I twist and sweep my hind hooves wide."),
("pixelmon:spectrier", "look_player", "I smell iron and sweat; it is you.", "我朝你转过来，虽然看不见。", "Iron and sweat; that is you."),
("pixelmon:spewpa", "idle", "我在等天黑一点。", "我缩着，等天色再暗些。", "I keep tucked in, waiting for darker sky."),
("pixelmon:spewpa", "look_player", "我盯着你的脚，不是脸。", "我的目光停在你鞋尖上。", "My gaze rests on the tips of your boots."),
("pixelmon:spewpa", "look_player", "你手里的东西在反光。", "那件东西亮得刺眼。", "That thing shines too brightly for my taste."),
("pixelmon:spewpa", "look_player", "你看我，我也在看你。", "你看过来，我也不躲开。", "You look my way, and I do not hide."),
("pixelmon:spewpa", "look_player", "I turn slowly to face you.", "我慢慢转过去，对着你。", "I swivel slowly until I face you."),
("pixelmon:spewpa", "pickup", "我把它塞进壳边的缝里。", "我把它推进壳下的空隙。", "I push it under the gap beneath my shell."),
("pixelmon:spewpa", "target_acquire", "我记住了这个方向。", "这个方位，我记牢了。", "That bearing is fixed in my mind."),
("pixelmon:spewpa", "hurt", "疼，我整个缩进去了。", "疼得我整只缩进壳里。", "It hurt so much I pulled all of me inside."),
("pixelmon:spewpa", "hurt", "我抖得停不下来。", "我的壳一直轻轻打颤。", "My shell keeps up a fine trembling."),
("pixelmon:spewpa", "tempted", "Just one bite; I am not greedy.", "就一口，我不贪。", "One nibble only; I ask no more."),
("pixelmon:spewpa", "collide", "I shift aside to give you room.", "我挪开，给你让出地方。", "I shuffle off so you have the space."),
("pixelmon:spheal", "idle", "风把我的毛吹得乱七八糟。", "海风把我一身短毛吹乱。", "Sea wind has tousled my short coat."),
("pixelmon:spheal", "look_player", "我认得你，你上次也来过。", "你上次也来过这片岸。", "You came to this shore once before."),
("pixelmon:spheal", "look_player", "别站那么远，我看不清。", "离近点，我眼睛看得浅。", "Come nearer; my eyes see only so far."),
("pixelmon:spheal", "look_player", "你的影子落在我身上，凉快。", "你的影子盖住我，正好乘凉。", "Your shadow covers me and that is a nice shade."),
("pixelmon:spheal", "look_player", "我在等你伸手。", "我等着你的手放下来。", "I wait for your hand to come down."),
("pixelmon:spheal", "pickup", "我把它顶在鼻子上。", "我把它托在鼻尖上转。", "I balance it spinning on my nose tip."),
("pixelmon:spheal", "pickup", "我咬着，别抢。", "我咬在嘴里，你别抢。", "I am holding it in my mouth; do not take it."),
("pixelmon:spheal", "target_acquire", "水里有东西在动。", "水面下有影子在游。", "A shape is swimming under the surface."),
("pixelmon:spheal", "target_acquire", "那个影子比我小。", "那影子看着没我大。", "That shape looks no bigger than I am."),
("pixelmon:spheal", "targeting", "我的鳍已经张开了。", "两只鳍都已经撑开了。", "Both flippers are already braced open."),
("pixelmon:spheal", "targeting", "它一动，我就跟着动。", "它挪半寸，我也挪半寸。", "It moves half an inch, and so do I."),
("pixelmon:spheal", "tempted", "I am not picky; I eat anything.", "我不挑食，什么都吃。", "I will not turn my nose up at a thing."),
("pixelmon:spheal", "tempted", "Hold it higher; I cannot reach.", "你举高一点，我够不到。", "Raise it a bit; my flippers fall short."),
("pixelmon:spheal", "collide", "That bump spun me three times around.", "这一碰，我转了三圈。", "Three full turns from that one knock."),
("pixelmon:spheal", "melee_attack", "打完了，我有点晕。", "撞完我自己也打了个转。", "After the collision I spun a circle myself."),
("pixelmon:spheal", "melee_attack", "别怪我，是你先靠近的。", "怪不得我，是你先贴过来的。", "Not my fault; you pressed in first."),
("pixelmon:spheal", "hurt", "摔下来，我弹了两下。", "从高处落下，我弹了两弹。", "Dropping from a height, I bounced twice."),
("pixelmon:spheal", "hurt", "你力气真大。", "你这一下力气真大。", "You hit surprisingly hard."),
("pixelmon:spheal", "hurt", "The blast threw me into the air.", "响声把我掀得老高。", "The blast tossed me up off my belly."),
("pixelmon:spheal", "hurt", "Something stuck in my thick hide.", "有东西扎进我的厚皮里。", "A barb is lodged in my thick fat."),
("pixelmon:spidops", "tempted", "我靠近一点，就一点。", "我挪近半寸，只半寸。", "I shuffle half an inch closer, only half."),
("pixelmon:spidops", "pickup", "谁掉的？我先收着。", "这掉的是谁的？我先守着。", "Whose did this fall from? I will keep watch on it."),
("pixelmon:spidops", "target_acquire", "有东西进了我的地盘。", "有活物踏进我的地界。", "Something living has crossed into my ground."),
("pixelmon:spidops", "target_acquire", "我从上面绕过去。", "我改走树上的那条路。", "I switch to the route along the branches."),
("pixelmon:spidops", "targeting", "I have worked out where to land.", "我算好了落点。", "I have the landing spot figured out."),
("pixelmon:spidops", "melee_attack", "我的前腿按住它。", "前腿一压，它动不了。", "One press of my front legs and it cannot move."),
("pixelmon:spidops", "spawn", "这里安静，适合埋伏。", "这么静的角落，正好设伏。", "A corner this quiet is ideal for a snare."),
("pixelmon:spidops", "hurt", "你比我预想的更沉。", "你比我预想的更沉。", "You carry more weight than I judged."),
]

def find(mob, scen):
    for m in d['mobs']:
        if m['mob_id'] == mob:
            v = m['scenarios'][scen]
            if isinstance(v, dict):
                return [x for arr in v.values() for x in arr]
            return v
    raise KeyError(mob)

for mob, scen, old, new_zh, new_en in FIX:
    hits = [x for x in find(mob, scen) if x['zh'] == old or x['en'] == old]
    assert len(hits) == 1, (mob, scen, old, len(hits))
    hits[0]['zh'] = new_zh
    hits[0]['en'] = new_en

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('patched', len(FIX))
