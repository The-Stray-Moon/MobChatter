# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PAIRS = [
("你靠过来，我不躲。", "你走近，我连耳朵都不动。", "You come closer; not even my ears move."),
("我低下头，角朝前。", "我把角尖压低，对准了。", "I lower my horn tips and take aim."),
("我一动不动，像块石头。", "我站着，像坡上多出一块石。", "I stand like one more stone on the slope."),
("火燎到我的毛，味道很难闻。", "火舔过我的背，毛卷了。", "Flame licked my back and my coat curled."),
("别从后面推，我会踢。", "后面别挨太近，蹄子有劲。", "Don't crowd my rear; my hooves are strong."),
("一支箭扎进我的肩。", "箭插在肩胛上，拔不出来。", "An arrow is stuck in my shoulder blade."),
("我咬住，甩到背上。", "我叼稳了，往背上一送。", "I grip it and toss it onto my back."),
("我等它先动。", "它不动，我也不动。", "It holds still, and so do I."),
("我盯住它，不眨眼。", "我看住那个方向，眼睛不眨。", "I keep my eyes on that side without blinking."),
("我用嘴把它挪到一边。", "我用嘴唇把它推开了。", "I push it aside with my lips."),
("这一下打在我肋骨上。", "肋骨那儿闷闷地疼。", "There's a dull ache along my ribs."),
("夜里我们挨着睡。", "天黑了，我们靠着取暖。", "Night falls and we lean together for warmth."),
("我抖了抖背上的露水。", "晨露压得我的毛发沉。", "Morning dew weighs down my coat."),
("我一步一步，不急。", "我一步一步往前踏。", "I plant one hoof, then the next."),
("我绕着它走，找角度。", "我挪着步子，找能顶的地方。", "I shift my feet, hunting for a spot to hit."),
("别抬头，抬头就晚了。", "头别抬，我就在你上面。", "Keep your head down; I'm right above."),
("我用翅膀扇它的脸。", "翅膀拍在它脸上，啪一声。", "My wing cracks across its face."),
("她的叫声比我的高。", "她的回声比我尖。", "Her echo is shriller than mine."),
("我歪着头看你。", "我把头侧过去，听你。", "I tip my head sideways to listen."),
("她叫一声，我就应一声。", "她一叫，我立刻接上。", "She calls, and I answer at once."),
("再近一点，就一下。", "等它再迈一步，就一下。", "One more step from it, and I strike."),
("我绕了两圈才敢靠近。", "我在它头顶转了两圈。", "I wheel twice above its head."),
("我把头埋进翅膀里。", "我把脸藏进翼膜里。", "I hide my face in my wing membrane."),
("我等它背对我。", "它一转背，我就动。", "The moment it turns, I move."),
("天黑了，我才出来。", "太阳一落，我才出洞。", "Only after sunset do I leave the cave."),
("我绕着你飞了半圈。", "我从你左边绕到右边。", "I sweep from your left side to your right."),
("我的影子盖住它了。", "我的影子落在它身上。", "My shadow settles over it."),
("我吐了个泡，看它浮上去。", "气泡从我嘴里升到水面。", "A bubble rises from my mouth to the surface."),
("水里全是我们的影子。", "水底映着我们两个。", "The bottom mirrors the two of us."),
("我的鳍被压住了。", "我的胸鳍夹在石头缝里。", "My pectoral fin is wedged in a crack."),
("我们绕着同一块石头转。", "我们围着那块青石打转。", "We swim rings around the blue stone."),
("鱼群在我们身后散开。", "后面那群鱼跟着我们走。", "The school behind us follows our lead."),
("水面上有东西在动。", "水面有东西在漂。", "Something is drifting on the surface."),
("我用嘴把它翻了个面。", "我把它顶得翻过来。", "I butt it until it flips over."),
("我游不动了，只能漂。", "我划不动鳍，任水推着。", "My fins won't work; the current moves me."),
("我被撞得翻了个身。", "我被撞得肚皮朝上。", "The blow left me belly-up."),
("我盯着你的脚。", "我看住你的脚跟。", "I keep my eyes on your heels."),
("你身上有别的宝可梦的味道。", "你身上混着陌生的气味。", "You carry a strange smell mixed in."),
("你的靴子上有草籽。", "你裤脚沾着草屑。", "There's grass dust on your cuffs."),
("你是来抓我的，还是路过？", "你是碰巧路过，还是找我？", "Did you wander by, or come for me?"),
("我们的味道混在一起了。", "两股味道缠成一团。", "Two scents have wound into one."),
("你咳了，那就对了。", "你咳了，那就对了。", "You're coughing. That's what I wanted."),
("我的蹄子磕裂了。", "我的蹄子磕在石上裂了。", "My hoof split on the stone."),
("我喘得很重。", "我用鼻子喘得很重。", "I'm breathing hard through my nose."),
("牙又断了一颗。", "又一颗牙当场折了。", "Another tooth snapped off just now."),
("我慢慢靠过去。", "我一点一点靠近。", "I drift closer through the murk."),
("我绕着它转圈。", "我绕着它转了一圈又一圈。", "I circle it once, then again."),
("打完我就潜下去。", "得手了，我潜回水底。", "That done, I dive back down."),
]

path = '.tmp_u0206_build.py'
s = open(path, encoding='utf-8').read()
for old_zh, new_zh, new_en in PAIRS:
    old = '("%s", "' % old_zh
    idx = s.find(old)
    if idx < 0:
        print('MISSING', old_zh)
        continue
    if s.count(old) != 1:
        print('AMBIG', old_zh, s.count(old))
        continue
    if old_zh == new_zh:
        # only english changes: replace the en string after zh
        start = idx
        end = s.find('")', start)
        seg = s[start:end]
        s = s[:start] + '("%s", "%s' % (new_zh, new_en) + s[end:]
        continue
    start = idx
    end = s.find('"),', start)
    s = s[:start] + '("%s", "%s")' % (new_zh, new_en) + s[end + 2:]
open(path, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
