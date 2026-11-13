# -*- coding: utf-8 -*-
import json, io, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = {}

data['pixelmon:gloom'] = {
"walk": [
("我拖着两片叶子慢慢挪。", "I drag my two leaves along slowly."),
("每一步都踩得草地发软。", "Every step leaves the grass soft."),
("头顶的花盘晃来晃去。", "The bloom on my head sways about."),
("我走得很慢，味道先到。", "I walk slowly; my smell arrives first."),
("花瓣擦过草尖，沙沙响。", "My petals brush the grass tips, whispering."),
("我的根须在地上拖着走。", "My root threads drag along the ground."),
("臭味跟着我一路留下。", "The stench trails behind me the whole way."),
("我边走边把嘴边的口水抹掉。", "I wipe the drool from my mouth as I go."),
("花蕊朝下，我怕晒。", "My pistil points down; I avoid the sun."),
("我踩弯一片草，又踩弯一片。", "I bend one blade of grass, then another."),
("走路的时候我不放味道。", "While walking, I keep the smell in."),
("我挪到阴影里再歇脚。", "I shuffle into the shade to rest."),
],
"idle": [
("心平气和时我什么味都不放。", "When I'm calm, I give off nothing at all."),
("花盘慢慢转，追着光。", "My bloom turns slowly, following the light."),
("我把叶子叠在一起挡太阳。", "I fold my leaves together against the sun."),
("口水滴在草上，黏黏的。", "Drool drips onto the grass, sticky."),
("我站着不动，草把我盖住了。", "I stand still and the grass covers me."),
("有虫靠近，我不理它。", "A bug comes near; I ignore it."),
("雌蕊里藏着一点甜味。", "A little sweetness hides in my pistil."),
("我呼吸很轻，味道也很轻。", "My breathing is light, and so is my smell."),
("太阳偏了，我换个朝向。", "The sun shifted; I turn to face it."),
("我在想今天要不要开一点花。", "I wonder whether to open a little today."),
("草叶上的露水凉到我的根。", "Dew on the grass cools my roots."),
("我一动不动地数着风。", "I count the gusts without moving."),
("安静的时候，连蜜蜂都不来。", "When I'm quiet, not even bees visit."),
("我把花盘低下去，打个盹。", "I lower my bloom and doze."),
],
"look_player": [
("你站得太近了，我闻到你。", "You're too close; I can smell you."),
("我看着你，先不放味道。", "I watch you and hold the smell back."),
("你裤脚沾着草屑。", "There's grass dust on your cuffs."),
("你抬手的时候我缩了一下。", "I flinch when you raise your hand."),
("我盯你的手，不盯你的脸。", "Your hands move; my pistil follows them."),
("你是碰巧路过，还是找我？", "Did you wander by, or come for me?"),
("我的花盘对着你慢慢转。", "My bloom turns slowly toward you."),
("你身上混着陌生的气味。", "You carry a strange smell mixed in."),
("我往后退了半步，草响了。", "I step back half a pace; the grass rustles."),
("你看我久一点，我就紧张。", "The longer you look, the tenser I get."),
("我的眼睛在花瓣下面。", "My eyes are under the petals."),
("你把影子投过来，我躲开。", "You cast a shadow; I move out of it."),
("我不眨眼，花也不动。", "I don't blink, and neither does my bloom."),
("你要摸我吗？先别。", "You want to touch me? Not yet."),
],
"tempted": [
("那果子闻起来比我的味道香。", "That berry smells better than I do."),
("我慢慢挪过去，装作路过。", "I shuffle over, pretending to wander."),
("甜的，我就往前一步。", "If it's sweet, I take one step closer."),
("我不抢，我就等它掉下来。", "I won't snatch it; I'll wait for it to fall."),
("叶子都竖起来了，我忍不住。", "My leaves lift; I can't help it."),
("那东西在动，我盯着它。", "It's moving; I'm watching it."),
("我嘴里开始流口水了。", "Drool already runs down from my mouth."),
("你晃一晃，我就靠得更近。", "Shake it and I come nearer."),
("这味道让我忘了收着气味。", "The smell makes me forget to hold mine in."),
("我伸出一片叶子去够。", "I reach out with one leaf."),
],
"collide": [
("撞到我，花盘歪了。", "You bumped me; my bloom is crooked."),
("别推，我的根还没扎稳。", "Don't push; my roots aren't set."),
("我软，撞一下就晃半天。", "I'm soft; one bump and I sway for ages."),
("叶子被你踩住了一片。", "Your boot crushed one of my green leaves."),
("我退开，草替我挡了一下。", "I back off and the grass takes the hit."),
("这一下把我藏的味道撞出来了。", "That knock let my stored smell out."),
("我的身体比看上去轻。", "My body is lighter than it looks."),
("你别再挤了，我站不住。", "Stop shoving; I can't keep my footing."),
("花盘磕到地面，沾了泥。", "My bloom hit the ground and picked up mud."),
("我转过身，把背对着你。", "I turn my back to you."),
],
"mate": [
("两朵花盘对着，慢慢摇。", "Two blooms face each other, swaying slowly."),
("两股味道缠成一团。", "Two scents have wound into one."),
("我把雌蕊抬高一点。", "I lift my pistil a little higher."),
("花粉落在叶子上了。", "Pollen has settled on the leaves."),
("我们不说话，只放味道。", "We don't talk; we only give off scent."),
("她的味道是甜的，不是臭的。", "Her scent is sweet, not foul."),
("我跟着她的花盘转。", "I turn with her bloom."),
("草地上多了一小片花。", "A small patch of flowers appeared on the grass."),
("我们挨着站了一下午。", "We stood side by side all afternoon."),
("等风来，把花粉带走。", "We wait for wind to carry the pollen."),
],
"pickup": [
("我用叶子卷起一个果子。", "I curl a leaf around a berry."),
("掉在地上的东西我都收着。", "I keep whatever falls to the ground."),
("这颗太小了，我还是要。", "This one's too small, but I'll take it."),
("我把东西塞进花盘底下。", "I tuck it under my bloom."),
("我捡东西的时候味道最淡。", "My smell is faintest when I'm gathering."),
("你掉的，我替你拿着。", "You dropped it; I'll hold it for you."),
("我拖不动，就滚着走。", "I can't drag it, so I roll it."),
("这堆里有一颗是软的。", "One of these is soft."),
("我把好的留给小的。", "I leave the good ones for the little ones."),
("叶子一松，东西掉了。", "My leaf loosens and it drops."),
],
"target_acquire": [
("你踏进我的地盘，站住。", "You walked into my patch, so hold still."),
("有东西在动，我盯住了。", "Something moved; I've got it."),
("危险来了，雌蕊开始发热。", "Danger's here; my pistil is warming up."),
("我闻到不是草的味道。", "I smell something that isn't grass."),
("我不追，我等它靠近。", "I don't chase; I let it wander into my scent."),
("影子落在我身上了。", "A shadow fell across me."),
("这声音不对，我转过去。", "That sound is wrong; I turn toward it."),
("我认准了，就这一个。", "I've picked one, just this one."),
("我的叶子绷紧了。", "My leaves have gone stiff."),
("别过来，我开始臭了。", "Don't come closer; I'm starting to stink."),
],
"targeting": [
("我一直对着你，不动。", "I keep facing you without moving."),
("花盘锁住你的方向。", "My bloom has locked onto your direction."),
("我慢慢逼近，草分开。", "I close in slowly; the grass parts."),
("味道越来越浓，你闻到了吗？", "The smell is thickening. Do you smell it?"),
("我在等一个破绽。", "I'm waiting for an opening."),
("你退，我就进一步。", "You give ground; my roots creep after you."),
("我看住你的脚跟。", "I keep my eyes on your heels."),
("我的花在抖，不是风。", "My bloom is shaking, and it isn't wind."),
("这味道会先让你晕。", "This smell will make you dizzy first."),
("我不急，我比你慢。", "I'm in no hurry; I'm slower than you."),
],
"melee_attack": [
("我把花盘甩过去。", "I swing my bloom at you."),
("花粉撒了你一脸。", "Pollen bursts across your face."),
("我用叶子抽你的腿。", "I whip your legs with my leaves."),
("这一下带着毒。", "This blow carries poison."),
("我撞得不重，味道重。", "My hit is light; the smell is not."),
("你咳了，那就对了。", "You're coughing. That's what I wanted."),
("我把根须缠上你的靴子。", "I wrap root threads around your boots."),
("我压上去，慢慢往下沉。", "I lean on you and sink down slowly."),
("别吸，吸了会更难受。", "Don't breathe it in; it gets worse."),
("我打一下就要歇一会。", "After one hit I need to rest."),
],
"spawn": [
("我从草里冒出来，先闻到土。", "I come up through the grass and smell soil first."),
("这片草地够老了，我在这。", "This meadow is old enough; here I am."),
("花盘还合着，我先醒一会。", "My bloom is still closed; let me wake slowly."),
("早晨的草把我盖了一半。", "The morning grass covers half of me."),
("我在这里扎根很多天了。", "I've been rooted here for many days."),
("露水顺着花瓣流进嘴里。", "Dew runs down my petals into my mouth."),
("我慢慢把叶子展开。", "I unfold my leaves slowly."),
("风把远处的味道带过来。", "The wind brings smells from far off."),
("我这一片没有别的花。", "There are no other blooms in this patch."),
("我从土里顶出来，身上全是泥。", "I push up out of the soil, covered in mud."),
("太阳一照，我就想开花了。", "The sun hits me and I want to bloom."),
("别踩这一片，我刚长出来。", "Don't step here; I've just sprouted."),
],
"hurt": {
"generic": [
("我的花盘被打歪了。", "My bloom got knocked crooked."),
("叶子断了一片。", "One of my leaves snapped."),
("疼的时候味道会失控。", "When it hurts, the smell gets away from me."),
("我缩起来，把根收回去。", "I curl up and pull my roots in."),
("这一下让我透不过气。", "The hit squeezed the air out of my leaves."),
("泥溅进花心里了。", "Mud splashed into my flower's heart."),
("我缓了很久才站稳。", "It took me a long time to steady myself."),
("别打了，我本来就不硬。", "Stop; I was never tough."),
("粘液从伤口流出来。", "Slime seeps from the wound."),
("我的味道变苦了。", "My smell has turned bitter."),
],
"fire": [("火一碰花瓣就卷了。", "One touch of flame and my petals curl.")],
"fall": [("从坡上滚下来，花盘先落地。", "Rolled down the slope; my bloom landed first.")],
"drown": [("水灌进花心，我不会游。", "Water fills my flower's heart; I can't swim.")],
"explosion": [("爆炸把我掀进了草里。", "The blast flung me flat into the weeds.")],
"projectile": [("那支箭穿过两片叶子。", "The arrow went through two of my leaves.")],
"magic": [("有什么东西在动我的根。", "Something is moving my roots.")],
"starvation": [("土里的养分越来越少了。", "There's less and less in the soil.")],
"lightning": [("雷打下来，花瓣全焦了。", "Lightning struck and scorched all my petals.")],
"void": [("这里没有土，我扎不下根。", "There's no soil here; I can't root.")],
},
}

data['pixelmon:gogoat'] = {
"walk": [
("蹄子踩过石头，稳稳的。", "My hooves cross the stone, steady."),
("我在前面走，草自动分开。", "I walk ahead and the grass parts."),
("角上还挂着昨天的草。", "Grass from yesterday still hangs on my horns."),
("我一步一步往前踏。", "I plant one hoof, then the next."),
("这座山坡我走惯了。", "I know these slopes well."),
("尾巴甩一下，赶走虫子。", "One flick of my tail chases the flies."),
("我边走边闻岩缝。", "I sniff the rock cracks as I go."),
("蹄声在坡上回响。", "My hoofbeats echo on the slope."),
("我背得动，也走得动。", "I can carry weight and still walk."),
("这坡再陡我也不停。", "However steep, I don't stop."),
("我把路让给小的。", "I give the path to the little ones."),
("我低头看看脚下的草。", "I lower my head to check the grass underfoot."),
],
"idle": [
("我站着，听风从坡上来。", "I stand and listen to the wind off the slope."),
("角上落了灰，我蹭一蹭。", "Dust settled on my horns; I rub them."),
("草够吃，我就慢慢嚼。", "There's enough grass; I chew slowly."),
("我抬头看云往哪边走。", "I look up to see which way the clouds go."),
("我不用谁陪，也不赶谁。", "I need no company and chase none."),
("有一只鸟落在我背上。", "A heron settled on my back and stayed."),
("嚼着草，我嚼到一半停了。", "I chew, then stop halfway."),
("风大的时候我背对着它。", "When the wind is strong, I turn my back to it."),
("我把体重放在前腿上。", "I rest my weight on my front legs."),
("我的角在发痒。", "My horns are itching."),
("坡上的草比谷里的硬。", "The grass on the slope is tougher than in the valley."),
("我站着，像坡上多出一块石。", "I stand like one more stone on the slope."),
("太阳晒到角尖，暖的。", "Sun warms the tips of my horns."),
("我打了个响鼻，鸟飞走了。", "I snort and the bird flies off."),
],
"look_player": [
("我低下头，让你看清我的角。", "I lower my head so you can see my horns."),
("你今天心情不好。", "You're not in a good mood today."),
("你的手别抖，我不喜欢。", "Don't let your hands shake; I don't like it."),
("我闻到你袖口的草味。", "I smell grass on your sleeve."),
("你要骑我，还是只是看看？", "Are you riding me, or just looking?"),
("我读得出你的犹豫。", "I can read your hesitation."),
("你走近，我连耳朵都不动。", "You come closer; not even my ears move."),
("你的呼吸太快了。", "You're breathing too fast."),
("我盯着你的眼睛，别移开。", "I hold your eyes. Don't look away."),
("握住我的角，我就知道了。", "Take my horns and I'll know."),
("你不必说话，我都懂。", "You needn't speak; I understand."),
("我往前半步，是给你让路。", "I step forward half a pace to make room."),
("你的影子比人先到。", "Your shadow reaches my horns before you do."),
("我甩了甩头，那是打招呼。", "I toss my head; that's a greeting."),
],
"tempted": [
("你手里那把草，我认得。", "I know that handful of grass."),
("我慢慢过来，不抢。", "I amble over; the grass stays in your hand."),
("甜一点的草，我走快些。", "For sweeter grass, I walk faster."),
("我闻到了，就不用你叫。", "I can smell it; you needn't call."),
("让我先咬一口。", "Let me have one bite first."),
("你把草举高，我就抬头。", "Hold it higher and I lift my head."),
("我吃的时候别摸角。", "Don't touch my horns while I eat."),
("这味道比坡上的好。", "This tastes better than the slope's."),
("我嚼得慢，你别催。", "I chew slowly; don't rush me."),
("吃完我就跟你走。", "When I'm done, I'll follow you."),
],
"collide": [
("撞上来，我几乎没动。", "You ran into me; I barely moved."),
("我的角不是用来顶你的。", "My horns aren't for butting you."),
("你撞得自己后退了吧。", "You're the one who stepped back."),
("站稳，我身上有分量。", "Steady; there's weight in me."),
("我侧了一下身，让你过去。", "I angled my body so you could pass."),
("后面别挨太近，蹄子有劲。", "Don't crowd my rear; my hooves are strong."),
("我的蹄子踩到了你的脚。", "My hoof found your foot."),
("这一下把我的草震掉了。", "That knocked the grass from my mouth."),
("我退开，是给你面子。", "I stepped back out of courtesy."),
("下次绕一下，坡很宽。", "Next time go around; the slope is wide."),
],
"mate": [
("我们用角轻轻碰了一下。", "Our horns touched, gently."),
("她走前面，我跟着。", "She takes the slope first; I trail her."),
("我们一起啃同一片草。", "We graze the same patch together."),
("我把高的草让给她。", "I leave the taller grass to her."),
("两只角靠在一起，很静。", "Two sets of horns together, very quiet."),
("她跑起来，我就追。", "When she runs, I chase."),
("我们在坡上站成一排。", "We stand in a line on the slope."),
("她闻我的角，我低下头。", "She sniffs my horns; I lower my head."),
("天黑了，我们靠着取暖。", "Night falls and we lean together for warmth."),
("小羊跟着，我们就放慢。", "The little one trails us; we slow down."),
],
"pickup": [
("我叼起一束草，慢慢走。", "I pick up a bundle of grass and walk."),
("这东西我能背。", "I can carry this."),
("我用嘴唇把它推开了。", "I push it aside with my lips."),
("掉下来的果子我捡了。", "I gathered the fallen fruit."),
("我背上已经有一捆了。", "There's already a bundle on my back."),
("别放太重，上坡要稳。", "Don't load too much; I need balance uphill."),
("我把它放在两角之间。", "I set it between my horns."),
("这一颗我留给小的。", "This one I save for the little one."),
("我叼稳了，往背上一送。", "I grip it and toss it onto my back."),
("松口的时候差点掉了。", "It nearly fell when I let go."),
],
"target_acquire": [
("坡下有东西在动。", "Something's moving below the slope."),
("那不是草的味道。", "That's not the smell of grass."),
("我把角尖压低，对准了。", "I lower my horn tips and take aim."),
("有谁在跟着我们。", "Someone is following us."),
("我挡在小羊前面。", "I step in front of the little one."),
("这声音我记住了。", "I've got that sound now."),
("我看住那个方向，眼睛不眨。", "I keep my eyes on that side without blinking."),
("风把它吹到我这来了。", "The wind brought it to me."),
("它动一下，我就动一下。", "It moves; I move."),
("这次我不让路。", "This time I'm not stepping aside."),
],
"targeting": [
("我挪着步子，找能顶的地方。", "I shift my feet, hunting for a spot to hit."),
("角已经对准了。", "My horns are lined up."),
("我压上一步，地面在震。", "I press forward a step; the ground shakes."),
("它退到坡边了。", "It's backed to the slope's edge."),
("它站住，我的角也停在半空。", "It stops short; my lowered horns stop too."),
("我的呼吸沉下去了。", "My breath has gone slow and heavy."),
("它想跑，路我堵着。", "It wants to run; I hold the way."),
("我把它逼到岩石那儿。", "I herd it toward the rock."),
("我一下就能顶翻它。", "One push and I'd flip it."),
("别站在我后面。", "Don't stand behind me."),
],
"melee_attack": [
("我低头，角先到。", "I lower my head; the horns arrive first."),
("这一顶把你挑了起来。", "This butt lifted you off your feet."),
("蹄子跟着落下。", "The hooves come down after."),
("我撞得不快，但很沉。", "I'm not fast, but I'm heavy."),
("你退了三步才停。", "You took three steps back before stopping."),
("我甩头，把你甩开。", "I toss my head and throw you off."),
("角尖擦过你的肩。", "My horn tip grazed your shoulder."),
("我不追，站着看你。", "I don't chase; I stand and watch."),
("这一下我自己也震得发麻。", "The blow left my own head ringing."),
("再来我就用后腿。", "Come again and I'll use my hind legs."),
],
"spawn": [
("我从坡上下来，蹄子先着地。", "I come down the slope, hooves first."),
("这片草够我吃一季。", "This grass will last me a season."),
("晨雾里我先露的是角。", "In the morning mist, my horns show first."),
("我在这里等一个肯骑我的人。", "I wait here for someone willing to ride."),
("我从岩缝里走出来。", "I step out from the rock crevice."),
("坡上风大，我站稳了。", "The wind is strong up here; I've found my footing."),
("晨露压得我的毛发沉。", "Morning dew weighs down my coat."),
("这里离水远，但草好。", "Water's far, but the grass is good."),
("我找了块平地落脚。", "I found level ground to stand on."),
("来的路上我踩塌了一块土。", "On my way here I broke a patch of soil."),
("天刚亮，我就到了。", "I arrived just at daybreak."),
("我在这片坡上有一阵了。", "I've been on this slope a while."),
],
"hurt": {
"generic": [
("角被撞得发闷。", "My horns took it and went dull."),
("我的前腿软了一下。", "My front leg gave for a moment."),
("肋骨那儿闷闷地疼。", "There's a dull ache along my ribs."),
("我退了两步才站住。", "I took two steps back before I held."),
("我疼，但不叫。", "Pain blooms under my ribs; I stay quiet."),
("背上的毛被扯掉一撮。", "A tuft of fur came off my back."),
("我的蹄子磕在石上裂了。", "My hoof split on the stone."),
("我用鼻子喘得很重。", "I'm breathing hard through my nose."),
("角根在发热。", "The base of my horns is hot."),
("我低头护住脖子。", "I tuck my chin behind my two horns."),
],
"fire": [("火舔过我的背，毛卷了。", "Flame licked my back and my coat curled.")],
"fall": [("我从坡上滑下来，撞在石头上。", "I slid down the slope and hit stone.")],
"drown": [("我的蹄子够不到底了。", "My hooves can't find the bottom.")],
"explosion": [("爆炸把坡上的土掀起来。", "The blast threw the slope's soil up.")],
"projectile": [("箭插在肩胛上，拔不出来。", "An arrow is stuck in my shoulder blade.")],
"magic": [("魔法在我角尖上打转。", "Magic swirls around the tips of my horns.")],
"starvation": [("这片草被我啃光了。", "I've eaten this patch bare.")],
"lightning": [("雷落在坡上，角还麻着。", "Lightning struck the slope; my horns still tingle.")],
"void": [("脚下没有坡，也没有草。", "No slope beneath me, no grass.")],
},
}

data['pixelmon:golbat'] = {
"walk": [
("我用翅膀一下一下往前挪。", "I push forward with one wingbeat at a time."),
("低低地贴着草飞。", "I fly low, skimming the grass."),
("我的翅膀刮到了草尖。", "My wings clip the grass tips."),
("我歪着飞，因为嘴太重。", "I fly crooked; my mouth is heavy."),
("影子从我下面掠过。", "My shadow sweeps beneath me."),
("我停不下来，只能绕圈。", "I can't stop; I can only circle."),
("我往前扑一段，又滑一段。", "I lunge forward, then glide."),
("耳朵里全是自己的回声。", "My ears are full of my own echoes."),
("我贴着岩壁飞。", "I keep close to the rock wall."),
("翅膀薄，风一大就晃。", "My wings are thin; strong wind makes me wobble."),
("我飞得不高，够了。", "I don't fly high. It's enough."),
("我边飞边张着嘴。", "I fly with my mouth open."),
],
"idle": [
("我挂在岩壁上，倒着。", "I hang from the rock wall, upside down."),
("嘴里空空的，牙齿也是空的。", "My mouth is empty, and so are my teeth."),
("我张嘴喘气，风灌进来。", "I open my mouth to breathe; wind rushes in."),
("我的牙像吸管，一碰就断。", "My teeth are like straws, and they snap."),
("夜里我醒着，白天我睡。", "I'm awake at night and asleep by day."),
("我舔了舔牙缝。", "I lick between my teeth."),
("洞里很凉，我的翅膀收着。", "The cave is cool; my wings are folded."),
("我听见水滴在石头上。", "I hear water dripping on stone."),
("我的叫声在洞里绕。", "My cry circles in the cave."),
("有蛾子飞过，我没动。", "A moth passed; I didn't move."),
("我把脸藏进翼膜里。", "I hide my face in my wing membrane."),
("这口牙让我咬不住东西。", "These teeth keep me from gripping anything."),
("我挂着，慢慢地晃。", "I hang there, swaying slowly."),
("我张开嘴，又合上。", "My jaw opens wide, then shuts on nothing."),
],
"look_player": [
("你的血在响，我听得见。", "Your blood is loud; I can hear it."),
("我把头侧过去，听你。", "I tip my head sideways to listen."),
("你举着火把，我不喜欢。", "You're holding a torch. I don't like it."),
("我嘴张着，不是要咬。", "My mouth is open; it's not for biting."),
("你站那儿别动，让我听。", "Stand still and let me listen."),
("我闻到你身上的铁。", "There's iron in your blood; I taste it."),
("你的呼吸太整齐了。", "Your breathing is too even."),
("我在这上面看得清楚。", "I see clearly from up here."),
("你的影子都比我大。", "Even your shadow is bigger than me."),
("我朝你叫了一声，你退了吗？", "I called at you. Did you step back?"),
("我的牙露在外面，收不回去。", "My teeth stick out; I can't pull them in."),
("你要抓我，得先够得着。", "To catch me, you'd have to reach me."),
("我从你左边绕到右边。", "I sweep from your left side to your right."),
("你眼睛眨得比我快。", "Your eyes blink quicker than my echoes return."),
],
"tempted": [
("那血味太近了。", "That smell of blood is too close."),
("我在它头顶转了两圈。", "I wheel twice above its head."),
("我不咬，我只舔一下。", "I won't bite; just one lick."),
("甜的东西我很少遇到。", "Sweet things rarely come my way."),
("你要是给我，我就落下来。", "Give it to me and I'll come down."),
("我的牙咬不住，只能吸。", "My teeth can't grip; I can only suck."),
("这味道让我忘了倒挂。", "The smell made me forget I was hanging."),
("我落在地上，很不习惯。", "I've landed on the ground. Strange."),
("你手别动，我马上就好。", "Keep your hand still; I'm nearly done."),
("我闻着味就过来了。", "I came following the smell."),
],
"collide": [
("撞到我的翅膀了。", "You hit my wing."),
("我一歪，差点掉下去。", "I tipped and nearly fell."),
("我的骨头轻，撞不起。", "My bones are light; I can't take a hit."),
("你把我从墙上撞下来了。", "You knocked me off the wall."),
("我扑棱着找回平衡。", "I flapped to find my balance again."),
("牙磕到你的肩，断了半颗。", "My tooth hit your shoulder and broke."),
("我退到洞顶去了。", "I retreated to the cave ceiling."),
("别往上撞，我就在上面。", "Don't bump upward; that's where I am."),
("这一下把我的回声打乱了。", "That scrambled my echoes."),
("我掉在草上，翻了个身。", "I fell on the grass and rolled over."),
],
"mate": [
("我们倒挂着，挨在一起。", "We hang upside down, side by side."),
("她的回声比我尖。", "Her echo is shriller than mine."),
("我用翅膀碰了碰她。", "I brushed her with my wing."),
("洞里全是我们的回声。", "The cave is full of our echoes."),
("我们一起飞出去找食。", "We fly out to hunt together."),
("她的牙也是空的。", "Her teeth are hollow too."),
("我们互相理翅膀。", "We groom each other's wings."),
("她先飞，我跟在后头。", "She flies first; I follow."),
("岩壁上并排两个影子。", "Two shadows side by side on the rock."),
("她一叫，我立刻接上。", "She calls, and I answer at once."),
],
"pickup": [
("我用嘴叼，可牙咬不住。", "I try to carry it, but my teeth won't grip."),
("我用翅膀把它兜起来。", "I scoop it up with my wings."),
("这东西比我还沉。", "My hollow bones can't lift this much."),
("叼着它我飞不高。", "With this in my mouth, I can't fly high."),
("半路掉了，我又回去捡。", "I dropped it halfway and went back."),
("我把它挂在岩缝里。", "I hang it in a rock crevice."),
("这点分量我还行。", "This much I can manage."),
("我用爪子抓着走。", "I carry it in my claws."),
("叼着东西就没法叫了。", "With my mouth full, I can't call."),
("我把它藏在洞顶。", "I hide it on the cave ceiling."),
],
"target_acquire": [
("有东西在动，回声变了。", "Something moved; the echoes changed."),
("我听见心跳，不是我的。", "I hear a heartbeat that isn't mine."),
("这味道是热的。", "This smell is warm."),
("我松开岩壁，落下来。", "I let go of the wall and drop."),
("它在草里，我听得到。", "It's in the grass; I can hear it."),
("我张嘴，先叫一声。", "I open my mouth and call first."),
("我盯上了，就不换。", "Once I've picked it, I don't switch."),
("这个比蛾子大。", "This is bigger than a moth."),
("我在它头顶绕了半圈。", "I circled it once."),
("风把它往我这边吹。", "The wind pushes it my way."),
],
"targeting": [
("我越飞越低。", "I'm flying lower and lower."),
("我的影子落在它身上。", "My shadow settles over it."),
("我叫了一声，它抬头了。", "I called, and it looked up."),
("我在找它的脖子。", "I'm looking for its neck."),
("它往哪跑，我都听得见。", "Wherever it runs, I hear it."),
("我的牙准备好了，虽然不牢。", "My teeth are ready, though they're weak."),
("我停在它头顶的枝上。", "I perch on the branch above it."),
("等它再迈一步，就一下。", "One more step from it, and I strike."),
("它一转背，我就动。", "It turns its back; my wings are already open."),
("头别抬，我就在你上面。", "Keep your head down; I'm right above."),
],
"melee_attack": [
("我扑下去，张嘴就咬。", "I dive and bite with my mouth open."),
("牙扎进去，又滑出来。", "The teeth went in and slid back out."),
("翅膀拍在它脸上，啪一声。", "My wing cracks across its face."),
("这一口没咬牢。", "That bite didn't hold."),
("我叫得太响，它捂耳朵了。", "I screamed so loud it covered its ears."),
("我从背后抓它的肩。", "I grab its shoulder from behind."),
("我的爪子划了一道。", "My claws left a line."),
("它一挥，我就往上飞。", "It swung; I flew up."),
("我咬第二口才见血。", "The second bite drew blood."),
("我吸了一口就退开。", "I took one sip and pulled back."),
],
"spawn": [
("我从洞顶松开爪子。", "I let go of the cave ceiling."),
("太阳一落，我才出洞。", "Only after sunset do I leave the cave."),
("我的叫声先到，我后到。", "My cry arrives before I do."),
("我挂在洞口，等风停。", "I hang at the cave mouth, waiting for the wind to die."),
("我沿着岩壁爬出来。", "I crawl out along the rock wall."),
("这洞里已经有我的味道。", "My smell is already in this cave."),
("我张开翅膀，晾一晾。", "I spread my wings to dry them."),
("外面太亮了，我眯着眼。", "It's too bright out; I squint."),
("我是饿着出来的。", "I came out hungry."),
("我从上面掉下来，又飞起来。", "I dropped from above and caught myself."),
("草太高，我看不清。", "The grass is too tall; I can't see well."),
("我找了一处背光的石头。", "I found a stone away from the light."),
],
"hurt": {
"generic": [
("我的翅膀破了个口。", "There's a tear in my wing."),
("又一颗牙当场折了。", "Another tooth snapped off just now."),
("我撞在石头上，头还晕。", "I hit the stone; my head is still spinning."),
("骨头太轻，一打就疼。", "My bones are light, so every hit hurts."),
("我从空中掉了下来。", "I fell out of the air."),
("我叫不出来，气不够。", "I can't cry out; I have no breath."),
("这一下打在我的翼膜上。", "That hit the membrane of my wing."),
("我缩成一团挂着。", "I curl into a ball and hang."),
("回声全乱了，我辨不清方向。", "My echoes are a mess; I can't tell direction."),
("我的嘴合不上了。", "I can't close my mouth."),
],
"fire": [("火一照，我的翅膀就卷。", "One flash of fire and my wings curl.")],
"fall": [("我从洞顶摔到石头上。", "I fell from the ceiling onto stone.")],
"drown": [("水进了嘴，我咽不下去。", "Water got in my mouth and I can't swallow.")],
"explosion": [("爆炸震得洞顶直落灰。", "The blast shook dust off the ceiling.")],
"projectile": [("箭穿了我翅膀的膜。", "The arrow tore through my wing membrane.")],
"magic": [("有东西把我的回声打散了。", "Something scattered my echoes.")],
"starvation": [("我好几夜没喝到东西。", "I haven't fed in several nights.")],
"lightning": [("雷光刺眼，我什么都听不见。", "The lightning glare blinded me; I hear nothing.")],
"void": [("下面没有回声，是空的。", "There's no echo below. It's empty.")],
},
}

data['pixelmon:goldeen'] = {
"walk": [
("我摆尾，往前一窜。", "One flick of my tail and I shoot forward."),
("水从我的鳃边过去。", "Water passes my gills."),
("我的鳍在水里张开。", "My fins spread in the water."),
("我沿着水底的石头游。", "I swim along the stones on the bottom."),
("水草擦过我的肚子。", "Weeds brush my belly."),
("我转个弯，水面起了圈。", "I turn and rings spread on the surface."),
("我游得比看上去快。", "I swim faster than I look."),
("角在前面划开水流。", "My horn parts the current."),
("我贴着水面往上跳了一下。", "I skim the surface and jump once."),
("尾巴一甩，水花溅起来。", "A tail flick throws up spray."),
("我逆着水试了试。", "I test myself against the current."),
("我穿过一片水草。", "I pass through a patch of weeds."),
("水浅了，我侧着身子。", "The water's shallow; I tilt on my side."),
("我往上浮了一点。", "I rise a little toward the surface."),
],
"idle": [
("我停在水里，鳍轻轻摆。", "I hover in the water, fins barely moving."),
("水面的光落在我背上。", "Light from the surface falls on my back."),
("我张着嘴，等小虫掉下来。", "I hold my mouth open for insects to fall."),
("水底的沙很软。", "The sand on the bottom is soft."),
("我对着自己的影子发愣。", "I stare at my own shadow."),
("尾巴上的鳍像裙摆。", "The fin on my tail is like a skirt."),
("水温刚好，我不动。", "The water's just right; I don't move."),
("气泡从我嘴里升到水面。", "A bubble rises from my mouth to the surface."),
("有鱼从我身边过，我没理。", "A fish passed; I ignored it."),
("我把身体侧过去晒太阳。", "I turn my side to the sun."),
("水草在动，是水流。", "The weeds move; it's just the current."),
("我一下一下地开合鳃盖。", "My gill covers open and close."),
("这里听不见岸上的声音。", "I can't hear the shore from here."),
("我慢慢沉到石缝边。", "I sink slowly to the edge of the rocks."),
],
"look_player": [
("你站在岸上，水里有你的影子。", "You stand on the bank; your shadow's in the water."),
("我游到你的倒影下面。", "I swim under your reflection."),
("你伸手进来，水就乱了。", "You reach in and the water goes cloudy."),
("我看着你的靴子，不看你。", "I watch your boots, not you."),
("你要抓我，手得再快些。", "To catch me, your hands must be quicker."),
("我绕着你手的影子转。", "I circle the shadow of your hand."),
("你的影子太大了，我躲开。", "Your shadow is too big; I move away."),
("我在水里，你在岸上，正好。", "I'm in the water, you're on land. Good."),
("我不怕你，我怕网。", "I'm not afraid of you; I'm afraid of nets."),
("你蹲下来了，水纹变了。", "You crouched; the ripples changed."),
("我露出背鳍给你看。", "I show you my dorsal fin."),
("你说话，声音在水里闷闷的。", "You speak, and your voice is muffled underwater."),
("我顶了一下你的倒影。", "I bumped your reflection."),
("别踩水边的草，那是我的。", "Don't step on the bank weeds; they're mine."),
],
"tempted": [
("水面有东西在漂。", "Something is drifting on the surface."),
("我上来闻了闻，又沉下去。", "I rise to sniff, then sink back."),
("那点碎屑够我一口。", "That crumb is one mouthful for me."),
("我绕着它游了两圈。", "I swam two circles around it."),
("我张嘴，水也进来了。", "I open my mouth and water comes too."),
("我跳起来够了一下。", "I jumped once to reach it."),
("这味道我没在水底闻过。", "I've never smelled this on the bottom."),
("我靠近了，又退回去。", "I came close, then backed off."),
("你再放低一点。", "Lower it a little more."),
("我一口吞了，刺都没吐。", "I swallowed it whole, spines and all."),
],
"collide": [
("你踩进水里，撞到我了。", "You stepped in and hit me."),
("我被撞得肚皮朝上。", "The blow left me belly-up."),
("我的胸鳍夹在石头缝里。", "My pectoral fin is wedged in a crack."),
("水一晃，我找不到方向。", "The water sloshed; I lost my bearings."),
("我撞到石头上，鳞掉了一片。", "I hit a stone and lost a scale."),
("你别在水里乱走。", "Don't thrash around in the water."),
("我窜出去，撞进草里。", "I bolted and crashed into the weeds."),
("角顶到你腿上，是意外。", "My horn hit your leg. An accident."),
("我沉下去，躲开你的脚。", "I sank to avoid your feet."),
("这一下把我冲出去老远。", "That pushed me a long way off."),
],
"mate": [
("我们并排逆着水游。", "We swim upstream side by side."),
("她的鳍比我红。", "Her fins are redder than mine."),
("我们围着那块青石打转。", "We swim rings around the blue stone."),
("水暖了，我们就一起上溯。", "The water warmed, so we head upstream."),
("她用尾巴碰了我一下。", "She brushed me with her tail."),
("我们的角差点撞在一起。", "Our horns nearly met."),
("水底映着我们两个。", "The bottom mirrors the two of us."),
("她游前面，我跟着她。", "She leads; I follow her."),
("我们找了一处浅滩。", "We found a shallow bank."),
("后面那群鱼跟着我们走。", "The school behind us follows our lead."),
],
"pickup": [
("我叼起一颗小石子。", "I nudge a pebble along the riverbed."),
("我含在嘴里，又吐出来。", "I mouth it once, then let the current take it."),
("这个太沉，我推着走。", "This is too heavy; I push it along."),
("我把它顶得翻过来。", "I butt it until it flips over."),
("我在水底捡了点亮的。", "I picked up something bright on the bottom."),
("一张嘴，它就漂走了。", "I opened my mouth and it drifted away."),
("我把东西塞进石缝。", "I wedge it into a rock crevice."),
("这个能当巢的底。", "This could floor a nest."),
("我把它顶着游。", "I swim with it braced on my horn."),
("掉了一半，剩下的我留着。", "Half fell; I keep the rest."),
],
"target_acquire": [
("水里有血的味道。", "There's blood in the water."),
("波纹不对，有东西在动。", "The ripples are wrong; something's moving."),
("我看见水底有影子。", "I see a shadow on the bottom."),
("它落进水里了。", "It fell into the water."),
("我沉下去，从下面看。", "I sink and look from below."),
("这条水沟只有一条路。", "This channel has only one way out."),
("我认准那个方向了。", "I've fixed on that direction."),
("水面上的动静太小。", "The disturbance on the surface is small."),
("我一点一点靠近。", "I drift closer through the murk."),
("我一下就能穿过去。", "I could dart through in one go."),
],
"targeting": [
("我绕着它转了一圈又一圈。", "I circle it once, then again."),
("我的角对着它的侧面。", "My horn is squared at its silver side."),
("水帮我藏着。", "The water hides me."),
("它一动，水就告诉我。", "When it moves, the water tells me."),
("我等它靠近岸边。", "I wait for it to near the bank."),
("我贴着水底靠近。", "I creep along the bottom."),
("我的尾鳍绷紧了。", "My tail fin has gone taut."),
("它再靠近半步，我就冲。", "One more stroke of my tail and I ram it."),
("它没看见我。", "It hasn't seen me."),
("这口水塘太小，它跑不掉。", "This pond is too small for it to escape."),
],
"melee_attack": [
("我冲上去用角顶。", "I charge and drive my horn in."),
("角扎进去，水变红了。", "The horn went in; the water reddened."),
("我甩尾打它的腿。", "I slap its legs with my tail."),
("我跳起来撞它。", "I leap and strike it."),
("这一下我自己也晕。", "That left me dizzy too."),
("我咬住不放。", "I bite and hold."),
("它一挥手，我被拍到岸上。", "It swung and knocked me onto the bank."),
("我翻回来，又冲一次。", "I flopped back and charged again."),
("我的角不算尖，但够用。", "My horn isn't sharp, but it works."),
("得手了，我潜回水底。", "That done, I dive back down."),
],
"spawn": [
("我从水底浮上来，先看见光。", "I rise from the bottom and see light first."),
("这水面暖了，我才来。", "I only come when the water warms."),
("我顺流游到这里。", "I swam downstream to get here."),
("水草间有个空处，我占了。", "There was a gap in the weeds; I took it."),
("我的鳞还是湿的。", "My scales are still wet."),
("天暖了，鱼群开始往上走。", "It's warm; the school starts moving up."),
("我从水底的石洞钻出来。", "I slipped out of a rock crevice."),
("这里水浅，够我转身。", "The water's shallow but I can turn."),
("我跳了一下，落回水里。", "I jumped once and fell back in."),
("岸上没人，正好。", "No one on the bank. Good."),
("我跟着水声过来的。", "I followed the sound of the water."),
("这一片是我的水道。", "This stretch is my channel."),
],
"hurt": {
"generic": [
("我的鳞掉了几片。", "A few of my scales came off."),
("鳍撕开了一道。", "There's a tear in my fin."),
("水把血冲淡了。", "The water thins my blood."),
("我翻着肚皮浮了一会。", "I floated belly-up for a while."),
("角被撞钝了。", "My horn got blunted."),
("我躲进石缝里。", "I hid in a rock crevice."),
("我的鳃动得很急。", "My gills are working fast."),
("疼得我直往水底钻。", "The pain drives me to the bottom."),
("我划不动鳍，任水推着。", "My fins won't work; the current moves me."),
("这一下打在我的侧线。", "That hit my lateral line."),
],
"fire": [("水都热了，我的鳍缩起来。", "The water's hot; my fins curl.")],
"fall": [("我被摔在岸上，又蹦回去。", "I was thrown onto the bank and flopped back.")],
"drown": [("水太多，我反而喘不上气。", "Too much water, and I can't breathe.")],
"explosion": [("爆炸把水底掀翻了。", "The blast turned the bottom over.")],
"projectile": [("箭从水面扎下来。", "An arrow came down through the surface.")],
"magic": [("有股力量在水里推我。", "Something in the water is pushing me.")],
"starvation": [("水里的小虫越来越少了。", "There are fewer and fewer insects in the water.")],
"lightning": [("雷打在水面，我全身一麻。", "Lightning hit the surface; my body went numb.")],
"void": [("这里没有水，我的鳃张着。", "There's no water here; my gills hang open.")],
},
}

ORDER = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
         "target_acquire", "targeting", "melee_attack", "spawn"]
HURT = ["generic", "fire", "fall", "drown", "explosion", "projectile", "magic",
        "starvation", "lightning", "void"]

plan = json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))['u0206']
plan_ids = [m['mob_id'] for m in plan]

errors = []
for m in plan:
    mid = m['mob_id']
    if mid not in data:
        errors.append('missing mob ' + mid)
        continue
    for sc in ORDER:
        items = data[mid][sc]
        need = 10 + max(0, min(4, round(10 * (m['weights'][sc] - 1))))
        if len(items) != need:
            errors.append('%s %s count %d != %d' % (mid, sc, len(items), need))
    for k in HURT:
        items = data[mid]['hurt'][k]
        if len(items) != (10 if k == 'generic' else 1):
            errors.append('%s hurt %s len %d' % (mid, k, len(items)))

allzh, allen = {}, {}
for mid, scs in data.items():
    for sc, items in scs.items():
        groups = [items] if isinstance(items, list) else items.values()
        for g in groups:
            for zh, en in g:
                if not (6 <= len(zh) <= 20):
                    errors.append('zh len %d: %s' % (len(zh), zh))
                n = len(en.split())
                if not (4 <= n <= 14):
                    errors.append('en words %d: %s' % (n, en))
                if zh in allzh:
                    errors.append('dup zh: ' + zh)
                allzh[zh] = mid
                if en in allen:
                    errors.append('dup en: ' + en)
                allen[en] = mid

for f in glob.glob('data/dialogue/unique/u*.json'):
    if f.endswith('u0206.json'):
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    for mob in d.get('mobs', []):
        for sc, items in mob.get('scenarios', {}).items():
            groups = [items] if isinstance(items, list) else items.values()
            for g in groups:
                for line in g:
                    if not isinstance(line, dict):
                        continue
                    if line.get('zh') in allzh:
                        errors.append('cross dup zh in %s: %s' % (f, line['zh']))
                    if line.get('en') in allen:
                        errors.append('cross dup en in %s: %s' % (f, line['en']))

if errors:
    for e in errors[:60]:
        print('ERR', e)
    print('total errors', len(errors))
    sys.exit(1)

out = {"batch": "u0206", "mobs": []}
for m in plan:
    mid = m['mob_id']
    scs = {}
    for sc in ORDER:
        scs[sc] = [{"zh": zh, "en": en} for zh, en in data[mid][sc]]
    scs['hurt'] = {k: [{"zh": zh, "en": en} for zh, en in data[mid]['hurt'][k]] for k in HURT}
    out['mobs'].append({"mob_id": mid, "scenarios": scs})

with open('data/dialogue/unique/u0206.json', 'w', encoding='utf-8', newline='\n') as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
    fp.write('\n')

total = 0
for mob in out['mobs']:
    for sc, items in mob['scenarios'].items():
        groups = [items] if isinstance(items, list) else items.values()
        for g in groups:
            total += len(g)
print('ok', len(out['mobs']), 'mobs', total, 'lines')
