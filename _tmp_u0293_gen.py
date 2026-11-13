# -*- coding: utf-8 -*-
import json, re, sys

def L(s):
    out = []
    for line in s.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        zh, en = [x.strip() for x in line.split("|")]
        out.append({"zh": zh, "en": en})
    return out

PUR = {}
PUR["walk"] = L("""
我把尾巴裹紧腰身，走得更宽。|I wrap my tail around my waist and walk wider.
肚子下的肉一晃一晃。|The fat under my belly sways with each step.
虎斑纹在草里像一道影子。|My tabby stripes move like a shadow in the grass.
我踩着地埂，一步不漏。|I keep to the ridge and miss no step.
我尽量走得比实际更大。|I try to look bigger than I am.
尾巴竖起来，像多了一条腿。|My tail stands up like an extra leg.
草叶顺着我的肚子倒下去。|The grass falls flat under my belly.
我侧身走，让身子显宽。|I walk sideways to show my width.
一步一步，我不急。|Step by step, I am in no hurry.
我的爪子踩得很轻。|My paws press the ground very lightly.
我绕过石头，肚子擦过去。|I go around the stone and my belly brushes it.
我拖着尾巴扫过草地。|I drag my tail across the meadow.
""")
PUR["idle"] = L("""
我把尾巴裹在身前保暖。|I wrap my tail in front of me for warmth.
我坐着，看起来像一堆毛。|Sitting, I look like a heap of fur.
虎斑纹随呼吸起伏。|My tabby stripes rise and fall with my breath.
我眯着眼，懒得动。|I squint and cannot be bothered to move.
尾巴尖一抽一抽的。|The tip of my tail twitches now and then.
我舔前爪，慢慢来。|I lick my front paws, slowly.
我数草叶，数到第七根就乱了。|I count blades and lose track at seven.
一只虫飞过，我没追。|A bug flies past; I do not chase it.
有一只耳朵朝声音转过去。|One ear swivels toward the sound.
我打了个哈欠，露出尖牙。|I yawn and show my pointed teeth.
太阳晒得我的毛发烫。|The sun makes my fur hot.
我用尾巴盖住自己的脚。|I cover my own feet with my tail.
我听见远处有什么在响。|I hear something moving far away.
我换了个姿势，还是一样懒。|I shift position and stay just as lazy.
""")
PUR["look_player"] = L("""
你的视线落在我的虎斑上。|Your gaze is resting on my tabby coat.
你把我看得这么仔细？|You are looking at me very closely.
我这身虎斑没什么好看。|There is nothing special about my tabby coat.
别伸手，我会用尾巴抽你。|Do not reach out; my tail will hit you.
你是来量我有多宽的吗？|Are you here to measure how wide I am?
我尾巴裹起来，你就怕了？|I wrap my tail up; does that scare you?
你的影子挡了我的太阳。|Your shadow is blocking my sun.
那个圆球，我在草地上见过。|I have seen that round ball in this grass.
看够了吗，我要坐下了。|Seen enough? I am sitting down.
你站得那么高，我懒得抬头。|Standing so tall, and I am too lazy to look up.
我的眼睛在草里发亮。|My eyes shine in the grass.
你退后两步，我就满意了。|Take two steps back and I am satisfied.
我这样显得很大，是吧？|I look big like this, do I not?
你笑什么，我本来就这么宽。|What are you laughing at? I am this wide.
""")
PUR["tempted"] = L("""
有吃的？先让我闻闻。|Food? Let me smell it first.
你把东西举高，我够不到。|You hold it high, out of my reach.
我尾巴先伸过去探一探。|My tail reaches out to test it first.
我不为食物跑，太远了。|I will not run for food; too far.
你手里那点不够我塞牙。|That little bit will not fill my teeth.
我拖着肚子，一步一步挨近。|I drag my belly forward, one step at a time.
闻起来不错，我考虑一下。|It smells good; I will consider it.
我把尾巴松开了一点。|I loosen my tail a little.
你晃它，我就跟着晃头。|You wiggle it; my head wiggles too.
这算诱饵吗？我早知道。|Is this bait? I knew already.
""")
PUR["collide"] = L("""
我撞上你了，是你太窄。|I bumped you; you are too narrow.
我这么宽，路当然不够。|I am this wide; of course the path is too small.
我的尾巴扫到你的腿。|My tail swept your leg.
抱歉，我转身很慢。|Sorry, I turn very slowly.
你踩到我的肚子了。|You stepped on my belly.
草地这么窄，怪谁。|The meadow is this narrow; whose fault?
我侧过身，还是挤到了你。|I turned sideways and still crowded you.
撞一下，我身上全是肉。|One bump, and I am all padding.
你退半步，我们都能走。|Take half a step back and we both pass.
我撞你没事，你撞我就有事。|I bump you, fine; you bump me, not fine.
""")
PUR["mate"] = L("""
我竖起尾巴，绕你三圈。|I raise my tail and circle you three times.
我把自己裹成一个球。|I wrap myself into a ball.
你闻起来不像同类。|You do not smell like one of my kind.
我的虎斑纹比平时亮。|My tabby stripes are brighter than usual.
草地够大，我们慢慢来。|The meadow is large; let us take our time.
我把最肥的一面朝你。|I turn my plumpest side toward you.
尾巴缠住尾巴，就这样。|Tail around tail, just like that.
你别急着走，坐一会儿。|Do not hurry off; sit a while.
我的呼噜声很响。|My purring is very loud.
今年冬天我有人挤了。|This winter I have someone to crowd against.
""")
PUR["pickup"] = L("""
我用牙齿轻轻咬住它。|I take it gently between my teeth.
这么小的东西我懒得捡。|I cannot be bothered with something this small.
我用肉垫把它推到草里。|I shove it into the grass with my pad.
我的爪子太大，抓不住。|My paws are too big to grip it.
尾巴一卷，东西就来了。|One curl of my tail brings it over.
它不是吃的，我不要。|It is not food; I do not want it.
我用肉垫碰了碰它。|I touch it with my soft pad.
掉在地上就是我的了。|If it falls on the ground, it is mine.
我叼起来又放下了。|I pick it up and put it down again.
这点重量，我尾巴都嫌轻。|This weight is light even for my tail.
""")
PUR["target_acquire"] = L("""
草里有动静，我压低身子。|Something moves in the grass; I crouch low.
我的尾巴先绷紧了。|My tail goes stiff first.
那东西我一口就能解决。|I could finish that in one bite.
我慢慢靠近，不发出声音。|I creep closer without a sound.
它的影子在动，我看见了。|Its shadow moved; I saw it.
这场追逐我不会跑太久。|I will not run long for this chase.
耳朵朝前，眼睛眯起。|Ears forward, eyes narrowed.
我把自己撑大给它看。|I puff myself up at it.
我在这片草地升到四十级。|I leveled to forty in this very meadow.
你一动手我就扑。|Move first and I pounce.
""")
PUR["targeting"] = L("""
我绕着你转，尾巴翘起。|I circle you with my tail raised.
我不喊，我只盯着。|I do not shout; I only stare.
你挪一寸，我就跟上一寸。|You shift an inch; I follow an inch.
我的呼噜声变成低吼。|My purr drops into a growl.
我让影子先到你脚边。|I let my shadow reach your feet first.
别把你的背对着我。|Do not turn your back on me.
爪子从肉垫里露了尖。|Claws show their tips from my pads.
你跑不过我这四条腿。|You cannot outrun these four legs.
我在等你先犯错。|I am waiting for your first mistake.
这一扑我练过很多次。|I have practiced this pounce many times.
""")
PUR["melee_attack"] = L("""
前爪拍下去，草都塌了。|My paw slams down and the grass flattens.
我整个身子的分量压上来。|My full weight comes down on you.
尾巴抽在你腿上。|My tail whips across your legs.
我咬住就不松。|Once I bite, I do not let go.
虎斑的爪子藏在肉里。|Tabby claws hide in my pads.
我一掌能推倒小树。|One swipe of mine can push over a sapling.
你被我的重量压住了。|My weight has you pinned.
我抓完就退回去坐着。|After the swipe I sit back down.
我的牙齿不尖，但够用。|My teeth are not sharp, but they work.
别以为胖就慢。|Do not think fat means slow.
""")
PUR["spawn"] = L("""
我从草里站起来，草叶乱飞。|I stand up from the grass, blades flying.
四十级的草地，我来了。|Level forty grass, here I come.
我抖了抖虎斑的毛。|I shake out my tabby fur.
我把尾巴裹好，先看四周。|I wrap my tail and look around first.
这片草地我先占下了。|I have claimed this meadow first.
我踩倒一片草才站稳。|I flatten a patch of grass to stand.
我从睡里醒来，先伸了伸腰。|I wake from sleep and stretch first.
阳光照在我的背上。|Sunlight lands on my back.
我从高草里露出脑袋。|My head rises out of the tall grass.
我在这里等很久了。|I have waited here a long while.
我把自己撑得很大。|I make myself look very large.
草地的味道，我认得。|I know the smell of this meadow.
""")
PUR["hurt"] = {
"generic": L("""
我的尾巴被打散了。|My tail came unwrapped.
别碰我的肚子。|Do not touch my belly.
虎斑的毛掉了一撮。|A tuft of tabby fur came off.
我被打得坐到地上。|The hit sat me down on the ground.
我没想到这一下这么疼。|I did not expect it to hurt this much.
我的呼噜声断了。|My purring stopped short.
我缩起来，变成一团。|I curl into a ball.
我把两只耳朵压到脑后。|I pin both ears back against my head.
我退了两步，还在盯你。|I back off two steps, still watching you.
草叶扎进我的伤口。|Grass blades poke into my wound.
"""),
"fire": L("毛被烧焦了一块。|A patch of my fur is scorched."),
"fall": L("从高处摔下来，肚子先着地。|I hit the ground belly first."),
"drown": L("我不太会游，灌了水。|I am a poor swimmer and swallowed water."),
"explosion": L("冲击把我掀翻了。|The blast rolled me over."),
"projectile": L("有东西扎进我的背。|Something struck my back."),
"magic": L("奇怪的力量按住了我。|Some strange force holds me down."),
"starvation": L("空着肚子，我一步也不想走。|Empty, I refuse to take another step."),
"lightning": L("雷打过来，我的毛全竖了。|Lightning struck and all my fur stands up."),
"void": L("我掉下去了，什么也抓不住。|I am falling with nothing to grab."),
}

PYR = {}
PYR["walk"] = L("""
我踏过草地，鬃毛在烧。|I cross the meadow with my mane burning.
每走一步，热气就散开。|Every step gives off a wave of heat.
我是这群里鬃毛最大的。|Mine is the largest mane in this pride.
我的爪子踩出焦痕。|My paws leave scorch marks.
我走在最前面，后面跟着。|I walk in front; the others follow.
火光把我的影子拉长。|The firelight stretches my shadow.
我走得不快，但很稳。|I do not walk fast, but I walk steady.
草在我脚边卷起来。|The grass curls beside my feet.
我抬头，看看自己的地盘。|I lift my head and survey my land.
鬃毛热得我不敢低头。|My mane is too hot for me to lower my head.
我的尾巴像一束火把。|My tail is like a torch.
我一步一步巡视边界。|I patrol the border step by step.
""")
PYR["idle"] = L("""
我坐着，鬃毛还在亮。|I sit still and my mane keeps glowing.
火从我鬃毛尖上冒出来。|Flame rises from the tips of my mane.
我舔爪子，火苗绕着。|I lick my paws with flames curling around.
我眯眼，让鬃毛慢慢熄。|I squint and let my mane settle.
风一吹，火苗都朝一边。|The wind bends every flame the same way.
我张嘴，热气从牙缝里出来。|I open my mouth and heat escapes my teeth.
我的鬃毛就是我的王冠。|My mane is my crown.
我听见远处有狮子在叫。|I hear a lion call far off.
我抖抖鬃毛，火星四溅。|I shake my mane and sparks fly.
谁在我的草地上生火。|Someone has lit a fire on my grass.
我坐得很正，像在等臣民。|I sit straight as if awaiting subjects.
我不睡，我守着。|I do not sleep; I keep watch.
太阳和我的鬃毛一样烫。|The sun is as hot as my mane.
我想想今天该管什么。|I think about what needs ordering today.
""")
PYR["look_player"] = L("""
你站住，先看我的鬃毛。|Halt and look at my mane.
你在衡量我的火有多大？|Are you measuring how big my fire is?
鬃毛小的雄狮不会站这么近。|A small-maned male would not stand this close.
我允许你抬头。|I permit you to look up.
你的眼睛被我的火晃到了。|My fire is dazzling your eyes.
你手里那个球，我看得懂。|I understand that ball in your hand.
别用那种眼神看我的鬃毛。|Do not look at my mane that way.
我是这里的首领，记住了。|I lead here. Remember that.
你退下，我还要巡视。|Withdraw; I still have a patrol.
你在发抖，是因为热吗？|Are you trembling from the heat?
我的鬃毛比你的火把亮。|My mane outshines your torch.
你靠近一步，火就高一寸。|One step closer and the flame rises.
你身上没有火的味道。|You carry no smell of fire.
看完了就低下头。|When you have looked, lower your head.
""")
PYR["tempted"] = L("""
生肉？放在地上。|Raw meat? Put it on the ground.
我不用你喂，我自己猎。|I do not need feeding; I hunt.
你手里的肉太小了。|The meat in your hand is too small.
我靠近，你得先退开。|As I approach, you move back first.
熟的不吃，我要生的。|Not cooked; I want it raw.
这点东西不够我一口。|That is not one mouthful for me.
我鬃毛上的火会烤熟它。|The fire on my mane will cook it.
你举高些，我懒得弯腰。|Hold it higher; I will not bend down.
我低头嗅了嗅这块肉。|I lower my head and sniff the meat.
你给的东西，我得先试毒。|I must test your gift for poison.
""")
PYR["collide"] = L("""
你撞到我的鬃毛了。|You bumped into my mane.
我这么烫，你还敢挤过来。|I am this hot, and you still crowd me.
火苗扫到你的袖子。|A flame licked your sleeve.
往旁边站，别挡我的路。|Stand aside and do not block my path.
你的靴子压住我的尾尖。|Your boot is pressing on my tail tip.
我的肩膀撞得你退后。|My shoulder knocked you back a step.
这条路容不下我们两个。|This path will not hold us both.
抱歉，我的鬃毛太宽。|Sorry, my mane is too wide.
我们别靠这么近。|Let us not stand this close.
你再挤，火就烧到你。|Crowd me again and the fire reaches you.
""")
PYR["mate"] = L("""
我的鬃毛是这群最大的。|My mane is the largest in the pride.
你愿意站到我的火光里吗？|Will you stand in my firelight?
雌狮看的是鬃毛，不是话。|Lionesses judge the mane, not words.
我绕着你走，火跟着转。|I circle you; the fire circles too.
我把最亮的一侧朝向你。|I turn my brightest side toward you.
别怕烫，靠过来。|Do not fear the heat; come closer.
首领的位置，我留了一半。|I saved half the leader's place.
我低吼，草地都在震。|I growl low and the meadow shakes.
我们并肩坐着，火连成一片。|Side by side, our fires merge.
这一群以后有两个影子。|This pride will have two shadows.
""")
PYR["pickup"] = L("""
我用嘴叼，爪子太烫。|I carry it in my mouth; my claws are too hot.
我把东西叼给你。|I carry it over to you.
这玩意儿会被我的火烤坏。|My fire will ruin this thing.
我不捡，地上的东西不配。|I do not pick up things from the ground.
我用爪子拨了一下。|I nudge it with one claw.
肉掉地上，还是我的。|Meat dropped on the ground is still mine.
我叼着它，火苗绕开。|I hold it and the flames part around it.
你掉了什么？我看看。|What did you drop? Let me see.
这点重量我嫌轻。|This is too light to bother with.
我叼回去给雌狮。|I carry it back to the lionesses.
""")
PYR["target_acquire"] = L("""
草地边上有陌生的脚印。|There are unfamiliar prints at the meadow's edge.
我的鬃毛一下子旺了。|My mane flares up at once.
我压低头，火往前烧。|I lower my head and the fire pushes forward.
那影子跑得不慢。|That shadow runs quickly.
我不用追，火会拦住它。|I need not chase; fire will cut it off.
我的爪子已经抓进土里。|My claws are already in the dirt.
谁敢在我的地盘抬头。|Who dares raise their head on my land?
我吼一声，草都压低。|I roar once and the grass lies flat.
我数着它的步数。|I count its footsteps.
它退，我就知道它怕了。|It backs off; now I know it fears me.
我先让它跑十步。|I let it run ten steps first.
这片草地只认一个首领。|This meadow knows only one leader.
我已经闻到它的味道。|I have its scent already.
火沿草线烧过去了。|The fire runs along the grass line.
""")
PYR["targeting"] = L("""
我正对你，鬃毛全开。|I face you with my whole mane ablaze.
你退到哪儿，火跟到哪儿。|Wherever you retreat, the fire follows.
我不叫，我在蓄火。|I am silent; I am gathering fire.
你的影子已经被我圈住。|My circle has closed on your shadow.
我用爪子在地上划线。|I draw a line in the dirt with my claw.
线那边不是我允许的地方。|Beyond that line is not permitted.
你听见我的呼吸了吗。|Do you hear my breathing?
每口呼吸都带火星。|Every breath carries sparks.
我在等你的第一步。|I am waiting for your first step.
这一扑会烧到你身后。|This pounce will burn behind you.
你身后也是我的草地。|The grass behind you is mine too.
眼睛留在我鬃毛上。|Keep your eyes on my mane.
我鬃毛里的火不会灭。|The fire in my mane does not go out.
你只剩转身的机会。|You have only one turn left.
""")
PYR["melee_attack"] = L("""
我的爪子带着火拍下。|My burning claw comes down.
咬住，再甩出去。|I bite, then throw you aside.
鬃毛的火先扑到你脸上。|My mane fire hits your face first.
我整个身子压过去。|I put my whole weight into the charge.
爪子落处，草烧成灰。|Where my claw lands, grass turns to ash.
我不止一下。|I do not stop at one blow.
你被我的热气逼得后退。|My heat drives you back.
咬合力比火更实在。|My bite is more solid than my fire.
我甩头，把你摔开。|I shake my head and throw you off.
打完我还要整理鬃毛。|After this I must tidy my mane.
""")
PYR["spawn"] = L("""
我从火光里走出来。|I step out of the firelight.
鬃毛先亮，我才现身。|My mane lights first, then I appear.
这片草地从今天归我。|This meadow belongs to me from today.
我抖开鬃毛，火星落满草地。|I shake my mane and sparks rain on the grass.
三十六级的草地，我熟。|Level thirty-six grass; I know it well.
我踩下的第一脚就冒烟。|My first step already smokes.
远处有狮群应我的吼。|A pride answers my roar from afar.
我站在最高的土坡上。|I stand on the highest rise.
火先到，我才到。|The fire arrives before I do.
我来的时候草是绿的。|The grass was green when I came.
我的鬃毛把夜照亮。|My mane lights up the night.
我慢慢睁眼，火就起来了。|I open my eyes and the fire starts.
空气里有股陌生的味道。|There is an unfamiliar smell in the air.
王者的位置空着，我坐了。|The king's place was empty; I took it.
""")
PYR["hurt"] = {
"generic": L("""
我的鬃毛被打歪了。|My mane has been knocked crooked.
火一时灭了半边。|Half my fire went out.
谁敢碰我的脸。|Who dares strike my face?
我只让了半步，别多要。|I yielded half a step, no more.
这一下打断了我的吼。|That cut my roar short.
我的爪子在地上抓出沟。|My claws dig furrows in the dirt.
我疼，但我还站着。|I hurt, but I am still standing.
鬃毛烧回来要时间。|The mane takes time to burn back.
我低吼，火重新亮起。|I growl and the fire relights.
你把我的威严撞出个口子。|You chipped my dignity.
"""),
"fire": L("我的鬃毛和它一起烧。|My mane burns along with it."),
"fall": L("我从土坡上滚下去了。|I rolled down the slope."),
"drown": L("水浇灭了我的鬃毛。|Water put out my mane."),
"explosion": L("冲击把我的火吹散。|The blast scattered my fire."),
"projectile": L("箭扎进我的肩膀。|An arrow sticks in my shoulder."),
"magic": L("有东西压住了我的火。|Something is smothering my fire."),
"starvation": L("我饿了，火也弱了。|I am hungry and my fire is weak."),
"lightning": L("雷劈下来，鬃毛全炸开。|Lightning struck and my mane exploded outward."),
"void": L("火在下坠里灭了。|My fire dies in the fall."),
}

PYU = {}
PYU["walk"] = L("""
我用腹部一点点挪。|I inch along on my belly.
我走得很慢，像被冲上岸。|I move slowly, like I was washed ashore.
身后留下一道湿痕。|A wet trail follows behind me.
我挪到石头边就停。|I stop when I reach the stone.
我的身子软，路也软。|My body is soft; so is my path.
我滚了一下，翻了。|I rolled once and tipped over.
我挪得比潮水还慢。|I move slower than the tide.
我一寸一寸地挪，不赶。|I inch along, in no hurry at all.
沙子粘在我身上。|Sand clings to my body.
我朝有水的方向挪。|I crawl toward the sound of water.
我挪过的地方亮亮的。|Where I pass, the ground shines.
我这身皮又滑又软。|My skin is slippery and soft.
""")
PYU["idle"] = L("""
我摊在沙上，一动不动。|I lie spread on the sand, motionless.
我的嘴一张一合。|My mouth opens and closes.
我在等潮水回来。|I am waiting for the tide to return.
太阳晒得我暖乎乎的。|The sun makes me comfortably warm.
浪打上来，我数到第四下。|A wave comes; I count to four.
我肚子里咕噜响。|My insides gurgle from time to time.
我被冲上来了，又来一次。|Washed ashore again, I see.
我不动，别人就以为我是石头。|If I keep still, they think I am a stone.
我的小触手缩了一下。|My little tentacles twitch.
沙粒下面有东西在钻。|Something is burrowing under the sand.
我把身体朝海那边偏了偏。|I tilt my body a little toward the sea.
我身上开始发干。|My skin is starting to dry.
海浪的声音我听得清。|I hear the waves clearly.
我准备再躺一会儿。|I plan to lie here a while longer.
""")
PYU["look_player"] = L("""
你挡着风了，请让开。|You are blocking the breeze; please move.
你要把我扔回海里吗？|Are you going to throw me back?
我这样躺是有原因的。|I lie like this for a reason.
你的手指别碰我的皮。|Keep your fingers off my skin.
你脚边就是我的潮线。|Your feet are on my tide line.
我在等你弯腰。|I am waiting for you to bend down.
你这身衣服沾了沙。|Your clothes have sand on them.
你看我做什么，我不能走快。|Why look at me? I cannot go faster.
我不是石头，我会动。|I am not a stone; I do move.
海在那里，我在你前面。|The sea is there; I am in front of you.
你笑我被冲上岸？|Laughing because I washed ashore?
我软，但不好踩。|I am soft, but not good to step on.
你裤脚上有咸水味。|There is salt water on your cuffs.
你看着好像想帮我。|You look like you want to help.
""")
PYU["tempted"] = L("""
海藻？我张嘴就能吸。|Seaweed? I can suck it in.
你把东西放水里，我才要。|Put it in the water and I will take it.
我不追，它会飘过来。|I do not chase; it drifts to me.
我伸手？我没有手。|Reach for it? I have no hands.
你先放地上，别晃。|Set it down and stop waving it.
我只吃水里带来的。|I only eat what the water brings.
这么小的东西我吸不进去。|I cannot suck up anything this small.
你把它浸湿，我再考虑。|Soak it first; then I will consider.
我张着嘴，你扔吧。|My mouth is open; throw it.
我不为食物挪半寸。|I will not move an inch for food.
""")
PYU["collide"] = L("""
你踩到我软的地方了。|You stepped on my soft part.
我被你撞得翻过来。|Your bump rolled me over.
我这么矮，你都没看见。|I am this low; you still missed me.
麻烦把我扶正。|Please set me upright again.
我的皮上留下你的鞋印。|Your bootprint is on my skin.
我被撞得翻了两个跟头。|The bump sent me tumbling twice.
你踢我，我飞不远。|Kick me and I will not go far.
用脚推我，我会黏上你。|Push me with your foot and I stick.
沙滩这么大，你还踩我。|The beach is huge and you still step on me.
我身上本来就没什么硬度。|I have no hardness to begin with.
""")
PYU["mate"] = L("""
潮水里，我慢慢靠向你。|In the tide, I drift toward you.
我不跳舞，我只挪过去。|I do not dance; I shuffle over.
你能不能留在潮线边。|Would you stay by the tide line?
我的身体在月光下发亮。|My body glistens in the moonlight.
我们找个水洼待着吧。|Let us find a pool and stay there.
我挪到你身边，就这些。|I move beside you; that is all.
沙上留了两道湿印。|Two wet trails are left on the sand.
潮水退了，我们还在。|The tide went out; we are still here.
我轻轻地贴着你。|I press gently against you.
明年我还会被冲到这里。|Next year the tide brings me here again.
""")
PYU["pickup"] = L("""
我连抓握都做不到，只能含。|I cannot grip at all; I can only hold.
我用嘴吸，别的东西不行。|I suck with my mouth; nothing else works.
我用软软的身子盖住它。|I cover it with my soft body.
这东西硌得我不舒服。|This thing is uncomfortable under me.
我挪过去，把它盖住。|I shuffle over and cover it.
掉在沙里的，我收着。|What falls in the sand, I keep.
我用触手碰了一下。|I touch it with a tentacle.
我吞不下这么大的。|I cannot swallow something this big.
你掉的？在我肚子底下。|Yours? It is under my belly.
我只捡能吃的东西。|I only pick up what I can eat.
""")
PYU["target_acquire"] = L("""
有什么在沙上爬。|Something is crawling on the sand.
我把身体转向它。|I turn my body toward it.
我张开了嘴。|I open my mouth wide.
它靠得更近了。|It is coming closer.
我不追，我等它自己来。|I do not chase; I let it come.
沙粒在我身下滚动。|Grains roll beneath my body.
我的触手都伸了出来。|All my tentacles have come out.
它踩到了我的潮线。|It stepped on my tide line.
这里离海太远了。|This is too far from the sea.
它一动，我就缩紧。|When it moves, I tighten up.
""")
PYU["targeting"] = L("""
我对着你，一动不动。|I face you without moving.
你要不要试试踩我。|Want to try stepping on me?
我身上有黏的东西。|There is something sticky on my skin.
你越靠近，我越紧。|The closer you come, the tighter I get.
我不跑，反正也跑不快。|I will not run; I am not fast anyway.
我等着你伸手。|I wait for your hand to reach.
沙滩上只有我们两个。|Only the two of us are on this beach.
我的眼睛很小，但看得见。|My eyes are small, but I can see.
你别以为我软就好欺负。|Do not think soft means easy.
我绷紧了全身。|I have tensed my whole body.
""")
PYU["melee_attack"] = L("""
碰我一下，你自己疼。|Touch me and you will be the one hurting.
我把黏液压在你鞋上。|I smear sticky fluid on your boot.
我绷紧全身，硬得像石头。|I tense up hard as stone.
你打我，里面的东西会还你。|Hit me and my insides will answer.
我用整个身子砸过去。|I slam my whole body into you.
我滚到你脚背上压着。|I roll onto your foot and press.
我吐出一口黏水。|I spit out a mouthful of slime.
我不咬，我只是很黏。|I do not bite; I am simply sticky.
这一下不算攻击，算提醒。|This is less attack than reminder.
是你先踩上来的。|You stepped on me first.
""")
PYU["spawn"] = L("""
潮水把我推上沙滩。|The tide pushes me onto the beach.
我躺在湿沙上，还带着水。|I lie on wet sand, still dripping.
第二十级的草地，就这里。|Level twenty grass; this is the spot.
我翻了个身，找到海的方向。|I roll over and find the sea.
我来的时候身上裹着海藻。|I arrived wrapped in seaweed.
沙里冒出我半个身子。|Half of me emerges from the sand.
我贴着地面慢慢展开。|I spread out slowly against the ground.
这里比海里晒得厉害。|It is far sunnier here than in the sea.
我听见浪在我身后。|I hear the waves behind me.
我又被扔上来了。|I have been thrown ashore again.
我身上还挂着水珠。|Water still hangs on my skin.
我先躺着，等潮水。|I will lie here and wait for the tide.
""")
PYU["hurt"] = {
"generic": L("""
我缩成一团软的。|I curl into a soft lump.
我的皮破了一点。|My skin has a small tear.
别踩，我里面很脆。|Do not step; I am fragile inside.
我弹了一下，滚开了。|I bounced once and rolled away.
这一下让我漏了点水。|That made me leak a little water.
我疼得贴紧了沙。|I press flat against the sand in pain.
我的触手全缩回去了。|All my tentacles have pulled in.
我本来就不经打。|I was never built to take hits.
沙粘在我的伤口上。|Sand sticks to my wound.
我慢慢挪，离你远点。|I shuffle slowly away from you.
"""),
"fire": L("我的皮被烤得发干。|My skin is drying in the heat."),
"fall": L("摔下来，我差点散了。|I fell and nearly came apart."),
"drown": L("我沉下去了，看不见沙。|I sank and lost sight of the sand."),
"explosion": L("我被震得飞起来。|The blast threw me into the air."),
"projectile": L("有东西扎进我软的身子。|Something pierced my soft body."),
"magic": L("有力量在我身体里打转。|A force is churning inside me."),
"starvation": L("我空着肚子，更没力气。|Empty, I have even less strength."),
"lightning": L("雷落进水里，我缩得紧紧的。|Lightning hit the water and I clenched up tight."),
"void": L("我掉进没有沙的地方。|I fell where there is no sand."),
}

QUA = {}
QUA["walk"] = L("""
我走一步，水花一朵。|One step, one splash.
我踩着河底的石头过去。|I walk across the stones on the riverbed.
我的尾巴在后面拖着水。|My tail drags water behind me.
我慢慢走，不赶时间。|I walk slowly; no hurry.
我脚下的泥软软的。|The mud under my feet is soft.
我不看路，也不会摔。|I do not watch the path, yet I never fall.
我的步子又大又稳。|My steps are wide and steady.
我从浅水走到岸上。|I walk from the shallows onto the bank.
我甩甩尾巴上的水。|I shake the water off my tail.
我一边走一边打盹。|I doze a little as I walk.
我的鳍摆得像在挥手。|My fins wave as if greeting you.
水面被我推开一条线。|The water parts in a line behind me.
""")
QUA["idle"] = L("""
我站在水里，什么都不想。|I stand in the water thinking nothing.
我的嘴慢慢张开又合上。|My mouth opens and closes slowly.
水从我背上流下去。|Water runs down my back.
我的尾巴在水里慢慢摆。|My tail sways slowly underwater.
我想不起来刚才在想什么。|I forget what I was thinking about.
一只鱼游过我的腿边。|A fish swims past my leg.
我在数石头，数到三就停了。|I count stones and stop at three.
我的皮一直湿漉漉的。|My skin stays wet all the time.
我抬头，看云慢慢走。|I look up and watch the clouds drift.
我打了个嗝，水面起泡。|I burp and bubbles rise.
我不怕冷，水是我的被子。|I do not mind cold; water is my blanket.
我的眼睛半睁着。|My eyes are half open.
河里的声音我全听得见。|I hear everything in the river.
我一动不动，鱼也不怕我。|I stay still, and the fish stop fearing me.
""")
QUA["look_player"] = L("""
你站在岸上看我做什么。|Why do you stand on the bank watching me?
你要下水吗，水不深。|Coming in? The water is shallow.
我这样看着你，没有恶意。|I look at you this way without malice.
你的鞋子会湿的。|Your shoes are going to get wet.
我脑袋撞过船底，也不疼。|I bumped a boat's hull and felt nothing.
你手里的球，我见过。|I have seen that ball before.
你踩的那块石头我认识。|I know the stone you are standing on.
我很少把谁放在心上。|I rarely take anyone to heart.
河里有船经过，我不躲。|Boats pass; I do not move.
你笑起来跟我差不多。|Your smile is a lot like mine.
我游得慢，你等得起吗？|I swim slowly; can you wait?
太阳被你整个人挡住了。|You are blocking the whole sun.
我没什么可告诉你的。|I have nothing to tell you.
你不用一直盯着我。|You do not have to keep staring.
""")
QUA["tempted"] = L("""
有吃的？我游过去。|Food? I will swim over.
你把它扔进水里吧。|Throw it into the water.
我不挑，什么都吃。|I am not picky; I eat anything.
这一点不够我一口。|That is not a mouthful for me.
我慢，但我一定到。|I am slow, but I always get there.
你手伸得太远了。|Your hand is stretched out too far.
水里的东西我自己找。|I find my own food in the water.
我闻到味道了，等一下。|I smell it; give me a moment.
你不用一直摇。|You do not need to keep waving it.
吃完了我继续泡水。|When I am done, I go back to soaking.
""")
QUA["collide"] = L("""
你撞我，我一点感觉都没有。|You bump me; I feel nothing.
我太软了，撞不出声。|I am too soft to make a sound.
我们撞上，我还在原地。|We collided; I have not moved.
你的肩膀撞上我的肚子。|Your shoulder met my belly.
我转身很慢，你等等。|I turn slowly; wait a moment.
河水把我们挤在一起。|The current pushed us together.
我撞上船底也无所谓。|Hitting a boat's hull is fine by me.
你退开点，我要上岸。|Step aside; I am coming ashore.
我们谁也没让。|Neither of us gave way.
我这一身都是软的。|Everything on me is soft.
""")
QUA["mate"] = L("""
我在水里等你。|I am waiting for you in the water.
你愿意一起泡着吗？|Would you soak here with me?
我慢慢靠过来。|I drift slowly up beside you.
我的尾巴碰到你的了。|My tail has touched yours.
河底很平，正合适。|The riverbed is flat; just right.
我没什么花样，就这样。|I have no tricks; this is it.
我们一起浮在水面上。|We float together on the surface.
你不用说话，我懂。|You do not need to speak; I understand.
水声会盖住我们的动静。|The water will cover any sound we make.
明年这个时候，还在这条河。|Same river, same time next year.
""")
QUA["pickup"] = L("""
我用嘴含住，别让它沉。|I hold it in my mouth so it will not sink.
我从河底把它捞起来。|I scoop it up from the riverbed.
我爪子上全是泥。|My claws are covered in mud.
它滑，我按不住。|It is slippery; I cannot hold it.
我让它停在我的鼻尖。|I let it rest on my snout.
掉了就掉了，水会带走。|Dropped is dropped; the water takes it.
我慢慢沉下去找。|I sink slowly to look for it.
这东西不值钱吧。|This is not worth much, is it?
我把它放进浅水。|I put it in the shallows.
我用尾巴把它扫过来。|I sweep it over with my tail.
""")
QUA["target_acquire"] = L("""
河面上有一圈波纹。|There is a ring spreading on the river.
我慢慢转过头。|I slowly turn my head.
它比我快，我不急。|It is faster than me; I am not worried.
我朝它的方向游。|I swim toward it.
我张开嘴，等它过来。|I open my mouth and let it come.
河底的泥被它搅起来了。|It stirred up mud from the bottom.
它撞到我，我不介意。|It bumped me; I do not mind.
我也该动一动了。|I suppose I should move.
它躲到石头后面了。|It hid behind the stone.
我跟着水声走。|I follow the sound of the water.
""")
QUA["targeting"] = L("""
我看着你，眼睛都不眨。|I watch you without blinking.
你在岸上，我在水里。|You are on the bank; I am in the water.
你要下来，还是要走？|Are you coming down or leaving?
我不生气，只是靠近点。|I am not angry, just coming closer.
你退一寸，我进一寸。|You give an inch; I take an inch.
河水会替我把路堵住。|The river will block your way for me.
我的尾巴在水下摆。|My tail sways beneath the water.
你听，水声停了。|Listen; the water sound has stopped.
我没有恶意，但我不让。|No malice in me, but I do not yield.
你站在那里已经很久了。|You have stood there a long time.
""")
QUA["melee_attack"] = L("""
我用尾巴横扫过去。|My tail sweeps across at you.
我一头撞上去。|I butt my head into you.
溅起来的水打湿你的脸。|The splash soaks your face.
我的体重压得你站不稳。|My weight makes you lose footing.
我咬一口，慢慢咬。|I bite once, slowly.
你打我，我照旧游。|You hit me; I keep swimming.
河底的石头被我踢起来。|My kick sends river stones flying.
撞完我头都不晃。|After the hit my head does not even wobble.
我不追，我等你回来。|I will not chase; I wait for you to return.
打完我继续泡水。|When it is over I go back to soaking.
""")
QUA["spawn"] = L("""
我从河底浮上来。|I rise from the riverbed.
水面上先冒出我的头。|My head breaks the surface first.
我抖了抖，水珠四处飞。|I shake myself and droplets fly.
我踩着泥慢慢上岸。|I walk up the muddy bank.
我在这条河里待很久了。|I have been in this river a long time.
水草缠在我的腿上。|Water weeds cling to my legs.
我又回到这片浅滩。|I am back at these shallows.
我抬头，太阳正好。|I look up; the sun is just right.
河底的石头硌不着我。|The river stones do not bother me.
我的尾巴先探出水面。|My tail comes out of the water first.
我游了一圈才停下。|I swim one lap before stopping.
这里的水温我认得。|I know the temperature of this water.
""")
QUA["hurt"] = {
"generic": L("""
撞一下，我晃了晃。|One hit, and I wobbled a little.
我连船底都撞过，不怕。|I have hit a boat's hull; this is nothing.
我的皮厚，但会疼。|My hide is thick, but it still hurts.
我从水里退了一步。|I retreated one step into the water.
我原本快睡着了，现在醒了。|I was nearly asleep; now I am awake.
我的尾巴沉下去了。|My tail sank into the mud.
我慢慢转过头看你。|I turn my head slowly to look at you.
河底的泥沾上伤口。|River mud gets into the wound.
我不喊，我只是泡着。|I do not cry out; I just soak.
疼一会儿就过去了。|The pain will pass soon enough.
"""),
"fire": L("水都烧热了，难受。|Even the water is hot; unpleasant."),
"fall": L("我从岸上滚进河里。|I rolled off the bank into the river."),
"drown": L("水太深，我透不过气。|The water is too deep; I cannot breathe."),
"explosion": L("冲击把水都推开了。|The blast pushed the water away."),
"projectile": L("有个硬东西扎进我的背。|Something hard drove into my back."),
"magic": L("有股力气把我按在河底。|A force pins me to the riverbed."),
"starvation": L("我肚子空，游不动了。|Empty, I can barely swim."),
"lightning": L("雷打进河里，我麻了。|Lightning hit the river and numbed me."),
"void": L("我掉出水面，什么都没有。|I fell out of the water into nothing."),
}

MOBS = [
    ("pixelmon:purugly", "东施喵", PUR),
    ("pixelmon:pyroar", "火炎狮", PYR),
    ("pixelmon:pyukumuku", "拳海参", PYU),
    ("pixelmon:quagsire", "沼王", QUA),
]

plan = json.load(open("data/dialogue/unique_plan.json", encoding="utf-8"))["u0293"]
weights = {m["mob_id"]: m["weights"] for m in plan}

def extra(w):
    return max(0, min(4, round(10 * (w - 1))))

errs = []
scen_names = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
              "target_acquire", "targeting", "melee_attack", "spawn"]
seen = set()
mobs_out = []
total = 0
for mob_id, zh_name, table in MOBS:
    w = weights[mob_id]
    scen = {}
    for s in scen_names:
        lines = table[s]
        want = 10 + extra(w[s])
        if len(lines) != want:
            errs.append(f"{mob_id} {s}: got {len(lines)} want {want}")
        scen[s] = lines
    h = table["hurt"]
    scen["hurt"] = {k: v for k, v in h.items()}
    if len(h["generic"]) != 10:
        errs.append(f"{mob_id} hurt.generic {len(h['generic'])}")
    for k in ["fire", "fall", "drown", "explosion", "projectile", "magic", "starvation", "lightning", "void"]:
        if len(h[k]) != 1:
            errs.append(f"{mob_id} hurt.{k} {len(h[k])}")
    for s, lines in scen.items():
        group = lines if isinstance(lines, list) else [x for v in lines.values() for x in v]
        for it in group:
            zh, en = it["zh"], it["en"]
            n = len(re.sub(r"\s", "", zh))
            if not 6 <= n <= 20:
                errs.append(f"{mob_id} {s} zh len {n}: {zh}")
            cw = len(en.split())
            if not 4 <= cw <= 14:
                errs.append(f"{mob_id} {s} en words {cw}: {en}")
            if zh in seen:
                errs.append(f"dup zh: {zh}")
            seen.add(zh)
            total += 1
    mobs_out.append({"mob_id": mob_id, "scenarios": scen})

if errs:
    print("\n".join(errs))
    sys.exit(1)

json.dump({"batch": "u0293", "mobs": mobs_out},
          open("data/dialogue/unique/u0293.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("ok", len(mobs_out), total)
