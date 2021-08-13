# 2020-8-12
import redis ,json
rdic = redis.Redis(host='dev.werror.com', port=4328, decode_responses=True) # combined to one db only , __formula:default

errant_type = {
"M:DET":"{ 'error': '冠词缺失', 'explanation':f'建议添加冠词<b>{edit.c_str}</b>'}",
"M:NOUN:POSS":"{ 'error': '名词所有格缺失', 'explanation':f'建议添加名词所有格<b>{edit.c_str}</b>'}",
"R:VERB:SVA":"{ 'error': '主谓不一致', 'explanation':f'请检查动词<b>{edit.o_str}</b>形态'}",
"UNK":"{ 'error': '未知错误', 'explanation':f'检测到但未修正错误'}",
"R:ADJ:FORM":"{ 'error': '形容词形式错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:VERB:TENSE":"{ 'error': '动词时态缺失', 'explanation':f'建议添加动词时态<b>{edit.c_str}</b>'}",
"R:DET":"{ 'error': '冠词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:NOUN":"{ 'error': '名词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:NOUN":"{ 'error': '名词多余', 'explanation':f'名词<b>{edit.o_str}</b>疑似多余'}",
"R:NOUN:INFL":"{ 'error': '名词词形变化错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:ORTH":"{ 'error': '大小写/或空格错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:CONJ":"{ 'error': '连词缺失', 'explanation':f'建议添加连词<b>{edit.c_str}</b>'}",
"U:ADV":"{ 'error': '副词多余', 'explanation':f'副词<b>{edit.o_str}</b>疑似多余'}",
"U:PREP":"{ 'error': '介词多余', 'explanation':f'介词<b>{edit.o_str}</b>疑似多余'}",
"M:VERB":"{ 'error': '动词缺失', 'explanation':f'建议添加动词<b>{edit.c_str}</b>'}",
"U:PART":"{ 'error': '与动词构成短语动词的副词或介词多余', 'explanation':f'与动词构成短语动词的副词或介词<b>{edit.o_str}</b>疑似多余'}",
"R:OTHER":"{ 'error': '单词误用', 'explanation':f'建议修改为<b>{edit.c_str}</b>'}",
"R:PREP":"{ 'error': '介词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:INFL":"{ 'error': '动词词形变化错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:CONJ":"{ 'error': '连词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:SPELL":"{ 'error': '拼写错误', 'explanation':f'请检查<b>{edit.o_str}</b>拼写'}",
"R:MORPH":"{ 'error': '词性误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:FORM":"{ 'error': '动词形式误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:ADJ":"{ 'error': '形容词多余', 'explanation':f'形容词<b>{edit.o_str}</b>疑似多余'}",
"M:PART":"{ 'error': '与动词构成短语动词的副词或介词缺失', 'explanation':f'建议添加与动词构成短语动词的副词或介词<b>{edit.c_str}</b>'}",
"M:PUNCT":"{ 'error': '标点符号缺失', 'explanation':f'建议添加标点符号<b>{edit.c_str}</b>'}",
"R:ADV":"{ 'error': '副词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:PREP":"{ 'error': '介词缺失', 'explanation':f'建议添加介词<b>{edit.c_str}</b>'}",
"R:PRON":"{ 'error': '代词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:ADJ":"{ 'error': '形容词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:CONTR":"{ 'error': '缩略形式缺失', 'explanation':f'建议添加缩略形式<b>{edit.c_str}</b>'}",
"U:VERB:TENSE":"{ 'error': '动词时态多余', 'explanation':f'动词时态<b>{edit.o_str}</b>疑似多余'}",
"R:NOUN:POSS":"{ 'error': '名词所有格误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:TENSE":"{ 'error': '动词时态误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:VERB:FORM":"{ 'error': '动词形式多余', 'explanation':f'动词形式<b>{edit.o_str}</b>疑似多余'}",
"U:PUNCT":"{ 'error': '标点符号多余', 'explanation':f'标点符号<b>{edit.o_str}</b>疑似多余'}",
"R:NOUN:NUM":"{ 'error': '名词单复数错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB":"{ 'error': '动词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:PRON":"{ 'error': '代词缺失', 'explanation':f'建议添加代词<b>{edit.c_str}</b>'}",
"M:NOUN":"{ 'error': '名词缺失', 'explanation':f'建议添加名词<b>{edit.c_str}</b>'}",
"U:CONJ":"{ 'error': '连词多余', 'explanation':f'连词<b>{edit.o_str}</b>疑似多余'}",
"M:ADV":"{ 'error': '副词缺失', 'explanation':f'建议添加副词<b>{edit.c_str}</b>'}",
"R:PUNCT":"{ 'error': '标点符号误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:CONTR":"{ 'error': '缩略形式错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:VERB:FORM":"{ 'error': '动词形式缺失', 'explanation':f'建议添加动词形式<b>{edit.c_str}</b>'}",
"U:DET":"{ 'error': '冠词多余', 'explanation':f'冠词<b>{edit.o_str}</b>疑似多余'}",
"M:ADJ":"{ 'error': '形容词缺失', 'explanation':f'建议添加形容词<b>{edit.c_str}</b>'}",
"U:CONTR":"{ 'error': '缩略形式多余', 'explanation':f'缩略形式<b>{edit.o_str}</b>疑似多余'}",
"U:VERB":"{ 'error': '动词多余', 'explanation':f'动词<b>{edit.o_str}</b>疑似多余'}",
"U:NOUN:POSS":"{ 'error': '名词所有格多余', 'explanation':f'名词所有格<b>{edit.o_str}</b>疑似多余'}",
"R:WO":"{ 'error': '语序错误', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:PRON":"{ 'error': '代词多余', 'explanation':f'代词<b>{edit.o_str}</b>疑似多余'}",
"R:PART":"{ 'error': '与动词构成短语动词的副词或介词误用', 'explanation':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:SPACE":"{ 'error': '空格多余', 'explanation':f'建议删除空格'}",
"U:OTHER":"{ 'error': '单词冗余', 'explanation':f'建议删除<b>{edit.o_str} </b>'}",
"M:OTHER":"{ 'error': '单词缺失', 'explanation':f'建议添加<b>{edit.c_str}</b>'}",
}
for k,v in errant_type.items(): 
	rdic.hset("__errant:type", k,v )

rdic.hset("__errant:filter","R:SPELL=NNP","t.tag_ not in ('NNP','NNPS')")

cate_cn= {
"e_DET.d": "{'error':'冠词多余','explanation':f'删除<b>{text}</b>'}",
"e_DET.i": "{'error':'冠词缺失','explanation':f'添加冠词<b>{replaceText}</b>'}",
"e_DET.s":  "{'error':'冠词误用','explanation':f'建议<b>{text}</b>替换为<b>{replaceText}</b>'}", #"e_DET.s": '''{'error':'冠词误用','explanation':f"建议<b>{hit.get('text','')}</b>替换为<b>{hit.get('replaceText','')}</b>"}''',
"e_IN.d:vpn": "{'error':'介词多余','explanation':f'删除{text}'}",
"e_IN.d": "{'error':'介词多余','explanation':f'删除{text}'}",
"e_IN.i": "{'error':'介词缺失','explanation':f'添加介词{replaceText}'}",
"e_IN.s": "{'error':'介词误用','explanation':f'建议<b>{text}</b>替换为<b>{replaceText}</b>'}",
"e_NOUN.NN_NNS": "{'error':'名词误用','explanation':f'建议<b>{text}</b>替换为<b>{replaceText}</b>'}",
}
for k,v in cate_cn.items(): rdic.hset("__cate:cn", k,v)

trie_gec = {'* * + % *':"{'cate':f'e_word.miss','op':'i','ibeg':arr[i+4].i,'text':'','replaceText':arr[i+3].text}",
'* + % $':"{'cate':f'e_{arr[i+2].pos_}.miss','op':'i','ibeg':arr[i].i,'position':f'{arr[i].idx + len(arr[i].text) + 1}', 'text':arr[i+2].text}",
'* - * + %':"{'cate':f'e_{arr[i+2].pos_}.s', 'op':'s','ibeg':arr[i+2].i, 'text':arr[i+2].text, 'replaceText':arr[i+4].text}",
'+ have - VERB + VERB':"{'cate':f'e_verb.tense', 'op':'s','ibeg':arr[i+3].i, 'text':arr[i+3].text, 'replaceText':f'{arr[i+1].text} {arr[i+5].text}'}",
'- *':"{'cate':f'e_{arr[i+1].pos_}.extra', 'op':'d','ibeg':arr[i+1].i,  'text':arr[i+1].text, 'replaceText':''}",
'- * + %':"{'cate':'e_word', 'op':'s','ibeg':arr[i+1].i, 'text':arr[i+1].text, 'replaceText':arr[i+3].text}",
'- * + % + %':"{'cate':'e_word','op':'s','ibeg':arr[i+1].i, 'text':arr[i+1].text, 'replaceText':f'{arr[i+3].text} {arr[i+5].text}'}",
'- * - * + % + %':"{'cate':'e_word', 'op':'s','ibeg':{arr[i+1].i, 'text':f'{arr[i+1].text} {arr[i+3].text}', 'replaceText':f'{arr[i+5].text} {arr[i+7].text}'}",
'- have + be':"{'cate':'e_verb.have', 'op':'s','ibeg':arr[i+1].i,'text':arr[i+1].text, 'replaceText':arr[i+3].text}",
'NOUN + _mark VERB':"{'cate':'e_word.miss', 'op':'i', 'ibeg':{arr[i+3].i, 'replaceText':arr[i+2].text}",
'PRON - VBZ + VBP':"{'cate':'e_snt.nv_agree', 'op':'s','ibeg':arr[i+2].i, 'text':arr[i+2].text, 'replaceText':arr[i+4].text}",
'PRON - VBP + VBZ':"{'cate':'e_snt.nv_agree', 'op':'s','ibeg':arr[i+2].i, 'text':arr[i+2].text, 'replaceText':arr[i+4].text}",
'* + % - * *':"{'cate':'e_word.miss','op':'i','ibeg':arr[i+4].i, 'text':arr[i+2].text}", #which + has - becomes 
'^ + %':"{'op':'i','ibeg':0, 'text':arr[i+2].text}",
'^ + % + %':"{'op':'i','ibeg':0, 'text':f'{arr[i+2].text} {arr[i+4].text}'}",
'there - have + be':"{'cate':'e_verb.there', 'op':'s', 'ibeg':f'{arr[i+2].i}',  'text':f'{arr[i+2].text}', 'replaceText':f'{arr[i+4].text}', 'explanation':'<b>there be</b>句型用法错误'}",
'- a/an + the':"{'cate':'e_DET.s', 'op':'s', 'ibeg':arr[i+1].i,'text':arr[i+1].text, 'replaceText':arr[i+3].text}", 
'+ a/an NN/JJ':"{'cate':'e_DET.i', 'op':'i', 'ibeg':arr[i+2].i, 'replaceText':arr[i+1].text}",
'VERB - IN *':"{'cate':'e_IN.d:vpn', 'op':'d', 'ibeg':arr[i+2].i, 'text':arr[i+2].text}",  # contact with _sb 
'ADJ - NN + NNS *':"{'cate':'e_NOUN.NN_NNS', 'op':'s', 'ibeg':arr[i+2].i, 'text':arr[i+2].text, 'replaceText':arr[i+4].text}", # many book -> books
}
for k,v in trie_gec.items() : rdic.hset('__trie:gec', k,v )

conjs={
"引入":  ( ("首先","first of all"),("首先","to begin with"),("首先","to start with"),("以概述要点","to outline the main points"),("要想对……做出抉择","in order to decide whether or not") ),
"承接":  ( ("在此之前","previously"),("在此之前","preceding this"),("在此之前","prior to this"),("接下来","next"),("在此之后","since then"),("在此之后","afterwards"),("在此之后","following this") ),
"最后":  ( ("最后","to end with"),("最后","eventually"),("最后","ultimately"),("最后","finally"),("最后","last but not least") ),
"因果关系":  ( ("因为","because"),("因此","because of this"),("由于","since"),("由于","as"),("因为","for"),("由于","owing to"),("由于","due to"),("由于","for the reason that..."),("因为","in view of"),("由于","for such a reason"),("由……导致","as a result of"),("因此","therefore"),("因此","consequently"),("因此","as a result"),("所以","thus"),("所以","hence"),("所以","so"),("所以","so that"),("所以","in consequence"),("所以","as a consequence"),("所以","consequently"),("所以","accordingly"),("不可避免地","inevitably"),("在这种情况下","under these conditions") ),
"转折关系":  ( ("但是","but"),("即使如此","even so"),("然而","however"),("虽然","even though"),("尽管","reckless of"),("尽管","despite"),("尽管","in spite of"),("尽管","regardless of"),("尽管……但是……","while…yet…"),("除非","unless"),("然而","nevertheless"),("然而","whereas"),("虽然","although"),("虽然","though"),("恰恰相反","on the contrary") ),
"并列关系":  ( ("和","and"),("也","also"),("也","too"),("和","as well as"),("同时","meanwhile"),("同时","at the same time"),("同时","simultaneously"),("……和……两者都……","both...and..."),("一方面……另一方面……","for one thing… for another..."),("一方面……另一方面……","on the one hand… on the other hand…"),("既……又……","not only...but also...") ),
"递进关系":  ( ("此外","furthermore"),("此外","moreover"),("此外","further"),("还要，更","still"),("不但……而且……","not...but..."),("此外","in addition (to)"),("进一步","additionally"),("更具体地说","more specifically"),("其次","next"),("另外","besides"),("而且","moreover"),("而且","furthermore"),("换言之","in other words"),("甚至","even"),("尤其是","above all"),("使事情变得更好（更糟）","to make things better(worse)") ),
"比较关系（相同点）":  ( ("类似地","similarly"),("类似地","like"),("类似地","likewise"),("与……比较而言","in comparison with"),("与……比较而言","when compared with"),("与……比较而言","compared with"),("同样重要","similarly important"),("同样","as well as"),("同样","in the same way") ),
"对照关系（不同点）":  ( ("但是，然而","yet"),("但是，然而","still"),("尽管如此","for all of that"),("更准确地说","rather"),("既不……也不……","neither ... nor"),("虽然","although"),("虽然","though"),("但是","but"),("但是","however"),("恰恰相反","something is just the other way around"),("相反地","conversely"),("相反地","opposed to"),("相反地","in contrast"),("相反地","on the contrary"),("相反地","contrary to"),("与……不同","different from this"),("与……不同","nevertheless"),("与……不同","unlike"),("然而","whereas"),("然而","while"),("对比……和……","to draw/make a comparison between… and …") ),
"举例关系":  ( ("例如","for example"),("例如","for instance"),("例如","in this case"),("例如","namely"),("例如","like"),("例如","such as"),("例如","a case in point"),("众所周知","as is known to all"),("尤其；特别","in particular"),("包括","including"),("简单来说","put it simply"),("大致说来","stated roughly"),("作为例子","as an illustration"),("为了详细说明这一点，我想……","to detail this, I would like to..."),("一个很好的例子是……","a good example would be..."),("值得注意的是……","It is interesting to note that..."),("就……的例子来说","take the case of…"),("以……为例","take…as example"),("关于","as regards"),("根据","according to"),("在这种情况下","on this occasion"),("为了说明这一点","to illustrate this point"),("等等","et cetera"),("等等","and so on"),("等等","and so forth") ),
"例外关系":  ( ("除……之外","apart from"),("除……之外","except"),("除……之外","with the exception from") ),
"强调关系":  ( ("实际上","in fact"),("尤其","especially"),("尤其","particularly"),("尤其","moreover"),("顺理成章地","naturally"),("值得特别关注的是","what is particular"),("不用说；更不必说","not to mention"),("信不信由你","believe it or not"),("毫无疑问","undeniably"),("可以肯定的是……","it is certain／sure that..."),("顾名思义","by definition"),("确切地","definitely"),("毫无疑问","undoubtedly"),("毫无疑问","without a doubt"),("事实上","in truth"),("无论如何；不管怎样","in any event"),("毫无保留地","without reservation"),("显然","obviously"),("不仅仅","not only") ),
"条件关系":  ( ("如果","if"),("当……的时候","when"),("除非","unless"),("以免","lest"),("假如","provided that"),("如果是这样的话","if it is the case"),("从这种意义上来说","in this sense"),("一旦","once"),("如果可能","if possible"),("如有必要","if necessary"),("如果是这样","if so"),("要说真的有什么的话","if anything") ),
"归纳总结":  ( ("换言之","in other words"),("因此","therefore"),("因此","hence"),("简而言之","in short"),("简而言之","in brief"),("简而言之","to put it in a nutshell"),("总体上来说","in general"),("总体上来说","generally"),("总体上来说","in sum"),("总体上来说","to sum up"),("总体上来说","in conclusion"),("总体上来说","in summary"),("总体上来说","to conclude"),("总体上来说","the conclusion can be drawn that..."),("总体上来说","on the whole"),("总体上来说","to sum up"),("总体上来说","all in all"),("总体上来说","to summarize"),("基本上","basically"),("在各个方面","in all respects"),("在各个方面","in many ways"),("在各个方面","in many/most cases"),("我觉得很难得出结论，但我想说……","I find it difficult to reach a conclusion but I’m tempted to say"),("我们可以得出结论","we can draw the conclusion") ),
"方位关系":  ( ("在（或向）……较远的一边；超出","beyond"),("在对面","opposite to"),("比邻于；毗连","adjacent to"),("在同样的地方","at the same place"),("那里","there"),("在……之上","over"),("在中间","in the middle"),("在周围","around"),("在……之前","in front of"),("在远处","in the distance"),("更远的地方","farther"),("在各处；零散地","here and there"),("在……之上","above"),("在……之下","below"),("在两者之间","between"),("在这一边","on this side") ),
"目的关系":  ( ("以此为目的","with this object"),("以此为目的","for this purpose"),("为了","in order that"),("由于；既然","since"),("因此；以便","so that"),("为了那个缘故","on that account"),("为了；以便","with a view to"),("同理","for the same reason") ),
"重申关系":  ( ("换言之","in other words"),("换言之","that is to say"),("换言之","namely"),("换言之","to put it in another way"),("又一次；再次","again"),("又一次；再次","once again") ),
"时间关系":  ( ("立刻","at once"),("立刻","immediately"),("同时","in the meantime"),("同时","meanwhile"),("同时","at the same time"),("最终","in the end"),("最终","at length"),("然后","then"),("不久之后","soon"),("不久之后","not long after"),("后来","later"),("最后","at last"),("最后","finally"),("前些时；一段时间以前","some time ago"),("现在","at present"),("突然","all of a sudden"),("从这时起","from this time on"),("从那时起","since then"),("间或；偶尔","from time to time"),("在……时候","when"),("无论何时","whenever"),("几分钟之后","a few minutes later"),("以前","formerly"),("在……的时候","as"),("一旦","once"),("自从","since"),("偶尔","occasionally"),("一会儿，马上","in a moment"),("一会儿，马上","shortly"),("然后；于是","whereupon"),("（一段时间）以前","previously") ),
"结果关系":  ( ("因此","accordingly"),("因此","thus"),("因此","consequently"),("因此","hence"),("因此","thereupon"),("难以避免地","inevitably"),("在这样的情况下","under these circumstances"),("在这样的情况下","under these conditions"),("结果","as a result"),("结果","in consequence"),("结果","consequently"),("因此；以便","so that"),("因此","so"),("太……以致于","so… that") ),
"依据关系":  ( ("根据","with reference to"),("根据","regarding"),("根据","as regards"),("根据","as far as… is concerned"),("根据","according to") ),
"个人观点":  ( ("我认为……","I believe"),("据我所知","as far as I know"),("据我所知","as far as I am concerned"),("据我所知","in my opinion"),("据我所知","to my mind"),("据我所知","in my view"),("我相信……","I am convinced that"),("我坚信……","I firmly believe that") ),
"同意观点":  ( ("我完全同意……","I entirely / absolutely agree with"),("这正是我的观点","that’s exactly my own view"),("我的看法完全一样","I’m of exactly the same opinion"),("（以上观点）完全正确","that’s perfectly true"),("我倾向于支持该观点","I’d like to support this view") ),
"不同意观点":  ( ("我一定程度上同意","I partly disagree with"),("我不完全同意","I don’t entirely agree with"),("原则上我同意，但是……","I agree in principle, but"),("我的看法与之不同","That’s not the way I see it"),("我的看法与之不同","I see things rather differently myself"),("我一点都不同意……","I’m not at all convinced that"),("我对……不敢下定论","I’m not absolutely sure") ),
"兴趣或计划":  ( ("对……感兴趣","to be interested in sth / in doing sth"),("我对……十分有兴趣","It interests me a lot"),("我主要的兴趣是……","My main / particular interest is"),("我有……的打算","I have the intention of doing"),("我准备做……","I am prepared to do sth"),("我决定做……","I am determined to do sth"),("我计划做……","I’m planning to do sth"),("我热衷于……","I’m very keen on doing sth") ),
"缺少兴趣":  ( ("我觉得…相当无聊","I find … rather uninteresting / boring"),("我对……不感兴趣","I don’t take any interest in"),("是否……对我来说没有区别","It’s all the same to me whether"),("对我来说没有意义","It means nothing to me") ),
}
for k,v in conjs.items(): rdic.hset("__dic:conj", k,json.dumps(v))

rdic.hset("__trie:vp", "contact with _sb","{'cate':'e_verb.prep_extra','ibeg':ibeg,'by':'trievp'}")
rdic.hset("__trie:tag", "knowledges","{'cate':'e_noun.nns','ibeg':ibeg, 'text':doc[ibeg].text}")
rdic.hset("__trie:tag", "DT key of DT door","{'cate':'e_prep','ibeg':ibeg, 'text':'of', 'replaceText':'to' }")
rdic.hset("__trie:tag", "a lot of the","{'cate':'e_art.extra','ibeg':ibeg, 'text':doc[ibeg+3].text, 'replaceText':''}")
rdic.hset("__trie:iftrue:as JJR NNS as", "doc[i+1].text.lower() not in {'more','less'}","{'cate':'e_adj.jjr','ibeg':ibeg+1, 'text':doc[ibeg+1].text}")
rdic.hset("__trie:np", "many teacher","{'cate':'e_noun.nns_exp','by':'trienp'}")
rdic.hset("__trie:np", "CD apples tree","{'cate':'e_noun.nn_exp','by':'trienp'}")
rdic.hset("__trie:snt", "IN NP , IN NP CC RB/ IN NP .","{'cate':'e_snt.frag','ie':'In Japan, during the last war and just before the armistice.'}")
rdic.hset("__trie:snt", "TO VB IN NN IN NN IN NN .","{'cate':'e_snt.frag','ie':'To apply for a job at the new store in the mall.'}")
rdic.hset("__trie:snt", "TO VB IN NP IN NP IN NP .","{'cate':'e_snt.frag','ie':'To apply for a job at the new store in the mall.'}")
rdic.hset("__trie:snt", "VBG RB/ IN NP IN NP TO VB NP .","{'cate':'e_snt.frag','ie':'Working far into the night in an effort to salvage her little boat.'}")
rdic.hset("__code:snt_has", " ,",'''r.hset(snt,'e_punct:comma_space_prefix', "{'error':'No space before comma'}")''')
rdic.hset("__code:tok_has", "not only",'''if not 'but also' in line: r.hset(snt, 'e_pair:not_only:but_also', "{'cate':'e_pair', 'error':'not only/but also'}" )''')
rdic.hset("__code:tok_has", "but also",'''if not 'not only' in line: r.hset(snt, 'e_pair:not_only:but_also', "{'cate':'e_pair', 'error':'not only/but also'}" )''')
rdic.hset("__code:tok_has", ", but",'''if '^ although' in line: r.hset(snt, 'e_pair:although:but', "{'cate':'e_pair', 'error':'although/but'}" )''')
rdic.hset("__stop:np","many book",'book')
rdic.hset("__stop:dobj","learn knowledge", 1)
rdic.hset("__stop:dobj","open light", 1)

map_formula= {"ast":[0.12,[9.9, 11.99, 15.3, 18.51, 25.32],2],"awl":[0.12,[3.5, 4.1, 4.56, 5.1, 6.0],3],"b3":[0.13,[0, 0.03, 0.08, 0.12, 0.15],1],"cl_sum":[0.06,[1, 6.68, 12, 16, 26],2],"grammar_correct_ri":[0.05,[0.6, 0.85, 0.92, 0.97,1.0],2],"internal_sim":[0.1,[0.0, 0.08, 0.2, 0.3, 0.4],4],"kp_correct_ri":[0.05,[0.7, 0.9, 0.95, 0.97, 1],1],"mwe_pv":[0.03,[0.01,8.03, 12, 20.21, 25],4],"pred_diff_max3":[0.05,[3.84, 5.11, 6.51, 7.9, 10.09],1],"prmods_ratio":[0.04,[0.06, 0.21, 0.3, 0.4, 0.5],2],"prmods_tc":[0.05,[1.1, 2.76, 4.75, 6.76, 10.0],2],"simple_sent_ri":[0.05,[0.4, 0.65, 0.9, 0.95, 1],2],"snt_correct_ratio":[0.05,[0.01, 0.2, 0.45, 0.75, 1],1],"spell_correct_ratio":[0.2,[0.8, 0.9, 0.97, 0.99, 1],1],"ttr1":[0.12,[3.43, 4.28, 5.2, 6, 6.8],3],"word_diff_avg":[0.06,[4.47, 4.73, 5.25,5.8, 6.6],1],"word_gt7":[0.08,[0.11, 0.19, 0.3, 0.42, 0.49],1]}
def init_formula():
	k = "__formula:default"
	if not rdic.exists(k): 
		[rdic.hset(k, name, json.dumps(v)) for name, v in map_formula.items()]

if __name__ == '__main__':
	#init_data()
	init_formula()
	print(rdic.scan(0, count=10))

#September was nearing, and part of me did not want to leave.  Noticing that Grandpa was gazing at Grandma’s photo rooted to the ground again and again, my desire to stay with him became stronger and stronger. However, this idea was extremely objected by Grandpa. “School is your own place.” He patted my shoulder gently. On the day when I leave for my college, I gave him a big hug．As I drove away,  in the rearview mirror of my car, I found him stood himself upright and waved at me, wearing a faint smile.Mum called me at school on a windy October day.  Choked by tears, she informed me that Grandpa had died of a stroke, same as Grandma. As I entered the crowded room, it is a relief for me that there was a calm and peaceful expression on Grandpa’s face. Next to him, lied a photo in which they smiled brightly. It was that moment that I understood Grandpa’s words near the pond——nothing could separate the permanent love.
