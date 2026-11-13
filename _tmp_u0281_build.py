import json, math, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def S(zh, en):
    return {"zh": zh, "en": en}

MOBS = []

# ---------------- passimian ----------------
p = {}
p['walk'] = [
S("我把叶片按在肩上，标记队伍。", "I press leaves onto my shoulder to mark my team."),
S("每一步都踏得整齐，像在列队。", "Every step lands even, as if I were on parade."),
S("从树冠到地面，我走一条直线。", "From canopy to ground I keep one straight line."),
S("我抱着一颗果子，脚步不停。", "I clutch a berry and never break my stride."),
S("肩上的叶标在风里轻轻晃。", "The leaf mark on my shoulder sways in the breeze."),
S("我踩过落叶，几乎不发出声。", "I cross the fallen leaves with almost no sound."),
S("先探半步，再把整只脚落下。", "I test half a step, then set my whole foot down."),
S("队伍在前面等我，不能慢。", "My troop waits ahead, so I cannot slow down."),
S("我边走边数，一共十二只。", "I count as I walk: twelve of us in all."),
S("我用唾液把松掉的叶子粘牢。", "I glue a loose leaf back down with my spit."),
S("枝头太细，我改走地面。", "That branch is too thin, so I take the ground."),
S("我抬手护住肩上那枚标记。", "I raise a hand to guard the mark on my shoulder."),
]
p['idle'] = [
S("我坐下，把队形在脑中排一遍。", "I sit and rearrange the formation in my head."),
S("叶子有点干了，该换新的。", "This leaf is drying out; time to swap it."),
S("我在等远处那声召唤。", "I am listening for a call from far off."),
S("肩上的标记是我唯一的身份。", "The mark on my shoulder is my only rank."),
S("我把手心的果子翻来覆去。", "I turn the berry in my palm over and over."),
S("风从树冠下来，带着果香。", "Wind slides down from the canopy, smelling of fruit."),
S("我试着投了一下，只是虚投。", "I test a throw, but only into empty air."),
S("谁在偷看？我抬高下巴。", "Who is watching? I lift my chin higher."),
S("我梳理肩毛，把标记理顺。", "I groom my shoulder fur and straighten the mark."),
S("队伍里没人说话，我也不说。", "No one in the troop speaks, so neither do I."),
S("我盯着树梢，像在等信号。", "I stare at the treetops, waiting for a signal."),
S("手上的老茧又厚了一层。", "The callus on my hand has thickened again."),
S("我把落叶堆成一小摞。", "I stack the fallen leaves into a small pile."),
S("站久了，我换个肩承重。", "Standing long, I shift weight to the other shoulder."),
]
p['look_player'] = [
S("你肩上有叶子，是我们的吗？", "You have a leaf on your shoulder. Ours?"),
S("我歪头看你，先估你的力气。", "I tilt my head and size up your strength."),
S("你站得太直，不像我们。", "You stand too straight to be one of us."),
S("我盯着你的手，那里能扔东西。", "I watch your hands; they can throw things."),
S("你是来加入，还是来抢果子？", "Are you joining us, or here for our berries?"),
S("我把脸凑近，闻你身上的味道。", "I lean in and sniff the scent you carry."),
S("你身后没人，我看清楚了。", "There is nobody behind you; I checked."),
S("眼睛对眼睛，我不先眨眼。", "Eye to eye, I will not blink first."),
S("我抬手，你最好别躲。", "I raise my hand; better not flinch."),
S("你这个高度，正好递果子。", "Your height is just right for handing over berries."),
S("我记住你站的位置了。", "I have memorized where you are standing."),
S("你笑什么？我们不打笑脸。", "What are you grinning at? We spare smiling faces."),
S("我在看你有没有藏东西。", "I am checking whether you are hiding something."),
S("你走近一步，我就退半步。", "Take one step closer and I take half a step back."),
]
p['tempted'] = [
S("果子？拿来，我替队伍收下。", "A berry? Hand it over; I will hold it for the troop."),
S("这个味道，和我藏的一样。", "That smell matches the ones I have stored."),
S("我先闻三下，再决定要不要。", "I sniff three times before I decide."),
S("你给我一颗，我记你一次好。", "Give me one and I will owe you a favor."),
S("别举太高，我够得到的才吃。", "Do not hold it too high; I only eat what I can reach."),
S("我伸手了，你最好松手。", "My hand is out; you had better let go."),
S("这果子够不够分给十二只？", "Is this enough to share among twelve of us?"),
S("我咽了口口水，有点丢脸。", "I swallowed hard, which is a little embarrassing."),
S("甜的我就收，酸的留给别人。", "Sweet ones are mine; sour ones go to someone else."),
S("你带了几颗？我数一下。", "How many did you bring? Let me count."),
]
p['collide'] = [
S("站稳，别撞散我的队形。", "Steady there; do not break up my formation."),
S("我用肩膀顶回去，礼尚往来。", "I push back with my shoulder; fair exchange."),
S("撞到我的标记，你赔得起？", "You bumped my mark; can you pay for that?"),
S("我踉跄一步，叶子掉了。", "I stumble once, and my leaf falls off."),
S("身体碰身体，我不怕。", "Body against body, I am not afraid."),
S("你比我矮，撞起来不太公平。", "You are shorter than me; this bump is unfair."),
S("我抬手扶住你，免得你倒。", "I catch your arm before you topple over."),
S("别从侧面来，我最讨厌那个。", "Not from the side; that is what I hate most."),
S("这一下把果子撞出怀了。", "That knocked the berry out of my arms."),
S("我们互相撞，然后都笑了。", "We knock into each other, then both laugh."),
]
p['mate'] = [
S("我把最直的叶子贴在你肩上。", "I press my straightest leaf onto your shoulder."),
S("从今天起，我们用一个标记。", "From today we share a single mark."),
S("你投得远，我投得准。", "You throw far, and I throw true."),
S("树冠上那处空位，留给你。", "That empty spot in the canopy is yours."),
S("我们俩站一班岗，轮着看。", "We will share a watch, taking turns."),
S("先别急着走，让我理理毛。", "Do not leave yet; let me groom your fur."),
S("你的手掌比我宽，正好。", "Your palm is broader than mine, which suits me."),
S("以后果子分两半，一人一半。", "From now on, every berry splits two ways."),
S("我数过了，我们正好成对。", "I counted; we make a proper pair."),
S("叶子贴歪了，我重新粘一次。", "The leaf sits crooked; I will glue it again."),
]
p['pickup'] = [
S("这果子掉了，我顺手捡。", "A berry dropped; I will pick it up."),
S("地上有片好叶子，归我了。", "A good leaf on the ground, and it is mine."),
S("我先闻一下，再塞进怀里。", "I sniff it once before tucking it away."),
S("这块石头能砸果子，有点用。", "This stone could crack berries; that is useful."),
S("我一手一个，还能再夹一个。", "One in each hand, and room for one more."),
S("你掉的？我帮你拿着。", "Did you drop this? I will hold it."),
S("这堆东西里，我挑最圆的。", "Of this pile, I take the roundest one."),
S("队里的份，我先替他收着。", "I will keep my troop's share for them."),
S("捡到就归我，这是规矩。", "Finders keepers; that is the rule."),
S("我把它们排成一排数了数。", "I line them all up and count."),
]
p['target_acquire'] = [
S("前面那只有动静，我盯上了。", "Something moved ahead; I have locked on."),
S("我先压低身子，再靠近。", "I lower my body before closing the distance."),
S("队形散开，从左和右包。", "Spread out; we take the left and right."),
S("它的脚步乱了，是机会。", "Its footsteps are messy; that is my chance."),
S("我捏紧手里的果子当暗器。", "I grip my berry like a throwing stone."),
S("别回头看，它就在你后面。", "Do not look back; it is right behind you."),
S("我抬手示意，别出声。", "I raise a hand for silence."),
S("它的肩比我的宽，不好对付。", "Its shoulders are broader than mine; it will be stubborn."),
S("我先绕到树下，占个高点。", "I circle to the tree for the high ground."),
S("目标是我，别牵进队伍。", "The target is me; keep the troop out of it."),
]
p['targeting'] = [
S("我再走三步，就能碰到它。", "Three steps more and I can reach it."),
S("它往左躲，我就往左压。", "It dodges left, so I press left."),
S("手臂抬到肩高，蓄着力。", "My arm is at shoulder height, storing power."),
S("别急着扑，先看它的脚。", "Do not rush; watch its feet first."),
S("它在喘，比刚才慢了。", "It is panting, slower than before."),
S("我把重心压低，随时能冲。", "Weight low, ready to launch at any moment."),
S("它的影子朝我，说明背光。", "Its shadow points at me; the sun is behind it."),
S("我绕半步，把它的退路封上。", "Half a step around and its retreat is sealed."),
S("这一投我要正中它的胸口。", "This throw goes straight at its chest."),
S("队友在右边，我们同时出手。", "My troop is on the right; we strike together."),
]
p['melee_attack'] = [
S("接这一记，用肩撞过去。", "Take this: a full shoulder charge."),
S("我抓住它的手臂，往下拽。", "I grab its arm and drag it down."),
S("拳头落在它肋骨上，闷响。", "My fist lands on its ribs with a dull thud."),
S("它挡了，我换手再打。", "It blocked, so I switch hands."),
S("我用膝盖顶它的肚子。", "I drive my knee into its belly."),
S("这一下是替队伍还的。", "That one was repaid for my troop."),
S("它退了，我跟上半步。", "It retreats, and I follow half a step."),
S("别硬接，我的掌比石头沉。", "Do not block it; my palm is heavier than stone."),
S("我把它掀翻，按在落叶上。", "I flip it over and pin it to the leaves."),
S("打完这只，我们还要换岗。", "Once this one is done, we swap watch."),
]
p['spawn'] = [
S("我从树冠跳下，落在落叶上。", "I drop from the canopy onto fallen leaves."),
S("这里树够高，适合我们。", "The trees are tall enough here for us."),
S("我先找高处，再找队伍。", "First the high ground, then my troop."),
S("肩上是空的，我得做标记。", "My shoulder is bare; I need a mark."),
S("这片林子有果子的味道。", "These woods smell of fruit."),
S("我落地时，叶子被风带起来。", "Leaves lift in the wind as I land."),
S("四处看看，谁在放哨？", "Looking around: who is standing watch?"),
S("十五级以上的林子，正合适。", "A forest of level fifteen and up suits me."),
S("我拍了拍身上的碎叶。", "I brush the leaf bits off myself."),
S("刚来就闻到同类的味道。", "I smell my own kind already."),
S("树影够密，我放心了。", "The shade is thick enough; I am at ease."),
S("第一件事，找根好枝条。", "First order of business: find a good branch."),
]
p['hurt'] = {
"generic": [
S("疼，我的肩标被撞歪了。", "Ouch, my shoulder mark got knocked crooked."),
S("你打得准，正好在肋骨。", "Good aim; that landed right on my ribs."),
S("我咬牙，把疼咽回去。", "I grit my teeth and swallow the pain."),
S("我的叶子掉了，动作别踩。", "My leaf fell; do not step on it."),
S("这一下让我退了半步。", "That one pushed me back half a step."),
S("队伍会替我记着的。", "My troop will remember this for me."),
S("我捂着肩，指甲都白了。", "I clutch my shoulder, nails gone pale."),
S("还站得住，但不太稳。", "I am still standing, though not steadily."),
S("谁从背后打的我？", "Who hit me from behind?"),
S("喘口气，我还能再打。", "One breath, and I can fight again."),
],
"fire": [S("火烤到肩毛，闻着像焦叶。", "Flame singes my shoulder fur, smelling of burnt leaves.")],
"fall": [S("从树冠摔下来，背先着地。", "I hit the ground back first, right off the canopy.")],
"drown": [S("水比树冠高，我喘不上气。", "The water is over my head; I cannot breathe.")],
"explosion": [S("炸开的土把我埋了半截。", "The blast buried me halfway in dirt.")],
"projectile": [S("这支箭钉在我肩上。", "An arrow is stuck in my shoulder.")],
"magic": [S("这道光让我忘了队形。", "That light made me forget the formation.")],
"starvation": [S("肚子空了，投不出力气。", "My stomach is empty; my throws have no strength.")],
"lightning": [S("雷打在枝上，我全身麻。", "Lightning struck the branch and numbed me.")],
"void": [S("脚下什么都没有，连叶子。", "Nothing under my feet, not even a leaf.")],
}
MOBS.append(("pixelmon:passimian", p))

# ---------------- patrat ----------------
p = {}
p['walk'] = [
S("我一步一停，先看左右。", "I step, stop, and check both sides."),
S("尾巴翘着，草地被我踩响。", "Tail up, I crunch my way through the grass."),
S("我沿着田边巡视，不快不慢。", "I patrol the field edge at a steady pace."),
S("颊袋鼓鼓的，走路有点歪。", "Cheeks full, I walk a little lopsided."),
S("这条路上有脚印，我跟着。", "There are prints on this path; I follow them."),
S("我抬头看天，怕有影子落下。", "I glance up, wary of a falling shadow."),
S("后腿蹬一下，我蹿出半米。", "One push of my hind legs, half a meter gone."),
S("我绕开石头，不惊动草。", "I skirt the stone without rustling grass."),
S("从草丛到田埂，我走熟了。", "From grass to ridge, I know this route."),
S("我边走边听，耳朵先转。", "I walk and listen, ears turning first."),
S("前面有响动，我放慢脚。", "Something stirs ahead; I slow my feet."),
S("我踩过自己的影子，继续走。", "I walk over my own shadow and keep going."),
]
p['idle'] = [
S("我坐下来，尾巴还在抖。", "I sit down, but my tail keeps twitching."),
S("颊袋里还有三颗种子。", "Three seeds are still in my cheek pouches."),
S("我在数草叶，数到一半忘了。", "I was counting grass blades and lost my place."),
S("有声音，我停下听。", "A sound; I stop and listen."),
S("天有点阴，可能下雨。", "The sky is grey; rain may come."),
S("我把种子推到舌头边。", "I push a seed against my tongue."),
S("后颈有点痒，我挠了两下。", "My neck itches; I scratch it twice."),
S("放哨很闷，但不能走。", "Watch duty is dull, but I cannot leave."),
S("我打个哈欠，马上闭嘴。", "I yawn, then shut my mouth at once."),
S("远处有鹰，我压低身子。", "A hawk is far off; I crouch lower."),
S("我舔了舔爪子，再抹脸。", "I lick my paws and wipe my face."),
S("这处草够高，能藏住我。", "The grass here is tall enough to hide me."),
S("我忽然想起，该换岗了。", "It occurs to me that my watch is over."),
S("风一吹，我耳朵转向西。", "The wind shifts, and my ears turn west."),
]
p['look_player'] = [
S("你从正面来，我看得见。", "You came from the front, so I see you."),
S("站住，这里归我看守。", "Halt; this ground is under my watch."),
S("我眯起眼，先估你的步子。", "I squint and judge the length of your stride."),
S("你手上没有武器，还行。", "No weapon in your hands; that helps."),
S("我歪头，把你从头看到脚。", "I tilt my head and look you up and down."),
S("别绕到我后面，我会紧张。", "Do not slip behind me; it makes me nervous."),
S("你的影子好大，我不太喜欢。", "Your shadow is very large and I dislike it."),
S("我看你，你也看我，谁先动？", "I look at you, you look at me; who moves?"),
S("我拍了下尾巴，算是警告。", "I slap my tail once as a warning."),
S("你要过来，就先说句话。", "If you are coming over, say something first."),
S("我记住了你的鞋，别换。", "I have noted your boots; do not change them."),
S("你的味道里没有敌意。", "There is no hostility in your scent."),
S("我仰头看你，脖子有点酸。", "Looking up at you makes my neck ache."),
S("你要是朋友，就慢慢走过来。", "If you are friendly, walk over slowly."),
]
p['tempted'] = [
S("种子？给我，我放颊袋。", "Seeds? Give them here; they go in my cheeks."),
S("我先闻，闻完才敢吃。", "I sniff first; only then do I dare eat."),
S("你手别抖，我怕你抓我。", "Keep your hand still; I fear being grabbed."),
S("这个味道，和谷仓里一样。", "This smells like the grain store back home."),
S("我再靠近一点，就一点。", "I will come a little closer, just a little."),
S("放地上，你退后两步。", "Put it down and step back two paces."),
S("我颊袋还能再塞两颗。", "My cheeks can hold two more."),
S("甜的东西我最没辙。", "Sweet things are my one weakness."),
S("我伸爪子了，你看着办。", "My paw is out; do as you like."),
S("吃完这颗，我还想要。", "After this one, I will want another."),
]
p['collide'] = [
S("哎，你踩到我的尾巴。", "Hey, you stepped on my tail."),
S("我一屁股坐地上了。", "I landed flat on my backside."),
S("我撞得头昏，站不稳。", "The bump left me dizzy and unsteady."),
S("别挤，我颊袋里有东西。", "Do not crowd me; my cheeks are full."),
S("我退开让你，别追着撞。", "I step aside for you; stop bumping."),
S("这一撞，种子撒了两颗。", "That bump spilled two seeds."),
S("我抬头瞪你，很凶的那种。", "I glare up at you, my fiercest look."),
S("你腿比我粗，我认输。", "Your legs are thicker than mine; I yield."),
S("我翻了半圈，又爬起来。", "I roll half over and scramble up."),
S("下次绕开点，我在这儿站着。", "Walk around next time; I am standing here."),
]
p['mate'] = [
S("你先站岗，我去找吃的。", "You take watch; I will go forage."),
S("我们轮流守夜，一人两小时。", "We take turns at night, two hours each."),
S("靠近点，让我闻闻你。", "Come closer and let me smell you."),
S("颊袋里那颗，分你一半。", "That seed in my cheek is half yours."),
S("你耳朵比我灵，听你的。", "Your ears are sharper, so I follow yours."),
S("我把草压平，做个窝。", "I flatten the grass to make a nest."),
S("别睡太沉，我替你看着。", "Do not sleep too deep; I am watching."),
S("我们两家挨着，方便照应。", "Our burrows sit side by side, easy to help."),
S("你抖尾巴，我就懂了。", "You twitch your tail and I understand."),
S("从今天起，我们轮着放哨。", "From today, we share the watch."),
]
p['pickup'] = [
S("这颗种子，我收下了。", "I will take this seed."),
S("掉在地上的，都是我的。", "Whatever falls to the ground is mine."),
S("我咬一下，看看是不是石头。", "I bite it once to check it is not stone."),
S("这堆够我塞到明天。", "This pile will fill me till tomorrow."),
S("我拿不动太多，先挑大的。", "I cannot carry much, so I take the big ones."),
S("地上有个亮东西，我去看。", "Something bright on the ground; I will look."),
S("我把它们堆在窝边。", "I pile them beside my burrow."),
S("你掉的？那就是我的了。", "You dropped it, so it is mine now."),
S("我抱着走，走三步掉一颗。", "I carry them and drop one every three steps."),
S("先存起来，冬天很长。", "Better store it; winter is long."),
]
p['target_acquire'] = [
S("有东西靠近，我竖起耳朵。", "Something is coming; my ears stand up."),
S("我先叫一声，叫醒同伴。", "I call once to wake my companions."),
S("它比我大，但我不能跑。", "It is bigger than me, but I cannot run."),
S("我把身子压低，尾巴不动。", "I flatten low and still my tail."),
S("它从正面来，正好。", "It comes at my front, which is fine."),
S("草丛在动，就在左边。", "The grass moves, just on the left."),
S("我龇牙，让它先停一下。", "I bare my teeth to make it pause."),
S("退路我看好了，随时能跑。", "I have picked my escape route already."),
S("队里的幼崽在后面，别过来。", "The young ones are behind me; stay back."),
S("它绕圈了，想从我背后。", "It circles, meaning to get behind me."),
]
p['targeting'] = [
S("它再近两步，我就扑。", "Two more steps and I pounce."),
S("我压低前身，后腿蹬紧。", "Front low, hind legs coiled tight."),
S("它动一下，我跟着动。", "It moves, and I move with it."),
S("我盯着它的脚，不看眼。", "I watch its feet, not its eyes."),
S("它喘得厉害，快撑不住。", "It is panting hard and nearly done."),
S("我从侧面绕，别正面硬碰。", "I go around the side, not head on."),
S("尖叫声正招来同伴。", "My squeal is bringing my companions."),
S("它退了半步，我进一步。", "It gives half a step; I take one."),
S("我尾巴绷直，这是要冲。", "My tail is straight; that means I charge."),
S("它分神了，就是现在。", "It looked away; now is the moment."),
]
p['melee_attack'] = [
S("我咬它的脚跟，咬完就跑。", "I bite its heel, then run."),
S("一爪子挠过去，留三道印。", "One swipe leaves three marks."),
S("我用头顶它，它退了一步。", "I butt it with my head and it steps back."),
S("它慢，因为比我沉。", "It is slow because it is heavier."),
S("我撞它的膝，那里最软。", "I ram its knee, the softest spot."),
S("尖叫，咬一口，再退。", "Squeal, bite once, then retreat again."),
S("我跳上它的脚背，再蹬开。", "I leap onto its foot and kick away."),
S("这一口没咬穿，牙有点疼。", "That bite did not pierce, and my teeth ache."),
S("它挥过来，我矮身躲开。", "It swings; I duck under it."),
S("打不过就换地方，不丢人。", "Retreating to a better spot is no shame."),
]
p['spawn'] = [
S("我从草里钻出来，先蹲下。", "I push out of the grass and crouch first."),
S("这片草地草够高，我留下。", "This grass is tall enough; I will stay."),
S("我先找块石头，站上去望。", "I find a stone and climb it to look."),
S("四下安静，我竖起耳朵。", "All is quiet; I raise my ears."),
S("颊袋是空的，得去觅食。", "My cheeks are empty; time to forage."),
S("我落地时尾巴甩了一下。", "My tail flicked as I landed."),
S("六级的草地，是我出生的地方。", "A level six meadow, much like where I was born."),
S("我闻到谷子的味道。", "I smell grain in the air."),
S("先别动，看看有没有鹰。", "Hold still and check for hawks."),
S("我抖掉背上的草籽。", "I shake the grass seeds off my back."),
S("这里有田埂，适合放哨。", "There is a field ridge here, good for watching."),
S("我一出现，就先叫两声。", "I arrive, and I call twice."),
]
p['hurt'] = {
"generic": [
S("疼，我尾巴都僵了。", "Ouch, my tail has gone stiff."),
S("那一下打在颊袋上。", "That blow landed on my full cheek."),
S("我尖叫，声音有点破。", "I squeal, and my voice cracks."),
S("腿软了，我扶住草茎。", "My legs give, so I grip a grass stem."),
S("我退到石头后面喘气。", "I retreat behind the stone to breathe."),
S("这一下比鹰爪还重。", "That hit was heavier than a hawk's talon."),
S("我眼睛花了，看不清。", "My eyes blur and I cannot see straight."),
S("耳朵里嗡嗡响。", "There is a ringing in my ears."),
S("疼得我咬紧牙。", "The pain makes me clench my teeth."),
S("我还能站，别小看我。", "I can still stand; do not count me out."),
],
"fire": [S("火烧到我的毛，味道很冲。", "Fire caught my fur and the smell is sharp.")],
"fall": [S("从田埂跌下去，摔了个滚。", "I tumble off the ridge and roll.")],
"drown": [S("水进了鼻子，我乱蹬。", "Water up my nose; I kick wildly.")],
"explosion": [S("炸响把我掀进草里。", "The blast threw me into the grass.")],
"projectile": [S("有东西扎进我后腿。", "Something is stuck in my hind leg.")],
"magic": [S("怪光一闪，我忘了要跑。", "A strange flash and I forgot to run.")],
"starvation": [S("颊袋空了，胃也空了。", "My cheeks are empty and so is my stomach.")],
"lightning": [S("雷声太大，我伏在地上。", "The thunder is huge; I press to the ground.")],
"void": [S("没有草，没有土，只有空。", "No grass, no soil, only emptiness.")],
}
MOBS.append(("pixelmon:patrat", p))

# ---------------- pawmi ----------------
p = {}
p['walk'] = [
S("我小跑，尾巴一颠一颠。", "I trot along with my tail bobbing."),
S("四只脚一起动，声音很轻。", "All four paws move, barely making a sound."),
S("我蹭着草走，顺便充点电。", "I brush through grass to pick up charge."),
S("这条小路我走过很多次。", "I have walked this little path many times."),
S("我走三步，就停下来听。", "Three steps, then I stop to listen."),
S("后脚一蹬，我窜出去。", "A push of my hind paws and I dart off."),
S("我顺着石缝走，脚不沾水。", "I follow the stone cracks to keep dry."),
S("小跑起来，我脸颊会发亮。", "When I trot, my cheeks start to glow."),
S("我跟在你影子里走。", "I follow along inside your shadow."),
S("走快了会打滑，我慢点。", "Too fast and I slip, so I slow down."),
S("尾巴扫过草丛，沙沙响。", "My tail sweeps the grass, rustling softly."),
S("我抬头看你的腿，好高。", "I look up at your legs; they are so tall."),
]
p['idle'] = [
S("我坐着，把前爪擦干净。", "I sit and wipe my front paws clean."),
S("脸颊有点麻，是电攒多了。", "My cheeks tingle; too much charge stored."),
S("我抖抖耳朵，掉下一根草。", "I shake my ears and a grass blade falls."),
S("刚才那道闪光，是我吗？", "Was that flash of light from me?"),
S("我蜷成一团，暖和一点。", "I curl into a ball to keep warm."),
S("小石子被我电了一下。", "I gave that pebble a small shock."),
S("我盯着自己的尾巴打转。", "I chase my own tail in a circle."),
S("风里有铁锈的味道。", "There is a smell of rust in the wind."),
S("我舔爪子，毛翘起来了。", "I lick a paw and my fur stands up."),
S("有人来了？我先躲一下。", "Someone coming? I will hide a moment."),
S("饿是饿了，但懒得动。", "I am hungry, but too lazy to move."),
S("我把鼻尖贴着地面闻。", "I press my nose to the ground and sniff."),
S("这块石头晒得暖暖的。", "This stone is warm from the sun."),
S("我打了个小喷嚏，冒火星。", "I sneeze once and a spark flies out."),
]
p['look_player'] = [
S("你蹲下来，我才能看清。", "Crouch down so I can see you properly."),
S("我歪头，你比树还高。", "I tilt my head; you are taller than trees."),
S("你身上有静电的味道。", "You smell faintly of static."),
S("我抬起前爪，跟你打招呼。", "I lift a front paw to greet you."),
S("你别笑，我是认真的。", "Do not laugh; I am serious."),
S("我一步步靠近，又停下。", "I take a step closer, then stop."),
S("你的手好大，能握住我。", "Your hands are huge enough to hold me."),
S("我盯着你的手指看。", "I stare at your fingers."),
S("你眨眼的功夫，我挪近了。", "While you blinked, I crept closer."),
S("我尾巴竖起，表示不怕。", "My tail is up, which means I am not afraid."),
S("你要摸我？先让我闻闻。", "You want to pet me? Let me sniff first."),
S("我眼睛里全是你的影子。", "Your shadow fills both my eyes."),
S("你说话声音低，我不怕了。", "Your voice is low, so I stop being scared."),
S("我绕着你转，找破绽。", "I circle you, looking for an opening."),
]
p['tempted'] = [
S("是甜的？我耳朵先动了。", "Something sweet? My ears moved first."),
S("我靠近，但爪子收着。", "I come close, but keep my claws in."),
S("给我一小口，就一小口。", "Just one small bite, that is all."),
S("我闻着像浆果，我猜对了。", "Smells like berries; I guessed right."),
S("你别晃，我抓不准。", "Hold it still; I cannot aim."),
S("我鼻尖碰到它了。", "My nose just touched it."),
S("吃完这个，我还会电你吗？", "After this, will I still shock you?"),
S("我得两只爪子捧着吃。", "I need both paws to hold it."),
S("香味顺着风钻进鼻子。", "The smell drifts straight into my nose."),
S("我咽口水，声音很响。", "I swallow, and it is very loud."),
]
p['collide'] = [
S("你差点把我踩扁。", "You almost flattened me."),
S("我被撞得翻了半圈。", "The bump rolled me half over."),
S("我身上的毛全炸起来了。", "All my fur puffed up at once."),
S("没事，我皮实，电还多。", "No harm; I am tough and still charged."),
S("你踢到我了，脚麻不麻？", "You kicked me; is your foot numb?"),
S("我从你脚边滚开，又回来。", "I roll from your foot, then come back."),
S("这一撞，我冒了火花。", "That bump threw a spark off me."),
S("慢点走，我腿短。", "Walk slower, my legs are short."),
S("我抬头瞪你，其实不生气。", "I glare up at you, though I am not angry."),
S("再来一下，我就咬你鞋带。", "Once more and I bite your laces."),
]
p['mate'] = [
S("我们尾巴缠在一起，算约定。", "Our tails are tangled, and that is a promise."),
S("我替你理耳朵后面的毛。", "I groom the fur behind your ears."),
S("两颗浆果，我们一人一颗。", "Two berries, one for each of us."),
S("雨来了就挤在一起睡。", "When it rains we sleep pressed together."),
S("我放电轻一点，不会伤你。", "I discharge gently so it will not hurt you."),
S("你先走，我跟在你后面。", "You go first, and I follow behind."),
S("这处石缝够我们两个躲。", "This crack in the rock fits us both."),
S("我们磨磨脸颊，记住了彼此。", "We rub cheeks and remember each other."),
S("以后找吃的，一起找。", "From now on we forage together."),
S("你听，我的心跳很快。", "Listen, my heartbeat is very fast."),
]
p['pickup'] = [
S("这颗浆果掉了，我要。", "A berry dropped, and I want it."),
S("我用两只爪子捧起来。", "I scoop it up with both paws."),
S("轻的我能拖，重的算了。", "I can drag light things; heavy ones, no."),
S("这粒东西会滚，追起来好玩。", "This little thing rolls, which is fun."),
S("我咬一口，看看是不是吃的。", "I bite it once to see if it is food."),
S("我抱着它走，走两步掉了。", "I carry it two steps and drop it."),
S("这是我的，别伸手。", "This is mine; keep your hands away."),
S("亮亮的东西我都想捡。", "I want to pick up anything that shines."),
S("我把它推到你脚边。", "I push it over to your feet."),
S("捡多了，我就地吃起来。", "Once I have enough, I eat right here."),
]
p['target_acquire'] = [
S("有东西在动，我尾巴绷紧。", "Something moves and my tail goes stiff."),
S("脸颊开始麻，我准备放电。", "My cheeks tingle; I am charging up."),
S("它不大，我能对付。", "It is not big; I can handle it."),
S("我先伏低，把身子藏进草。", "I crouch and hide my body in the grass."),
S("它背对我，机会来了。", "It turned its back; here is my chance."),
S("火花在我爪间跳。", "Sparks jump between my paws."),
S("我吱吱叫，是让同伴退开。", "I squeak to warn my companions back."),
S("我先绕一圈，看它怎么动。", "I circle once to see how it moves."),
S("这个对手有点高，我得跳。", "This one is tall; I will have to jump."),
S("它没发现我，我贴近了。", "It has not noticed me; I closed in."),
]
p['targeting'] = [
S("再近一点，我就能碰到。", "A little closer and I can reach it."),
S("我压低身子，电在攒。", "I lower myself and gather my charge."),
S("它脚一挪，我就跟着挪。", "When its foot moves, mine follows."),
S("我数三下，然后冲。", "I count to three, then dash."),
S("它喘气了，比我累。", "It is panting, more tired than I am."),
S("我的尾巴在打信号。", "My tail is sending a signal."),
S("这一下要打它的脚踝。", "This one goes for its ankle."),
S("它往石头那边退，我堵住。", "It backs toward the stone; I cut it off."),
S("我跳起来，比它高一点。", "I leap, and I am briefly above it."),
S("火候到了，我要动了。", "The moment has come; I move."),
]
p['melee_attack'] = [
S("我扑上去，一口咬脚。", "I leap in and bite its foot."),
S("爪子带电，抓一下会麻。", "My charged claws make it go numb."),
S("我用头撞它，撞完就跑。", "I headbutt it, then dash away."),
S("电光一闪，它抖了一下。", "A flash of current; it flinched."),
S("我咬住不放，腿在蹬。", "I bite and hold, kicking with my legs."),
S("它挥手，我从下面钻过去。", "It swings; I dart underneath."),
S("这一下够它麻一会儿。", "That will leave it numb for a while."),
S("我跳上它背，找软处咬。", "I jump on its back and bite the soft spot."),
S("打不过，我钻进石缝。", "If it goes badly, I slip into the rocks."),
S("小个子也能咬得很疼。", "Small as I am, my bite still hurts."),
]
p['spawn'] = [
S("我从石缝里钻出来。", "I squeeze out of a crack in the rocks."),
S("这里的草刚够我藏身。", "The grass here is just tall enough to hide me."),
S("我先抖抖毛，把土弄掉。", "I shake the dirt out of my fur."),
S("空气里有淡淡的电味。", "There is a faint electric smell in the air."),
S("我一落地，脸颊就亮了。", "The moment I land, my cheeks light up."),
S("五级的草地，正合适我。", "A level five meadow suits me fine."),
S("我抬头看，树好高。", "I look up; the trees are very tall."),
S("先找个暖和的地方。", "First, a warm place to settle."),
S("我把鼻尖探出去闻。", "I poke my nose out and sniff."),
S("有人吗？我小心地走。", "Anyone about? I walk carefully."),
S("我刚充过电，精神很好。", "I just charged up, so I feel lively."),
S("这片地方安静，我留下。", "This place is quiet; I will stay."),
]
p['hurt'] = {
"generic": [
S("疼，我毛都竖起来了。", "Ouch, all my fur stands up."),
S("这一下把我电都打散了。", "That knocked the charge right out of me."),
S("我滚了两圈才停。", "I rolled twice before I stopped."),
S("别踩我尾巴，很疼的。", "Do not step on my tail; it really hurts."),
S("我缩成一团，装死。", "I curl into a ball and play dead."),
S("脸颊一麻，是疼还是电？", "My cheek tingles; pain or charge?"),
S("我吱了一声，声音很小。", "I squeak, very quietly."),
S("腿有点抖，但没断。", "My legs shake, but nothing is broken."),
S("我退到石头后面躲。", "I duck behind the stone."),
S("等一下，我还没缓过来。", "Give me a moment; I am not ready."),
],
"fire": [S("火一烤，我的毛尖卷了。", "The heat curled the tips of my fur.")],
"fall": [S("从高处掉下，我翻了身。", "I tumbled in the air before hitting the ground.")],
"drown": [S("我怕水，脚一直乱划。", "I hate water and paddle wildly.")],
"explosion": [S("响声太大，我耳朵嗡嗡。", "The blast was huge and my ears ring.")],
"projectile": [S("有东西擦过我的耳朵。", "Something grazed past my ear.")],
"magic": [S("光一照，我的电乱了。", "The light hit and my current scrambled.")],
"starvation": [S("肚子空了，电也弱了。", "My belly is empty and my sparks are weak.")],
"lightning": [S("天上的雷和我的电对上了。", "The sky's lightning answered my own.")],
"void": [S("这里没有地，我抓不住。", "There is no ground here; I cannot grip.")],
}
MOBS.append(("pixelmon:pawmi", p))

# ---------------- pawmo ----------------
p = {}
p['walk'] = [
S("我两脚走路，步子很稳。", "I walk on two legs with steady steps."),
S("拳头垂着，走路带风。", "Fists low, I walk with a breeze behind me."),
S("我踩实每一步，像在练功。", "I plant each step like a drill."),
S("我甩甩手，把电散掉一点。", "I shake my hands to shed some charge."),
S("路边那块石头，我跳过去。", "I hop over the stone by the path."),
S("我走在队伍前面，不回头。", "I walk ahead of the group without looking back."),
S("脚步落地的声音像鼓点。", "My footsteps land like drumbeats."),
S("我转身时，尾巴画个弧。", "When I turn, my tail draws an arc."),
S("我慢慢走，让电沉下来。", "I walk slowly and let the charge settle."),
S("这条路我熟，闭眼也走。", "I know this road well enough to walk blind."),
S("我抬脚跨过田埂。", "I lift a foot over the field ridge."),
S("有人在后面，我放慢。", "Someone is behind me, so I slow down."),
]
p['idle'] = [
S("我站着不动，练呼吸。", "I stand still and practise my breathing."),
S("手掌还有点麻，慢慢放掉。", "My palms still tingle; I let it fade."),
S("我一拳打在空气里，试力。", "I punch the air to test my strength."),
S("这一带的草被我踩平了。", "The grass here is flattened by my steps."),
S("我看看手心，有细小的火花。", "I check my palms; small sparks remain."),
S("腿有点酸，昨天跑太多。", "My legs ache; I ran too much yesterday."),
S("我在想下一招怎么出。", "I am thinking about my next move."),
S("风把汗吹干了。", "The wind dries the sweat on me."),
S("我把拳头握紧，又松开。", "I clench my fists, then let go."),
S("周围很安静，反而舒服。", "It is quiet around here, and I like it."),
S("我抬头，云走得很快。", "I look up; the clouds move fast."),
S("有只小鸟在看我，我不动。", "A small bird watches me and I hold still."),
S("我把脚边的石子踢开。", "I kick a pebble out of my way."),
S("歇够了，我就站起来。", "Once rested enough, I get up."),
]
p['look_player'] = [
S("你站得不错，重心很稳。", "You stand well, with a steady center."),
S("我看你的手，那是出拳的手。", "I study your hands; they know how to strike."),
S("要比一场吗？我不让招。", "Fancy a match? I will not hold back."),
S("你比我高，但我练过。", "You are taller, but I have trained."),
S("我慢慢点头，算打过招呼。", "I nod slowly, which counts as a greeting."),
S("你脚步虚，重心在左脚。", "Your stance is loose, weight on the left."),
S("我不喜欢有人站在我背后。", "I dislike anyone standing behind me."),
S("你的眼神没恶意，我放松。", "Your eyes hold no malice, so I relax."),
S("我把拳头放在身侧。", "I keep my fists down at my sides."),
S("你想摸我？先伸手让我看。", "You want to pet me? Show me your hand."),
S("我盯了你三秒，够了。", "Three seconds of staring is enough."),
S("我们是同类吗？不太像。", "Are we the same kind? Not really."),
S("你退了半步，我记下了。", "You stepped back half a pace; noted."),
S("我歪头，等你先说话。", "I tilt my head and wait for you to speak."),
]
p['tempted'] = [
S("那果子，你搁地上就行。", "That berry, just set it on the ground."),
S("我饿了，但我不抢。", "I am hungry, but I do not snatch."),
S("先给我闻闻，别靠太近。", "Let me smell it first, and not too close."),
S("我吃东西很快，别眨眼。", "I eat quickly, so do not blink."),
S("你手里还有吗？我看见了。", "Do you have more? I saw it."),
S("这一颗，我分两次吃。", "I will eat this one in two bites."),
S("我接过来，用两只手。", "I take it with both hands."),
S("味道不错，我记你的好。", "Good taste; I will remember the favor."),
S("我吃完会甩甩手，谢了。", "After eating I shake my hands in thanks."),
S("别逗我，我耐性一般。", "Do not tease me; my patience is average."),
]
p['collide'] = [
S("站稳，我可不轻。", "Steady there; I am not light."),
S("我用肩膀接住你，没倒。", "I caught you with my shoulder; you held."),
S("这一撞，我手都抬起来了。", "That bump brought my hands up."),
S("我们各退一步，扯平。", "We each step back; even now."),
S("你撞到我拳头了，疼吗？", "You bumped my fist; does it hurt?"),
S("我脚底打滑，差点摔。", "My feet slipped and I nearly fell."),
S("别从侧面推我。", "Do not shove me from the side."),
S("我低身稳住，没让你倒。", "I drop low and keep you upright."),
S("撞完我们都停了一会儿。", "After the bump we both pause."),
S("下次用走的，不用撞。", "Next time just walk; no need to collide."),
]
p['mate'] = [
S("我们把尾巴搭在一起。", "We lay our tails side by side."),
S("你出拳，我接，练得刚好。", "You punch, I block; we practise well together."),
S("以后巡路，我在前面。", "When we patrol, I take the front."),
S("这一片的石头，我替你搬。", "I will move these stones for you."),
S("累了就靠着我站会儿。", "When tired, lean on me a while."),
S("我手上的电会绕开你。", "My current will flow around you."),
S("我们分半，你吃大的。", "We split it; you take the bigger half."),
S("你听我心跳，一下一下。", "Listen to my heart, beat by beat."),
S("这处窝我压平了草。", "I flattened the grass for this nest."),
S("明天换你带路。", "Tomorrow you lead the way."),
]
p['pickup'] = [
S("这果子我捡了，分你一半。", "I picked up this berry; half is yours."),
S("我一只手就提起来了。", "I lift it with one hand."),
S("石头太重，我抱着走。", "The stone is heavy, so I hug it along."),
S("掉的东西，我先看清。", "I look closely before taking what fell."),
S("这个有电，我闻得出来。", "This one is charged; I can smell it."),
S("我把它们堆在石头下。", "I stack them under the rock."),
S("轻的归你，重的归我。", "Light things for you, heavy ones for me."),
S("我弯腰捡的时候，尾巴翘着。", "My tail lifts as I bend to pick it up."),
S("这堆是我攒的口粮。", "This pile is my saved ration."),
S("别帮忙，我自己来。", "Do not help; I can do it."),
]
p['target_acquire'] = [
S("它挡路了，我去清清。", "It blocks the path; I will clear it."),
S("我把拳头抬起，往前走。", "I raise my fists and walk forward."),
S("这家伙比上一个壮。", "This one is sturdier than the last."),
S("它看我，我也看它。", "It looks at me; I look back."),
S("我数它的脚步，找空档。", "I count its steps to find a gap."),
S("它叫了一声，是挑衅。", "It called out once, a challenge."),
S("我压低膝盖，准备贴上去。", "Knees bent, I prepare to close in."),
S("后面的交给同伴，我上前。", "I take the front; my companions cover the rest."),
S("它的手一直没抬起。", "Its hands have not come up."),
S("我先绕半圈，看清它。", "I circle half around to see it clearly."),
]
p['targeting'] = [
S("三步之内，我就能打到。", "Within three steps I can land a hit."),
S("它往前压，我侧身让。", "It presses forward; I turn aside."),
S("我掌心在发烫，电满了。", "My palms are hot, charged to the brim."),
S("它一出手，我就知道空了。", "When it swings, I know it missed."),
S("我盯着它膝盖，那里会软。", "I fix on its knee; that will buckle."),
S("它在退，我跟着压上去。", "It retreats and I press on."),
S("我脚下一转，换到侧面。", "I pivot and take its flank."),
S("再等一秒，它就会露空。", "One second more and it will open up."),
S("我的尾巴在稳重心。", "My tail is steadying my balance."),
S("这一拳，我留了后手。", "For this punch I keep a follow up."),
]
p['melee_attack'] = [
S("直拳打胸口，接着上勾。", "A straight punch, then an uppercut."),
S("我踢它膝侧，它站不稳。", "I kick the side of its knee."),
S("拳上带电，它半边发麻。", "Current on my fist leaves it numb."),
S("我抬手挡住它的爪。", "I raise my arm to block its claw."),
S("打中之后，我立刻退开。", "After the hit I step straight back."),
S("它扑空，我从下往上打。", "It misses, and I strike from below."),
S("这一记是练了半个月的。", "This one took half a month of practice."),
S("别站着挨，往侧边挪。", "Do not stand and take it; move aside."),
S("我把它撂倒，按住肩膀。", "I take it down and pin its shoulder."),
S("两声闷响，它退了三步。", "Two dull thuds, and it backs three steps."),
]
p['spawn'] = [
S("我落在草上，膝盖一弯。", "I land in the grass with knees bent."),
S("这里的风，适合练拳。", "This wind is good for training."),
S("我先看地形，再找退路。", "I check the ground, then my way out."),
S("十八级的林边，我来过。", "A level eighteen forest edge, familiar ground."),
S("我握拳试了一下，电很足。", "I test my fists; plenty of charge."),
S("四下无人，我松了肩。", "No one around, so I drop my shoulders."),
S("草叶擦过我的腿。", "Grass blades brush against my legs."),
S("我闻到了河水的味道。", "I smell river water nearby."),
S("先站一会儿，看清楚。", "I stand a moment and look around."),
S("我甩甩手，抖掉土。", "I shake the dirt off my hands."),
S("身后有脚步声，我转身。", "Footsteps behind me; I turn around."),
S("这地方能打，也能跑。", "This spot is good for fighting and fleeing."),
]
p['hurt'] = {
"generic": [
S("疼，但站得住。", "It hurts, but I am standing."),
S("这一下打中我肩膀。", "That one landed on my shoulder."),
S("我退了半步，又稳住。", "I give half a step, then steady."),
S("手上电散了，得重新攒。", "My charge scattered; I must build it again."),
S("我咬牙，把拳抬起来。", "I grit my teeth and raise my fists."),
S("别连着打，让我喘一下。", "Do not keep hitting; let me breathe."),
S("血从鼻子里流下来。", "Blood is running from my nose."),
S("这一下比想象的重。", "That was heavier than I expected."),
S("我护住肋，慢慢挪。", "I guard my ribs and shuffle back."),
S("还没结束，我还能打。", "It is not over; I can still fight."),
],
"fire": [S("火苗舔过我的耳朵。", "Flames licked across my ear.")],
"fall": [S("落地时我用膝盖顶住了。", "I caught the fall on my knees.")],
"drown": [S("水没过胸口，我挣不动。", "Water is at my chest; I cannot move.")],
"explosion": [S("冲击把我推到树上。", "The blast threw me into a tree.")],
"projectile": [S("箭卡进我的护腕。", "An arrow lodged in my wrist.")],
"magic": [S("那道光让我手脚发沉。", "That light made my limbs heavy.")],
"starvation": [S("饿得拳头发软。", "Hunger has made my fists weak.")],
"lightning": [S("雷落下来，我的电全乱了。", "Lightning struck and my current scattered.")],
"void": [S("脚下空空的，我抓不住力。", "Nothing underfoot; I cannot find leverage.")],
}
MOBS.append(("pixelmon:pawmo", p))

# ---------------- overrides for lines shared with other batches ----------------
REPL = {
"这一下让我退了半步。": ("挨了这一下，我靠住树干。", "I took the blow and leaned on the trunk."),
"这支箭钉在我肩上。": ("箭头卡在我肩胛骨缝里。", "The arrowhead is wedged between my shoulder blades."),
"炸开的土把我埋了半截。": ("爆炸掀翻落叶，我半截埋进土。", "The blast flipped the leaves and half buried me."),
"我伸手了，你最好松手。": ("我手掌摊开了，把果子放上来。", "My palm is open; set the berry here."),
"我退到石头后面喘气。": ("我钻到石头底下，光是喘。", "I duck under the stone and just pant."),
"我缩成一团，装死。": ("我缩紧身子，尾巴也收进来。", "I pull myself small and tuck my tail in."),
"我打了个小喷嚏，冒火星。": ("一个喷嚏，鼻尖跳出火星。", "One sneeze and a spark hops off my nose."),
"我滚了两圈才停。": ("我摔出去，草接住了我。", "I skid away and the grass catches me."),
"我被撞得翻了半圈。": ("这一下把我撞得翻了个身。", "That knocked me clean over onto my side."),
"我翻了半圈，又爬起来。": ("我在地上打了个滚，再站起。", "I roll on the ground, then get back up."),
"哎，你踩到我的尾巴。": ("喂，我的尾巴在你脚下。", "Oi, my tail is under your foot."),
"掉在地上的，都是我的。": ("土里滚过的种子，全归我。", "Any seed that hits the dirt belongs to me."),
"我抖掉背上的草籽。": ("背上粘的草籽，我一颗颗抖掉。", "I flick the grass seeds off my back one by one."),
"我在数草叶，数到一半忘了。": ("我数着草茎，数到七就乱了。", "Counting grass stems, I get confused at seven."),
"它退了半步，我进一步。": ("它往后挪，我就往前挪。", "It shuffles back, so I shuffle forward."),
"靠近点，让我闻闻你。": ("凑近些，我要认你的气味。", "Lean in a bit; I want to learn your scent."),
"你身上有静电的味道。": ("你袖口有细小的静电声。", "Your sleeve carries a faint crackle of static."),
"你退了半步，我记下了。": ("你后退那一下，我记在心里。", "That step you took back stays in my mind."),
"再近一点，我就能碰到。": ("它再挪一寸，我的爪子就到。", "One inch nearer and my paw arrives."),
"我再靠近一点，就一点。": ("我挪过去半步，先试探一下。", "I edge half a step over, just testing."),
"我把它推到你脚边。": ("我拿鼻子把它拱到你脚前。", "I nudge it with my nose to your feet."),
"这是我的，别伸手。": ("这是我先看见的，别拿。", "I saw it first, so leave it alone."),
"我盯着它的脚，不看眼。": ("我看它的前脚，眼睛会骗人。", "I watch its front feet; eyes can lie."),
"我看你，你也看我，谁先动？": ("两个人对着看，谁先眨眼？", "Two of us staring; who blinks first?"),
"我绕着你转，找破绽。": ("我贴着你靴子转，找空子。", "I pad around your boots, hunting a gap."),
"饿是饿了，但懒得动。": ("肚子叫了，我还是不想动。", "My stomach growls, and I still will not move."),
"甜的东西我最没辙。": ("一见甜的，爪子就不听话。", "Around anything sweet my paws stop listening."),
"这处草够高，能藏住我。": ("草高过我的耳朵，正好藏身。", "The grass rises past my ears, perfect cover."),
"我从石缝里钻出来。": ("我从两块石头之间的缝挤出来。", "I worm my way out between two stones."),
"你差点把我踩扁。": ("你的鞋底差点落在我头上。", "Your boot sole nearly came down on my head."),
"你蹲下来，我才能看清。": ("你弯下腰，我才看得清你的脸。", "Bend down and I can see your face."),
"我歪头，等你先说话。": ("我把头一歪，先听你说。", "Head tilted, I listen for you to start."),
"亮亮的东西我都想捡。": ("看见会反光的东西，我就想叼走。", "Anything that glints, I want to carry off."),
"我抱着它走，走两步掉了。": ("我叼着它，走三步就掉了。", "I hold it in my teeth and lose it in three steps."),
"我先闻一下，再塞进怀里。": ("鼻子碰一碰，再藏到腋下。", "One touch of the nose, then under my arm."),
"我饿了，但我不抢。": ("我饿着，也不会伸手抢。", "Hungry as I am, I will not grab."),
"这一下打中我肩膀。": ("肩膀挨了一记，有点沉。", "A heavy blow caught me on the shoulder."),
"炸响把我掀进草里。": ("一声炸响，我摔进草堆。", "A blast sent me tumbling into the weeds."),
"它动一下，我跟着动。": ("它一动，我的脚就跟着动。", "The instant it stirs, my feet answer."),
"我仰头看你，脖子有点酸。": ("我仰着脖子看你，酸得很。", "Craning up at you, my neck complains."),
"我把拳头握紧，又松开。": ("拳头先攥紧，再慢慢摊开。", "My fists tighten, then slowly open."),
"有东西擦过我的耳朵。": ("一道影子擦过我的耳根。", "A shadow cut past the base of my ear."),
"给我一小口，就一小口。": ("咬一小口就好，真的。", "A tiny bite will do, truly."),
"肚子空了，电也弱了。": ("饿得连火花都点不亮。", "Too hungry to strike even a spark."),
"这条路我熟，闭眼也走。": ("这条道我走了几十遍。", "I have walked this trail dozens of times."),
}
name, data = REPL["挨了这一下，我靠住树干。"]

for _, scen in MOBS:
    for skey, sv in scen.items():
        groups = sv.values() if skey == "hurt" else [sv]
        for g in groups:
            for line in g:
                if line["zh"] in REPL:
                    zh, en = REPL[line["zh"]]
                    line["zh"], line["en"] = zh, en

# ---------------- validate & write ----------------
SCEN = ["walk", "idle", "look_player", "tempted", "collide", "mate",
        "pickup", "target_acquire", "targeting", "melee_attack", "spawn"]
HURT_TYPES = ["fire", "fall", "drown", "explosion", "projectile", "magic",
              "starvation", "lightning", "void"]

plan = json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))['u0281']
weights = {m['mob_id']: m['weights'] for m in plan}

def cjk_len(s):
    return len(s)

problems = []
seen = set()
out = {"batch": "u0281", "mobs": []}
total = 0
for mob_id, scen in MOBS:
    w = weights[mob_id]
    entry = {"mob_id": mob_id, "scenarios": {}}
    for k in SCEN:
        base = scen[k]
        extra = max(0, min(4, round(10 * (w[k] - 1))))
        want = 10 + extra
        if len(base) != want:
            problems.append(f"{mob_id}.{k} count {len(base)} != {want}")
        entry["scenarios"][k] = base
        total += len(base)
    h = scen["hurt"]
    if len(h["generic"]) != 10:
        problems.append(f"{mob_id}.hurt.generic count {len(h['generic'])}")
    for t in HURT_TYPES:
        if len(h[t]) != 1:
            problems.append(f"{mob_id}.hurt.{t} count {len(h[t])}")
    entry["scenarios"]["hurt"] = h
    total += 19
    out["mobs"].append(entry)

for m in out["mobs"]:
    for k, v in m["scenarios"].items():
        groups = v.values() if k == "hurt" else [v]
        for g in groups:
            for line in g:
                z, e = line["zh"], line["en"]
                if not (6 <= len(z) <= 20):
                    problems.append(f"zh len {len(z)}: {z}")
                if not (4 <= len(e.split()) <= 14):
                    problems.append(f"en words {len(e.split())}: {e}")
                if z in seen:
                    problems.append(f"dup zh: {z}")
                seen.add(z)
                if e in seen:
                    problems.append(f"dup en: {e}")
                seen.add(e)
                if re.search(r'[A-Za-z]{3,}', z) or re.search(r'[\u4e00-\u9fff]', e):
                    problems.append(f"language mix: {line}")

if problems:
    print("\n".join(problems))
    print("PROBLEMS", len(problems))
else:
    with open('data/dialogue/unique/u0281.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("ok", len(out["mobs"]), total)
