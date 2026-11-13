# -*- coding: utf-8 -*-
import json, re, sys
from pathlib import Path

ROOT = Path(r"D:\work\MobChatter")

STD = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
       "target_acquire", "targeting", "melee_attack", "spawn"]
DAMAGE = ["fire", "fall", "drown", "explosion", "projectile", "magic",
          "starvation", "lightning", "void"]

W = {"walk": 1.2, "idle": 1.4, "look_player": 1.4, "tempted": 1.0, "collide": 0.8,
     "mate": 0.8, "pickup": 0.2, "target_acquire": 1.0, "targeting": 1.0,
     "melee_attack": 1.0, "spawn": 1.2}


def n_for(key):
    return 10 + max(0, min(4, round(10 * (W[key] - 1))))


def L(zh, en):
    return {"zh": zh, "en": en}


DATA = {}

DATA["pixelmon:trapinch"] = {
    "walk": [
        L("沙土在脚下陷成浅浅的坑。", "The sand sinks into a shallow pit under me."),
        L("我走一步，漏斗就深一寸。", "Each step I take deepens the funnel."),
        L("大颚拖在沙面上，划出沟。", "My jaws drag the sand into a groove."),
        L("慢慢挪，别把巢踩塌了。", "Move slowly; do not crush my nest."),
        L("绕过石头，沙坑得留在原地。", "Around the stone; the pit stays put."),
        L("六条腿一起拨沙，沙往两边飞。", "Six legs scoop sand to either side."),
        L("我沿着坑沿走，一圈又一圈。", "I walk the rim, circle after circle."),
        L("猎物气味从坡上滚下来。", "Prey scent rolls down the slope to me."),
        L("这坡太陡，我自己也站不稳。", "Too steep; even I cannot stand firm."),
        L("走两步停一下，听听沙里的动静。", "Two steps, then a pause to listen."),
        L("我的脚印在坑里留不久。", "My prints do not last in the pit."),
        L("沙粒钻进关节，走起来沙沙响。", "Grit in my joints, I crunch as I walk."),
    ],
    "idle": [
        L("我趴在坑底，只露两只眼睛。", "I lie at the bottom, only my eyes showing."),
        L("等猎物掉下来，比追省力。", "Waiting for prey is easier than chasing."),
        L("沙壁的坡度是我量过的。", "I measured the slope of this wall."),
        L("有虫爬过坑沿，我不动。", "A bug crosses the rim; I stay still."),
        L("大颚合上又张开，磨磨牙。", "My jaws close and open, a slow grind."),
        L("风把落叶吹进坑，我推出去。", "Wind sends a leaf in; I shove it out."),
        L("这坑是漏斗形，爬不出去的。", "The pit is a funnel; nothing climbs out."),
        L("我听见沙粒滑落的声音。", "I hear grains of sand sliding down."),
        L("草丛里有东西在动，忍住。", "Something moves in the grass; hold still."),
        L("太阳晒得沙面发烫，我往下缩。", "The sun heats the sand; I sink lower."),
        L("一整天没吃东西，也还行。", "A whole day unfed is still fine."),
        L("我用前脚把沙拨平。", "I smooth the sand with my front feet."),
        L("巢不深，但够我藏住整个身子。", "Shallow nest, but it hides all of me."),
        L("上面有影子晃过，是云。", "A shadow passes over; just a cloud."),
    ],
    "look_player": [
        L("你站在坑边，脚离边缘太近。", "You stand too close to my rim."),
        L("我抬眼看你，大颚先动了。", "I look up, and my jaws move first."),
        L("再往前一步，沙子会塌。", "One more step and the sand gives."),
        L("你的影子落进坑里，挡住了光。", "Your shadow falls in and blocks my light."),
        L("我歪头，猜你会不会掉下来。", "I tilt my head, guessing if you will fall."),
        L("别伸手，我的颚比你想的快。", "Do not reach in; my jaws are quick."),
        L("你看我像看一块石头。", "You look at me like a stone."),
        L("我眼睛小，但看得住你。", "My eyes are small but they hold you."),
        L("你的靴子沾了沙，滑得很。", "Your boots are sandy and slick."),
        L("我盯住你的脚，不盯脸。", "I watch your feet, not your face."),
        L("退后一步，我给你让点位置。", "Step back; I will make room."),
        L("你蹲下来，坑沿又塌了一点。", "You crouch, and the rim crumbles more."),
        L("别往下看，那是我要你觉得晕的。", "Do not look down; I want you dizzy."),
        L("我认得你的味道，第二次了。", "I know your scent; second visit."),
    ],
    "tempted": [
        L("是虫子吗，我闻到甲壳味了。", "A bug? I smell shell."),
        L("你把食物举高，我看不清。", "You hold it high; I cannot see it."),
        L("我不吃果子，我要会动的东西。", "Not fruit; I want something that moves."),
        L("往坑里丢，别站在边上。", "Drop it in the pit, not at the rim."),
        L("那股腥味让我的颚自己张开了。", "That smell opens my jaws on its own."),
        L("我往前挪了半步，就半步。", "I shifted half a step, only half."),
        L("你别晃手，我看不准落点。", "Stop waving; I cannot judge the fall."),
        L("蚂蚁在沙里走，我听见了。", "Ants walk in the sand; I hear them."),
        L("这味道比沙里的蚯蚓好些。", "Better than the worms in this sand."),
        L("我先等它自己滚进来。", "I will wait for it to roll in."),
    ],
    "collide": [
        L("你撞到坑沿，塌了一片沙。", "You hit the rim and knocked sand loose."),
        L("我身子低，你撞不疼我。", "I am low; your bump does not hurt."),
        L("退开，你踩到我的大颚了。", "Back off, you stepped on my jaw."),
        L("沙坑被撞歪，得重新挖。", "The pit is skewed; I must dig again."),
        L("我用身体顶回去，很轻的。", "I push back with my body, gently."),
        L("别推，我一退就埋进沙里。", "Do not push; I sink back into sand."),
        L("这一下让我的巢塌了半边。", "That blow caved in half my nest."),
        L("我不生气，我只是重新挖。", "I am not angry; I just dig again."),
        L("你比我重，我顶不住。", "You are heavier; I cannot hold."),
        L("沙进了眼睛，我眨了两下。", "Sand in my eyes; I blink twice."),
    ],
    "mate": [
        L("两只蚁狮守一个坑，也是可以的。", "Two antlions can keep one pit."),
        L("我把最深的位置让给你。", "I give you the deepest spot."),
        L("慢慢来，巢还要再挖宽一点。", "Slowly; the nest needs widening."),
        L("你的颚比我的小，我不介意。", "Your jaws are smaller; I do not mind."),
        L("一起听沙，谁先动谁去抓。", "Let us listen; whoever moves first catches."),
        L("别急，先把坑沿拍结实。", "Easy; firm the rim first."),
        L("这片草地够我们挖两个坑。", "This grass holds two pits for us."),
        L("我靠过去，把沙盖在你背上。", "I lean over and cover your back with sand."),
        L("夜里凉，沙底还是暖的。", "Night is cold; the sand below stays warm."),
        L("有猎物就一起吃，不必争。", "If prey comes, we share it."),
    ],
    "pickup": [
        L("我用大颚夹起一块石子。", "I pick up a pebble in my jaws."),
        L("掉进来的东西，都归坑底的我。", "Whatever falls in belongs to me."),
        L("这枚亮的东西，咬不动。", "This shiny thing will not crack."),
        L("把它推到坑边，省得绊脚。", "Push it to the rim so it stops tripping."),
        L("有颗果子滚进来，我先闻。", "A fruit rolled in; I sniff it first."),
        L("我埋东西很快，用前脚盖沙。", "I bury fast, sweeping sand with my feet."),
        L("太重了，拖得我满嘴沙。", "Too heavy; I drag a mouthful of sand."),
        L("这是你的？那我放下。", "Is this yours? I will put it down."),
        L("沙里有东西硬硬的，别是骨头。", "Something hard in the sand; maybe bone."),
        L("我把它藏到坑角，明天再想。", "I tuck it in the corner until tomorrow."),
    ],
    "target_acquire": [
        L("沙动了一下，我锁定了。", "The sand moves; I have it."),
        L("猎物靠近坑口了，我压低身子。", "Prey nears the rim; I flatten down."),
        L("那是一只甲虫，够吃一顿。", "A beetle; enough for one meal."),
        L("我盯着它的影子，不看本体。", "I watch its shadow, not its body."),
        L("它踩到松沙了，就快了。", "It stepped on loose sand; soon."),
        L("我算好了它滑下去的路线。", "I have its sliding path worked out."),
        L("目标不大，但动得很急。", "Small target, but moving fast."),
        L("我张开颚，等在坡底。", "I open my jaws and wait below."),
        L("沙流开始往下带它了。", "The sand is carrying it down now."),
        L("这一次不会让它爬回去。", "This time it will not climb back."),
    ],
    "targeting": [
        L("我跟着沙的流向挪位置。", "I shift with the flow of sand."),
        L("它抓住坑壁了，我拨松那一片。", "It grips the wall; I loosen that patch."),
        L("再滑一点，就到我嘴边。", "A little more and it reaches my jaws."),
        L("我不追，我让沙替我推。", "I do not chase; the sand pushes for me."),
        L("它停住了，我也不动。", "It freezes; so do I."),
        L("我慢慢往坡上顶，逼它往下。", "I creep uphill to force it down."),
        L("距离只剩两个身位。", "Only two body lengths away."),
        L("它的腿在沙里打滑，很好。", "Its legs slip in the sand; good."),
        L("我把坑口堵上一半。", "I block half the pit mouth."),
        L("等它掉进最深处再动。", "I wait until it reaches the bottom."),
    ],
    "melee_attack": [
        L("大颚合上，沙子都溅起来。", "My jaws snap shut and sand sprays."),
        L("咬住就不松，这是我唯一的招。", "Once I bite, I hold; it is my only move."),
        L("这一口咬在甲壳上，硌牙。", "This bite lands on shell and grates."),
        L("我把它往沙里按。", "I press it down into the sand."),
        L("它挣得很凶，我加了力气。", "It thrashes hard, so I squeeze harder."),
        L("沙子灌进它嘴里，它慢了。", "Sand fills its mouth and it slows."),
        L("我咬住腿，不放。", "I hold the leg and do not let go."),
        L("这一下够它记很久。", "This will stay with it a long while."),
        L("我退开半步，看它还动不动。", "I step back to see if it still moves."),
        L("别学我，我的颚不给人碰。", "Do not copy me; my jaws are not for touching."),
    ],
    "spawn": [
        L("我从沙里钻出来，先抖抖身子。", "I climb out of the sand and shake."),
        L("这片草地有很多松土，正合适。", "Loose soil all over this meadow; perfect."),
        L("五级的蚁狮，坑还挖不深。", "A level-five antlion cannot dig deep yet."),
        L("我先找一块没有树根的地方。", "First I find ground without tree roots."),
        L("第一件事，挖一个漏斗。", "First thing: dig a funnel."),
        L("沙子太湿，坑壁撑不住。", "The sand is too wet to hold a wall."),
        L("我绕了一圈，选了这个坡。", "I circled once and chose this slope."),
        L("头顶有草叶遮着，安全些。", "Grass overhead keeps me hidden."),
        L("刚孵化就饿了，先挖坑再说。", "Hungry since hatching; dig first, then eat."),
        L("附近有别的坑，是同类。", "Another pit nearby; one of my kind."),
        L("我趴下，让沙盖住背。", "I lie down and let sand cover my back."),
        L("从今天起，这块沙归我。", "From today this sand is mine."),
    ],
    "hurt": {
        "generic": [
            L("疼，我把身子缩进沙里。", "It hurts; I pull into the sand."),
            L("我的大颚被打偏了。", "My jaws got knocked aside."),
            L("沙坑塌了，我埋在下面。", "The pit caved and buried me."),
            L("这一下让我眼前发白。", "That blow whited out my sight."),
            L("别打头，壳薄的地方在那儿。", "Not the head; my shell is thin there."),
            L("我往坑底退，退不动了。", "I back toward the pit floor; no more room."),
            L("血混着沙，糊在颚上。", "Blood and sand cake on my jaws."),
            L("你比甲虫重太多了。", "You are far heavier than a beetle."),
            L("我哼了一声，声音很闷。", "I grunt, and the sound is muffled."),
            L("再打，我就只能硬碰了。", "Hit me again and I can only push back."),
        ],
        "fire": [L("沙被烧成硬块，粘在身上。", "The sand baked hard and stuck to me.")],
        "fall": [L("从坑沿摔下去，摔进自己的巢。", "I fell off the rim into my own nest.")],
        "drown": [L("水灌进坑里，我往沙下钻。", "Water pours in; I dig down into sand.")],
        "explosion": [L("整座漏斗被掀平了。", "The whole funnel got flattened.")],
        "projectile": [L("有东西钉进了我的沙壁。", "Something stuck into my pit wall.")],
        "magic": [L("奇怪的光让沙粒自己跳。", "Strange light makes the grains jump.")],
        "starvation": [L("三天没猎物，颚都软了。", "Three days without prey; my jaws feel soft.")],
        "lightning": [L("雷打进沙里，沙结成了玻璃。", "Lightning struck sand and made glass.")],
        "void": [L("没有沙，没有坑，只有空。", "No sand, no pit, only emptiness.")],
    },
}

DATA["pixelmon:treecko"] = {
    "walk": [
        L("墙壁和地面，对我来说一样。", "Walls and floors are the same to me."),
        L("脚趾上的细刺扣住木纹。", "Tiny spines on my toes grip the grain."),
        L("我从这棵树跳到那棵树。", "I leap from this tree to that one."),
        L("走在天花板上，头不晕。", "Walking on the ceiling does not dizzy me."),
        L("轻一点，树皮会留下印子。", "Gently; the bark keeps my marks."),
        L("我沿着树枝走到最末端。", "I walk to the very tip of the branch."),
        L("每一步都先试着力点。", "Each step tests the next foothold."),
        L("叶子挡路，我钻过去。", "Leaves block me; I slip through."),
        L("地面太吵，我更喜欢上面。", "The ground is noisy; I like it up here."),
        L("尾巴甩一下，转身很利落。", "One tail flick and I turn cleanly."),
        L("我走得很慢，像在打量。", "I walk slowly, as if appraising."),
        L("树冠的风比地面凉。", "Canopy wind is cooler than the ground."),
    ],
    "idle": [
        L("我咬着一段树枝，磨磨牙。", "I chew a twig to keep my teeth sharp."),
        L("趴在树杈上，看下面的人。", "Perched on a fork, watching the people below."),
        L("风一吹，我就换个姿势。", "When the wind rises, I shift position."),
        L("这棵树我熟，每根枝都踩过。", "I know this tree, every branch walked."),
        L("有只虫爬上来，我先不抓。", "A bug climbs up; I let it be."),
        L("树液的味道有点甜。", "The sap tastes faintly sweet."),
        L("我尾巴垂着，慢慢摆。", "My tail hangs and sways slowly."),
        L("眼睛半闭，其实我没睡。", "Eyes half shut, but I am not asleep."),
        L("高处没人打扰，正好。", "Up high, nobody bothers me."),
        L("我用舌头舔了舔前爪。", "I lick my front toes clean."),
        L("这片树冠归我，别争。", "This canopy is mine; do not argue."),
        L("叶子上有露水，我喝了一点。", "Dew on the leaves; I drink a little."),
        L("树下有影子走过，不是我的。", "A shadow passes below, not mine."),
        L("安静的时候，我能听见树在响。", "In the quiet I hear the tree creak."),
    ],
    "look_player": [
        L("你抬头看，我就在你上面。", "You look up; I am right above you."),
        L("我低头，我们的眼睛对上了。", "I look down and our eyes meet."),
        L("你的手离树干太近了。", "Your hand is far too close to the trunk."),
        L("我不怕你，只是不想下来。", "I am not afraid; I just will not come down."),
        L("你看我的样子，像在挑东西。", "You look at me like I am merchandise."),
        L("我斜眼瞥你，慢慢眨眼。", "I glance sideways and blink slowly."),
        L("你会爬树吗？我在上面等你。", "Can you climb? I will wait up here."),
        L("别伸手，我的脚刺不软。", "Do not reach; my toe spines are not soft."),
        L("你站的那个位置，我看得很清。", "I can see your spot perfectly."),
        L("我不叫，叫了就不酷了。", "I will not squeak; that would spoil it."),
        L("你笑了，我也翘了翘尾巴。", "You laughed, so I lifted my tail."),
        L("退开两步，我的枝要断了。", "Two steps back; my branch is bending."),
        L("你身上有别的树的味道。", "You smell of a different tree."),
        L("我一直看着你，从你进门起。", "I have watched you since you came in."),
    ],
    "tempted": [
        L("那果子熟了吗，闻着有点酸。", "Is that ripe? It smells a bit sour."),
        L("你把东西放低，我才好拿。", "Lower it, and I can take it properly."),
        L("我不挑食，但也不贪。", "I am not picky, and not greedy."),
        L("树果比虫子好对付。", "Berries are easier than bugs."),
        L("我往下爬了两寸，就两寸。", "I climbed down two inches, only two."),
        L("别晃，我看不准落点。", "Stop shaking; my aim is off."),
        L("甜的东西我不常吃。", "I do not often eat sweet things."),
        L("这味道让我的尾巴动了。", "That scent made my tail twitch."),
        L("放地上，我自己过去拿。", "Put it down; I will fetch it myself."),
        L("你手别伸过来，我咬得快。", "Keep your hand back; I bite fast."),
    ],
    "collide": [
        L("你撞到树干，我在上面晃了一下。", "You hit the trunk; I swayed up here."),
        L("别推，我脚下这块树皮松了。", "Do not push; this bark is loose."),
        L("我们撞上了，我先退开。", "We collided; I backed off first."),
        L("你的肩碰到我的尾巴。", "Your shoulder brushed my tail."),
        L("我落地很稳，不用扶。", "I land steady; no need to catch me."),
        L("这一下把我从树上撞下来了。", "That knocked me right off the tree."),
        L("你比我想的硬。", "You are harder than I expected."),
        L("撞完我甩甩头，没事。", "I shake my head after; I am fine."),
        L("我贴着树干滑下来，站稳。", "I slide down the trunk and land."),
        L("下次绕开树，别撞我。", "Next time walk around the tree."),
    ],
    "mate": [
        L("两只木守宫守一片树冠，够用。", "Two geckos can hold one canopy."),
        L("我把最直的枝让给你。", "I give you the straightest branch."),
        L("你走天花板，我走墙。", "You take the ceiling; I take the wall."),
        L("尾巴碰一下，算是说好了。", "A touch of tails seals it."),
        L("慢慢来，树不会跑。", "No hurry; the tree is not going anywhere."),
        L("你的脚刺比我的细。", "Your toe spines are finer than mine."),
        L("一起晒太阳，谁也别挡谁。", "Let us bask; neither blocks the other."),
        L("这棵树够高，我们分上下。", "The tree is tall; let us split it."),
        L("夜里我守上面那半。", "At night I keep the upper half."),
        L("明天带你去另一棵树。", "Tomorrow I will show you another tree."),
    ],
    "pickup": [
        L("我用脚趾夹住一片叶子。", "I pinch a leaf between my toes."),
        L("这颗果子掉在我脚边。", "This berry fell right by my foot."),
        L("小东西我都能带上树。", "I can carry small things up the tree."),
        L("它太滑了，我换脚夹。", "Too slippery; I switch feet."),
        L("我把它塞进树皮的缝里。", "I wedge it into a crack in the bark."),
        L("这是你的？我放回原处。", "Yours? I will put it back."),
        L("捡东西不耽误我走墙。", "Picking things up does not slow my climbing."),
        L("有枚亮片，我多看了一眼。", "A shiny shard; I glance twice."),
        L("我用尾巴卷起来带走。", "I curl my tail around it and go."),
        L("树洞是我的仓库。", "The hollow is my storehouse."),
    ],
    "target_acquire": [
        L("下面有东西在动，我看见了。", "Something moves below; I saw it."),
        L("那只虫爬得慢，正好。", "That bug climbs slowly; perfect."),
        L("我从上面靠近，它不知道。", "I come from above; it does not know."),
        L("尾巴绷紧，我准备好了。", "My tail tightens; I am ready."),
        L("目标在树皮上，离我三寸。", "Target on the bark, three inches away."),
        L("我盯住它的腿，不盯别的。", "I fix on its legs, nothing else."),
        L("它停下，我就再等一会。", "It stops, so I wait a little longer."),
        L("这一跳不会落空。", "This leap will not miss."),
        L("眼睛眯起来，是为了看得准。", "I narrow my eyes to aim better."),
        L("它爬进我的范围了。", "It has entered my reach."),
    ],
    "targeting": [
        L("我顺着树干横着挪过去。", "I sidle sideways along the trunk."),
        L("它往左，我就先到左边。", "It goes left, so I get there first."),
        L("叶影挡住我，它看不见。", "Leaf shadow hides me from it."),
        L("距离两寸，我放慢呼吸。", "Two inches away; I slow my breath."),
        L("我贴着树皮，几乎不动。", "I press to the bark, barely moving."),
        L("它回头了，我停住。", "It turns back; I freeze."),
        L("树液的味道会盖住我。", "The sap smell will cover mine."),
        L("我在它上方的枝上等着。", "I wait on the branch above it."),
        L("它一停，我就出手。", "When it pauses, I strike."),
        L("这个角度，它躲不开。", "From this angle it cannot dodge."),
    ],
    "melee_attack": [
        L("我从上面落下去，先抓后咬。", "I drop from above, grab, then bite."),
        L("前爪按住，牙齿随后。", "Front claws pin it, teeth follow."),
        L("这一口咬在翅膀上。", "My bite lands on its wing."),
        L("它挣扎，我用尾巴压住。", "It struggles; I press with my tail."),
        L("我的爪子比看起来利。", "My claws are sharper than they look."),
        L("咬完我退开，看它跑不跑。", "After biting I step back and watch."),
        L("树皮碎屑落了一地。", "Bark flakes scatter on the ground."),
        L("它的血沾在我脚刺上。", "Its blood sticks to my toe spines."),
        L("我甩甩头，把这口气吐掉。", "I shake my head and huff it out."),
        L("别在下面对着我招手。", "Do not wave at me from down there."),
    ],
    "spawn": [
        L("我从树冠的叶缝里探出头。", "I poke out through a gap in the canopy."),
        L("十级的木守宫，脚刺已经长好。", "A level-ten gecko, toe spines grown in."),
        L("这棵树够粗，能藏住我。", "This trunk is thick enough to hide me."),
        L("我先试着爬了一圈树皮。", "First I test the bark by climbing a lap."),
        L("风大，我抓紧了再动。", "The wind is strong; I grip before moving."),
        L("树梢有虫鸣，听着舒服。", "Insects hum in the tips; pleasant."),
        L("这片树冠没有别的木守宫。", "No other geckos in this canopy."),
        L("我挑了一根朝南的枝。", "I chose a branch facing south."),
        L("刚到这里，先说清楚：树归我。", "New here, so to be clear: this tree is mine."),
        L("叶子有点老，但还结实。", "The leaves are old but still strong."),
        L("我从地上爬到树顶，不喘。", "Ground to treetop without panting."),
        L("以后这里就是我的地盘。", "From now on this is my territory."),
    ],
    "hurt": {
        "generic": [
            L("疼，我脚下一滑。", "It stings; my grip slips."),
            L("别打我的尾巴，它很脆。", "Not my tail; it is fragile."),
            L("这一下让我贴紧了树皮。", "That pressed me flat against the bark."),
            L("我掉了半尺，又抓住了。", "I dropped half a foot and caught myself."),
            L("血滴在叶子上，我不喜欢。", "Blood on the leaves; I dislike that."),
            L("我咬紧牙，没出声。", "I clench my teeth and stay silent."),
            L("我的脚刺断了一根。", "One of my toe spines snapped."),
            L("你打中了我的肋。", "You hit my ribs."),
            L("我退到枝的另一头。", "I retreat to the far end of the branch."),
            L("这不算什么，树还在。", "This is nothing; the tree remains."),
        ],
        "fire": [L("叶子烧起来，我只能往高处跑。", "Leaves burn; I can only climb higher.")],
        "fall": [L("从高处摔下来，脚先着地。", "I hit the ground feet first.")],
        "drown": [L("水漫过树根，我往上游。", "Water rises past the roots; I climb up.")],
        "explosion": [L("冲击把我从枝上掀飞了。", "The blast swept me off the branch.")],
        "projectile": [L("有东西擦过我的耳朵。", "Something grazed my ear.")],
        "magic": [L("奇怪的光让我的鳞竖起来。", "Strange light makes my scales prickle.")],
        "starvation": [L("一天没吃东西，跳不动了。", "A day without food and I cannot leap.")],
        "lightning": [L("雷打在树上，我整只麻了。", "Lightning hit the tree and numbed me.")],
        "void": [L("没有树，也没有可以落的地方。", "No tree, and nowhere to land.")],
    },
}

DATA["pixelmon:trevenant"] = {
    "walk": [
        L("根须从土里拔出，又插回去。", "Roots pull out of the soil and sink back."),
        L("我一步一步，走得很慢。", "I go one step at a time, slowly."),
        L("周围的树朝我这边偏了一点。", "The nearby trees lean slightly toward me."),
        L("脚踩下去，草就枯了。", "Where I tread, the grass withers."),
        L("我走过的地方会留下浅坑。", "I leave shallow hollows where I pass."),
        L("树枝挡路，我不必绕。", "Branches block me; I do not go around."),
        L("林子里没有谁敢挡我。", "Nothing in this wood dares block me."),
        L("我的影子比本体长很多。", "My shadow runs longer than my body."),
        L("走一步，身下的落叶都翻起来。", "Each step flips the leaves beneath me."),
        L("我朝那片最老的林子走。", "I head for the oldest part of the wood."),
        L("树干挪开给我让路。", "Tree trunks shift aside to let me pass."),
        L("我不着急，树也不着急。", "I am in no hurry; neither are the trees."),
    ],
    "idle": [
        L("我站着，像一棵普通的树。", "I stand like any ordinary tree."),
        L("有小鸟落在我肩上。", "A small bird lands on my shoulder."),
        L("我数着林子里的呼吸声。", "I count the breathing in the wood."),
        L("有人在远处砍树，我听见了。", "Someone is felling trees far off; I hear it."),
        L("我抬起手，又慢慢放下。", "I raise a hand and let it fall."),
        L("树皮里有虫，我不赶它们。", "Grubs live in my bark; I let them stay."),
        L("这根枝不长叶子了，还留着。", "This branch grows no leaves; I keep it."),
        L("风穿过我，声音是空的。", "Wind passes through me, sounding hollow."),
        L("我记不清自己活了多少年。", "I have lost count of my years."),
        L("泥土的味道，比什么都久。", "The smell of soil outlasts everything."),
        L("有只鹿在远处看我，我装成树。", "A deer watches; I play at being a tree."),
        L("我把根往深处送了一寸。", "I push my roots an inch deeper."),
        L("落叶堆在脚边，我不扫。", "Leaves pile at my feet; I leave them."),
        L("天要黑了，林子会亮起来。", "It will be dark soon, and the wood will glow."),
    ],
    "look_player": [
        L("你不该一个人走进这片林子。", "You should not walk this wood alone."),
        L("我低头，树皮做的脸没有表情。", "I lower my bark face, expressionless."),
        L("你带着斧头，我闻得出来。", "You carry an axe; I can smell it."),
        L("我眼睛里的光是绿的。", "The light in my eyes is green."),
        L("你再走近，树根会先动。", "Come closer and the roots move first."),
        L("我看着你，像看一棵还没长成的树。", "I watch you like an unfinished tree."),
        L("你脚下这块地，是我的根。", "The ground you stand on is my root."),
        L("别回头，后面那棵树也在看你。", "Do not turn; the tree behind watches too."),
        L("我抬起手，林子就安静了。", "I raise a hand and the wood goes quiet."),
        L("你的影子落在我身上，很轻。", "Your shadow falls on me, very light."),
        L("我很久没有和人说话了。", "I have not spoken with anyone in ages."),
        L("你的心跳太快，我不喜欢。", "Your heartbeat is too fast for me."),
        L("那棵树刚才点了头。", "That tree just nodded."),
        L("走的时候，把斧头留下。", "Leave the axe when you go."),
    ],
    "tempted": [
        L("你手里那点湿土，很香。", "The damp soil in your hand smells good."),
        L("我不吃，我只是想闻。", "I do not eat; I only want to smell."),
        L("树苗的味道，我认得。", "The smell of a sapling, I know it."),
        L("你把水倒下来，我会接住。", "Pour the water down; I will catch it."),
        L("骨粉？那是我同类的骨头。", "Bone meal? Those are my kin's bones."),
        L("我往前挪了一寸。", "I shifted forward an inch."),
        L("别把手缩回去，我看得见。", "Do not pull your hand back; I saw it."),
        L("这点东西不够整片林子吃。", "This is not enough for the whole wood."),
        L("我可以拿一根枝和你换。", "I could trade a branch for that."),
        L("放下就行，你可以走了。", "Just set it down and you may go."),
    ],
    "collide": [
        L("你撞在我身上，像撞一棵树。", "You hit me like hitting a tree."),
        L("树皮裂了一点，不碍事。", "The bark split a little; no matter."),
        L("我太沉，撞你一下会很疼。", "I am heavy; bumping me hurts you more."),
        L("别贴着我，我的根会缠上来。", "Do not press close; my roots wrap."),
        L("你撞落了我的几片叶子。", "You knocked a few of my leaves loose."),
        L("我退了半步，地面震了一下。", "I stepped back and the ground shook."),
        L("这点力气推不动我。", "That much force cannot move me."),
        L("你的肩膀磕在我的枝上。", "Your shoulder struck my branch."),
        L("我低头看你，顺便让开路。", "I look down and step aside."),
        L("下次别从背后靠近。", "Next time, not from behind."),
    ],
    "mate": [
        L("两棵树站在一起，可以站很久。", "Two trees can stand together a long while."),
        L("我把最向阳的那一面让给你。", "I give you the side facing the sun."),
        L("根在地下缠着，不用说话。", "Roots twine underground; no words needed."),
        L("慢慢来，我们的时间还长。", "Slowly; we still have plenty of time."),
        L("你的树干比我的直。", "Your trunk is straighter than mine."),
        L("林子会记得我们站的这个地方。", "The wood will remember where we stood."),
        L("我把落叶分你一半。", "I share half the fallen leaves with you."),
        L("夜里风大，靠紧一点。", "The night wind is strong; stand closer."),
        L("有东西在树下走过，别管它。", "Something passes below; let it."),
        L("明年春天，这里会有小树。", "Next spring there will be saplings here."),
    ],
    "pickup": [
        L("我用树枝一样的手捡起它。", "I pick it up with a branch-like hand."),
        L("有东西掉在我根边。", "Something dropped beside my roots."),
        L("这东西不属于林子。", "This thing does not belong to the wood."),
        L("我把它埋在落叶下面。", "I bury it under the fallen leaves."),
        L("很轻，像一片干枯的皮。", "Very light, like a scrap of dry skin."),
        L("是谁落下的？还给你。", "Who dropped this? Take it."),
        L("我的手指太粗，夹不住。", "My fingers are too thick to pinch it."),
        L("树上的东西，我都能拿到。", "Anything in the trees, I can reach."),
        L("先放在树洞里，改天再说。", "Into the hollow for now; later."),
        L("埋起来的东西，才算安全。", "Only buried things are safe."),
    ],
    "target_acquire": [
        L("斧头举起的那一刻，我动了。", "The moment the axe rose, I moved."),
        L("有人在我的林子里砍树。", "Someone is cutting trees in my wood."),
        L("目标是那个拿铁的人。", "The target is the one with iron."),
        L("我用根探到他的位置。", "My roots have found his position."),
        L("树都朝同一个方向偏，是他。", "The trees lean one way; it is him."),
        L("我不喊，喊会吓跑他。", "I do not shout; that would scare him off."),
        L("这一片林子，我说了算。", "This wood answers to me."),
        L("他踩断的枝，我记着。", "I remember the branch he broke."),
        L("动手前，我先让树合拢。", "Before I move, I let the trees close."),
        L("猎物进了林子，就别想出去。", "Prey that enters the wood does not leave."),
    ],
    "targeting": [
        L("我跟着他，根在地下走。", "I follow him, roots moving underground."),
        L("他往东，东边的树就让开。", "He goes east; the eastern trees part."),
        L("距离够了，我抬起手。", "Close enough; I raise my hand."),
        L("树影把他围在中间。", "Tree shadows close around him."),
        L("他回头看，只看见树。", "He looks back and sees only trees."),
        L("我把路一段一段封起来。", "I seal the path piece by piece."),
        L("他跑得再快，也跑不过根。", "However fast he runs, roots are faster."),
        L("我在等他自己走到树下。", "I wait for him to walk under a tree."),
        L("这一圈树已经准备好了。", "This ring of trees is ready."),
        L("他停下，我就再靠近一棵。", "When he stops, I close one tree nearer."),
    ],
    "melee_attack": [
        L("一根树枝从背后抽过去。", "A branch whips across from behind."),
        L("树根缠住他的脚。", "Roots coil around his feet."),
        L("我用整棵树的分量压下去。", "I press down with a whole tree's weight."),
        L("树皮擦过他的脸，很粗。", "Bark scrapes his face, rough and dry."),
        L("他的手一松，斧头掉了。", "His grip loosens and the axe drops."),
        L("我没有牙齿，只有年轮。", "I have no teeth, only tree rings."),
        L("这一下是替那些被砍的树。", "This one is for the trees he felled."),
        L("他撞在树干上，喘得厉害。", "He hits a trunk and gasps."),
        L("我把他推回林子里。", "I push him back into the wood."),
        L("打完，我把他放下了。", "When it is done, I set him down."),
    ],
    "spawn": [
        L("我从一棵枯树里走出来。", "I step out of a dead tree."),
        L("十五级的朽木妖，根还没扎深。", "A level-fifteen Trevenant, roots shallow."),
        L("这片林子的树，都在等我。", "The trees of this wood were waiting."),
        L("我落地时，脚下的草枯了。", "Grass withered where I landed."),
        L("先看看这片林子缺什么。", "First I see what this wood lacks."),
        L("我的树皮很旧，比这里的树都旧。", "My bark is older than any tree here."),
        L("有风吹来，带着斧头的味道。", "Wind brings the smell of an axe."),
        L("我站了很久，才动第一步。", "I stood a long while before moving."),
        L("落叶盖住我，像盖住一棵树。", "Leaves cover me like a fallen tree."),
        L("这片林地，从今天归我照看。", "This grove is mine to watch over."),
        L("附近的树都把根转向我。", "The nearby trees turn their roots to me."),
        L("我抬起手，天光暗了半分。", "I raise a hand and the light dims."),
    ],
    "hurt": {
        "generic": [
            L("树皮掉了一块，露出白的。", "A chunk of bark fell, showing white."),
            L("疼，但树会慢慢长回来。", "It hurts, but trees grow back slowly."),
            L("我的枝断了一根。", "One of my branches snapped."),
            L("这一击让整片林子都晃了。", "That blow made the whole wood sway."),
            L("你砍在年轮最密的地方。", "You struck where my rings are densest."),
            L("我不流血，我流树液。", "I do not bleed; I run with sap."),
            L("光从伤口里漏出去了。", "Light leaks out through the wound."),
            L("我退了一步，根拔断了。", "I step back and tear a root."),
            L("这声音，像树倒了一半。", "That sound is a tree half falling."),
            L("我记住了你的斧头。", "I have remembered your axe."),
        ],
        "fire": [L("火顺着树皮往上爬。", "Fire climbs up along my bark.")],
        "fall": [L("我摔进自己的落叶堆里。", "I fall into my own pile of leaves.")],
        "drown": [L("根泡在水里，开始发软。", "Roots soak in water and go soft.")],
        "explosion": [L("冲击把一圈树吹倒了。", "The blast flattened a ring of trees.")],
        "projectile": [L("有东西钉进我的树干。", "Something is lodged in my trunk.")],
        "magic": [L("奇怪的力量让年轮发烫。", "Strange power heats my tree rings.")],
        "starvation": [L("土太贫，根吸不到东西。", "The soil is poor; my roots find nothing.")],
        "lightning": [L("雷劈中我，整棵都亮了。", "Lightning struck me; the whole tree lit.")],
        "void": [L("这里没有土，根扎不下去。", "There is no soil, so I cannot root.")],
    },
}

DATA["pixelmon:tropius"] = {
    "walk": [
        L("我落地走几步，翅膀收着。", "I walk a few steps with wings folded."),
        L("叶子做的翅膀太大，走路笨。", "Leaf wings are huge; walking is clumsy."),
        L("每走一步，脖子上的果子晃。", "Every step swings the fruit on my neck."),
        L("我把长脖子放低，避开树枝。", "I lower my long neck under the branches."),
        L("草地软，踩下去有沙沙声。", "The grass is soft and rustles underfoot."),
        L("我慢慢挪，不想压坏花。", "I move slowly so I do not crush flowers."),
        L("走了几步，还是想飞。", "A few steps in, and I want to fly."),
        L("风一来，我的叶子就张开。", "When wind comes, my leaves open."),
        L("我的脚印比牛还大。", "My footprints are bigger than a cow's."),
        L("前面的坡适合起飞。", "The slope ahead is good for takeoff."),
        L("我低头，让脖子上的果子垂下。", "I bow to let my neck fruit hang lower."),
        L("走累了，就找棵树靠着。", "When tired, I lean against a tree."),
    ],
    "idle": [
        L("我站在风里，叶子慢慢张合。", "I stand in the wind, leaves opening slowly."),
        L("脖子上的果子又熟了一颗。", "Another fruit on my neck has ripened."),
        L("有孩子远远看着，不敢过来。", "A child watches from afar, afraid to approach."),
        L("我低头，把最甜的那颗让出来。", "I bow and offer the sweetest one."),
        L("我的翅膀晒得暖烘烘的。", "My wings are warm from the sun."),
        L("这片天空今天很干净。", "The sky is very clean today."),
        L("我用尾巴扫了扫脚边的草。", "I sweep the grass with my tail."),
        L("果子熟透的味道，会招来鸟。", "Ripe fruit draws birds to me."),
        L("我在等风，风来了就飞。", "I wait for wind; when it comes, I fly."),
        L("脖子有点酸，果子太重了。", "My neck aches; the fruit is heavy."),
        L("我慢慢眨眼，像在打盹。", "I blink slowly, as if dozing."),
        L("有片云正好挡了太阳。", "A cloud happens to block the sun."),
        L("我歪头蹭了蹭自己的肩。", "I tilt my head and rub my own shoulder."),
        L("这片草地上的果子，都归我管。", "Every fruit in this meadow is my charge."),
    ],
    "look_player": [
        L("你抬头看我的时候，我正好低头。", "You look up just as I look down."),
        L("你想要一颗吗？我摘给你。", "Want one? I will pick it for you."),
        L("孩子都喜欢吃我头上的果子。", "Children love the fruit on my head."),
        L("我低下头，果子就在你眼前。", "I lower my head; the fruit is before you."),
        L("你伸手的样子，很小心。", "The way you reach out is very careful."),
        L("别怕，我不咬人。", "Do not be afraid; I do not bite."),
        L("我的叶子比你的手臂还宽。", "My leaves are wider than your arm."),
        L("你身上有草和土的味道。", "You smell of grass and soil."),
        L("我眨眨眼，示意你拿吧。", "I blink, telling you to take it."),
        L("果子还带点青，再等两天。", "It is still green; give it two days."),
        L("你笑了，我也把脖子伸低。", "You smile, so I lower my neck."),
        L("我这么大的身子，不会突然动。", "A body this big does not move suddenly."),
        L("你刚才是不是想摸我的翅膀？", "Were you about to touch my wing?"),
        L("拿走吧，别客气。", "Take it; do not be shy."),
    ],
    "tempted": [
        L("那果子闻起来很甜。", "That fruit smells very sweet."),
        L("你也带了果子来？给我看看。", "You brought fruit too? Let me see."),
        L("我头上的够吃，可我想尝你的。", "Mine is plenty, but I want a taste."),
        L("甜的东西我从来不拒绝。", "I never refuse anything sweet."),
        L("你把果子举高，我够得着。", "Hold it up; I can reach it."),
        L("我低头闻了闻，是熟的。", "I lower my head and sniff; it is ripe."),
        L("我用嘴唇碰了一下。", "I touch it with my lips."),
        L("好吃的话，我拿我的换。", "If it is good, I will trade mine."),
        L("别拿走，我才刚尝到。", "Do not take it away; I just tasted it."),
        L("这一口够我记一整天。", "One bite will last me all day."),
    ],
    "collide": [
        L("你撞在我腿上，像撞柱子。", "You hit my leg like a pillar."),
        L("我太重，撞一下地都震。", "I am heavy; the ground shakes when hit."),
        L("我的翅膀挡了你的路。", "My wing is in your way."),
        L("有颗果子被撞掉了。", "One fruit got knocked off."),
        L("我侧身让你过去。", "I turn sideways to let you pass."),
        L("别推我的脖子，果子会掉。", "Do not push my neck; the fruit falls."),
        L("你没事吧，我皮很厚。", "Are you all right? My hide is thick."),
        L("我退了半步，喘了口气。", "I step back and take a breath."),
        L("这一撞，把我的叶子压折了。", "That bent one of my leaves."),
        L("下次从我前面走，别撞后面。", "Next time pass in front, not behind."),
    ],
    "mate": [
        L("我的果子分你一半。", "I give you half my fruit."),
        L("两只热带龙飞起来，遮住一片天。", "Two Tropius in flight can shade the sky."),
        L("你飞得比我稳，我跟着。", "You fly steadier; I follow."),
        L("慢慢来，果子还要几天才熟。", "Slowly; the fruit needs a few more days."),
        L("我把最甜的那颗留给你。", "I saved the sweetest one for you."),
        L("风好的时候，我们一起往南飞。", "When the wind is good, we fly south together."),
        L("你的翅膀比我的宽。", "Your wings are wider than mine."),
        L("站近点，我替你挡风。", "Stand close; I will block the wind."),
        L("有孩子来了，我们一起低头。", "When children come, we both bow."),
        L("这片草原够我们吃很久。", "This plain can feed us a long while."),
    ],
    "pickup": [
        L("我用嘴叼起掉落的果子。", "I pick up a fallen fruit in my mouth."),
        L("地上这颗摔坏了，可惜。", "This one on the ground broke; a pity."),
        L("我用叶子把东西卷起来。", "I roll it up in one of my leaves."),
        L("这个太小，留给小鸟。", "Too small; I leave it for the birds."),
        L("我低头去捡，脖子很酸。", "I bend to pick it up, and my neck aches."),
        L("是不是你掉的？还给你。", "Did you drop this? Here."),
        L("我有四只脚，捡东西不难。", "With four feet, picking things up is easy."),
        L("这块石头压着我的果子。", "This stone is pressing on my fruit."),
        L("我把它放在背上了。", "I set it on my back."),
        L("捡起来才发现是空的壳。", "I picked it up and found an empty shell."),
    ],
    "target_acquire": [
        L("那人手里拿着刀，我看见了。", "That one holds a blade; I see it."),
        L("他在摘我的果子，还折枝。", "He picks my fruit and snaps branches."),
        L("我飞低了一点，看清了。", "I dropped lower and saw clearly."),
        L("目标就在那棵树下。", "The target is under that tree."),
        L("我把翅膀张开，影子盖住他。", "I spread my wings and shadow him."),
        L("我不喜欢动手，但这次不同。", "I dislike fighting, but not this time."),
        L("他拿走的是给孩子的果子。", "He took the fruit meant for children."),
        L("我落在他前面的空地上。", "I land on the open ground ahead of him."),
        L("这一片草原，我照看很久了。", "I have watched this plain a long time."),
        L("跑不掉的，天上看得清。", "You cannot hide; from above I see all."),
    ],
    "targeting": [
        L("我在他头顶盘旋，慢慢降。", "I circle above him, sinking slowly."),
        L("他往左跑，我在左边等。", "He runs left; I wait on the left."),
        L("翅膀的影子一直跟着他。", "My wing shadow keeps following him."),
        L("我算好了落点，就在他前面。", "I know my landing spot, ahead of him."),
        L("风把我往他那边推。", "The wind pushes me toward him."),
        L("他抬头看了，我停住不动。", "He looks up; I hold still."),
        L("这个高度，他跑不掉。", "From this height, he cannot escape."),
        L("我把脖子压低，准备俯冲。", "I lower my neck, ready to dive."),
        L("只剩三次扇翅的距离了。", "Only three wingbeats left between us."),
        L("他很累，我看得出来。", "He is tired; I can tell."),
    ],
    "melee_attack": [
        L("我落下时，地面震了一下。", "When I land, the ground jolts."),
        L("翅膀一拍，把他推开了。", "One wingbeat shoves him back."),
        L("我用脖子撞过去，很沉。", "I swing my neck forward; it lands heavy."),
        L("他退开，我也没有追。", "He backs off, and I do not chase."),
        L("这一下是替那些果子。", "That one is for the fruit."),
        L("我的脚很大，踩下去没轻没重。", "My feet are big, my steps not gentle."),
        L("他手里的刀掉了。", "The blade falls from his hand."),
        L("我甩甩头，叶子哗哗响。", "I shake my head; my leaves rattle."),
        L("我不想再打第二次。", "I do not want to strike twice."),
        L("走开吧，别再回来。", "Go away and do not come back."),
    ],
    "spawn": [
        L("我从云下面飞过来，慢慢降落。", "I fly down from beneath the clouds."),
        L("十五级的热带龙，果子刚结。", "A level-fifteen Tropius, fruit just set."),
        L("这片空中归我，风很好。", "This air is mine; the wind is good."),
        L("先找一棵能停脚的大树。", "First I find a big tree to perch on."),
        L("我落地时，草被压平了一片。", "I land and flatten a patch of grass."),
        L("背上的叶子还带着高空的水汽。", "My leaves still carry high-altitude mist."),
        L("有孩子仰头看我，我低下头。", "A child looks up; I lower my head."),
        L("我脖子上的果子还很小。", "The fruit on my neck is still small."),
        L("这里够暖，适合结果子。", "Warm enough here for fruit to grow."),
        L("我先绕一圈，看看有没有威胁。", "I circle once to check for threats."),
        L("天上的路，我比谁都熟。", "I know the skyways better than anyone."),
        L("以后我会常在这片草地停。", "I will rest in this meadow often."),
    ],
    "hurt": {
        "generic": [
            L("我的叶子被划开了一道。", "A cut opened across one of my leaves."),
            L("疼，我把脖子缩回去了。", "It hurts; I pull my neck back."),
            L("我这么大，也会怕疼。", "Big as I am, I still fear pain."),
            L("这一下让我站不太稳。", "That blow left me unsteady."),
            L("果子掉了两颗，可惜。", "Two fruits fell; a shame."),
            L("我翅膀一歪，飞不直了。", "One wing is bent; I cannot fly straight."),
            L("你打在我最薄的地方。", "You hit my thinnest spot."),
            L("我哼了一声，很沉。", "I let out a low, heavy grunt."),
            L("我退开，用翅膀护住脖子。", "I back off and shield my neck."),
            L("别再来一下，我脾气不坏。", "Not another; my temper is not bad."),
        ],
        "fire": [L("叶子一着火，我立刻往下落。", "Fire on my leaves and I drop at once.")],
        "fall": [L("从高空摔下来，翅膀折了。", "I fell from high and folded a wing.")],
        "drown": [L("我不会游泳，只能拼命扇翅。", "I cannot swim; I beat my wings hard.")],
        "explosion": [L("气浪把我掀翻了。", "The blast flipped me over.")],
        "projectile": [L("有东西扎进了我的翅膀。", "Something lodged in my wing.")],
        "magic": [L("奇怪的光缠住了我的脖子。", "Strange light wrapped around my neck.")],
        "starvation": [L("两天没吃果子，飞不动了。", "Two days without fruit and I cannot fly.")],
        "lightning": [L("雷打在叶子上，整片焦了。", "Lightning hit my leaf and scorched it.")],
        "void": [L("这里没有风，也没有果子。", "No wind here, and no fruit.")],
    },
}

ORDER = ["pixelmon:trapinch", "pixelmon:treecko",
         "pixelmon:trevenant", "pixelmon:tropius"]


def zh_len(s):
    return len(s.strip())


def en_words(s):
    return len(re.findall(r"[A-Za-z0-9'\-]+", s))


def main():
    errors = []
    seen = {}
    out = {"batch": "u0351", "mobs": []}
    lines_total = 0
    for mid in ORDER:
        sc = DATA[mid]
        mob = {"mob_id": mid, "scenarios": {}}
        for key in STD:
            need = n_for(key)
            got = sc.get(key, [])
            if len(got) != need:
                errors.append(f"{mid} {key}: {len(got)} != {need}")
            for ln in got:
                z, e = ln["zh"], ln["en"]
                if not (6 <= zh_len(z) <= 20):
                    errors.append(f"{mid} {key} zh len {zh_len(z)}: {z}")
                if not (4 <= en_words(e) <= 14):
                    errors.append(f"{mid} {key} en words {en_words(e)}: {e}")
                if z in seen:
                    errors.append(f"dup zh {z} ({seen[z]} / {mid})")
                seen[z] = mid
        hurt = sc["hurt"]
        if len(hurt["generic"]) != 10:
            errors.append(f"{mid} hurt.generic {len(hurt['generic'])}")
        for d in DAMAGE:
            if len(hurt[d]) != 1:
                errors.append(f"{mid} hurt.{d} {len(hurt[d])}")
        for ln in hurt["generic"] + [x for d in DAMAGE for x in hurt[d]]:
            z, e = ln["zh"], ln["en"]
            if not (6 <= zh_len(z) <= 20):
                errors.append(f"{mid} hurt zh len {zh_len(z)}: {z}")
            if not (4 <= en_words(e) <= 14):
                errors.append(f"{mid} hurt en words {en_words(e)}: {e}")
            if z in seen:
                errors.append(f"dup zh {z} ({seen[z]} / {mid})")
            seen[z] = mid
        mob["scenarios"] = {
            **{k: sc[k] for k in STD},
            "hurt": {"generic": hurt["generic"],
                     **{d: hurt[d] for d in DAMAGE}},
        }
        lines_total += sum(len(v) for v in mob["scenarios"].values()
                           if isinstance(v, list))
        lines_total += len(hurt["generic"]) + sum(len(hurt[d]) for d in DAMAGE)
        out["mobs"].append(mob)

    if errors:
        print("FAIL", len(errors))
        for e in errors:
            print(" -", e)
        return 1

    path = ROOT / "data" / "dialogue" / "unique" / "u0351.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path} mobs={len(out['mobs'])} lines={lines_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
