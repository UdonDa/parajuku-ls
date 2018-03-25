import os, sys
sys.path.append(os.getcwd())

from place_regex.PuriparaRegex import PuriparaRegex

def test1():
    p = PuriparaRegex()
    assert "渋谷" == p.matching("東京都渋谷区道玄坂")

def test2():
    p = PuriparaRegex()
    assert "千代田" == p.matching("東京都千代田区秋葉原 千代田区有料トイレ")

def test3():
    p = PuriparaRegex()
    assert "八王子" == p.matching("東京都八王子市高倉町55−4")

