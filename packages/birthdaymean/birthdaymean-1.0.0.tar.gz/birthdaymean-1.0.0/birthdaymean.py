# -*- coding: UTF-8 -*-

L=['猴','鸡','狗','猪','鼠','牛','虎','兔','龙','蛇','马','羊']
zodiac_name = ['摩羯座','水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座']
zodiac_date = [(1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23)]

def Animal(year):
    return L[year%12]

def zodiac(month,day):
    #return (zodiac_name[len(list(filter(lambda x: x < (month, day), zodiac_date))) % 12])
    for i in range(0,12):
        if (month,day) < zodiac_date[i]:
            return zodiac_name[i]
    return zodiac_name[0]

def allmean(y,m,d):
    return [Animal(y),zodiac(m,d)]

