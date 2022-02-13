
import pandas as pd
from itertools import combinations, permutations
import argparse


def combine(types, num):
    comb = combinations(types, num)
    return list(comb)


def lookup(attack, defend):
    return float(df.loc[df.iloc[:, 0] == attack][defend])

##  case 1: 攻方克制的属性，即技能属性，技能属性只有一个
##  attack_type 攻击属性
##  all_combines 所有考虑的属性组合（最多为2，单属性需要用无元素补全tuple）
##  same_type bool 类型，宝可梦是否有这个技能的属性
##  df  data frame for the input sheet
def attack_side(attack_type, all_combines, same_type: bool, df):
    strong = []
    weak = []
    normal = []
    for comb in all_combines:
        mul = 1.0
        if same_type:
            mul = 1.5
        for t in comb:
            mul = mul * lookup(attack_type, t)
        if mul > 1.0:
            strong.append((comb, mul))
        elif mul < 1.0:
            weak.append((comb, mul))
        else:
            normal.append((comb, mul))
    return (strong, weak, normal)


##  case 2: 防守方克制的属性，即我们不怕什么攻击
##  攻击方只会有一个属性，所以这里是all_types不是all_combines
def defend_side(defend_types, all_types, same_type: bool, df):
    strong = []
    weak = []
    normal = []
    for attack_type in all_types:
        mul = 1.0
        if same_type:
            mul = 1.5
        for t in defend_types:
            mul = mul * lookup(attack_type, t)
        if mul < 1.0:
            strong.append(((attack_type,), mul))
        elif mul > 1.0:
            weak.append(((attack_type,), mul))
        else:
            normal.append(((attack_type,), mul))
    return (strong, weak, normal)


def to_string(info):
    types = info[0]
    mul = info[1]
    if len(types) == 1:
        return types[0] + ' ' + str(mul)
    elif len(types) == 2:
        return types[0] + '+' + types[1] + ' ' + str(mul)


def print_set(the_set, muls):
    for comb in the_set:
        print(comb, muls[comb])


def runs_attacker(attacker_types, combs, df):
    types_set = set(combs)
    perms = permutations(attacker_types, len(attacker_types))

    for perm in perms:
        p = False
        for t in attacker_types:
            strong, weak, normal = attack_side(t, combs, True, df)
            muls = {}
            for (comb, mul) in weak:
                muls[comb] = mul
            weak = set([comb for (comb, _) in weak])
            new_types_set = types_set.intersection(weak)
            if len(new_types_set) > 0:
                types_set = new_types_set
                p = True
            else:
                print_set(types_set, muls)
                types_set = set(combs)
                p = False
        if p:
            print_set(types_set, muls)
        print('=' * 120)




    # print('克制：')
    # for res in strong:
    #     print(to_string(res))

    # print()
    # print('被克：')
    # for res in weak:
    #     print(to_string(res))


# def runs_defender(types, all_types, df):
#     strong, weak, normal = defend_side(types, [t for (t,) in all_types], True, df)
#     print('克制：')
#     for res in strong:
#         print(to_string(res))

#     print()
#     print('被克：')
#     for res in weak:
#         print(to_string(res))
    
#     print()
#     print('普通')
#     for res in normal:
#         print(to_string(res))

'''
已知攻击类型，求一个或几个属性组合，能counter全部
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--types', nargs='+', required=True)
    args = parser.parse_args()
    # for _, value in parser.parse_args()._get_kwargs():
        # if len(value) == 1:
        #     attacker_types = (value[0],)
        # elif len(value) == 2:
        #     attacker_types = tuple(value)
    attacker_types = args.types
    

    filename = "克制关系表.ods"

    df = pd.read_excel(filename)
    df = df.fillna(1)

    types = list(df.columns[1:])
    combs = combine(types, 2)
    types = [(i,) for i in types]
    combs = combs + types
    # 好像没什么用，提示都有
    runs_attacker(attacker_types, combs, df)
    # print('=' * 120)

    # print(defender_types)
    # runs_defender(defender_types, False, types, df)
