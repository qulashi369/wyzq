#coding: utf8

#books = [ '星河大帝',   '雪中悍刀行', '光明纪元', '神印王座',   '宠魅', '官场之风流人生',  '王牌情敌',  '异世灵武天下']

#books = ['绝世唐门', '莽荒纪', '傲世九重天', '剑道独尊', '凡人修仙传', '大主宰', '痒', '求魔', '校花的贴身高手', '武动乾坤', '斗破苍穹', '最强弃少', '圣堂', '星河大帝', '全职高手', '我的美女总裁老婆', '医道官途', '唐砖', '将夜', '火爆天王', '神武', '首席御医', '重生小地主', '雪中悍刀行', '光明纪元', '神印王座', '校园全能高手', '官术', '武神空间', '九星天辰诀', '宠魅', '官场之风流人生', '大圣传', '雄霸蛮荒', '红色仕途', '遮天', '悍戚', '醉枕江山', '天骄无双', '奥术神座', '武极天下', '斩龙', '我们是兄弟', '明末边军一小兵', '王牌情敌', '权财', '吞噬星空', '异世灵武天下', '花都十二钗', '无尽剑装']


def load():
    bs = open("books.txt", "r")
    return (b for i, b in enumerate(bs) if i <250)

books = load()

# 150:16
