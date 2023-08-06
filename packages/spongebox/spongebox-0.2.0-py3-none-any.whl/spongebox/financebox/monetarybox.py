import spongebox.structbox as structbox
import re


def decompose_amount(cn_amount):
    if len(cn_amount) <= 1:
        return cn_amount
    # print(cn_amount)
    _ = re.search(
        "(?P<yi>.*亿)*(?P<wan>.*万)*(?P<qian>.*[千仟])*(?P<bai>.*[百佰])*(?P<shi>.*[十拾])*(?P<yuan>.*[元圆块])*(?P<jiao>.*[角毛])*(?P<fen>.*分)*(?P<tbd>.*)",
        cn_amount)
    ret = [_.group("yi"), _.group("wan"), _.group("qian"), _.group("bai"), _.group("shi"), _.group("yuan"),
           _.group("jiao"), _.group("fen"), _.group("tbd")]
    # print(ret)

    only_tbd = True
    for p in ret[:-1]:
        if p != None:
            only_tbd = False
            break
    if only_tbd:
        return list(ret[-1] + "零零")

    ret = [amt if amt != None else "" for amt in ret]

    def switch(i, stop):
        if ret[i - 1] == "" and i > stop:
            ret[i - 1], ret[i] = ret[i], ret[i - 1]
            switch(i - 1, stop)
        else:
            pass

    if ret[8] != "":
        stop = 4
        if "零" in ret[8]:
            stop = 5
        switch(8, stop)
    units = ["亿", "万", "仟千", "佰百", "拾十", "元圆块", "角毛", "分"]
    for i in range(0, 8):
        for unit in units[i]:
            ret[i] = ret[i].replace(unit, "")
    ret = [x.lstrip("零") for x in ret]
    ret = [x if x != "" else "零" for x in ret]
    ret[1] = decompose_amount(ret[1])[2:6]
    # ret = flatten_list(ret)
    ret[0] = decompose_amount(ret[0])[:-2]
    ret = [x if x != "" else "零" for x in ret]
    # print(ret[:8])
    # print()
    return ret[:8]


def digitalize_chinese_moneytary(cn_amount):
    print(cn_amount)
    cn_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8,
              '玖': 9, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2}
    ret = ""
    _ = ""
    if len(cn_amount) == 1:
        _ = cn_amount + "零零"
    else:
        _ = decompose_amount(cn_amount)
        _ = "".join(structbox.flatten_list(_))
    for n in _:
        ret += str(cn_num[n])
    ret = int(ret)
    print(ret)
    print()
    return ret


if __name__ == "__main__":
    _ = []
    _.append(digitalize_chinese_moneytary("玖仟捌佰柒拾陆万伍仟肆佰叁拾贰亿壹仟零玖拾捌万柒仟陆佰伍拾肆元叁角贰分") == 987654321098765432)
    _.append(digitalize_chinese_moneytary("柒仟陆佰伍拾肆元叁角贰分") == 765432)
    _.append(digitalize_chinese_moneytary("柒仟陆佰伍拾肆元贰分") == 765402)
    _.append(digitalize_chinese_moneytary("一千零四") == 100400)
    _.append(digitalize_chinese_moneytary("一千零四拾") == 104000)
    _.append(digitalize_chinese_moneytary("一千零四拾五") == 104500)
    _.append(digitalize_chinese_moneytary("一块两毛二") == 122)
    _.append(digitalize_chinese_moneytary("三百四") == 34000)
    _.append(digitalize_chinese_moneytary("三百零四") == 30400)
    _.append(digitalize_chinese_moneytary("三百零四块") == 30400)
    _.append(digitalize_chinese_moneytary("三千叁佰万") == 3300000000)
    _.append(digitalize_chinese_moneytary("二十") == 2000)
    _.append(digitalize_chinese_moneytary("一块二") == 120)
    _.append(digitalize_chinese_moneytary("三毛一") == 31)
    _.append(digitalize_chinese_moneytary("三块") == 300)
    _.append(digitalize_chinese_moneytary("三百") == 30000)
    _.append(digitalize_chinese_moneytary("三") == 300)
    _.append(digitalize_chinese_moneytary("壹二三") == 12300)
    _.append(digitalize_chinese_moneytary("九八三四") == 983400)
    print(_)
