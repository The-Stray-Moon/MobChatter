# -*- coding: utf-8 -*-
import json, io


def P(block):
    out = []
    for raw in block.strip().splitlines():
        raw = raw.strip()
        if not raw:
            continue
        zh, en = raw.split("|")
        out.append({"zh": zh.strip(), "en": en.strip()})
    return out


poipole = {
"walk": P("""
毒针朝前，我踩着异世界的土。|Poison needle forward, I tread another world's soil.
我这颗大头一颠一颠地走。|My big head bobs with every step I take.
针尖滴下一滴紫色的汗。|A drop of purple sweat falls from my needle.
我在地面上试着自己的腿。|I test my own legs here on solid ground.
走一步，嗡嗡声就高一格。|Each step lifts my humming one note higher.
别怕，我只想跟着你走。|Don't be afraid; I only want to walk beside you.
四十级的力气，脚步很轻。|At level forty, my steps are still light.
我把毒收好，只留下脚印。|I tuck my poison away and leave only footprints.
异世界的风推着我向前。|Another world's wind pushes me forward.
这条路我打算走很久。|I intend to walk this road a long while.
针在头顶晃，像根小旗子。|My needle sways overhead like a tiny flag.
慢慢走，别踩坏你的花。|I walk slowly so I won't crush your flowers.
"""),
"idle": P("""
我把毒针转过来又转过去。|I turn my poison needle back and forth.
嗡嗡的低音从我喉咙里出来。|A low hum rises out of my throat.
这里的天空，和异世界不同。|This sky is nothing like the one back home.
我数着草叶上的光点数数。|I count the flecks of light on the grass.
针尖不滴毒的时候很安静。|My needle is quiet when no poison drips.
我在想，旅伴该是什么样子。|I wonder what a traveling companion should be.
究极异兽也会坐着发呆的。|Even an Ultra Beast can sit and stare.
大脑袋歪着，什么也没想。|My big head tilts; I am thinking nothing.
我闻了闻空气里的甜味。|I sniff the sweetness floating in the air.
有人愿意带我走吗？|Would anyone be willing to take me along?
我把身体缩成一团暖的。|I curl my body into one warm knot.
毒囊里还存着一点，够用。|There is a little left in my poison sac.
我听见远处有同伴在叫。|I hear a companion calling from far away.
待着也好，不用一直赶路。|Staying put is fine; we need not always hurry.
"""),
"look_player": P("""
我抬头，用针尖对着你的脸。|I look up and point my needle at your face.
你眼里有我认不出的星星。|Your eyes hold stars I do not recognize.
你也从另一个世界来吗？|Did you come from another world too?
我歪头，想读懂你的表情。|I tilt my head, trying to read your face.
别躲，我的毒收在针里。|Don't flinch; my poison stays in the needle.
我一直盯着你手里的球。|I keep staring at the ball in your hand.
你这样看我，我会害羞的。|Looking at me like that makes me shy.
你能带我上路吗，就一次。|Will you take me along, just this once?
我记住你走路的样子了。|I have memorized the way you walk.
人类的手，比我想的小。|Human hands are smaller than I imagined.
你在犹豫，我看得出来。|You are hesitating; I can tell.
我把针收低一点，够友好了吧。|I lower my needle; is this friendly enough?
你的影子正好落在我头上。|Your shadow falls right across my head.
我一直看着，直到你先走开。|I keep watching until you look away first.
"""),
"tempted": P("""
那味道甜得像异世界的果子。|That smell is sweet as otherworld fruit.
是给我的吗？我先闻一闻。|Is that for me? Let me sniff it first.
我的针不听话地抖起来了。|My needle is trembling without permission.
只要一口，我就跟你走。|Just one bite, and I will follow you.
这味道让我忘了自己是异兽。|This smell makes me forget I'm an Ultra Beast.
我凑近，又怕吓到你。|I lean close, then fear I'll frighten you.
好吃的东西，比战斗重要。|Good food matters more than any battle.
我的毒囊在催我咬一口。|My poison sac is urging me to take a bite.
你手里是不是还有？|Is there more of that in your hand?
我让步了，我不擅长忍。|I give in; patience is not my strength.
"""),
"collide": P("""
撞上你，我针尖赶紧偏开。|I bump you and jerk my needle aside.
对不起，我的头太靠前了。|Sorry, my head sticks out too far.
这一下撞得我嗡嗡直响。|The knock set me humming out loud.
我退开半步，把毒收回去。|I step back and pull my poison in.
别怕，撞到的是硬壳那面。|Don't worry, you hit my hard side.
我太矮，正好撞到你膝盖。|I'm short enough to hit your knees.
这身体比看上去要结实。|This little body is tougher than it looks.
我蹭了你一下，算打招呼。|I brush against you as a greeting.
撞疼了吗？我看看。|Did that hurt? Let me look at it.
我以为你会让开的。|I assumed you would step aside.
"""),
"mate": P("""
同伴之间，这样靠一靠就好。|Companions only need to lean together.
我把针收平，不扎到对方。|I flatten my needle so it cannot sting.
异世界也有愿意留下的人。|Even my world has someone worth staying for.
我们一起嗡嗡，声音合上了。|We hum together and our voices match.
找同伴比找对手难多了。|Finding a companion is harder than a rival.
我轻轻碰了碰它的针。|I tap its needle gently with mine.
这一路，总算不只我一个。|At last this road holds more than me.
我记下了它的味道。|I have memorized its scent now.
别走太远，我会跟丢。|Don't wander far; I might lose you.
我们并排，谁也不用开口。|We stand side by side needing no words.
"""),
"pickup": P("""
这个亮的东西，我捡起来了。|I picked up this bright little thing.
我用针尖挑起，递给你。|I lift it on my needle and offer it.
地上掉的，应该有人要吧。|Someone must want what fell here.
我叼着，走得一摇一晃。|I carry it in my mouth, swaying as I walk.
异世界的规矩，捡到就留着。|Where I'm from, you keep what you find.
这个能换一口吃的吗？|Could this be traded for a bite to eat?
我把它放进你手心里。|I place it in the middle of your palm.
我捡东西，从来不留名。|I take what I find and leave no name.
太小了，差点没看见。|It was so small I almost missed it.
收好，别让它再掉了。|Keep it safe so it doesn't drop again.
"""),
"target_acquire": P("""
那东西在动，我盯上它了。|That thing is moving; I've got my eye on it.
我的针尖对准了它的方向。|My needle points straight at its direction.
第一次交手，我先看清。|First meeting—I will watch before I strike.
它比我大，但我不怕。|It's bigger than me, but I'm not afraid.
毒要省着用，先靠近。|Poison must be saved; I'll close in first.
我低低地嗡了一声，警告它。|I hum low, once, as a warning.
这一战，我不打算拖长。|I don't intend to drag this fight out.
它闻不出我身上的毒。|It cannot smell the poison on me.
我往前挪半步，它退了。|I shift half a step and it retreats.
好了，目标锁定。|Good—the target is locked in.
"""),
"targeting": P("""
我在等它露出侧面。|I am waiting for it to show its flank.
针尖上的毒，慢慢渗出来。|Poison seeps slowly onto my needle tip.
它一动，我就跟着转。|When it moves, I turn with it.
呼吸放慢，别让它听见。|Slow my breathing so it cannot hear.
我算着距离，还差两步。|I measure the gap: two steps still.
它怕毒，我从它的眼神看出来。|It fears poison; I see that in its eyes.
再等一会儿，就一会儿。|Just a little longer—only a little.
我压低身子，短腿绷紧。|I crouch low and tense my short legs.
它转身了，机会来了。|It turns away; my chance is here.
我不喊，喊了就咬不中。|I stay silent; a shout would spoil the bite.
"""),
"melee_attack": P("""
毒针一送，扎进它的侧腹。|My needle goes in, deep in its side.
我撞过去，用整个脑袋。|I charge with the whole of my head.
一点毒，够它麻上一阵。|A little poison will numb it for a while.
我咬着不放，尾巴甩来甩去。|I bite and hold, my tail whipping about.
它扑空了，我从下面顶上去。|It misses; I shove up from below.
针收回去的声音很轻。|My needle slides back out almost silently.
别怪我，是你先动手的。|Don't blame me—you struck first.
这一下我只用了一半毒。|I used only half my poison on that one.
它退了，我没有追。|It pulled back, and I did not chase.
打完我就开始嗡，压不住。|After fighting I hum, and cannot stop it.
"""),
"spawn": P("""
我从异世界的裂缝里掉出来。|I fell out of a rift from another world.
这里的重力，好像轻一点。|Gravity here feels a little lighter.
四下都是草，没有我的针草。|Grass everywhere, none of my needle grass.
四十级的第一天，从我脚下开始。|Level forty begins under my feet today.
我在陌生的土上站稳了。|I have found my footing on strange soil.
有人在附近，我闻到了。|Someone is nearby; I can smell them.
毒针先亮，再收回去。|My poison needle glints once, then retracts.
这个世界比我想的亮。|This world is brighter than I expected.
我试着叫一声，声音很陌生。|I try a call; my voice sounds unfamiliar.
落地时我先看看有没有同伴。|On landing, I first look for companions.
我又一次站在了旅程的起点。|Once again I stand where a journey begins.
这一次，我想跟人一起走。|This time, I want to travel with someone.
"""),
"hurt": {
"generic": P("""
针被撞歪了，我扶正它。|My needle is bent; I straighten it.
毒漏出来一点，很浪费。|A little poison leaked—what a waste.
我这小身子骨，别打太重。|I'm small; please don't hit so hard.
疼得我嗡嗡声都变调了。|It hurt enough to warp my humming.
我缩成一团，护住针尖。|I curl up and shield my needle tip.
这一下从异世界跟到了这里。|That blow followed me from another world.
我还站得住，别担心。|I can still stand—don't worry about me.
伤在背上，我看不见。|The wound is on my back where I can't see.
我退开，先让毒缓一缓。|I back off and let my poison settle.
痛是痛，可我还没想跑。|It hurts, but I'm not running yet.
"""),
"fire": P("""火烤到针尖，毒都干了。|Fire on my needle dried the poison out."""),
"fall": P("""从高处掉下，针先着地。|I fell from a height, needle first."""),
"drown": P("""我不该在深水里逞强。|I should not have braved deep water."""),
"explosion": P("""爆炸把我推得翻了半圈。|The blast flipped me half around."""),
"projectile": P("""一支箭擦过我的侧腹。|An arrow grazed along my flank."""),
"magic": P("""那股力量在我毒囊里打转。|That force is churning in my poison sac."""),
"starvation": P("""毒囊空了，肚子也空了。|My poison sac is empty, and so is my belly."""),
"lightning": P("""雷打在我针上，全身发麻。|Lightning struck my needle and numbed me all over."""),
"void": P("""我掉出这个世界，针还亮着。|I fell out of this world, needle still glowing."""),
},
}

politoed = {
"walk": P("""
我一步一步，走在队伍最前面。|Step by step, I walk at the front of the group.
皇冠似的卷毛在风里抖。|My crown of curls shivers in the wind.
身后的蝌蚪们跟得很整齐。|The tadpoles behind me keep perfect order.
水面被我一脚踩出圆纹。|Each step presses a round ring into the water.
我落地很稳，水花不大。|I land steadily, throwing only small splashes.
走这条路，我说了算。|On this road, my word decides things.
我的叫声还压在喉咙里。|My call stays pressed down in my throat.
巡一圈领地，顺便看看水草。|I patrol my land and check the weeds.
蛙的步子，比看起来要远。|A frog's stride reaches farther than it looks.
别踩到小的，绕开走。|Don't step on the little ones; walk around.
水边归我管，路上也归我管。|I rule the bank, and the road as well.
三十级以后，我才走得这么稳。|Past level thirty, I walk this steadily.
皇者不必快，只要不偏。|A king needn't be fast, only sure.
我回头点一下数，一只不少。|I look back and count—not one is missing.
"""),
"idle": P("""
我蹲在水边，肚子一鼓一鼓。|I squat by the water, my belly swelling.
卷毛里藏着一只小虫，随它去。|A bug hides in my curls; I let it stay.
只要我开口，蝌蚪就会安静。|When I speak, the tadpoles fall silent.
蚊香蛙皇的皇冠，其实是毛。|This crown of mine is only hair.
我听着水下的动静。|I listen to the sounds beneath the water.
水属性，可我也怕干。|I am a Water type, yet I dread drying out.
这一片蛙鸣，都是我教出来的。|Every croak here is one I taught.
我把脚蹼摊开晾着。|I spread my webbed feet out to dry.
有什么在草丛里动，不管它。|Something stirs in the grass; I ignore it.
领袖也得有空坐着。|Even a leader deserves time to sit.
我试着叫一声，水纹就散了。|I try one call and the ripples scatter.
前辈说过，皇者要沉住气。|My elders said a king must stay calm.
肚子饿了，可我不想动。|I'm hungry, and I'd rather not move.
我数着水面的泡泡。|I count the bubbles breaking on the surface.
"""),
"look_player": P("""
你站得太近了，人类。|You stand too close, human.
我抬眼，从卷毛底下看你。|I raise my eyes and look from under my curls.
你手里那根竿子，我认得。|I know that rod in your hands.
我的叫声，你听得懂吗？|Can you understand my call?
别伸手，先让我看看你。|Keep your hand back; let me look at you first.
你身上没有水味，奇怪。|You carry no smell of water—strange.
我慢慢眨眼，这是好意。|I blink slowly; that means goodwill.
你想钓我？我早看见了。|You mean to fish for me? I saw it.
我歪头，卷毛跟着晃。|I tilt my head and my curls sway with it.
三四十级的人，我见得多。|I've met many trainers level forty and up.
你的影子挡住了我的水。|Your shadow is blocking my water.
我不怕你，只是不想动。|I'm not afraid of you, just unwilling to move.
你退一步，我们再谈。|Step back one pace, then we can talk.
我看着你，直到你先低头。|I watch you until you lower your eyes first.
"""),
"tempted": P("""
那饵的味道，隔着水就来了。|That bait's smell reaches me through the water.
我是皇者，可我也馋。|I am a king, but I still have cravings.
你别以为叫一声我就跳。|Don't think one call makes me jump.
这味道像是谁特意配的。|This scent seems mixed just for me.
我往前挪了一步，就一步。|I shift forward one step—only one.
蝌蚪们在看，我得端着。|The tadpoles are watching; I must keep poise.
好饵难得，我承认。|Good bait is rare; I'll admit that.
你退后，我再靠近。|Move back, and I will come closer.
我的肚子先答应了。|My belly said yes before I did.
就这一次，别到处说。|Just this once—and don't tell anyone.
"""),
"collide": P("""
你撞到皇者了，注意点。|You bumped a king; mind your step.
我的身子滑，撞了也不疼。|My body is slick; the bump didn't hurt.
我稳住脚蹼，没有倒。|I braced my webbed feet and did not fall.
这一下撞散了我的队形。|That knock broke up my formation.
我退开，把路让给你。|I step aside and let you pass.
皇者不跟人计较这一下。|A king won't hold a bump against you.
我的卷毛被撞歪了。|My curls got knocked crooked.
撞上来的时候，水花四溅。|Water flew everywhere when we collided.
站稳，别踩到我的蝌蚪。|Steady—don't step on my tadpoles.
下次先喊一声。|Next time, call out first.
"""),
"mate": P("""
我把叫声放低，只给它听。|I lower my call so only it can hear.
两只蛙并排蹲着，很安静。|Two frogs squat side by side, very quiet.
它的卷毛比我翘得高。|Its curls stand higher than mine.
我们叫了一夜，水边都是回音。|We called all night; the bank kept echoing.
蝌蚪们会有个好队伍。|These tadpoles will grow into a fine group.
我轻轻碰了碰它的额头。|I gently touch my forehead to its own.
皇者也有需要陪着的时候。|Even a king sometimes needs company.
这一片水，够我们两家用。|This stretch of water serves both our families.
我们分着叫，一高一低。|We take turns calling, one high, one low.
它点头了，那我就留下。|It nodded; then I will stay.
"""),
"pickup": P("""
水里漂来的东西，我捡了。|I picked up what drifted in on the water.
用脚蹼夹住，稳稳的。|I hold it between my webbed feet.
这玩意儿，是哪个粗心鬼掉的。|Whose carelessness dropped this thing here?
我把它推到你脚边。|I nudge it over to your feet.
皇者也要管水面的干净。|A king keeps his water surface clean too.
这里面好像有东西在响。|Something seems to rattle inside this.
我拎起来看了看，又放下。|I lift it, look, and set it down.
谁的，自己来拿。|Whoever owns this, come and claim it.
我捡的都是水里的。|Everything I pick up comes from the water.
这个留给蝌蚪当玩具。|This can be a toy for the tadpoles.
"""),
"target_acquire": P("""
有东西进了我的水域。|Something has entered my waters.
我停下叫声，先听清它。|I stop calling and listen to it first.
那影子不顺眼，我盯上了。|That shape offends me; I've marked it.
皇者出手，先立规矩。|When a king acts, he sets terms first.
它踩坏了水边的草。|It trampled the grass along the bank.
我鼓一口气，喉咙热起来。|I draw a breath and my throat warms.
我朝它游过去，不快不慢。|I swim toward it, neither fast nor slow.
这一片归我，它得知道。|This place is mine; it must learn that.
我先叫一声，算最后警告。|I call once—my final warning.
好了，它没退。|Good—it did not back away.
"""),
"targeting": P("""
我在等它靠近水边。|I wait for it to near the water's edge.
脚蹼贴着水底，一动不动。|My webbed feet press the bottom, perfectly still.
它每动一下，我算一步。|Every move it makes, I count one step.
它以为蛙跳不远。|It thinks a frog cannot jump far.
我把嘴里的气憋住。|I hold the air inside my mouth.
再近一点，我就能压住它。|A little closer and I can pin it down.
卷毛底下，我一直看着。|From under my curls, I never stop watching.
它转身去顾别处了。|It turned to mind something else.
我的腿已经蹲好了。|My legs are already crouched and ready.
就是现在，它露出破绽。|Right now—it has shown an opening.
"""),
"melee_attack": P("""
我一跳，整个身子压下去。|I leap and bring my whole body down.
脚蹼拍在它脸上，很响。|My webbed feet slap its face loudly.
我用头撞，卷毛先到。|I ram with my head; my curls arrive first.
这一下把它推退了两步。|That shove pushed it back two steps.
水里我更快，它跟不上。|In water I'm faster; it cannot keep up.
我压住它，等它认输。|I pin it down and wait for surrender.
皇者动手，一次就够。|A king strikes once, and that suffices.
它滑开了，我再来一次。|It slipped free; I'll try again.
我的叫声也震得它后退。|Even my call pushes it back a step.
打完我理了理卷毛。|When it's done, I smooth my curls.
"""),
"spawn": P("""
我从水里被钓线拉了上来。|A fishing line drew me up out of the water.
超级钓竿，专钓我这样的。|A Super Rod—made for catching my kind.
三十级的第一次呼吸，很凉。|My first breath at level thirty is cold.
这岸边的草，比旧地方矮。|The grass on this bank is shorter than home.
我落到水边，先找蝌蚪。|I land by the water and look for tadpoles.
四下没有同类，只有风。|No kin anywhere—only wind.
我抖掉身上的水。|I shake the water from my body.
新的水域，得重新立规矩。|New waters mean new rules to establish.
卷毛湿了，等它干。|My curls are wet; I'll wait for them to dry.
我叫一声，看有没有回音。|I call once to see if anything answers.
这地方安静得不太对。|This place is quiet in a way that bothers me.
从今天起，这里由我来看。|From today, I will watch over this place.
"""),
"hurt": {
"generic": P("""
这一下撞在我滑溜溜的皮上。|That blow landed on my slippery skin.
我退了一步，脚蹼踩空了。|I fell back a step and missed my footing.
皇者也会疼，别笑。|A king feels pain too; don't laugh.
卷毛上蹭掉了一块。|A patch got scraped off my curls.
我闷哼一声，没叫出声。|I grunt once and keep from crying out.
疼，可我更在意丢脸。|It hurts, but the shame bothers me more.
我蹲低，把重心放稳。|I crouch lower and settle my weight.
这一下是从侧面来的。|That one came in from my flank.
我舔了舔伤处，有点咸。|I lick the wound; it tastes of salt.
别追，我还能站着。|Don't press on—I can still stand.
"""),
"fire": P("""火烤到我的皮，一下就白了。|Fire charred my skin pale in an instant."""),
"fall": P("""从岸上摔下去，脚蹼先着地。|I fell off the bank, webbed feet first."""),
"drown": P("""皇者也会呛水，别传出去。|Even a king can choke on water—keep it quiet."""),
"explosion": P("""爆炸把水掀起来，我被打翻。|The blast threw up water and flipped me over."""),
"projectile": P("""一支箭钉在我肩边。|An arrow stuck in beside my shoulder."""),
"magic": P("""那股力量穿过我，叫声都乱了。|That force passed through me and broke my call."""),
"starvation": P("""水边的虫子少得可怜。|There are pitifully few bugs by this water."""),
"lightning": P("""雷落进水里，我全身一麻。|Lightning hit the water and numbed me everywhere."""),
"void": P("""水没了，我掉进空的地方。|The water ended and I fell into nothing."""),
},
}

poliwag = {
"walk": P("""
我摆尾巴，一点点往前。|I swish my tail and inch forward.
刚长出的脚，总是绊自己。|My new legs keep tripping each other.
走三步，滑一下。|Three steps, and one slip.
水面上我走得很轻。|On the water's surface my steps are light.
尾巴先动，脚才跟上。|My tail moves first; my feet follow.
这双腿走路像划水。|These legs walk the way I swim.
我才十级，别走太快。|I'm only level ten; don't walk so fast.
薄皮底下，能看见我在动。|Through my thin skin you can see me move.
我绕着水草走了一圈。|I made one loop around the water weeds.
脚一软，我差点趴下。|My legs gave way and I nearly flopped down.
我顺着水面漂一小段。|I drift along the surface for a short stretch.
走不稳，可我不想停。|I walk unsteadily, but I don't want to stop.
"""),
"idle": P("""
我肚子上的螺旋慢慢转。|The spiral on my belly turns slowly.
尾巴一下一下，打着水。|My tail taps the water, one beat at a time.
隔着薄皮，能看见我的心脏。|Through my thin skin you can see my heart.
我把脚缩起来，不用它们。|I tuck my legs in and do without them.
水边的草，晃得我发困。|The bank grass sways and makes me drowsy.
十级的日子，过得很慢。|Life at level ten passes very slowly.
我试着跳，落回原处。|I try to hop and land where I started.
泡泡从嘴里飘出去几个。|A few bubbles drift out of my mouth.
这片水浅，正好给我。|This water is shallow—perfect for me.
我的圆身子晃了一晃。|My round body rocks once.
有只虫落在水面上，我没动。|A bug landed on the water; I didn't move.
我在想长大以后会怎样。|I wonder what I'll be when I grow up.
尾巴比脚好用多了。|My tail works far better than my legs.
我吐个泡，看它破掉。|I blow a bubble and watch it pop.
"""),
"look_player": P("""
你蹲下来，我就看得清。|If you crouch down, I can see you clearly.
我抬头，肚子贴在水上。|I look up with my belly against the water.
你手里的东西，亮亮的。|The thing in your hand is shiny.
我的螺旋，你看见了吗？|Did you see the spiral on my belly?
别用竿子指着我。|Don't point that rod at me.
你比我想的要高很多。|You are much taller than I expected.
我眨眼，水珠就掉了。|I blink and the water drops fall.
我没见过这么近的人。|I have never seen a human this close.
你在笑，我看得见。|You're smiling; I can see it.
我的眼睛长在头顶两边。|My eyes sit on either side of my head.
你能带我离开这浅水吗？|Could you carry me out of these shallows?
我歪头，尾巴跟着摆。|I tilt my head and my tail follows.
我盯着你看，忘了害怕。|I stare at you and forget to be afraid.
你先动，我就游开。|If you move first, I will swim away.
"""),
"tempted": P("""
那味道顺水漂过来了。|That smell drifted over on the water.
是甜的，还是咸的？|Is it sweet, or is it salty?
我游近了一点，又停住。|I swim a little closer, then stop.
我的尾巴先替我答应了。|My tail answered yes before I did.
这么小的嘴，也吃得下。|Even this small mouth can manage it.
你撒在水面上的东西，我看见了。|I saw what you scattered on the water.
我怕有钩子，可又想吃。|I fear the hook, and still I want it.
再飘近一点，就一点。|Let it drift closer—just a little.
我张了张嘴，没咬。|I opened my mouth and did not bite.
好吧，我游过去，就一口。|Fine, I'll swim over for one bite.
"""),
"collide": P("""
我被撞得在水面转圈。|The bump spun me around on the surface.
我的皮很薄，轻点撞。|My skin is thin; bump me gently.
这一下压到我的尾巴了。|That one pressed down on my tail.
我滑开了，像块湿石头。|I slid away like a wet stone.
脚又没站稳，摔了个跟头。|My feet failed me and I tumbled over.
你踩到水花，溅我一脸。|You splashed me right in the face.
我退到草边，躲一下。|I retreat to the grass edge and hide.
撞完我还得重新游。|After the bump I must swim back into place.
我的身子太软，不顶撞。|My body is too soft to take a hit.
对不起，我没看路。|Sorry, I wasn't watching where I went.
"""),
"mate": P("""
我们并排浮着，尾巴碰尾巴。|We float side by side, tails touching.
它的螺旋比我转得快。|Its spiral turns faster than mine.
两个泡泡，一起破了。|Two bubbles, and they pop together.
这么小的水洼，也够我们。|Even this small pool is enough for us.
我碰了碰它刚长的脚。|I touched its newly grown legs.
以后会有一群小的。|There will be a crowd of little ones later.
我们谁也没说话，水声够了。|Neither spoke; the water said enough.
它的尾巴扫过我的背。|Its tail brushed across my back.
我跟着它，慢一点也没关系。|I follow it; slower is fine.
这一片水，我们分着用。|We'll share this stretch of water.
"""),
"pickup": P("""
水底这个，我捞上来了。|I fished this up from the bottom.
我把它顶在头上，很稳。|I balance it on my head; it holds.
会沉的东西，我推不动。|I can't push the things that sink.
这个亮片，是谁掉的？|Whose shiny flake is this?
我用嘴叼着，游回去。|I carry it in my mouth and swim back.
太小了，差点滑走。|It's so small it nearly slipped away.
我把它放在你脚边的石头上。|I set it on the stone by your feet.
水里捡的，都是我的。|Whatever I find in the water is mine.
这个能当盖子玩。|This could work as a lid to play with.
我抱着它，浮不起来。|I hold it and cannot stay afloat.
"""),
"target_acquire": P("""
水里有东西在动。|Something is moving in the water.
我压低身子，尾巴停住。|I flatten down and my tail goes still.
它比我大，我先看看。|It's bigger than me; I'll watch first.
那是敌人，还是同伴？|Is that an enemy, or one of us?
我对着它的方向吐了个泡。|I blew a bubble toward its direction.
它若过来，我就撞。|If it comes near, I will ram it.
我十级，也敢盯着它。|Level ten, and still I stare it down.
它踩乱了水面，我不喜欢。|It muddied the surface; I don't like that.
我的脚往后撑稳了。|My legs are braced back firmly.
好了，我知道它在哪。|Good—I know where it is now.
"""),
"targeting": P("""
我跟着它的影子转。|I turn with its shadow.
水面一晃，我就知道它动了。|When the water shakes, I know it moved.
我等着它靠近水草。|I wait for it to come near the weeds.
尾巴绷紧，准备拍水。|My tail tenses, ready to slap the water.
它没看见我这双眼睛。|It hasn't seen these eyes of mine.
再近一步，我就能撞到。|One step closer and I can hit it.
我屏住呼吸，泡也不吐。|I hold my breath and blow no bubbles.
它转身，我立刻跟上去。|It turns, and I follow at once.
这个距离，我算得准。|At this distance I can judge it well.
我没出声，水帮我藏着。|I make no sound; the water hides me.
"""),
"melee_attack": P("""
我用整个身子撞过去。|I throw my whole body at it.
尾巴一甩，水花打在它脸上。|My tail lashes water into its face.
我咬住它，牙不多但够用。|I bite down; few teeth, but enough.
这一撞，我自己也弹开了。|I bounced off it as well.
它被我弄得站不稳。|I left it struggling for footing.
我撞完就退，不恋战。|I hit and retreat; no lingering.
我的螺旋转得飞快。|My spiral is spinning fast.
它甩开我，我翻了个身。|It flung me off and I rolled over.
十级的身子在发抖。|My level-ten body is trembling.
赢了，可我也累了。|I won, and I'm tired too.
"""),
"spawn": P("""
我浮上水面，第一次呼吸。|I surface and take my first breath.
这片水面很宽，我游得开。|This water is wide; I have room to swim.
十级的清晨，水是凉的。|The morning at level ten is cold water.
我旁边没有别的蝌蚪。|There are no other tadpoles beside me.
我从水里钻出来，四处看。|I poke out of the water and look around.
尾巴先动，我才醒过来。|My tail moves before I fully wake.
岸上站着人，很高。|A person stands on the bank, very tall.
我的脚还没学会踩地。|My legs have not learned to stand on land.
这片草，看起来能吃。|This grass looks like something to eat.
我叫不出声，只有泡泡。|I can't call yet—only bubbles come.
新的水域，水纹也是新的。|New water, and even the ripples are new.
我要在这里长到更大。|I will grow bigger here.
"""),
"hurt": {
"generic": P("""
我的皮太薄，一碰就红。|My skin is so thin it reddens at a touch.
这一下打在我肚子上。|That blow landed on my belly.
我翻过去，露出浅色的腹面。|I rolled over, showing my pale underside.
尾巴被打歪了，游不直。|My tail got knocked crooked; I can't swim straight.
我缩进水里，只露眼睛。|I sink until only my eyes show.
新长的脚也被撞疼了。|Even my new legs took the hit.
我在发抖，水都跟着抖。|I'm shivering, and the water shivers too.
还好我的骨头软。|At least my bones are soft.
我慢慢往水草里挪。|I inch my way into the water weeds.
疼得我吐不出泡。|It hurts too much to blow a bubble.
"""),
"fire": P("""水面被烤热，我只能往下躲。|The water grew hot; I could only dive."""),
"fall": P("""我被甩上岸，摔在草里。|I was thrown ashore and landed in grass."""),
"drown": P("""我明明会游，怎么还呛水？|I know how to swim—so why am I choking?"""),
"explosion": P("""水面炸开，我被掀到半空。|The surface burst and threw me into the air."""),
"projectile": P("""一支箭擦过我的尾巴。|An arrow grazed right past my tail."""),
"magic": P("""那股力量让我整个身子发麻。|That force left my whole body numb."""),
"starvation": P("""水里的小虫都躲起来了。|All the little water bugs have hidden."""),
"lightning": P("""雷打进水里，我一下就僵了。|Lightning struck the water and I went stiff."""),
"void": P("""水不见了，我只能乱摆尾巴。|The water vanished; I flail my tail at nothing."""),
},
}

poliwhirl = {
"walk": P("""
我用两只手撑着地走。|I walk with both hands braced on the ground.
腿比蝌蚪时好用一点了。|My legs work a bit better than as a tadpole.
肚子上的螺旋一晃一晃。|The spiral on my belly sways as I go.
我走过水面，留下一圈纹。|I cross the water, leaving one ring.
手上还有蹼，踩起来很稳。|My hands still have webbing; I step surely.
二十五级了，走得比从前直。|At twenty-five I walk straighter than before.
我沿着岸边慢慢挪。|I move slowly along the water's edge.
每一步都小心，别踩空。|Careful with each step so I don't slip.
我的身子圆，重心低。|My body is round, and my weight sits low.
水里走比岸上省力。|Walking in water costs me less than on land.
我晃着走，可从不倒。|I wobble as I walk, but never fall.
走到水草边，我停一下。|I reach the weeds and pause there.
"""),
"idle": P("""
我盯着自己的肚子看。|I stare down at my own belly.
那个螺旋，看着看着就困。|That spiral makes me sleepy just watching.
我把手摊在水上，不动。|I lay my hands flat on the water, still.
漩涡转得很慢，一圈又一圈。|The swirl turns slowly, ring after ring.
我的肚子是白的，边上有蓝。|My belly is white, edged in blue.
水里安静得能听见自己。|The water is so quiet I hear myself.
我差点睡着，又醒了。|I nearly fell asleep, then woke.
手上的蹼，薄得透光。|The webbing on my hands is thin enough to see light.
我在想，长大后会变成什么。|I wonder what I'll become when I grow.
这一片水，我熟得很。|I know this stretch of water well.
有东西在草里，我没理。|Something's in the grass; I paid it no mind.
我把下巴搁在手上。|I rest my chin on my hands.
转久了，漩涡像要把我卷进去。|Watching long, the swirl seems to pull me in.
我吐了口气，水面起皱。|I exhale, and the surface wrinkles.
"""),
"look_player": P("""
你也在看我的肚子吗？|Are you looking at my belly too?
别盯太久，真的会睡着。|Don't stare too long—you really will sleep.
我抬起头，螺旋还在转。|I look up, the spiral still turning.
你的影子落在水面上。|Your shadow lies across the water.
我认得钓竿，也认得手。|I know fishing rods, and I know hands.
你靠这么近，是想抓我？|So close—do you mean to grab me?
我的眼睛在头顶，看得清。|My eyes sit high; I see you clearly.
你先眨眼了，我赢了。|You blinked first—I win.
人类的脸，比水里倒影好看。|A human face beats a water reflection.
我慢慢转动手腕给你看。|I turn my wrist slowly for you to see.
你走路的节奏，我记住了。|I've memorized the rhythm of your steps.
我不躲，我只是懒。|I'm not hiding—I'm simply lazy.
你看够了就说一声。|Say something when you've looked enough.
我们一起发呆，也行。|We could sit here and drift off together.
"""),
"tempted": P("""
那东西挂得离水面很近。|That thing hangs close to the water.
我是好钓竿钓上来的，懂这个。|A Good Rod caught me; I know this game.
味道不错，可钩子在哪？|Smells good—but where's the hook?
我伸手去够，差一点。|I reach for it and fall just short.
肚子在叫，比我还急。|My belly is louder than I am.
我二十五级了，还是馋。|Twenty-five levels, and still greedy.
你晃一晃，我就跟过去。|Wiggle it once and I'll come along.
先给我闻闻，再谈别的。|Let me smell it first, then we'll talk.
这味道让我忘了要小心。|This smell made me forget caution.
好吧，这次我不装了。|Fine—this time I won't pretend.
"""),
"collide": P("""
撞到我，水面晃得厉害。|Bumping me set the water swaying.
我用手撑了一下，没倒。|I braced with one hand and stayed up.
你膝盖撞到我的肚子了。|Your knee got me right in the belly.
我滑开半米，又转回来。|I slid half a meter, then turned back.
这么圆的身子，很容易滚。|A body this round rolls easily.
我拍了拍被撞的地方。|I patted the spot where I was hit.
站稳了，我没事。|I've got my footing—I'm fine.
你的脚步比我重多了。|Your steps land much heavier than mine.
再撞一次，我又要睡着了。|Bump me again and I'll doze off.
下次绕开我，行吗？|Could you walk around me next time?
"""),
"mate": P("""
我们面对面，螺旋对着螺旋。|We face each other, spiral to spiral.
它的手比我的手大一圈。|Its hands are a size bigger than mine.
水面上并排浮着两个圆。|Two round shapes float side by side.
我们一起转，水纹合成一圈。|We turn together; our ripples merge.
这一片水，往后更热闹了。|This water will be busier from now on.
我碰了碰它的额头，很凉。|I touched its forehead; it was cool.
谁也不说话，都看着水面。|Neither speaks; both watch the water.
它的螺旋转得比我慢。|Its spiral turns slower than mine.
我们靠得很近，差点一起睡着。|We leaned close and nearly slept at once.
留下吧，这里够我们住。|Stay—there's room here for us both.
"""),
"pickup": P("""
我用手把这块石头翻起来。|I flip this stone over with my hands.
底下有个东西在动。|Something underneath is moving.
我夹在指间，拿得很稳。|I hold it between my fingers, steady.
这个圆圆的，像我的肚子。|This round thing looks like my belly.
我把捡到的东西排在岸边。|I line up what I found along the bank.
谁的？我放在这儿了。|Whose is this? I'll leave it here.
它滑得很，差点掉回水里。|It's slick and nearly slid back in.
我拿它换了块更小的。|I traded it for a smaller one.
水里捡东西，我手最稳。|For picking things from water, my hands are steadiest.
这个我留着，挺好看。|I'll keep this one; it looks nice.
"""),
"target_acquire": P("""
水面有动静，不是我弄的。|The water moved, and it wasn't me.
我抬头，手上的蹼张开了。|I look up and spread my webbed hands.
它站在我的水边。|It is standing at the edge of my water.
我先看它的手，再看眼睛。|I check its hands, then its eyes.
我不喜欢被踩到的水草。|I don't care for trampled water weeds.
这一片我一直守着。|I keep watch over this stretch.
它若下水，我就迎上去。|If it enters the water, I'll meet it.
我转着螺旋，慢慢靠近。|I turn my spiral and close in slowly.
它比我高，可水是我的。|It's taller, but the water is mine.
好，它没打算退。|Good—it has no intention of backing off.
"""),
"targeting": P("""
我在等它踩进浅水。|I wait for it to step into the shallows.
手腕放松，随时能拍出去。|My wrist stays loose, ready to swing.
它一动，水就替我报信。|When it moves, the water tells me.
这个距离，一步就到。|At this distance, one step is enough.
我把呼吸压得很低。|I keep my breathing very low.
它看着我的肚子，看入神了。|It's staring at my belly, absorbed.
再站一会儿，它就困了。|A moment more and it will grow drowsy.
我数着它眨眼的次数。|I count how many times it blinks.
它退后半步，我看在眼里。|It stepped back half a pace; I noticed.
现在，它侧过身去了。|Now—it has turned its side to me.
"""),
"melee_attack": P("""
我一掌拍在水面，水花炸开。|I smack the surface and water bursts up.
手打中了，它退了两步。|My hand landed; it fell back two steps.
我用圆身子顶它的腿。|I drive my round body into its legs.
它脚下一滑，摔进浅水。|Its feet slipped and it fell into the shallows.
这一下我用了全身的劲。|I put my whole weight behind that blow.
我打完就退开，喘着气。|I hit and then retreat, catching my breath.
手腕还麻着。|My wrist is still numb.
水里打架，我不吃亏。|In water fights, I don't come off badly.
它想抓我，抓了个空。|It tried to grab me and caught nothing.
别再来第二次。|Don't try that a second time.
"""),
"spawn": P("""
好钓竿把我从水里拉上来。|A Good Rod pulled me up from the water.
二十五级的太阳，照在我肚子上。|The level-twenty-five sun warms my belly.
我在浅水里站住，四处看。|I stand in the shallows and look around.
这片水比原来的窄。|This water is narrower than my old home.
我先试着走了两步。|I try walking two steps first.
岸边的草很高，挡住视线。|The bank grass is tall and blocks my view.
有人的味道，就在附近。|There's a human scent close by.
我转着肚子上的螺旋等他。|I turn my belly spiral and wait for him.
水是新的，凉得刚好。|The water is new, and just cold enough.
我叫了一声，只有回声。|I called once; only an echo answered.
这里没有同类，得慢慢找。|No kin here—I'll have to search slowly.
我从这里开始，重新认路。|I start here, learning the paths again.
"""),
"hurt": {
"generic": P("""
这一下打在我圆肚子上。|That blow landed on my round belly.
我的蹼被踩了一下。|One of my webbed hands got stepped on.
我缩起手，护住胸口。|I pull my hands in to guard my chest.
疼得我差点滚进水里。|It hurt enough to nearly roll me into the water.
我退到水草后面。|I back away behind the water weeds.
薄皮下面全是青的。|Under my thin skin everything is bruised.
我喘气，水面跟着起伏。|I gasp, and the water rises with me.
还好，骨头没断。|At least no bones are broken.
我用手按着伤处。|I press my hand against the wound.
还能走，只是慢。|I can still walk, only slower.
"""),
"fire": P("""火过来，我立刻沉进水里。|Fire came; I sank into the water at once."""),
"fall": P("""我从岸上滚下去，肚子朝下。|I rolled off the bank and landed belly-down."""),
"drown": P("""我天天泡水，怎么会呛？|I live in water—how am I choking?"""),
"explosion": P("""冲击把我推得翻了个身。|The blast rolled me right over."""),
"projectile": P("""箭插在我的手臂上。|An arrow is stuck in my arm."""),
"magic": P("""那股力量钻进我的螺旋里。|That force crawled into my spiral."""),
"starvation": P("""水里的小虾都跑光了。|All the little shrimp in the water are gone."""),
"lightning": P("""雷顺着水面过来，我僵住了。|Lightning ran along the water and froze me."""),
"void": P("""水没了，我落进黑里。|The water ended and I dropped into darkness."""),
},
}

MOBS = [
    ("pixelmon:poipole", poipole),
    ("pixelmon:politoed", politoed),
    ("pixelmon:poliwag", poliwag),
    ("pixelmon:poliwhirl", poliwhirl),
]

plan = {m["mob_id"]: m for m in json.load(io.open("data/dialogue/unique_plan.json", encoding="utf-8"))["u0288"]}
KEYS = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
        "target_acquire", "targeting", "melee_attack", "spawn"]
os_df = ["fire", "fall", "drown", "explosion", "projectile", "magic",
         "starvation", "lightning", "void"]

errs = []
total = 0
mobs = []
for mob_id, data in MOBS:
    p = plan[mob_id]
    scen = {}
    for k in KEYS:
        w = p["weights"][k]
        extra = max(0, min(4, round(10 * (w - 1))))
        want = 10 + extra
        got = len(data[k])
        if got != want:
            errs.append(f"{mob_id} {k} want {want} got {got}")
        scen[k] = data[k]
    h = {"generic": data["hurt"]["generic"]}
    if len(h["generic"]) != 10:
        errs.append(f"{mob_id} hurt.generic {len(h['generic'])}")
    for k in os_df:
        h[k] = data["hurt"][k]
        if len(h[k]) != 1:
            errs.append(f"{mob_id} hurt.{k} len {len(h[k])}")
    scen["hurt"] = h
    for k, lines in scen.items():
        if k == "hurt":
            continue
        for i, ln in enumerate(lines):
            zh, en = ln["zh"], ln["en"]
            if not (6 <= len(zh) <= 20):
                errs.append(f"{mob_id} {k}[{i}] zh len {len(zh)}: {zh}")
            nw = len(en.split())
            if not (4 <= nw <= 14):
                errs.append(f"{mob_id} {k}[{i}] en words {nw}: {en}")
            if not zh.endswith(("。", "？", "！")):
                errs.append(f"{mob_id} {k}[{i}] zh no end punct: {zh}")
    total += sum(len(v) if isinstance(v, list) else sum(len(x) for x in v.values()) for v in scen.values())
    mobs.append({"mob_id": mob_id, "scenarios": scen})

if errs:
    print("\n".join(errs))
    raise SystemExit(1)

out = {"batch": "u0288", "mobs": mobs}
s = json.dumps(out, ensure_ascii=False, indent=2)
io.open("data/dialogue/unique/u0288.json", "w", encoding="utf-8", newline="\n").write(s + "\n")
print("mobs", len(mobs), "lines", total)
