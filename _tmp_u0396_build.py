# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAN = json.loads((ROOT / "data/dialogue/unique_plan.json").read_text(encoding="utf-8"))["u0396"]
OUT = ROOT / "data/dialogue/unique/u0396.json"

DAMAGE = ["fire", "fall", "drown", "explosion", "projectile", "magic", "starvation", "lightning", "void"]
ORDER = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
         "target_acquire", "targeting", "melee_attack", "spawn"]


def clamp_extra(w):
    return max(0, min(4, round(10 * (w - 1))))


NEEDLEFISH = {
"walk": [
("我贴着海草床飞快穿梭。", "I dart quickly through the seagrass bed."),
("针一样的长嘴先我一步开路。", "My needle snout goes first and clears the way."),
("我们一群鱼拐弯从不同时。", "My school turns together, never one at a time."),
("温水浅海的沙底是我的跑道。", "The sandy shallows are my running track."),
("尾巴一摆我就窜出两格远。", "One tail flick shoots me two blocks ahead."),
("我沿着暖流边缘绕圈巡游。", "I circle along the edge of the warm current."),
("小身板转弯几乎不用减速。", "My small body turns without slowing down."),
("海草擦过我的侧鳍痒痒的。", "Seagrass brushes my side fins and tickles."),
("我跟在前一条鱼的正后方。", "I swim right behind the fish ahead."),
("水面亮起来我就往浅处走。", "When the surface brightens I head shallower."),
("我的影子在沙上细得像线。", "My shadow on the sand is thin as thread."),
("逆流时我把身体压得更低。", "Against the current I press my body lower."),
("一群针鱼游过像撒了银针。", "A school of us passes like scattered silver needles."),
("我绕开礁石，从缝里钻过去。", "I slip around the reef through a narrow gap."),
],
"idle": [
("我悬在水草间慢慢摆尾。", "I hover among the weeds and sway slowly."),
("有东西漂过我先把嘴张开。", "When something drifts by I open my mouth first."),
("我在数头顶有几条大鱼。", "I count the big fish passing overhead."),
("刚才那口碎食还卡在牙边。", "A crumb of food still sticks by my teeth."),
("我小小的鳃一直扇个不停。", "My tiny gills keep flapping without rest."),
("这片海草床今天格外安静。", "This seagrass bed is unusually quiet today."),
("我把嘴对准水流等食物。", "I point my mouth into the current and wait."),
("一条头足类躲进了石缝。", "A cephalopod has hidden in a rock crevice."),
("我听见远处鲨鱼翻身的水声。", "I hear a shark roll over far away."),
("我身上只有六点生命值。", "Six points of health is all I carry."),
("我抖了抖背鳍上的细沙。", "I shake the fine sand off my dorsal fin."),
("水流推我一下我懒得抵抗。", "The current nudges me and I do not resist."),
("我在等鱼群重新聚拢。", "I wait for the school to gather again."),
("嘴里空着让我有点不安。", "An empty mouth makes me a little restless."),
],
"look_player": [
("这个两条腿的东西比我大太多了。", "This two-legged thing is far bigger than me."),
("我抬头看你的脸，像看一座墙。", "I look up at your face like a wall."),
("你是抓我的还是喂我的？", "Are you here to catch me or feed me?"),
("我盯着你手里的东西看。", "I keep staring at what you are holding."),
("你的影子盖住了我的水面。", "Your shadow covers the water above me."),
("我慢慢后退，但没游远。", "I back away slowly but do not flee far."),
("我从你靴边探头看了一下。", "I peek out from beside your boots."),
("你弯腰时我吓得沉了半格。", "When you bend down I sink half a block."),
("我在判断你会不会伸手。", "I am judging whether you will reach in."),
("你不动，我也僵在水里。", "You hold still, so I freeze in the water."),
],
"tempted": [
("那点碎鱼肉的味道飘过来了。", "The smell of chopped fish drifts over here."),
("你要是丢只小虾我就过去。", "Drop a small shrimp and I will come."),
("我闻到软软的头足类气味。", "I smell something soft and cephalopod-like."),
("食物在水里，我绕了两圈。", "The food floats there, so I circle twice."),
("我贴着你手边打转不肯走。", "I circle your hand and refuse to leave."),
("那一小块比海草好吃多了。", "That little piece beats seagrass any day."),
("我馋得长嘴都开始抖。", "I am so greedy my long snout trembles."),
("你把食物按进水里，我冲了。", "You dunk the food, and I charge in."),
("我抢到一口就掉头跑开。", "I snatch one bite and dart away."),
("别收手，我还没吃够。", "Do not pull your hand back, I am not done."),
],
"collide": [
("我一头撞在你的膝盖上。", "I bump my head right into your knee."),
("针尖似的前嘴顶了你一下。", "My needle-like snout pokes you once."),
("抱歉，鱼群太挤我刹不住。", "Sorry, the school is crowded and I cannot stop."),
("我从你腿缝里挤过去。", "I squeeze through the gap between your legs."),
("你一动，我被水推得打转。", "You move, and the water spins me around."),
("我撞上你手里的桶沿。", "I knock against the rim of your bucket."),
("这一下把我撞得偏了方向。", "That knock sends me off my heading."),
("我贴着你游过去，擦了一下。", "I swim past you and graze your side."),
("水花溅起来，我躲都躲不开。", "The splash rises and I cannot dodge it."),
("我被你挡在礁石和你之间。", "I am trapped between the reef and you."),
("你后退一步，我正好撞上。", "You step back and I hit you exactly."),
("我甩甩嘴，当刚才没发生。", "I shake my snout and pretend nothing happened."),
],
"mate": [
("我要找一条同样细长的伴。", "I want a partner just as slender as me."),
("我们并排游，尾巴一个节奏。", "We swim side by side, tails in one rhythm."),
("海草床深处是我们产卵的地方。", "Deep in the seagrass bed is where we spawn."),
("我用嘴碰碰她的侧鳍。", "I nudge her side fin with my snout."),
("她游开了，我得追上去。", "She swims off, so I have to follow."),
("我们绕着彼此转了三圈。", "We circle each other three times over."),
("这一群小鱼会有自己的小鱼。", "This school will soon have small fry of its own."),
("我把最平的水草让给她。", "I give her the calmest patch of seagrass."),
("两条针鱼并游像一支箭。", "Two needlefish swimming together look like one arrow."),
("她点头了，我摆尾回应。", "She dips her head, and I flick my tail back."),
],
"pickup": [
("这块食物沉底了，我叼起来。", "This food sank, so I pick it up."),
("我捡水里漂着的碎渣吃。", "I eat the scraps drifting in the water."),
("掉下去的东西归我了。", "Whatever falls down here belongs to me."),
("我用嘴把食物从沙里翻出来。", "I flip the food out of the sand with my snout."),
("这块太大，我只能啄着吃。", "This piece is too big, so I peck at it."),
("我叼着它游到水草后面。", "I carry it behind the seagrass."),
("有别的鱼来抢，我先护住。", "Another fish comes for it, so I guard first."),
("我把食物顶在嘴尖上。", "I balance the food on my snout tip."),
("捡到的每口都算今天的好运。", "Every scrap I find counts as today's luck."),
("吃完我把嘴在沙上擦了擦。", "After eating I wipe my snout in the sand."),
],
"target_acquire": [
("那只小虾离我不到一格。", "That shrimp is less than a block away."),
("我看见一只头足类在动。", "I spot a cephalopod moving down there."),
("这条小鱼游得慢，我要它。", "That small fish swims slow, and I want it."),
("我锁定了沙底那团软东西。", "I lock onto that soft lump on the sand."),
("它比我小，那就是我的饭。", "It is smaller than me, so it is my meal."),
("我压低身子，嘴对准它。", "I lower my body and aim my snout."),
("目标在礁石边，我绕过去。", "The target is by the reef, so I go around."),
("我听见它拨水的小声音。", "I hear the tiny sound of it pushing water."),
("它停住了，这是好机会。", "It has stopped, and that is my chance."),
("我选最弱的那一只下手。", "I go for the weakest one of the group."),
],
"targeting": [
("我慢慢靠近，不让水花起来。", "I close in without making a splash."),
("我的长嘴指着它的背。", "My long snout points at its back."),
("再近半格我就能咬到。", "Half a block closer and I can bite."),
("它一跑我就换方向。", "If it runs, I switch direction at once."),
("我在等它离开石头边。", "I wait for it to leave the rock's edge."),
("身体绷紧，尾巴几乎不动。", "My body tightens and my tail barely moves."),
("我盯着它的鳃盖起伏。", "I watch the rise and fall of its gills."),
("它没发现我贴着海草。", "It has not noticed me against the seagrass."),
("我数着距离，一格一格。", "I count the distance, one block at a time."),
("就是现在，我冲出去。", "Now, right now, I shoot forward."),
],
"melee_attack": [
("我一口咬在它背上。", "I bite down on its back."),
("长嘴戳进去，只有三点伤害。", "My snout stabs in for just three damage."),
("我咬住不放，甩了两下。", "I hold on and shake it twice."),
("它挣开了，血丝散在水里。", "It breaks free, and red drifts in the water."),
("这一下够它受的了。", "That hit is enough for it."),
("我咬完马上退开半格。", "After biting I retreat half a block."),
("我的牙小，但很尖。", "My teeth are small but very sharp."),
("它翻过来了，我不松口。", "It flips over and I keep my grip."),
("我戳它侧面最软的地方。", "I jab the softest spot on its side."),
("打赢了我就原地吃。", "Once I win, I eat right there."),
],
"spawn": [
("我们四条针鱼一起进这片海。", "Four of us needlefish enter this sea together."),
("温水海洋里忽然多了几条细影。", "A few thin shadows appear in the warm ocean."),
("我从海草边缘游进这个世界。", "I swim into this world from the seagrass edge."),
("这次只来了我和另外两条。", "Only I and two others came this time."),
("浅海的沙子先落在我眼里。", "Shallow-sea sand is the first thing I see."),
("我出生时尾巴还没使上劲。", "My tail could barely move when I was born."),
("海草床接纳了我们这一小群。", "The seagrass bed takes in our little school."),
("我一落地就去找吃的。", "I go looking for food the moment I arrive."),
("水温刚好，我决定留下。", "The water is just right, so I stay."),
("我们的队伍从三只开始。", "Our school starts with three of us."),
],
"hurt_generic": [
("疼，我一下窜出好远。", "That hurt, and I bolt far away."),
("我的鳞片掉了一小片。", "A small scale has come off me."),
("我拼命摆尾才没被抓住。", "I flap my tail hard to escape the grab."),
("这比我预想的重多了。", "That landed harder than I expected."),
("我缩进海草里抖了一下。", "I shrink into the seagrass and tremble."),
("伤口在水里刺刺地疼。", "The wound stings sharply in the water."),
("我转身就跑，不顾队形。", "I turn and flee, forgetting the formation."),
("六点生命值经不起几下。", "Six points of health will not last long."),
("我嘴里还咬着半口气。", "I am still holding half a breath."),
("再来一下我就完了。", "One more hit and I am finished."),
],
"hurt_single": [
("水边的火烫得我乱窜。", "Fire near the water sends me darting."),
("摔在沙上，我半天没动。", "I hit the sand and lie still."),
("我本该在水里，可也会呛。", "I belong in water, yet I still choke."),
("这一声响把我震得发懵。", "The blast leaves my head ringing."),
("有东西扎进我的侧鳍。", "Something has pierced my side fin."),
("一股怪力钻进我的鳃里。", "Strange force crawls into my gills."),
("空着肚子，我游得越来越慢。", "With an empty belly I swim slower and slower."),
("水面一亮，我整个人麻了。", "The water flashes and my whole body numbs."),
("底下什么都没有，只有空。", "Below is nothing at all, only emptiness."),
],
}

JELLYFISH = {
"walk": [
("我不游，水流带我去哪算哪。", "I do not swim, the current takes me."),
("冷海的水推着我慢慢升高。", "Cold sea water pushes me slowly upward."),
("我的伞盖一收一放往前挪。", "My bell pulses and I inch forward."),
("冻洋的浮冰从我头顶漂过。", "Ice floes drift past above my head."),
("我被暗流卷着转了半圈。", "A current rolls me half a turn."),
("漂过一片海藻我停了一下。", "I drift past kelp and pause a moment."),
("水越冷，我动得越慢。", "The colder the water, the slower I move."),
("我随波上下，像块透明的布。", "I rise and fall like clear cloth."),
("一整天我只挪了几格。", "In a whole day I move a few blocks."),
("浪把我推回原来的位置。", "The wave pushes me back where I was."),
("我穿过一群鳕鱼，它们让开了。", "I pass a school of cod and they part."),
("水面结冰前我得往下沉。", "Before the surface freezes I must sink."),
("我漂得很慢，但从不迷路。", "I drift slowly but never lose my way."),
("洋流拐弯，我跟着拐。", "The current turns, and I turn with it."),
],
"idle": [
("我悬在冷水里一动不动。", "I hang in the cold water without moving."),
("伞盖张开又合上，像在呼吸。", "My bell opens and closes like breathing."),
("我只有三点生命，很轻很薄。", "Three points of health, and I am thin."),
("有浮游的小东西飘进我嘴里。", "Tiny drifting things float into my mouth."),
("我在等水流替我带饭。", "I wait for the current to bring food."),
("下面很深，我不打算下去。", "It is deep below and I will not go."),
("我的触手垂着，慢慢摆。", "My tentacles hang and sway slowly."),
("冷海的光是灰蓝色的。", "The light in this cold sea is grey-blue."),
("一只海鸟的影子掠过去了。", "A seabird's shadow sweeps past above."),
("我在水层里转了半圈。", "I turn half a circle in the water layer."),
("我身上有一点粘，像抹了油。", "My body feels slick, as if oiled."),
("这里没人打扰，很好。", "Nobody disturbs me here, which suits me."),
("我收拢伞盖省点力气。", "I fold my bell to save some strength."),
("水压稳稳压着我的伞顶。", "The water pressure rests steady on my bell."),
],
"look_player": [
("你从冰面下来时我就看见了。", "I saw you the moment you came under the ice."),
("我转过来正对着你的脸。", "I turn to face you directly."),
("你比这海里任何东西都亮。", "You are brighter than anything in this sea."),
("我在想你会不会碰我的触手。", "I wonder whether you will touch my tentacles."),
("我轻轻往上飘了一点。", "I float up just a little toward you."),
("你呼气的水泡在我旁边散开。", "Your breath bubbles scatter beside me."),
("我看不清你的表情，但你在看我。", "I cannot read your face, but you watch me."),
("我停在你面前，伞盖慢慢张。", "I stop before you and slowly open."),
("你是来抓水母的吗？", "Have you come here to catch jellyfish?"),
("我躲到一层薄冰的影子里。", "I hide in the shadow of thin ice."),
],
"tempted": [
("你手里的东西我从来没见过。", "I have never seen what you are holding."),
("是吃的吗？我飘近了一点。", "Is it food? I drift a little closer."),
("我顺着你手边的水流过去。", "I ride the current toward your hand."),
("那味道不重，但我感觉得到。", "The smell is faint, but I can feel it."),
("我绕着你手心转了一圈。", "I circle once around your palm."),
("别晃，我跟着你的手在动。", "Do not wave it, I am following your hand."),
("我为这点味道多游了两格。", "For that scent I move two extra blocks."),
("我的触手往你那边伸。", "My tentacles reach out toward your side."),
("你要是不给，我就慢慢退。", "If you do not give it, I will drift back."),
("这一点点就够我高兴半天。", "This little bit keeps me content for hours."),
],
"collide": [
("我软软地撞在你手臂上。", "I bump softly against your arm."),
("你穿过我，我散开又合上。", "You pass through me and I part, then close."),
("我的伞盖被你顶得歪了。", "Your push tilts my bell sideways."),
("我被你带起的水流推走。", "The current you make pushes me away."),
("我们撞在一起，谁都没事。", "We collide and neither of us is hurt."),
("我的触手缠到你手腕一下。", "My tentacle catches your wrist briefly."),
("你退后时把我挤到冰边。", "Your step back squeezes me to the ice."),
("我不硬，撞不出声音。", "I am soft, so the bump makes no sound."),
("这一撞让我转了个方向。", "That bump turned me a different way."),
("我又飘回来，贴着你的腿。", "I drift back and rest by your leg."),
],
"mate": [
("冷水里另一只水母亮起来了。", "Another jellyfish brightens in the cold water."),
("我们慢慢往同一片水层靠。", "We slowly drift into the same water layer."),
("我的伞盖碰了碰她的。", "My bell touches hers."),
("我们在冻洋下面一起漂。", "We drift together beneath the frozen ocean."),
("这一带只有我们两只。", "There are only the two of us here."),
("她把触手收短，我靠近了。", "She shortens her tentacles and I move closer."),
("我们一起被同一股流带走。", "One current carries us both away."),
("过些天这里会多一只小的。", "In a few days a small one will appear here."),
("我绕着她转了个慢圈。", "I circle her in a slow loop."),
("分开后我们各自漂走。", "Afterwards we each drift our own way."),
],
"pickup": [
("水里漂着的东西我收下了。", "I take whatever drifts by in the water."),
("我用触手把食物拨到嘴边。", "I sweep the food to my mouth with a tentacle."),
("这一块刚好落在我伞盖上。", "This piece landed right on my bell."),
("我把它卷住，慢慢吞下去。", "I curl around it and swallow slowly."),
("沉下来的碎屑也是吃的。", "Bits that sink down are food too."),
("我带着它漂了两格才吃。", "I drift two blocks with it before eating."),
("有鱼来抢，我把它包起来。", "A fish comes for it, so I wrap it up."),
("捡到东西让我高兴一整天。", "Finding something keeps me happy all day."),
("我嘴里塞着，触手还伸着。", "My mouth is full, my tentacles still reach."),
("吃完了我又变回透明。", "Once done eating I turn clear again."),
],
"target_acquire": [
("水里那点小动静被我发现了。", "I notice a small stirring in the water."),
("一群浮游的东西正好飘过来。", "A cloud of tiny drifting things comes by."),
("我把伞盖转向那股味道。", "I turn my bell toward that smell."),
("有小鱼擦过我的触手。", "A small fish grazes my tentacle."),
("这一小团东西够我吃一顿。", "That little cluster is a meal for me."),
("我慢慢沉下去靠近它。", "I sink slowly closer to it."),
("它没发现我，还在原地。", "It has not noticed me and stays put."),
("我选最近的那一团。", "I choose the nearest cluster."),
("水流把它送到我下面。", "The current delivers it right below me."),
("我张开了伞盖等它进来。", "I open my bell and wait for it."),
],
"targeting": [
("我的触手先垂下去探路。", "My tentacles hang down first to probe."),
("它离我不到半格了。", "It is less than half a block away."),
("我停住漂流，盯紧它。", "I stop drifting and fix on it."),
("它一动，我的伞盖就跟着转。", "When it moves my bell turns after it."),
("我在等它撞进触手范围。", "I wait for it to enter tentacle range."),
("水层很浅，它跑不掉。", "The layer is shallow, so it cannot escape."),
("我慢慢合拢，不让它察觉。", "I close in slowly so it never notices."),
("它越近，我的触手越收紧。", "The closer it comes, the tighter my tentacles."),
("我把它框在伞盖正下方。", "I frame it right under my bell."),
("好了，不用再等了。", "Good, there is no need to wait."),
],
"melee_attack": [
("触手一碰，它就不动了。", "One touch of my tentacle and it stops."),
("我把它裹住，慢慢收紧。", "I wrap it up and tighten slowly."),
("我的蜇刺很轻，但够用。", "My sting is light but it does the job."),
("它挣了两下就没力气了。", "It struggles twice and then goes limp."),
("它比我还小，一下就完。", "It is smaller than me, over in a moment."),
("我把它送到嘴下面。", "I move it under my mouth."),
("这一下没能伤到它太深。", "That hit did not cut very deep."),
("我收拢触手，吃得很慢。", "I gather my tentacles and eat slowly."),
("水里散开一点点血丝。", "A thin trace of red spreads in the water."),
("吃完我继续漂着。", "When I finish I keep drifting."),
],
"spawn": [
("冻洋里多了一只淡白的伞。", "A pale bell appears in the frozen ocean."),
("我一个人从冷水里浮起来。", "I rise alone out of the cold water."),
("这片海每次都只放我进来。", "This sea lets only me in each time."),
("我第一次张开伞盖，很慢。", "I open my bell for the first time, slowly."),
("冷水贴着我的身体，很舒服。", "Cold water hugs my body pleasantly."),
("我出生时身边没有别的同类。", "No kin of mine was near when I appeared."),
("冰下的光让我看清了水层。", "Light under the ice shows me the layers."),
("我漂进这片冷海就不走了。", "I drift into this cold sea and stay."),
("我只有三点生命，得小心。", "With three points of health I must be careful."),
("从今天起这里算我的水层。", "From today this water layer is mine."),
],
"hurt_generic": [
("我整只都缩了一下。", "My whole body shrinks for a moment."),
("疼得我伞盖紧紧合上。", "The pain makes my bell clamp shut."),
("我被打得往下沉了两格。", "The blow sinks me two blocks down."),
("我只有三点生命，别再来。", "I have only three health, so no more."),
("我的触手断了一根。", "One of my tentacles has torn off."),
("水里全是碎掉的气泡。", "The water fills with broken bubbles."),
("我慢慢往上飘，想躲开。", "I float up slowly, trying to escape."),
("这一下把我打懵了。", "That hit left me stunned."),
("我合起伞盖装成一块冰。", "I close my bell and pose as ice."),
("疼，但我不敢乱动。", "It hurts, but I dare not move wildly."),
],
"hurt_single": [
("热水烫得我整只发白。", "The hot water turns me pale all over."),
("我从水面摔下去，摔扁了。", "I fall from the surface and flatten out."),
("我本来就在水里，却也会淹。", "I live in water, yet I can still drown."),
("冲击把我推得散成几片。", "The blast pushes me apart into pieces."),
("一支箭穿过我透明的伞盖。", "An arrow passes through my clear bell."),
("奇怪的力气在我体内打转。", "Strange force swirls around inside me."),
("漂了太久，我饿得发软。", "I drifted too long and hunger makes me soft."),
("雷电下水里一片白光。", "Lightning turns the water white."),
("下面空得让我害怕。", "The emptiness below frightens me."),
],
}

OARFISH = {
"walk": [
("我长长一条横着穿过深海。", "I cross the deep sea in one long line."),
("我银白的身子像一条缎带。", "My silver body moves like a ribbon."),
("温水海沟的水压正好合适。", "The pressure in this warm trench suits me."),
("我慢慢摆，一次只前进一格。", "I sway slowly, one block at a time."),
("我的背鳍像波浪一样动。", "My dorsal fin ripples like a wave."),
("深海的蓝把我也染蓝了。", "The deep blue dyes me blue too."),
("我升到水层中间，又沉下去。", "I rise into the middle layer, then sink."),
("这条路线我游过很多次。", "I have swum this route many times."),
("我拐弯要拐好长一段。", "Turning takes me a long stretch of water."),
("我贴着海沟的岩壁往前走。", "I travel along the trench wall."),
("暖流把我轻轻往东推。", "The warm current nudges me eastward."),
("我游得不快，但不会停。", "I am not fast, but I never stop."),
("水越深，我的颜色越淡。", "The deeper I go, the paler I turn."),
("我从一片海沟游到另一片。", "I swim from one trench to another."),
],
"idle": [
("我悬在深水里，像根绳子。", "I hang in the deep water like a rope."),
("十二点生命让我不太慌张。", "Twelve points of health keep me calm."),
("我把身体拉直，节省力气。", "I straighten my body to save strength."),
("深海没有光，只有水声。", "There is no light here, only water sound."),
("我慢慢张开嘴，让水通过。", "I open my mouth and let water pass."),
("有只小东西在远处闪了一下。", "Something small glints far away."),
("我在水里停着，不急着走。", "I rest in the water, in no hurry."),
("我的鳍轻轻扇动保持位置。", "My fins flutter lightly to hold position."),
("这片深海安静得发闷。", "This deep sea is quiet enough to smother."),
("我把自己盘成半个圈。", "I curl myself into half a loop."),
("水压把我压得很稳。", "The water pressure holds me steady."),
("我在等猎物自己靠过来。", "I wait for prey to come to me."),
("深海的冷从骨里渗进来。", "The deep cold seeps into my bones."),
("我摆了一下尾，又不动了。", "I sway my tail once, then go still."),
],
"look_player": [
("你潜水下来，我停了很久。", "You dive down, and I freeze for a while."),
("我这条长身子在你面前打横。", "I turn my long body sideways before you."),
("深海里很少有人来。", "Few people ever come this deep."),
("你的灯把水照亮了一小块。", "Your lamp lights up one small patch."),
("我慢慢把脸转向光源。", "I slowly turn my face toward the light."),
("你是来找我的，还是路过？", "Did you come for me, or just pass?"),
("我的眼睛比你的手掌还大。", "My eye is wider than your palm."),
("我没有躲，只是绕开了。", "I do not hide, I simply go around."),
("你游得比我想的慢。", "You swim slower than I expected."),
("我盯着你的脚蹼看。", "I stare at your swim fins."),
],
"tempted": [
("你手上那点味道让我停下来。", "That smell on your hands makes me pause."),
("我慢慢转过来，身子还在漂。", "I turn while my body still drifts."),
("深海里几乎没有这样的香味。", "There is almost no scent like this down here."),
("我靠近时把嘴张得很小。", "I approach with my mouth barely open."),
("你要给我什么？我等着。", "What will you give me? I am waiting."),
("我绕着你转了一个大圈。", "I circle you in one wide loop."),
("我为这点东西多游了一趟。", "For that I made one extra pass."),
("我贴得很近，但没碰你。", "I come close but do not touch you."),
("味道淡了，我就慢下来。", "The smell fades, so I slow down."),
("别急，我这条身子转不快。", "Be patient, my long body turns slowly."),
],
"collide": [
("我整条撞上你的侧面。", "My whole length bumps into your side."),
("我的尾鳍扫到了你的腿。", "My tail fin sweeps across your leg."),
("这一下把水搅得很浑。", "That stirs the water into a muddy swirl."),
("我太长，转身总会碰到东西。", "I am too long to turn without bumping."),
("你被我一推，退了半格。", "My nudge pushes you back half a block."),
("我的头撞在岩壁上。", "My head knocks against the rock wall."),
("我们两个都在深水里让路。", "We both give way in the deep water."),
("我缠在你的绳子上了一下。", "I catch on your rope for a moment."),
("撞完我摆尾道了个歉。", "After the bump I flick my tail in apology."),
("水花没有，只有闷闷一声。", "No splash, only one dull thud."),
],
"mate": [
("另一条皇带鱼从深处上来了。", "Another oarfish rises from the depths."),
("我们两条并排，像两条缎带。", "Side by side we look like two ribbons."),
("我慢慢绕着她转。", "I circle her slowly."),
("她的银光比我的更亮。", "Her silver shine is brighter than mine."),
("我们把身体靠在一起，很长。", "We press our long bodies together."),
("深海的暖流帮我们聚到一处。", "The warm deep current brings us together."),
("她说这一窝只添两条。", "She says this brood adds only two."),
("我用吻部碰她的头侧。", "I touch her head with my snout."),
("分开之后各游各的深水。", "Afterwards we each swim our own depth."),
("她的尾巴绕了我一圈。", "Her tail curls once around me."),
],
"pickup": [
("沉到海沟底的东西我捡了。", "I collect whatever sinks to the trench floor."),
("我用嘴把食物从沙里拱出来。", "I root the food out of the sand."),
("这一块卡在石头缝里，我叼出来。", "This piece is stuck, so I pull it out."),
("我不挑，漂来的都吃。", "I am not picky and eat what drifts."),
("我把食物含在嘴里慢慢咽。", "I hold the food and swallow slowly."),
("捡起来比追一条鱼省力。", "Picking it up is easier than chasing fish."),
("我护着它游到石壁后面。", "I guard it and swim behind the rock."),
("有鲨鱼在附近，我加快了。", "A shark is nearby, so I hurry."),
("吃完我在水底留了道印。", "After eating I leave a mark on the floor."),
("这一口够我撑一阵子。", "This bite will last me a while."),
],
"target_acquire": [
("水里有团东西在慢慢动。", "Something in the water is moving slowly."),
("我的眼睛在暗处也能用。", "My eyes still work in the dark."),
("那只小鱼离我两格远。", "That small fish is two blocks away."),
("我把头对准了它的方向。", "I point my head toward it."),
("它比我小太多了。", "It is far smaller than I am."),
("我慢慢沉下去，不惊动它。", "I sink slowly so I do not startle it."),
("它的影子落在我下面的岩上。", "Its shadow falls on the rock below."),
("我选定它了，不再看别的。", "I pick it and look at nothing else."),
("我张开嘴，让水流进来。", "I open my mouth and let water in."),
("深海的猎物总是很瘦。", "Prey in the deep sea is always thin."),
],
"targeting": [
("我拉长身子靠近它。", "I stretch my body out toward it."),
("它躲到岩壁的凹处。", "It slips into a hollow in the wall."),
("我在外面等着，不动。", "I wait outside without moving."),
("我的长嘴对着那道缝。", "My long snout aims at that gap."),
("距离还剩一格半。", "One and a half blocks left between us."),
("它一出来我就动。", "The moment it comes out, I move."),
("我把身体放低，贴住海沟底。", "I flatten down against the trench floor."),
("它没看见我这条长影。", "It does not see my long shadow."),
("我把嘴张到最开。", "I open my mouth as wide as I can."),
("水流正好把它推向我。", "The current pushes it right toward me."),
],
"melee_attack": [
("我一口把它吞了进去。", "I swallow it in one gulp."),
("它在我嘴里还在挣。", "It is still struggling inside my mouth."),
("我的牙不大，但够抓住。", "My teeth are small but they hold."),
("这一下就让它软了。", "That one hit makes it go limp."),
("我摇了两下头把它咽下。", "I shake my head twice and swallow."),
("血在水里散成一条细线。", "Blood spreads in a thin line through water."),
("它太小吃不饱。", "It is too small to fill me."),
("我又张嘴等下一个。", "I open my mouth again for the next."),
("咬的时候我整个身子都绷紧。", "My whole body tightens as I bite."),
("打完了也没人跟我抢。", "Afterwards nobody comes to take it."),
],
"spawn": [
("我从深水沟里慢慢升上来。", "I rise slowly out of the deep trench."),
("这次只有我和另一条。", "This time there is only me and one other."),
("深海的压力一上来就裹住我。", "Deep pressure wraps around me at once."),
("我出生时已经很长了。", "I was already long when I appeared."),
("温水海沟是我睁眼的地方。", "The warm trench is where I first opened my eyes."),
("我慢慢摆尾，试了试力气。", "I sway my tail and test my strength."),
("十二点生命让我活得稳一些。", "Twelve health points keep me a bit steadier."),
("附近没有鲨鱼，运气不错。", "No sharks nearby, which is good luck."),
("我从这里开始往下走。", "I start heading downward from here."),
("深海多了一条长长的影子。", "The deep sea gains one long shadow."),
],
"hurt_generic": [
("疼得我整条都扭起来。", "The pain twists my whole long body."),
("我的侧线被打得发麻。", "My lateral line goes numb from the blow."),
("我立刻往下沉，躲进暗处。", "I sink at once into the dark."),
("十二点生命，还剩一些。", "Twelve points, and some are still left."),
("我的银鳞掉了几片。", "A few silver scales came loose."),
("这一下让我不敢再靠近。", "That blow keeps me from coming closer."),
("我摆尾想甩掉疼的地方。", "I flick my tail to shake off the ache."),
("伤口在水里凉凉的。", "The wound feels cold in the water."),
("我游得比刚才快。", "I swim faster than I did before."),
("再来两次我就撑不住。", "Two more of those and I am done."),
],
"hurt_single": [
("水面上方的火把水烤热了。", "Fire above the surface heats the water."),
("我摔在岩上，身子还在弹。", "I hit the rock and my body still bounces."),
("我在水里，可还是呛到了。", "I am in water, yet I still choke."),
("一声闷响把我推出了水沟。", "A dull blast pushes me out of the trench."),
("一根矛扎进我的背鳍。", "A spear pierces my dorsal fin."),
("奇怪的咒力顺着鳞片走。", "Strange magic runs along my scales."),
("饿久了，我游得像根木头。", "Hungry this long, I swim like driftwood."),
("一道白光穿过整片深水。", "A white flash cuts through the deep water."),
("下面是无底的虚空，我怕。", "Below lies bottomless void, and I fear it."),
],
}

SUNFISH = {
"walk": [
("我这么大一块，游起来很慢。", "Being this large, I swim very slowly."),
("我扇着两侧的鳍往前推。", "I flap both side fins to push ahead."),
("深海的暖水托着我这身重量。", "Warm deep water carries my heavy body."),
("我拐个大弯要花很久。", "A wide turn takes me a long time."),
("我像个大圆盘慢慢转。", "I turn slowly like a big round plate."),
("我贴着水层边缘游。", "I swim along the edge of the layer."),
("我的尾巴几乎不摆，只靠鳍。", "I barely use my tail, mostly my fins."),
("水流推我，我懒得顶回去。", "The current pushes and I do not resist."),
("我从深水慢慢升到中层。", "I climb slowly from deep water to mid."),
("我这身子一动就很显眼。", "My body is very noticeable when I move."),
("深温带海洋是我的老路。", "The deep temperate ocean is my old route."),
("我慢慢横过一片海沟。", "I cross a trench at a slow pace."),
("我游过的地方水会晃一下。", "The water sways a little where I pass."),
("我不赶路，反正没人等我。", "I am not rushing, nobody waits for me."),
],
"idle": [
("我停在水里，像一块石头。", "I hang in the water like a stone."),
("十六点生命让我很踏实。", "Sixteen points of health make me secure."),
("我张开嘴，等水母漂进来。", "I open my mouth for drifting jellyfish."),
("我的鳍慢慢摆，只为了不沉。", "My fins move just enough to stay up."),
("深海的暖让我昏昏欲睡。", "The warmth down here makes me drowsy."),
("我身上有几道旧的白痕。", "A few old white scars cross my body."),
("我在水层里慢慢翻了个身。", "I roll over slowly in the water layer."),
("有只水母在远处发亮。", "A jellyfish glows in the distance."),
("我不动的时候最像一块礁。", "Still, I look most like a reef rock."),
("头顶的光很远，照不到我。", "The light above is far and misses me."),
("我把身体侧过来晒太阳。", "I tilt my body to catch the sun."),
("水压压在我背上，很稳。", "Pressure rests steady on my back."),
("我在等饥饿自己上来。", "I wait for hunger to come to me."),
("这一层的水温刚刚好。", "The water temperature in this layer is perfect."),
],
"look_player": [
("你这么小，我差点没看见。", "You are so small I almost missed you."),
("我转过来，整块身子挡住光。", "I turn and my whole body blocks the light."),
("你在水里显得很轻。", "You look very light in the water."),
("我盯着你手里的东西。", "I stare at what you are holding."),
("你退后了，我不追。", "You step back, and I do not follow."),
("我的眼睛长在身体两侧。", "My eyes sit on either side of me."),
("我慢慢往上浮，看着你。", "I float up slowly and watch you."),
("你是不是来捕我的？", "Are you here to hunt me?"),
("我这条大影子盖住了你。", "My big shadow covers you completely."),
("你的灯在我身上照出一片白。", "Your lamp makes a white patch on me."),
],
"tempted": [
("那点气味从你手里飘出来。", "That scent drifts out of your hands."),
("是水母的味道吗？我来了。", "Is that jellyfish smell? I am coming."),
("我慢慢往你那边挪。", "I edge slowly in your direction."),
("我张着嘴等它落进来。", "I hold my mouth open for it to fall in."),
("我这么大，靠近要花点时间。", "Being this big, getting close takes time."),
("味道不浓，但我闻到了。", "The smell is weak, but I caught it."),
("我绕着你转，水都被带动。", "I circle you and the water turns with me."),
("你别动，我马上就够到。", "Hold still, I am almost within reach."),
("这点东西不够我塞牙。", "That much will not even fill a gap."),
("味道散了，我也慢下来。", "The scent fades and I slow down."),
],
"collide": [
("我一撞，你退了半步。", "I bump you and you slide back."),
("我的重量让你推不动我。", "My weight means you cannot push me."),
("我靠过来时水都变了形。", "The water bends when I lean in."),
("你我撞上，只有你晃。", "We collide and only you wobble."),
("我撞在岩壁上，岩壁闷响。", "I hit the rock wall and it thuds."),
("你被我挤到一边去了。", "You get squeezed off to one side."),
("我这身板从不被撞开。", "This body of mine is never knocked aside."),
("我慢慢转过身，擦过你的肩。", "I turn slowly and graze your shoulder."),
("我道歉，但我的声音很闷。", "I apologize, but my voice sounds muffled."),
("撞完我们各走各的。", "After the bump we go our own ways."),
],
"mate": [
("另一条大影子从深处升上来。", "Another big shadow rises from the deep."),
("我们并排慢慢往上游。", "We swim up side by side, slowly."),
("我们两条就能占满一片水。", "The two of us fill one stretch of water."),
("我侧身贴着她，很稳。", "I press my side to hers, steady."),
("深海的暖流把我们推到一处。", "The warm deep current pushes us together."),
("这一窝最多只添两条。", "This brood adds at most two more."),
("她转得比我快一点。", "She turns a little faster than I do."),
("我慢慢绕着她游了一圈。", "I circle her once at a slow pace."),
("分开后我们各占一层水。", "Afterwards we each take a water layer."),
("她的影子叠在我的上面。", "Her shadow lies across mine."),
],
"pickup": [
("沉下来的东西我接住了。", "I catch what sinks down toward me."),
("我用嘴把它顶住慢慢吞。", "I pin it with my mouth and swallow."),
("这块食物在我嘴边打转。", "This food circles right by my mouth."),
("我不动，等它自己飘进来。", "I stay still and let it drift in."),
("沉到海底的我也去捡。", "I also pick up what reaches the bottom."),
("我含在嘴里，像含着石子。", "I hold it like a pebble in my mouth."),
("这条水母整只都归我了。", "This whole jellyfish belongs to me."),
("吃完我在水里慢慢转身。", "After eating I turn slowly in the water."),
("捡一口比追半天省事。", "One easy scrap beats a long chase."),
("我嘴里还有一点没咽下。", "A little is still stuck in my mouth."),
],
"target_acquire": [
("一只水母在那边慢慢漂。", "A jellyfish is drifting over there."),
("我看见它发亮的伞盖。", "I see its glowing bell."),
("它比我小，正好一口。", "It is smaller than me, a single bite."),
("我转向它那个方向。", "I turn toward its direction."),
("我张开嘴，把水一起吸。", "I open my mouth and draw water in."),
("它还没发现我在附近。", "It has not noticed me nearby yet."),
("我慢慢升到它的下面。", "I rise slowly beneath it."),
("这一只够我吃一阵。", "This one will feed me for a while."),
("我锁定了那点白光。", "I fix on that small white glow."),
("别的我都不看了。", "I look at nothing else now."),
],
"targeting": [
("我贴近了，水开始动。", "I close in and the water stirs."),
("它往下沉了一点。", "It has sunk a little deeper."),
("我把嘴对准它的伞盖。", "I aim my mouth at its bell."),
("我的身体挡住了它的退路。", "My body blocks the way it could flee."),
("它碰到我的嘴唇了。", "It has touched my lips."),
("我慢慢合上嘴，不急。", "I close my mouth slowly, unhurried."),
("它在我嘴里还在漂。", "It is still drifting inside my mouth."),
("我把它往喉咙里送。", "I move it back toward my throat."),
("这一下它跑不掉了。", "Now it cannot get away."),
("我停住，开始咽。", "I stop and begin to swallow."),
],
"melee_attack": [
("我一口把它整个吞下。", "I swallow it whole in one go."),
("我的嘴一下合上，水都挤出来。", "My mouth shuts and water squeezes out."),
("它在我喉咙里还动了一下。", "It moves once inside my throat."),
("这一下没什么声音。", "The whole thing makes almost no sound."),
("我咬得不狠，只是吞。", "I do not bite hard, I only swallow."),
("水母的软在我嘴里散开。", "The jellyfish's softness spreads in my mouth."),
("我又张开嘴等着。", "I open my mouth again and wait."),
("这点东西不够我饱。", "This is not enough to fill me."),
("我慢慢摆鳍，消化它。", "I sway my fins slowly to digest it."),
("吃完我浮在原地。", "After eating I float in place."),
],
"spawn": [
("我从深海的暖水里浮出来。", "I surface from the warm deep water."),
("这次只我们两个来了。", "Only the two of us showed up this time."),
("我一生下来就占了半片水。", "I took half the water at birth."),
("十六点生命让我不慌。", "Sixteen points of health keep me calm."),
("深温带海洋的水包住我。", "Deep temperate water wraps around me."),
("我慢慢张开两侧的鳍。", "I slowly spread the fins on both sides."),
("附近有条鲨鱼，我先沉下去。", "A shark is near, so I sink first."),
("我这身子在水里很显眼。", "This body of mine stands out in water."),
("从今天起这层水归我。", "From now on this layer belongs to me."),
("我慢慢开始游第一段。", "I slowly begin my first stretch of swimming."),
],
"hurt_generic": [
("疼，可我没被推开。", "It hurts, but I am not pushed back."),
("我的厚皮挡了不少。", "My thick hide took most of it."),
("我整块身子晃了一下。", "My whole body rocks once."),
("十六点生命还撑得住。", "Sixteen points of health still hold."),
("我往下沉，躲开下一击。", "I sink away from the next blow."),
("水里散开一点血雾。", "A little blood mist spreads in the water."),
("我慢慢转身看是谁。", "I turn slowly to see who did that."),
("这点疼我受得住。", "I can take this much pain."),
("我的鳍还在稳稳地扇。", "My fins are still beating steadily."),
("再来几下我也不会退。", "A few more hits will not push me off."),
],
"hurt_single": [
("水面的火把这一带烤暖了。", "Fire at the surface warms this whole area."),
("我摔下去，水被砸得炸开。", "I fall and the water bursts apart."),
("我在水里，可也会喘不上气。", "I live in water, yet I can lose breath."),
("爆炸把我整块掀起来。", "The blast lifts my whole body up."),
("一支箭扎进我的厚皮。", "An arrow sticks in my thick hide."),
("咒力在我身体里乱撞。", "Magic knocks around inside my body."),
("饿了很久，我浮得越来越低。", "Starving so long, I float lower and lower."),
("雷打在水面，我全身一麻。", "Lightning hits the surface and numbs me."),
("下面的空让我不敢再沉。", "The void below stops me from sinking further."),
],
}

DATA = {
"hybrid_aquatic:needlefish": NEEDLEFISH,
"hybrid_aquatic:nomura_jellyfish": JELLYFISH,
"hybrid_aquatic:oarfish": OARFISH,
"hybrid_aquatic:ocean_sunfish": SUNFISH,
}


def check_zh(text):
    n = len(re.sub(r"[，。？！、；：…“”‘’（）]", "", text))
    return 6 <= n <= 20


def check_en(text):
    return 4 <= len(text.split()) <= 14


def main():
    problems = []
    out = {"batch": "u0396", "mobs": []}
    plan = {m["mob_id"]: m for m in PLAN}
    for mob in PLAN:
        mid = mob["mob_id"]
        data = DATA[mid]
        w = mob["weights"]
        scenarios = {}
        for key in ORDER:
            need = 10 + clamp_extra(w.get(key, 1.0))
            pairs = data[key]
            if len(pairs) < need:
                problems.append(f"{mid}.{key}: need {need}, have {len(pairs)}")
                continue
            scenarios[key] = [{"zh": zh, "en": en} for zh, en in pairs[:need]]
            if len(pairs) > need:
                problems.append(f"{mid}.{key}: extra pairs {len(pairs) - need}")
        hurt = {"generic": [{"zh": zh, "en": en} for zh, en in data["hurt_generic"][:10]]}
        for dmg, (zh, en) in zip(DAMAGE, data["hurt_single"]):
            hurt[dmg] = [{"zh": zh, "en": en}]
        scenarios["hurt"] = hurt
        out["mobs"].append({"mob_id": mid, "scenarios": scenarios})
        for key, val in scenarios.items():
            groups = val.values() if key == "hurt" else [val]
            for group in groups:
                for line in group:
                    if not check_zh(line["zh"]):
                        problems.append(f"{mid}.{key} zh [{len(re.sub(r'[，。？！、；：…“”‘’（）]', '', line['zh']))}] {line['zh']}")
                    if not check_en(line["en"]):
                        problems.append(f"{mid}.{key} en [{len(line['en'].split())}] {line['en']}")

    zh_lines = [line["zh"] for mob in out["mobs"] for key, val in mob["scenarios"].items()
                for group in (val.values() if key == "hurt" else [val]) for line in group]
    dupes = {x for x in zh_lines if zh_lines.count(x) > 1}
    if dupes:
        problems.append(f"duplicate zh: {dupes}")
    en_lines = [line["en"] for mob in out["mobs"] for key, val in mob["scenarios"].items()
                for group in (val.values() if key == "hurt" else [val]) for line in group]
    endupes = {x for x in en_lines if en_lines.count(x) > 1}
    if endupes:
        problems.append(f"duplicate en: {endupes}")

    if problems:
        print("\n".join(problems))
        print(f"PROBLEMS {len(problems)}")
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(len(group) for mob in out["mobs"] for key, val in mob["scenarios"].items()
                for group in (val.values() if key == "hurt" else [val]))
    print(f"u0396 ok {len(out['mobs'])} mobs {total} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
