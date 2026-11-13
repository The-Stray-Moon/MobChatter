# -*- coding: utf-8 -*-
p = '.tmp_u0284/gen.py'
s = open(p, encoding='utf-8').read()
pairs = [
 ('("我在等它先露出破绽。", "I wait for it to show a gap first.")',
  '("我先等它乱,再动手。", "I wait for it to slip before I move.")'),
 ('("我落地时几乎没有声音。", "I touch down with almost no sound.")',
  '("落地时,我把声音收住了。", "On landing, I keep the sound inside.")'),
 ('("我被推得转了个圈。", "I was pushed into a full spin.")',
  '("这一推,我在水里绕了一圈。", "That shove spun me a full turn in the water.")'),
 ('("你手里的东西在反光。", "What you hold is catching the light.")',
  '("你手里那样东西正晃我的眼。", "Whatever you hold is dazzling my eyes.")'),
 ('("你身上有谷子的味道。", "You smell of grain.")',
  '("你衣角沾着晒过的谷香。", "Your hem carries the smell of sun-dried grain.")'),
 ('("草被我们踩平了一片。", "We flattened a patch of grass between us.")',
  '("脚下这一小片草被压折了。", "A small patch of grass is bent under our feet.")'),
 ('("风向对我有利。", "The wind favors me.")',
  '("风顺着我,它逆着。", "The wind is with me and against it.")'),
 ('("哎,好麻。", "Ow. That tingles.")',
  '("哎哟,这一下好麻。", "Ow, that one really tingled.")'),
]
for a, b in pairs:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('patched', len(pairs))
