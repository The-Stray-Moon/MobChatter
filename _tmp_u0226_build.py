import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def L(zh, en):
    return {"zh": zh, "en": en}

ironbundle = {
 "walk": [
  L("我背着冰袋，沿雪线一路投递。", "I carry my ice sack along the snowline, making deliveries."),
  L("尾巴喷嘴扫过地面，结出一层霜。", "My tail nozzle sweeps the ground and lays down frost."),
  L("冰面太滑，我索性滑着走。", "The ice is slick, so I slide instead of walking."),
  L("哨音先到，脚步后到。", "My whistle arrives first; my footsteps come after."),
  L("这一单的地址是北边的冰湖。", "This delivery is addressed to the frozen lake up north."),
  L("我用翅膀保持平衡，一步一摇。", "I keep balance with my wings, rocking step by step."),
  L("袋子里的东西不能化，我得快。", "The cargo must not melt, so I keep moving fast."),
  L("雪地上只留两行窄脚印。", "Only two narrow lines of prints stay in the snow."),
  L("我沿着河岸走，水面结着薄冰。", "I follow the riverbank where thin ice skins the water."),
  L("前方有水汽，我改走高处。", "Steam ahead, so I take the higher ground."),
  L("冰属性让我走过的地方都发白。", "Being Ice-type, I leave white where I pass."),
  L("我的步子像节拍器，一下一下。", "My steps keep time like a metronome, one by one."),
 ],
 "idle": [
  L("我把袋子放下，检查封口。", "I set the sack down and check the seal."),
  L("霜从翅尖慢慢长出来。", "Frost slowly grows out from my wingtips."),
  L("没有订单的时候，我数雪花。", "With no orders, I count snowflakes."),
  L("我的叫声像一声短促的哨。", "My cry is one short, sharp whistle."),
  L("身体里只有五十六点生命值。", "Only fifty-six hit points sit inside this frame."),
  L("冰化了，我脚边积了一小摊水。", "The ice melts, leaving a small puddle at my feet."),
  L("我在等一个不会来的收件人。", "I wait for a recipient who will never come."),
  L("包裹上的标签被霜盖住了。", "Frost has covered the label on my parcel."),
  L("水属性让我不怕这点湿冷。", "Being Water-type, this damp cold does not bother me."),
  L("我把头低下去，像在打盹。", "I lower my head as if to doze."),
  L("尾巴滴下一滴水，立刻冻住。", "One drop falls from my tail and freezes at once."),
  L("远处有训练家的脚步声。", "A trainer's footsteps sound somewhere far off."),
  L("我的铁壳上结了一层薄霜。", "A thin rime has formed on my iron shell."),
  L("停着不动，比飞行更省电。", "Standing still drains less power than flying."),
 ],
 "look_player": [
  L("你签收吗？我这儿有一个包裹。", "Will you sign? I have a parcel for you."),
  L("我抬头看你，哨音短了一下。", "I look up at you and cut my whistle short."),
  L("你没有订过冰，为什么在这儿？", "You never ordered ice; why are you here?"),
  L("人类的手，比我的爪子暖。", "A human hand is warmer than my claws."),
  L("你腰上那个球，是给我的吗？", "That ball at your waist, is it meant for me?"),
  L("我看你的脸，像在看一张地址。", "I study your face the way I read an address."),
  L("别站太近，我的冷气会伤你。", "Do not stand close; my cold air can hurt you."),
  L("你身上有雪的味道。", "You smell of snow."),
  L("我歪头，确认你是不是收件人。", "I tilt my head to check if you are the recipient."),
  L("你在看我，我在记你的样子。", "You are watching me; I am recording your shape."),
  L("精灵球能装下我这样的机械吗？", "Can a Poké Ball hold a machine like me?"),
  L("捕获率五成，你未必一次成功。", "My catch rate is fifty; you may not succeed first try."),
  L("你的呼吸在冷气里变成白雾。", "Your breath turns white in my cold air."),
  L("我认得你，你上次也这样看我。", "I know you; you looked at me like this before."),
 ],
 "tempted": [
  L("冰果？那不在我的投递单上。", "Ice berries? Those are not on my delivery list."),
  L("你手里是冷的，我闻到了。", "What you hold is cold; I can smell it."),
  L("我靠近一步，袋子还背着。", "I come one step closer, sack still on my back."),
  L("如果是冰块，我可以收下。", "If it is ice, I am willing to accept it."),
  L("我的哨音变软了，你听见没有？", "My whistle softened; did you hear it?"),
  L("食物对我只是冷却剂。", "Food is only coolant to me."),
  L("你把东西放地上，我再过去。", "Set it on the ground and I will come over."),
  L("我的喷嘴在冒白气，是高兴。", "My nozzle steams white; that means I am pleased."),
  L("这不算订单，但我还是想要。", "It is not an order, but I still want it."),
  L("五十六点生命值，也需要补给。", "Fifty-six hit points still need resupply."),
 ],
 "collide": [
  L("撞到我了，冰袋差点掉。", "You bumped me; my ice sack nearly fell."),
  L("我的壳硬，你的膝盖还好吗？", "My shell is hard; is your knee all right?"),
  L("请让一让，我在赶时间。", "Please step aside; I am on a schedule."),
  L("这一撞，霜撒了你一身。", "That bump shook frost all over you."),
  L("我退开半步，重新对准路。", "I back off half a step and realign with the road."),
  L("别推，包裹会碎。", "Do not push; the parcel will break."),
  L("我们撞出一声金属响。", "We knocked together with a metal clang."),
  L("冰面太滑，是我没刹住。", "The ice was slick; I could not brake."),
  L("我翅膀张开，稳住身体。", "I spread my wings to steady myself."),
  L("你走左边，我走右边，好吗？", "You take the left, I take the right, agreed?"),
 ],
 "mate": [
  L("悖谬宝可梦没有同伴可寻。", "A Paradox Pokémon has no kin to seek."),
  L("我的同类只留在记录里。", "My own kind survive only in records."),
  L("繁殖对我没有意义。", "Breeding means nothing to this body."),
  L("我对着雪地叫了一声，没人应。", "I whistle at the snow; nothing answers."),
  L("冰原上只有我一串脚印。", "Only one line of prints crosses the ice field."),
  L("我用喷嘴画了个圈，又擦掉。", "I draw a circle with my nozzle, then erase it."),
  L("未来的我，也是这样独行。", "The me from the future walked alone too."),
  L("我把袋子抱紧，当作同伴。", "I hug my sack and treat it as company."),
  L("同类的声音，我记不清了。", "I can no longer recall my own kind's call."),
  L("这个时代没有我的巢。", "This era holds no nest of mine."),
 ],
 "pickup": [
  L("我捡起那块冰，放进袋子。", "I pick up that ice and drop it in my sack."),
  L("地上有东西，我顺手收好。", "Something lies on the ground; I tuck it away."),
  L("这块冰很干净，可以带走。", "This ice is clean enough to carry off."),
  L("我只捡冷的、硬的、能带的。", "I only take what is cold, hard, and portable."),
  L("蓝冰？我的袋子正好空着。", "Blue ice? My sack happens to be empty."),
  L("我弯腰时，尾巴翘起来。", "As I bend over, my tail lifts behind me."),
  L("这不是我的货，但先收着。", "This is not my cargo, but I will hold it."),
  L("我把东西塞进袋底，压实。", "I push it to the bottom of the sack and pack it down."),
  L("有东西反光，我停下来看。", "Something glints; I stop to look at it."),
  L("捡来的都要登记，我记性好。", "Everything I collect gets logged; my memory is good."),
 ],
 "target_acquire": [
  L("前方有热源，我锁定了。", "Heat ahead; I have locked on."),
  L("那个目标在动，我算好落点。", "The target moves; I have its landing point."),
  L("训练家抬手，我就知道要打了。", "The trainer raised a hand; I know it is a fight."),
  L("我压低身体，喷嘴对准前方。", "I lower my body and aim my nozzle forward."),
  L("冰属性先手，水属性收尾。", "Ice opens the exchange, water closes it."),
  L("目标已进入投递范围。", "The target has entered delivery range."),
  L("我发出一声长哨，作为警告。", "I let out a long whistle as a warning."),
  L("那团影子在草里，我看见了。", "That shadow in the grass — I see it."),
  L("我的复眼把距离量得很准。", "My eyes measure the distance precisely."),
  L("锁定完成，接下来是冷的。", "Lock complete; what follows will be cold."),
 ],
 "targeting": [
  L("我盯着它，喷嘴在结霜。", "I stare at it while my nozzle frosts over."),
  L("它一动，我的准星就跟着移。", "When it moves, my aim moves with it."),
  L("三十秒内，它会露出破绽。", "Within thirty seconds it will show a gap."),
  L("我计算风，计算它下一步。", "I weigh the wind and its next step."),
  L("冷气在我脚边打转。", "Cold air swirls around my feet."),
  L("我绕半圈，找一个好角度。", "I circle halfway around to find a better angle."),
  L("它退，我就进；它进，我退。", "If it retreats I advance; if it charges I give ground."),
  L("我的哨音停了，那是专注。", "My whistle stops; that is focus."),
  L("冰锥在喷嘴口成形了。", "An ice spike forms at my nozzle's mouth."),
  L("这一击我要打在关节上。", "I will put this shot on its joint."),
 ],
 "melee_attack": [
  L("我一头撞过去，带着寒气。", "I ram forward, cold trailing behind me."),
  L("喷嘴吐出一串冰锥。", "My nozzle spits a burst of ice spikes."),
  L("我的爪子短，但很硬。", "My claws are short but very hard."),
  L("打到它身上，结了一层霜。", "The hit lands, and frost coats it."),
  L("我借惯性滑过去，再补一下。", "I slide in on momentum and strike again."),
  L("这一下是冰，下一手是水。", "This one is ice; the next is water."),
  L("撞击时，我听见壳裂的声音。", "On impact I hear a shell crack."),
  L("我收爪，退回原来的位置。", "I pull my claws back and return to position."),
  L("别小看五十六点生命值。", "Do not underestimate fifty-six hit points."),
  L("打完了，我理一理翅膀。", "Done hitting; I smooth my wings."),
 ],
 "spawn": [
  L("我从时空裂缝里掉出来，落在雪上。", "I drop out of a time rift and land in snow."),
  L("第一次呼吸，空气冷得陌生。", "My first breath: the air is cold and unfamiliar."),
  L("这里不是我的时代。", "This is not my era."),
  L("我睁眼，先看见的是冰原。", "I open my eyes on an ice field."),
  L("悖谬宝可梦，就这么出现了。", "Thus a Paradox Pokémon simply appears."),
  L("我的系统自检：五十六点生命值。", "My systems check in: fifty-six hit points."),
  L("冰与水在我体内同时启动。", "Ice and water come online inside me at once."),
  L("周围没有路，我先走一条。", "No path exists here, so I make one."),
  L("天空中有一道我没见过的光。", "There is a light in the sky I have never seen."),
  L("哨音第一次响，很轻。", "My whistle sounds for the first time, softly."),
  L("我背上袋子，它本来就在。", "I shoulder the sack; it was always there."),
  L("有人在看我，我记下了。", "Someone is watching me; noted."),
 ],
 "hurt": {
  "generic": [
   L("壳上凹了一块。", "A dent appeared in my shell."),
   L("冷气漏出来，我压不住。", "Cold air leaks out and I cannot hold it."),
   L("袋子掉了，我顾不上捡。", "My sack fell, and I have no time to grab it."),
   L("这一下打断了我的哨音。", "That blow cut my whistle short."),
   L("我的喷嘴歪了，喷不直。", "My nozzle is bent and sprays crooked."),
   L("疼，但我不会叫出声。", "It hurts, but I will not cry out."),
   L("关节卡住了，我退两步。", "A joint sticks; I back off two steps."),
   L("霜从伤口往外爬。", "Frost creeps out from the wound."),
   L("我的动作慢了半拍。", "My movements lag by half a beat."),
   L("别打了，包裹还没送完。", "Stop hitting; the parcel is not delivered yet."),
  ],
  "fire": [L("火太热，我的冰袋在滴水。", "The fire is too hot; my ice sack is dripping.")],
  "fall": [L("我摔在冰面上，滑出去很远。", "I hit the ice and slide a long way.")],
  "drown": [L("水灌进喷嘴，我呛了一下。", "Water floods my nozzle and I choke.")],
  "explosion": [L("冲击把我整个人掀翻。", "The blast flips me over entirely.")],
  "projectile": [L("一支箭钉在我的袋子上。", "An arrow pins itself to my sack.")],
  "magic": [L("药水雾让我的冰结不住。", "Potion mist keeps my ice from setting.")],
  "starvation": [L("我不用吃饭，但冷气在变弱。", "I do not eat, but my cold is weakening.")],
  "lightning": [L("雷打在我壳上，嗡的一声。", "Lightning strikes my shell with a hum.")],
  "void": [L("下面没有雪，也没有回声。", "Below there is no snow and no echo.")],
 },
}

ironhands = {
 "walk": [
  L("我一步下去，地面陷了一块。", "Each step I take sinks the ground a little."),
  L("拳头垂着走，指节刮着草。", "My fists hang low; knuckles rake the grass."),
  L("电流从肩头窜到指尖。", "Current runs from my shoulders to my fingertips."),
  L("我走得慢，但没人敢挡。", "I walk slowly, and no one dares block me."),
  L("两只手太重，我身子往前倾。", "My arms are so heavy I lean forward."),
  L("脚下的碎石被踩成粉。", "The gravel under my feet grinds to powder."),
  L("我沿着山脊走，找能砸的东西。", "I follow the ridge looking for something to break."),
  L("每迈一步，肩上的线圈响一下。", "Every step, the coils in my shoulders tick."),
  L("草被我压出一条路。", "The grass flattens into a road behind me."),
  L("一百五十四点生命值，走得稳。", "One hundred fifty-four points, walking steady."),
  L("我抬头看天，脚没停。", "I look up at the sky without breaking stride."),
  L("风把我的热气吹散了。", "The wind scatters the heat off my body."),
 ],
 "idle": [
  L("我把两只拳头对撞，火花四散。", "I knock my fists together and sparks fly."),
  L("站着的时候，我在充电。", "While standing still, I am charging."),
  L("肩上的线圈嗡嗡作响。", "The coils on my shoulders hum."),
  L("我在数自己的心跳，很慢。", "I count my heartbeat; it is very slow."),
  L("地面被我的重量压出浅坑。", "My weight presses shallow pits into the ground."),
  L("电流在指缝间跳来跳去。", "Current hops between my fingers."),
  L("我不饿，只想找东西砸。", "I am not hungry; I just want something to break."),
  L("远处的雷声，让我精神一振。", "Distant thunder lifts my spirits."),
  L("我抬手，又慢慢放下。", "I raise a hand and let it fall again."),
  L("一百五十四点，够我硬撑很久。", "One hundred fifty-four points can take a lot."),
  L("铁皮上有一道旧划痕。", "An old scratch runs across my plating."),
  L("我坐着不动，像块石头。", "I sit still as a boulder."),
  L("有虫爬过我手臂，我没理。", "A bug crosses my arm; I ignore it."),
  L("我在等一个值得挥拳的东西。", "I wait for something worth a punch."),
 ],
 "look_player": [
  L("你比我矮一个头。", "You stand a head shorter than me."),
  L("你站那么近，是想试拳头？", "Standing that close, do you want to test my fist?"),
  L("我低头看你，影子盖住你。", "I look down and my shadow covers you."),
  L("你的手很小，握不住我的拳。", "Your hand is small; it cannot grip my fist."),
  L("我认得那种眼神，训练家的。", "I know that look — a trainer's look."),
  L("你想抓我？先用精灵球试试。", "Want to catch me? Try a Poké Ball first."),
  L("我抬拳，又放了下来。", "I raise a fist, then let it down."),
  L("你身上有铁和汗的味道。", "You smell of iron and sweat."),
  L("别摸我的手臂，会触电。", "Do not touch my arm; you will get shocked."),
  L("我在你眼里看到害怕。", "I see fear in your eyes."),
  L("你退一步，我就不动。", "Take one step back and I will stay still."),
  L("五成的捕获率，你赌不赌？", "Catch rate fifty; will you gamble on it?"),
  L("我歪头，铁片摩擦作响。", "I tilt my head and the plates grind."),
  L("你不说话，我也不说。", "You say nothing; neither do I."),
 ],
 "tempted": [
  L("那东西够我砸几下吗？", "Is that thing good for a few punches?"),
  L("你举着的手，我不太懂。", "I do not quite understand the hand you raise."),
  L("电的味道，比食物香。", "The smell of current beats any food."),
  L("我往前挪了一步，地动了。", "I shift one step forward and the ground moves."),
  L("你要是扔过来，我就接住。", "If you throw it, I will catch it."),
  L("我不吃，但我可以拿着。", "I do not eat, but I can hold it."),
  L("拳头松开，又握紧。", "My fist opens, then closes again."),
  L("你在哄我，我知道。", "You are coaxing me; I know."),
  L("好，我跟你走几步看看。", "Fine, I will walk a few steps with you."),
  L("一百五十四点，不差这一口。", "With one hundred fifty-four points, I can skip a bite."),
 ],
 "collide": [
  L("你撞上来，像撞一堵墙。", "You hit me like hitting a wall."),
  L("我没动，你退了两步。", "I did not move; you fell back two steps."),
  L("小心，我的肩甲很硬。", "Careful, my shoulder plate is hard."),
  L("这一撞，我听见你骨头响。", "On that bump I heard your bones creak."),
  L("我侧身让开，地面震了一下。", "I step aside and the ground shakes."),
  L("别从后面推，我会反击。", "Do not push from behind; I will hit back."),
  L("我们撞出一声闷响。", "We collide with a dull thud."),
  L("你的帽子掉了，我捡不起来。", "Your hat fell; I cannot pick it up."),
  L("我抬手扶住你，怕你倒。", "I put a hand out to keep you from falling."),
  L("路窄，你先过。", "The path is narrow; you go first."),
 ],
 "mate": [
  L("没有同类，只有回音。", "No kin here, only echoes."),
  L("我的拳头曾为一群同类挥过。", "My fists once swung for a crowd of my kind."),
  L("这个时代没有我的搭档。", "This era holds no partner for me."),
  L("我对着山谷吼，没人应。", "I roar into the valley; nothing answers."),
  L("繁殖不在我的程序里。", "Breeding is not in my programming."),
  L("我捶了一下地，算是发泄。", "I pound the ground once, just to let it out."),
  L("孤独对我来说，只是安静。", "To me, loneliness is only quiet."),
  L("我记得另一双手，和我一样的。", "I remember another pair of hands like mine."),
  L("悖谬宝可梦，本来就没有家。", "A Paradox Pokémon has no home to begin with."),
  L("我把手臂抱在胸前，睡了。", "I fold my arms over my chest and sleep."),
 ],
 "pickup": [
  L("我弯腰，捡起一块石头。", "I bend down and pick up a stone."),
  L("手指太粗，捏不住小东西。", "My fingers are too thick for small things."),
  L("这块铁不错，能垫拳。", "This iron is good for backing a punch."),
  L("我把东西往肩上一扛。", "I hoist the thing onto my shoulder."),
  L("捡起来，掂了掂，又放下。", "I pick it up, weigh it, and set it down."),
  L("地上那根木棍，一碰就断。", "That stick on the ground snaps at my touch."),
  L("我只捡能砸的。", "I only pick up what can be smashed."),
  L("我蹲下时，膝盖响了一声。", "My knee clicks as I crouch."),
  L("东西太重，地面被我踩陷。", "The load is heavy; my feet sink in."),
  L("拿稳了，我继续走。", "Grip secure, I walk on."),
 ],
 "target_acquire": [
  L("那个目标，够大。", "That target is big enough."),
  L("我双拳一碰，电流窜起来。", "I clash my fists and current arcs up."),
  L("它敢靠近，我就先动手。", "If it comes close, I strike first."),
  L("锁定，距离三步。", "Locked; three steps away."),
  L("我的影子先压过去。", "My shadow reaches it first."),
  L("训练家点头，我明白了。", "The trainer nods; I understand."),
  L("电流沿着手臂爬满。", "Current crawls all the way up my arms."),
  L("我压低重心，准备冲。", "I drop my weight, ready to charge."),
  L("它退了，我跟着进。", "It backs off; I follow."),
  L("这一战不会太久。", "This fight will not last long."),
 ],
 "targeting": [
  L("我盯着它的腿，那里最软。", "I watch its legs; they look softest."),
  L("我等它先动。", "I wait for it to move."),
  L("线圈越转越快，声音变大。", "The coils spin faster and grow louder."),
  L("它绕左，我转半身。", "It circles left; I turn half around."),
  L("拳头的落点，我算好了。", "I already know where the fist lands."),
  L("我的呼吸很重，很稳。", "My breathing is heavy and steady."),
  L("它一举手，我就知道要防。", "When it raises a hand, I know to guard."),
  L("电在拳面上积成一层光。", "Power gathers in a sheen over my knuckles."),
  L("我在等它露出侧面。", "I wait for it to show its flank."),
  L("数到三，我就出手。", "I count to three, then swing."),
 ],
 "melee_attack": [
  L("一拳砸下，土块飞起来。", "One fist comes down and clods of earth fly."),
  L("电流顺着拳头灌进去。", "Current pours through my knuckles into it."),
  L("我连着两拳，中间没停。", "Two punches in a row, no pause between."),
  L("它被砸退了三步。", "It gets knocked back three steps."),
  L("我换左手，再来一下。", "I switch to my left and hit again."),
  L("这一拳把石头打裂了。", "This punch splits the stone."),
  L("我抓着它，往地上按。", "I grab it and drive it into the ground."),
  L("打在甲上，手有点麻。", "Hitting its shell leaves my hand numb."),
  L("我收回拳头，甩了甩。", "I pull my fist back and shake it out."),
  L("一百五十四点，撑得住。", "One hundred fifty-four points; I can last."),
 ],
 "spawn": [
  L("我从裂缝里跌出来，跪在地上。", "I fall out of the rift and land on one knee."),
  L("第一次抬头，天是陌生的蓝。", "My first look up: an unfamiliar blue sky."),
  L("线圈自己启动了，嗡嗡响。", "The coils start themselves with a hum."),
  L("我一拳砸地，确认自己还在。", "I punch the ground to confirm I am here."),
  L("这里的地，太软了。", "The ground here is too soft."),
  L("我的同类不在这里。", "My own kind are not here."),
  L("悖谬宝可梦，落进了这个时代。", "A Paradox Pokémon has dropped into this era."),
  L("我站起来，比树还高一点。", "I stand up, a little taller than the trees."),
  L("远处有人，我还没决定。", "People in the distance; I have not decided yet."),
  L("电在体内走了一圈，通了。", "Current runs one lap through me and connects."),
  L("一百五十四点，全新。", "One hundred fifty-four points, brand new."),
  L("我握拳，空气炸了一声。", "I clench my fist and the air pops."),
 ],
 "hurt": {
  "generic": [
   L("这一下，擦掉了漆。", "That one scraped off paint."),
   L("我的手臂沉了一下。", "My arm sagged for a moment."),
   L("电流乱了，冒了火花。", "My current stutters and throws sparks."),
   L("疼，但我站着。", "It hurts, but I am still standing."),
   L("你打得动我，不错。", "You can actually move me; not bad."),
   L("肩上的线圈烧了一小片。", "A coil on my shoulder scorched."),
   L("我退了半步，又稳住。", "I give half a step, then steady myself."),
   L("这一下让我慢了。", "That slowed me down."),
   L("铁皮裂开，风灌进去。", "The plate splits and wind gets inside."),
   L("再来，我还没倒。", "Again; I have not fallen yet."),
  ],
  "fire": [L("火烤着我的关节，很烫。", "The fire roasts my joints; it is hot.")],
  "fall": [L("我从高处砸下来，砸出个坑。", "I crash down from above and leave a crater.")],
  "drown": [L("水漫过肩膀，电流弱了。", "Water rises past my shoulders and my current fades.")],
  "explosion": [L("爆炸把我推出去几丈。", "The blast throws me several yards.")],
  "projectile": [L("箭扎在我臂甲上，弹开了。", "An arrow hits my arm plate and bounces off.")],
  "magic": [L("药水雾让我的关节发涩。", "Potion mist makes my joints stiff.")],
  "starvation": [L("我不进食，只是越来越沉。", "I do not eat; I only get heavier.")],
  "lightning": [L("雷落在我身上，我咧开嘴。", "Lightning lands on me, and I grin.")],
  "void": [L("下落的时候，我什么也抓不住。", "Falling, I cannot grab anything at all.")],
 },
}

ironjugulis = {
 "walk": [
  L("三张嘴同时叫，声音叠在一起。", "Three mouths cry at once, the sounds stacking."),
  L("我低空掠过，草被压弯。", "I skim low and the grass bends under me."),
  L("翅膀喷出黑气，推着我走。", "Dark exhaust from my wings pushes me along."),
  L("两颗小头左右张望，替我看路。", "Two small heads look both ways and scout for me."),
  L("我贴着树梢飞，引擎声很闷。", "I fly just over the treetops, engines muffled."),
  L("黑影从我下面滑过去。", "My shadow slides along beneath me."),
  L("我一侧身，绕开了那座塔。", "I bank and swing around the tower."),
  L("风灌进我的喉管，叫声变尖。", "Wind fills my throat and my cry sharpens."),
  L("夜里的路，我靠声音画出来。", "I map the night road by sound."),
  L("飞得再低一点，我就能抓到它。", "A little lower and I can grab it."),
  L("尾迹是黑的，很久才散。", "My wake is black and slow to fade."),
  L("我的翅膀像两片刀刃。", "My wings are like two blades."),
 ],
 "idle": [
  L("我落在塔顶，三颗头各看一边。", "I land on the tower, each head facing a way."),
  L("引擎慢下来，只剩下低鸣。", "The engines slow to a low growl."),
  L("我用中间的嘴整理翅膀。", "I groom my wings with the middle mouth."),
  L("另外两颗头在吵架。", "The other two heads are arguing."),
  L("夜风把我的热气吹走了。", "The night wind carries my heat away."),
  L("我在听地面上的动静。", "I am listening to the ground below."),
  L("三十的捕获率，我不容易被收。", "Catch rate thirty: I am not easily taken."),
  L("我收拢翅膀，像收起两把刀。", "I fold my wings like sheathing two knives."),
  L("天上的云挡住了月亮。", "Clouds cover the moon."),
  L("我打了个响鼻，冒出黑烟。", "I snort and a puff of black smoke comes out."),
  L("九十四点生命值，不经打。", "Ninety-four hit points do not take much."),
  L("三颗头都饿了。", "All three heads are hungry."),
  L("我在数下面的火光。", "I count the fires below."),
  L("我磨了磨牙，金属声。", "I grind my teeth; it sounds like metal."),
 ],
 "look_player": [
  L("三颗头一起看你，你选哪个？", "Three heads look at you; pick one."),
  L("你站在那儿，像一只走失的羊。", "You stand there like a lost sheep."),
  L("我低头，气流扫过你的头发。", "I dip low and my draft ruffles your hair."),
  L("人，你身上有铁的味道。", "Human, you carry the smell of iron."),
  L("我不急着吃你。", "I am in no hurry to eat you."),
  L("中间的头说话，另两颗在听。", "The middle head speaks; the other two listen."),
  L("你手里的球，反射着火光。", "The ball in your hand catches the firelight."),
  L("我看你很久了。", "I have been watching you a long while."),
  L("你抬头的样子，挺有趣。", "The way you look up is rather amusing."),
  L("恶属性让我不喜欢光。", "Being Dark-type, I dislike light."),
  L("你别动，我闻闻就行。", "Hold still; I only want a sniff."),
  L("左边的头想咬你，我拦住了。", "The left head wants to bite you; I stopped it."),
  L("你敢一个人走夜路？", "You walk the night road alone?"),
  L("我的影子比你的大得多。", "My shadow is far larger than yours."),
 ],
 "tempted": [
  L("那点吃的，不够三张嘴分。", "That morsel will not feed three mouths."),
  L("你举高的手在抖。", "The hand you hold up is trembling."),
  L("我落下来一点，又停住。", "I drop a little closer, then stop."),
  L("是肉吗？我闻到了。", "Is that meat? I can smell it."),
  L("诱饵我见得多。", "I have seen plenty of bait."),
  L("你把东西扔远些，我再过去。", "Throw it farther and I will come over."),
  L("三颗头都在吞口水。", "All three heads are swallowing."),
  L("我不信你，但我饿。", "I do not trust you, but I am hungry."),
  L("就这一次，我下去看看。", "Just this once, I will go down and look."),
  L("引擎又响起来，是我在犹豫。", "The engines surge again; that is me hesitating."),
 ],
 "collide": [
  L("你撞在我的胸甲上，弹开了。", "You hit my chest plate and bounce off."),
  L("我的翅膀擦过你，很凉。", "My wing brushes you; it is cold."),
  L("别站我后面，尾巴会扫到你。", "Do not stand behind me; my tail will sweep you."),
  L("这一撞，我歪了一下。", "That bump tilted me off balance."),
  L("我抬翅，把你隔开。", "I raise a wing to hold you off."),
  L("你的肩撞在我的颈上。", "Your shoulder struck my neck."),
  L("三颗头同时转过来。", "All three heads turn at once."),
  L("我退到半空，重新落下。", "I lift off, then settle again."),
  L("你也不轻。", "You are not light either."),
  L("让开，我要起飞。", "Move aside; I am taking off."),
 ],
 "mate": [
  L("三颗头，没有一颗想找伴。", "Three heads, and not one seeks a mate."),
  L("我的同类在别的时代。", "My kind live in another era."),
  L("我对着夜空叫，只有回声。", "I call into the night; only echoes return."),
  L("繁殖这件事，与我无关。", "Breeding has nothing to do with me."),
  L("我在塔顶划了一块地方。", "I have marked a spot on the tower top."),
  L("两颗小头靠在一起。", "The two small heads lean together."),
  L("这个时代没有我的巢。", "This era holds no nest of mine."),
  L("我一个人守着一片天。", "I keep a piece of sky alone."),
  L("叫声传得很远，没人来。", "My cry travels far; no one comes."),
  L("我把翅膀盖住自己。", "I cover myself with my wings."),
 ],
 "pickup": [
  L("我抓起那只羊，飞高了。", "I snatch up that sheep and climb."),
  L("爪子勾住东西，我收起来。", "My talons hook something; I stow it."),
  L("这块肉，我先叼着。", "I will carry this meat in my mouth."),
  L("地上有闪的，我俯冲下去。", "Something glints below; I dive for it."),
  L("三颗头抢同一块。", "Three heads fight over the same piece."),
  L("我用嘴叼，用爪按。", "I hold with my mouth and pin with my claws."),
  L("太重了，我扔回去。", "Too heavy; I drop it back."),
  L("我捡起骨头，又丢了。", "I pick up a bone and toss it away."),
  L("带回去，慢慢吃。", "I will take it back and eat slowly."),
  L("爪子上沾了泥。", "Mud sticks to my talons."),
 ],
 "target_acquire": [
  L("下面有东西在跑。", "Something is running below."),
  L("三颗头同时盯住同一个方向。", "All three heads fix on the same direction."),
  L("引擎拉高，我准备俯冲。", "The engines spool up; I prepare to dive."),
  L("它没看见我。", "It has not seen me."),
  L("风向对了，我松爪。", "The wind is right; I let go."),
  L("我先叫一声，让它抬头。", "I cry once to make it look up."),
  L("影子盖住它了。", "My shadow covers it now."),
  L("训练家吹哨，我收到。", "The trainer whistles; message received."),
  L("目标不大，够一顿。", "The target is small, enough for one meal."),
  L("锁定，从上方来。", "Locked; coming from above."),
 ],
 "targeting": [
  L("我绕着它转圈，越转越低。", "I circle it, lower with every lap."),
  L("它往树后躲，我抬高。", "It hides behind a tree, so I climb."),
  L("三双眼睛，没有死角。", "Three pairs of eyes, no blind spot."),
  L("我等它跑累。", "I wait until it tires."),
  L("黑气在喉里聚起来。", "Dark energy gathers in my throat."),
  L("它一停，我就动。", "The moment it stops, I move."),
  L("我算好了风，也算了它的腿。", "I have counted the wind and its legs."),
  L("翅膀张到最开。", "My wings spread to their widest."),
  L("它抬头了，正好。", "It looks up; perfect."),
  L("就是现在，我松开爪子。", "Right now: I open my claws."),
 ],
 "melee_attack": [
  L("我俯冲下去，爪子先到。", "I dive, claws arriving first."),
  L("一口咬在它肩上。", "One bite lands on its shoulder."),
  L("黑气从嘴里喷出来。", "Dark energy bursts from my mouth."),
  L("翅膀一拍，把它掀翻。", "One wingbeat flips it over."),
  L("三颗头轮流咬。", "The three heads bite in turn."),
  L("我抓起它，又摔下去。", "I lift it and slam it back down."),
  L("爪子陷进甲缝。", "My talons sink into a gap in its shell."),
  L("它反击，我侧身躲开。", "It strikes back; I roll away."),
  L("引擎全开，我撞过去。", "Engines wide open, I ram it."),
  L("打完了，我整理羽毛。", "The fight is over; I preen."),
 ],
 "spawn": [
  L("我从裂缝里冲出来，撞断树枝。", "I burst from the rift and snap a branch."),
  L("三颗头第一次同时睁眼。", "Three heads open their eyes at once, first time."),
  L("这里的夜，比我记得的亮。", "The night here is brighter than I remember."),
  L("引擎空转，声音在谷里回荡。", "Engines idle; the sound rolls through the valley."),
  L("我落在一棵枯树上。", "I land on a dead tree."),
  L("悖谬宝可梦，又来了一个。", "Another Paradox Pokémon has arrived."),
  L("九十四点生命值，够飞一阵。", "Ninety-four points are enough to fly a while."),
  L("风从三个方向吹来。", "Wind comes from three directions."),
  L("我先叫，再决定去哪。", "I cry first, then decide where to go."),
  L("下面有村子，有灯。", "Below there is a village, with lights."),
  L("我的影子掠过屋顶。", "My shadow sweeps over the rooftops."),
  L("这个时代的风，味道很怪。", "The wind of this era tastes strange."),
 ],
 "hurt": {
  "generic": [
   L("翅膜破了一块。", "A piece of my wing membrane tore."),
   L("中间的头被砸偏了。", "The middle head got knocked aside."),
   L("我掉了几根铁羽。", "I shed a few iron feathers."),
   L("这一下让引擎咳了。", "That made my engines cough."),
   L("我叫得很尖，是疼。", "My cry goes shrill; that is pain."),
   L("三颗头都在叫。", "All three heads are crying out."),
   L("我升不起来，只能滑。", "I cannot climb; I can only glide."),
   L("黑气散了，聚不回来。", "The dark energy scatters and will not gather."),
   L("胸口凹进去一块。", "My chest has a dent in it now."),
   L("你打中了我，记住。", "You hit me; remember that."),
  ],
  "fire": [L("火燎到翅膀，我失了高度。", "Fire catches my wing and I lose height.")],
  "fall": [L("我转着圈往下掉。", "I spin downward, out of control.")],
  "drown": [L("水裹住我，引擎熄了。", "Water closes over me and my engines die.")],
  "explosion": [L("冲击把我掀到半空。", "The blast throws me into the air.")],
  "projectile": [L("一支箭穿了我的翅。", "An arrow punched through my wing.")],
  "magic": [L("紫色的雾让我的头昏。", "Violet mist makes all my heads swim.")],
  "starvation": [L("三颗头都在叫饿。", "All three heads are crying hunger.")],
  "lightning": [L("雷顺着我的颈爬上来。", "Lightning climbs up my neck.")],
  "void": [L("底下是空的，我一直在掉。", "There is nothing below and I keep falling.")],
 },
}

ironleaves = {
 "walk": [
  L("我的蹄子踩过苔藓，没有声音。", "My hooves cross the moss without a sound."),
  L("角上的刃割开垂下的藤。", "The blades on my horns cut through hanging vines."),
  L("我一步跨过倒下的树干。", "I leap over the fallen trunk in one stride."),
  L("草叶随着我的脚步发亮。", "The grass brightens as I pass."),
  L("我走在林线的阴影里。", "I walk in the shadow of the treeline."),
  L("身后的叶片慢慢合拢。", "The leaves close again behind me."),
  L("我的身体很轻，像一片叶。", "My body is light as a single leaf."),
  L("我绕着空地走，脚步很准。", "I circle the clearing with precise steps."),
  L("角刃擦过石头，溅出火星。", "My horn blade scrapes stone and throws sparks."),
  L("我在找一片安静的地方。", "I am looking for a quiet place."),
  L("超能力让我知道你在哪。", "My psychic sense tells me where you are."),
  L("我走得慢，是不想惊动谁。", "I walk slowly so as not to disturb anyone."),
 ],
 "idle": [
  L("我站着，像一株长错地方的树。", "I stand like a tree grown in the wrong place."),
  L("角刃上落着一只蝴蝶。", "A butterfly rests on my horn blade."),
  L("我在听森林呼吸。", "I am listening to the forest breathe."),
  L("草属性让我不必急着吃。", "Being Grass-type, I need not hurry to eat."),
  L("九十个生命值，很轻。", "Ninety hit points; I am light."),
  L("我闭上眼，叶子还在动。", "I close my eyes, and my leaves keep moving."),
  L("捕获率只有五，你很难遇到我。", "Catch rate five; I am hard to meet."),
  L("阳光穿过我的刃，投下绿光。", "Sun through my blade casts a green line."),
  L("我把重心移到另一条腿。", "I shift my weight to the other leg."),
  L("远处有斧头的声音。", "Axes sound in the distance."),
  L("我抬头，云走得很快。", "I look up; the clouds move fast."),
  L("身上的斑纹在暗处发微光。", "My markings glow faintly in the dark."),
  L("我抖了抖，落下一层叶屑。", "I shake and a layer of leaf dust falls."),
  L("这个时代很吵，但森林还好。", "This era is loud, but the forest is all right."),
 ],
 "look_player": [
  L("你踩断了一根树枝，我听见了。", "You snapped a twig; I heard it."),
  L("我侧过头，刃对着你。", "I turn my head, blade toward you."),
  L("你身上没有恶意。", "I find no ill will in you."),
  L("我退半步，给你留出距离。", "I step back to give you room."),
  L("人，你来这片林子做什么？", "Human, what brings you into this wood?"),
  L("我的眼睛在暗处是绿的。", "My eyes are green in the dark."),
  L("你想捕我？五的概率。", "You want to catch me? Five percent."),
  L("我看你的时候，你也停住了。", "When I look at you, you stop too."),
  L("你的影子落在我的叶子上。", "Your shadow falls on my leaves."),
  L("我不怕你，只是不想打。", "I am not afraid of you; I just do not want to fight."),
  L("我低头发出一声轻鸣。", "I lower my head and give a soft chime."),
  L("你手里的球，我认得。", "I recognize the ball in your hand."),
  L("别伸手，我的刃很快。", "Do not reach out; my blade is quick."),
  L("我让开路，你过去吧。", "I clear the path; go on through."),
 ],
 "tempted": [
  L("那株草，看着很嫩。", "That plant looks tender."),
  L("你举着的叶子，是给我的？", "Is the leaf you hold up for me?"),
  L("我靠近一步，蹄子很轻。", "I step closer, hooves very light."),
  L("我不吃你说的那种东西。", "I do not eat what you are describing."),
  L("露水比食物更合我意。", "Dew suits me better than food."),
  L("我低头闻了闻，又抬起。", "I sniff it, then lift my head."),
  L("你的手别抖，我不咬人。", "Keep your hand steady; I do not bite."),
  L("好香，像雨后的林子。", "It smells good, like a forest after rain."),
  L("我可以跟你走一小段。", "I can walk a short way with you."),
  L("九十个生命值，吃一点就够。", "With ninety points, a little is enough."),
 ],
 "collide": [
  L("你的肩撞在我的侧腹。", "Your shoulder struck my flank."),
  L("我纹丝不动，你先退了。", "I did not budge; you backed off first."),
  L("我的角差点划到你。", "My horn nearly grazed you."),
  L("这一撞，叶子落了一地。", "That bump shook leaves to the ground."),
  L("我侧身避开，蹄下打滑。", "I swerve aside and my hooves slip."),
  L("别碰我的角刃。", "Do not touch my horn blade."),
  L("我们撞在一起，声音很闷。", "We collide with a muffled sound."),
  L("我低头道歉，退开两步。", "I lower my head in apology and step back."),
  L("你没事吧？我力气不小。", "Are you all right? I am stronger than I look."),
  L("路窄，我贴边站。", "The path is narrow; I press to the edge."),
 ],
 "mate": [
  L("森林里没有第二个我。", "There is no second one of me in this forest."),
  L("我的同类只存在于图纸上。", "My kind exist only on blueprints."),
  L("我独自守着这片林地。", "I keep this woodland alone."),
  L("繁衍与我无关。", "Propagation has nothing to do with me."),
  L("我对着月亮叫了一声。", "I call once at the moon."),
  L("回音从树间传回来。", "The echo comes back between the trees."),
  L("我在地上踩出一个圈。", "I stamp a circle into the ground."),
  L("这个时代没有我的群落。", "This era holds no herd of mine."),
  L("我把角靠在树干上。", "I rest my horn against a trunk."),
  L("一个人也好，安静。", "Alone is fine too; it is quiet."),
 ],
 "pickup": [
  L("我低头衔起一片叶子。", "I lower my head and take up a leaf."),
  L("蹄子拨开落叶，找东西。", "My hoof pushes the litter aside, searching."),
  L("这块石头有棱，我带上。", "This stone has an edge; I take it."),
  L("我用角挑起那根藤。", "I hook the vine with my horn."),
  L("果实落在蹄边，我吃了。", "A fruit lands by my hoof; I eat it."),
  L("东西太沉，我放回原处。", "Too heavy; I set it back where it was."),
  L("我捡起一根断枝，闻了闻。", "I pick up a broken branch and sniff it."),
  L("叶子上还带着露水。", "The leaf still carries dew."),
  L("我把东西藏在树根下。", "I hide the thing under the roots."),
  L("捡完了，我抖抖身子。", "Finished, I shake myself out."),
 ],
 "target_acquire": [
  L("林子里有东西在动。", "Something is moving in the trees."),
  L("我的刃先亮了一下。", "My blade flashes once, first."),
  L("它踩断树枝的声音，我记住了。", "I remember the sound of it snapping twigs."),
  L("我不轻易出手。", "I do not strike lightly."),
  L("它挡在我与幼树之间。", "It stands between me and the saplings."),
  L("超能力先探到它的位置。", "My psychic sense finds its position first."),
  L("我压低身体，刃朝前。", "I lower my body, blades forward."),
  L("训练家退后，把场地让给我。", "The trainer steps back and gives me the field."),
  L("这一场，我认真了。", "Now I am serious about this one."),
  L("锁定，从侧面切入。", "Locked; I will enter from the flank."),
 ],
 "targeting": [
  L("我盯着它的重心。", "I watch where its weight sits."),
  L("它一动，我就跟上半步。", "When it moves, I match it half a step."),
  L("我的刃口对着它的关节。", "My edge lines up with its joint."),
  L("草叶都静下来，为我让路。", "The grass goes still to let me through."),
  L("我在等一个空隙。", "I am waiting for one opening."),
  L("它的呼吸乱了。", "Its breathing has gone uneven."),
  L("我把角压低一寸。", "I lower my horn by an inch."),
  L("绿色的光在刃上聚起来。", "Green light gathers along my blade."),
  L("它先动了。", "It moved first."),
  L("那就不客气了。", "Then I will stop being polite."),
 ],
 "melee_attack": [
  L("我的角横着扫过去。", "My horn sweeps across in a wide arc."),
  L("刃光一闪，它退了。", "The blade flashes once, and it retreats."),
  L("我跃起，蹄子先落地。", "I leap, and my hooves land first."),
  L("这一下切开了它的甲。", "This cut opened its shell."),
  L("我转身，用后蹄踢。", "I spin and kick with a hind hoof."),
  L("超能力把它推开半丈。", "My psychic shove sends it back several feet."),
  L("我收刃，退回原位。", "I draw my blade back and return to position."),
  L("它挡了一下，刃滑开了。", "It blocks; my blade slides off."),
  L("我不补第二下。", "I do not follow with a second blow."),
  L("九十个生命值，够我赢。", "Ninety points are enough for me to win."),
 ],
 "spawn": [
  L("我从裂缝里走出，落在苔上。", "I step out of the rift onto the moss."),
  L("睁眼第一件东西，是一棵树。", "The first thing I see is a tree."),
  L("这里的绿，比我知道的深。", "The green here is deeper than I know."),
  L("我的刃还没有名字。", "My blade has no name yet."),
  L("悖谬宝可梦，踏进了森林。", "A Paradox Pokémon has stepped into the forest."),
  L("风穿过我的叶片，很凉。", "Wind moves through my leaves, cool."),
  L("我试着抬起前蹄，稳的。", "I test a foreleg; it holds."),
  L("九十个生命值，刚好够走路。", "Ninety points, just enough to walk on."),
  L("远处有人在砍树。", "Someone is cutting trees far off."),
  L("我先去找水。", "I will find water first."),
  L("斑纹亮了一下，又暗下去。", "My markings flare once, then dim."),
  L("这个时代，树还在。", "In this era, trees still stand."),
 ],
 "hurt": {
  "generic": [
   L("我的刃上缺了一角。", "A corner is missing from my blade."),
   L("叶子被扯掉了几片。", "Several leaves were torn away."),
   L("这一下打断了我的步。", "That broke my stride."),
   L("我退开，蹄印歪了。", "I pull back, hoofprints crooked."),
   L("疼，但我站着没动。", "It hurts, but I hold my ground."),
   L("绿光暗了一下。", "My green glow dimmed."),
   L("我的侧腹擦破了。", "My flank is scraped raw."),
   L("别打角，那里最疼。", "Not the horn; that is where it hurts most."),
   L("我喘了一声，很轻。", "I let out one breath, very soft."),
   L("我还能再撑一阵。", "I can hold out a while longer."),
  ],
  "fire": [L("火沿着叶子爬上来。", "Fire climbs up along my leaves.")],
  "fall": [L("我从半空落下，砸在石上。", "I fall from midair and hit stone.")],
  "drown": [L("水淹过蹄子，我的光弱了。", "Water covers my hooves and my light fades.")],
  "explosion": [L("气浪把我掀进了灌木。", "The blast throws me into the bushes.")],
  "projectile": [L("一支箭擦过我的角。", "An arrow grazes my horn.")],
  "magic": [L("药水雾让我的刃发钝。", "Potion mist dulls my blade.")],
  "starvation": [L("没有阳光，我越来越虚。", "Without sunlight I grow weaker.")],
  "lightning": [L("雷劈在角上，我腿一软。", "Lightning strikes my horn and my legs buckle.")],
  "void": [L("落下时，连风都没有。", "Falling, there is not even wind.")],
 },
}

plan = json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))
batch = plan['u0226']
content = {
 'pixelmon:ironbundle': ironbundle,
 'pixelmon:ironhands': ironhands,
 'pixelmon:ironjugulis': ironjugulis,
 'pixelmon:ironleaves': ironleaves,
}

ORDER = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
         "target_acquire", "targeting", "melee_attack", "spawn", "hurt"]
HURT_ORDER = ["generic", "fire", "fall", "drown", "explosion", "projectile",
              "magic", "starvation", "lightning", "void"]

mobs = []
for pm in batch:
    mid = pm['mob_id']
    sc = content[mid]
    out = {}
    for key in ORDER:
        if key == 'hurt':
            src = sc['hurt']
            out['hurt'] = {k: src[k] for k in HURT_ORDER}
        else:
            out[key] = sc[key]
    mobs.append({"mob_id": mid, "scenarios": out})

data = {"batch": "u0226", "mobs": mobs}

# validations
import math
existing_zh, existing_en = set(), set()
import glob
for f in glob.glob('data/dialogue/unique/*.json'):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    for m in d.get('mobs', []):
        for k, v in m['scenarios'].items():
            items = v if isinstance(v, list) else [x for arr in v.values() for x in arr]
            for it in items:
                if isinstance(it, dict):
                    existing_zh.add(it.get('zh', ''))
                    existing_en.add(it.get('en', ''))

seen_zh, seen_en = {}, {}
errs = []
for pm in batch:
    mid = pm['mob_id']
    w = pm['weights']
    sc = content[mid]
    for key in ORDER:
        if key == 'hurt':
            for hk in HURT_ORDER:
                arr = sc['hurt'][hk]
                want = 10 if hk == 'generic' else 1
                if len(arr) != want:
                    errs.append(f"{mid} hurt.{hk} count {len(arr)} != {want}")
        else:
            want = 10 + max(0, min(4, round(10 * (w[key] - 1))))
            if len(arr) != want:
                errs.append(f"{mid} {key} count {len(arr)} != {want}")
            for it in arr:
                zh, en = it['zh'], it['en']
                if not (6 <= len(zh) <= 20):
                    errs.append(f"{mid} {key} zh len {len(zh)}: {zh}")
                n = len(en.split())
                if not (4 <= n <= 14):
                    errs.append(f"{mid} {key} en words {n}: {en}")
    for key in ORDER:
        items = sc['hurt'] if key == 'hurt' else sc[key]
        flat = [x for arr in items.values() for x in arr] if key == 'hurt' else items
        for it in flat:
            zh, en = it['zh'], it['en']
            if zh in existing_zh and key != 'hurt':
                errs.append(f"DUP-ZH-EXISTING {zh}")
            if zh in seen_zh:
                errs.append(f"DUP-ZH {zh} ({seen_zh[zh]} / {mid})")
            seen_zh[zh] = mid
            if en in existing_en:
                errs.append(f"DUP-EN-EXISTING {en}")
            if en in seen_en:
                errs.append(f"DUP-EN {en}")
            seen_en[en] = mid

if errs:
    print("ERRORS", len(errs))
    for e in errs[:60]:
        print(" ", e)
    sys.exit(1)

json.dump(data, open('data/dialogue/unique/u0226.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
open('data/dialogue/unique/u0226.json', 'a', encoding='utf-8').write('\n')
print("written mobs", len(mobs), "lines", len(seen_zh))
