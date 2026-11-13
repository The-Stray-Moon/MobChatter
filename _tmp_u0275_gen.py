import json
from pathlib import Path


def L(block):
    out = []
    for raw in block.strip().splitlines():
        raw = raw.strip()
        if not raw:
            continue
        zh, en = raw.split("|")
        out.append({"zh": zh.strip(), "en": en.strip()})
    return out


ODDISH = {
    "walk": L("""
白天把根脚埋进土里，现在才敢走。|Roots buried by day; only now do I dare walk.
我踩着草叶，一路撒下种子。|I tread on grass blades, scattering seeds as I go.
头顶的叶子比脚先晃。|The leaves on my head sway before my feet do.
夜里凉，正好出门散步。|The night is cool—perfect weather for a stroll.
别把我当杂草拔了。|Please do not pull me up thinking I am a weed.
圆身子滚不动，只能挪。|My round body cannot roll, so I shuffle.
草地是我的地盘，五级起步。|This grassland is mine, from level five upward.
脚底带毒，踩过的草会蔫。|My feet are poisonous; grass wilts where I step.
我沿着月光找松软的土。|I follow the moonlight toward soft, loose soil.
种子要撒到更远的地方。|These seeds must travel somewhere farther away.
一步一晃，叶子哗哗响。|Each wobbly step makes my leaves rustle loudly.
走累了就找个土坑蹲下。|When tired, I squat down in a dirt hollow.
"""),
    "idle": L("""
把根脚插回土里，充会儿电。|I sink my root-feet back into the soil to recharge.
白天我就这样站着不动。|By daylight I simply stand still like this.
有人路过，会不会以为我是花？|Will passing travelers mistake me for a flower?
叶子合拢，遮住了眼睛。|My leaves fold together and cover my eyes.
土里的水分顺着根往上爬。|Moisture climbs up through my roots from the soil.
我在数今晚要撒几颗种子。|I am counting seeds to scatter tonight.
毒性在叶尖凝成小点。|Poison beads up in tiny drops on my leaf tips.
风把我的气味吹向下风处。|The wind carries my scent off downwind.
泥土味真让人安心。|The smell of damp earth is deeply comforting.
我听见土里有虫子在动。|I hear insects moving around beneath the soil.
头顶三片叶子，一片有点黄。|Three leaves above; one of them looks a bit yellow.
夜里精神好，白天打瞌睡。|I am lively at night and drowsy through the day.
下雨前，根会先知道。|My roots always know before the rain arrives.
捕获率二百五十五，很容易被捉。|Catch rate two hundred fifty-five—I am easy to catch.
"""),
    "look_player": L("""
你踩到我的种子了。|You just stepped on one of my seeds.
我抬起头，叶子跟着一抖。|I lift my head, and my leaves twitch along.
你身上有肥料的味道。|You smell faintly of fertilizer, traveler.
别盯着我，我只是棵草。|Stop staring; I am only a weed.
你的鞋底沾了新鲜的土。|Fresh soil is stuck to the soles of your boots.
我认得你，昨晚你也从这过。|I know you; you passed here last night too.
你要拔我吗？我先缩一下。|Are you going to pull me up? I will shrink first.
眼睛在叶子底下眨了眨。|My eyes blink from beneath the leaves.
你挡住月光了，让一让。|You are blocking the moonlight—please move aside.
我闻到你口袋里的树果。|I smell berries in your pocket.
草地里很少有人弯腰看我。|Few people in this meadow bend down to look at me.
你的影子盖住我，有点凉。|Your shadow covers me, and it feels a little cold.
别踩，我根还在土里面。|Careful—my roots are still in the soil.
你想捉我？我跑得可慢了。|Want to catch me? I run terribly slow.
"""),
    "tempted": L("""
树果的味道，我闻到了。|I can smell that berry from here.
把果子放在土上，我过去。|Set the berry on the soil and I will come.
你手里那点水，我渴了。|That water in your hand—I am thirsty.
是腐叶土吗？快给我。|Is that leaf compost? Hand it over quickly.
我不吃肉，只喝露水。|I do not eat meat; only dew for me.
那颗果子熟得刚好。|That berry is ripe at exactly the right moment.
你先退两步，我再靠近。|Step back two paces, then I will come closer.
闻着甜，我就挪不动脚。|It smells sweet, and my feet will not move.
这土是新的，谁翻过？|This soil is fresh—who turned it over?
别晃，我眼睛跟不上。|Stop waving it; my eyes cannot keep up.
"""),
    "collide": L("""
撞到我了，叶子都歪了。|You bumped me; my leaves are crooked now.
我这么矮，你怎么会没看见。|I am this short—how did you miss me?
脚被踩进泥里了，拔一下。|My foot is pressed into the mud—pull it out.
轻点，我根还连着地。|Easy there; my roots are still tied to the ground.
你踢飞了我的种子。|You just kicked one of my seeds away.
我一歪，叶子扫到你腿。|I tip over, and my leaves brush your leg.
别推，我滚起来会晕。|Do not push; rolling makes me dizzy.
草被压扁了，就在你脚下。|The grass is flattened right under your feet.
我往旁边退，你往前走。|I will step aside; you keep going forward.
这么大块头，撞一下真疼。|Such a big frame—that bump really hurt.
"""),
    "mate": L("""
我的花粉只飘给同类。|My pollen drifts only toward my own kind.
种子成熟前，别打扰我。|Do not disturb me until the seeds ripen.
开花那几天，我特别香。|For those few flowering days, I smell wonderful.
同族的味道在风里。|The scent of my own kind rides on the wind.
根须缠在一起，就是答应了。|Our root threads twine together—that is a yes.
我的叶子会抖着打招呼。|My leaves shake as a greeting.
你把叶子石化，我会变样。|Use a Leaf Stone on me and I will change.
撒下的种子，总有一颗活。|Of all the seeds I scatter, one will survive.
别踩这块地，我们在忙。|Keep off this patch; we are busy here.
夜里才有的默契。|An understanding that only comes at night.
"""),
    "pickup": L("""
一颗树果，正好埋进土里。|A berry lands just right to bury in the soil.
这个亮片，我当宝贝。|This shiny scrap—I am keeping it as treasure.
捡了颗种子，不知道谁的。|Found a seed; no idea whose it was.
我把水珠顶在叶子上。|I balance a water bead on my leaf.
这块软土，正好当床。|This soft patch of soil would make a bed.
有东西落在我旁边，归我。|Something dropped beside me—it is mine now.
我用脚把它拨进坑里。|I nudge it into a hole with my foot.
骨头？草是不啃骨头的。|A bone? Weeds do not gnaw on bones.
这个小瓶子，闻着像药。|This little bottle smells like medicine.
捡到一半，根脚绊了一下。|Halfway through picking it up, my root-foot trips.
"""),
    "target_acquire": L("""
谁拔了我的根？就是你了。|Who pulled my roots? You, that is who.
那边有人踩坏了一片草地。|Someone over there trampled a patch of grass.
风带来敌意，我抬起头。|The wind brings hostility; I raise my head.
目标太近，跑也跑不掉。|The target is too close to escape now.
叶尖开始渗毒液。|Venom begins seeping from my leaf tips.
我盯上那个乱挖土的人。|I have my eye on the one digging up soil.
走得太近了，草也会恼。|Come any closer, and even a weed gets angry.
五级也有五级的脾气。|Even at level five, I have my temper.
有人要摘我头上叶子。|Someone wants to pluck the leaves off my head.
我慢慢转过身，对准他。|I slowly turn my body to face them.
"""),
    "targeting": L("""
一步，两步，我数着距离。|One step, two steps—I measure the distance.
他还没发现我埋着根。|They have not noticed my roots are buried.
毒粉在叶背攒着。|Poison powder gathers under my leaves.
我等他再靠近半步。|I wait for them to come half a step closer.
草丛够高，遮得住我。|The grass is tall enough to hide me.
别回头看这边。|Do not look back this way.
我的根已经拔出来一半。|Half of my roots are already pulled free.
瞄准他的脚踝就够了。|Aiming at their ankle is enough.
月光下，我的叶子发亮。|Under the moon, my leaves shine faintly.
再等一下，风还没转向。|Wait a little longer; the wind has not turned.
"""),
    "melee_attack": L("""
我整个身子撞上去。|I throw my whole round body into the hit.
叶刃扫过，带一道绿光。|My leaf blade sweeps past with a green flash.
酸液溅到他靴子上。|Acid splashes across their boots.
毒粉散开，别吸气。|Poison powder bursts out—do not breathe in.
我用根脚勾住他脚踝。|I hook my root-foot around their ankle.
吸收一点体力，就一点。|Just a little of your strength—only a little.
头顶叶子抽过去，很疼的。|My head leaves whip across—it stings badly.
撞完我自己也晃了两下。|After the tackle, I wobble twice myself.
别怪我，是你先踩的。|Do not blame me; you stepped first.
毒性顺着伤口往上游。|The poison creeps upward along the wound.
"""),
    "spawn": L("""
从草地里冒出来，五级。|I sprout from the grassland at level five.
种子落在这里，就长在这里。|The seed fell here, so here I grow.
早晨的露水把我浇醒。|The morning dew watered me awake.
这片草地，我第一次睁眼。|This meadow is the first thing I ever saw.
泥土翻开，我顶了出来。|The soil split open as I pushed through.
叶子先出土，身子后跟上。|My leaves broke ground first, then my body.
有人在这片草地撒过种子。|Someone scattered seeds across this meadow.
出生就带着一股草腥味。|I was born already smelling of green sap.
夜色里长出来的小家伙。|A little one that grew up in the dark.
我数了数，周围还有三株。|I counted three more of us nearby.
根扎下去那一刻，我就醒了。|I woke the moment my roots took hold.
草地二十一级之前，都算我的地盘。|Grassland below level twenty-one is my home.
"""),
    "hurt": {
        "generic": L("""
叶子被打掉半片。|Half of one leaf is gone.
疼，根都缩了一下。|That hurt—my roots flinched inward.
我这么点血，经不起几下。|With this little health, I cannot take much.
别打头，叶子还要用的。|Not the head—I still need those leaves.
泥土溅了我一脸。|Dirt splashed all over my face.
我往草里退了半步。|I retreat half a step into the grass.
这一下，我记着了。|I will remember that hit.
身体一歪，差点翻过去。|I tilt and nearly roll right over.
痛感顺着根往上走。|The ache travels upward through my roots.
我还能站，根还牢。|I can still stand; my roots hold firm.
"""),
        "fire": L("火一烧，叶子立刻卷边。|One touch of flame and my leaves curl at the edges."),
        "fall": L("从高处摔下，根脚先着地。|Dropping from a height, my root-feet land first."),
        "drown": L("水漫过叶子，我喘不上气。|Water covers my leaves and I cannot breathe."),
        "explosion": L("炸得我整株飞起来。|The blast sends my whole plant flying."),
        "projectile": L("远处射来一箭，扎进叶子。|An arrow from afar sticks into my leaves."),
        "magic": L("魔法打在身上，根都麻了。|Magic strikes me, and my roots go numb."),
        "starvation": L("土里没养分，叶子开始发黄。|No nutrients in the soil; my leaves yellow."),
        "lightning": L("雷劈下来，草味都焦了。|Lightning strikes, and the green smell turns burnt."),
        "void": L("脚下空了，我掉出世界。|The ground is gone; I fall out of the world."),
    },
}
