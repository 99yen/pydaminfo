#!/usr/bin/env python
# coding: utf-8

import unittest
from mock import Mock, patch

import daminfo

OUTER_HTML = u'''<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>リアルタイムダム諸量一覧表</TITLE>
</HEAD>
<BODY bgcolor="#ffffff">
<CENTER>
<P align="center"><FONT size="+2">リアルタイムダム諸量一覧表</FONT>
<A href="/dat/dload/download/5313680807000102014053117221.dat" target="_blank"><IMG src="/img/download.gif" BORDER="0"></A>
<P align="center"><FONT size="+1"><B>2014/5/31 ～ 2014/6/7</B></FONT></CENTER>
<IFRAME src="/html/frm/DamFree10Data2014060718552017221.html" scrolling="AUTO" width="840" height="65%" align="right" frameborder="0"  style="border-width : 0px 0px 0px 0px;"></IFRAME>
</BODY>
</HTML>'''

CSV_CONTENTS = u'''リアルタイムダム諸量一覧表
水系名,吉野川
河川名,吉野川
観測所名,早明浦ダム（機構）
観測所記号,1368080700010
#
#年月日,時刻,流域平均雨量,流域平均雨量属性,貯水量,貯水量属性,流入量,流入量属性,放流量,放流量属性,貯水率,貯水率属性
#属性　$:欠測 -:未受信
#
2014/05/31,00:50,0.0, ,158020, ,9.94, ,22.50, ,0.0,-
2014/05/31,01:00,0.0, ,158020, ,8.56, ,22.30, ,89.7, 
2014/05/31,01:10,0.0, ,157970, ,8.46, ,23.80, ,0.0,-
'''.replace('\n', '\r\n')

class DamInfoTest(unittest.TestCase):
    def setUp(self):
        self.daminfo = daminfo.DamInfo('1368080700010')

    def test_get_realtime_url(self):
        expected_val = 'http://www1.river.go.jp/cgi-bin/DspDamData.exe?ID=1368080700010&KIND=3&PAGE=0'
        return_val = self.daminfo._get_realtime_url()
        self.assertEqual(return_val, expected_val)

    def test_get_csv_url(self):
        expected_val = 'http://www1.river.go.jp/dat/dload/download/5313680807000102014053117221.dat'
        return_val = self.daminfo._get_csv_url(OUTER_HTML)
        self.assertEqual(return_val, expected_val)

    def test_format_csv(self):
        expected_val = [['2014/05/31', '00:50', '0.0', ' ', '158020', ' ', '9.94', ' ', '22.50', ' ', '0.0', '-'], \
                        ['2014/05/31', '01:00', '0.0', ' ', '158020', ' ', '8.56', ' ', '22.30', ' ', '89.7', ' '], \
                        ['2014/05/31', '01:10', '0.0', ' ', '157970', ' ', '8.46', ' ', '23.80', ' ', '0.0', '-']]
        return_val = self.daminfo._format_csv(CSV_CONTENTS)
        self.assertEqual(return_val, expected_val)

    @patch('daminfo.DamInfo.get_realtime_daminfo')
    def test_get_latest_storage(self, m):
        m.return_value =  self.daminfo._format_csv(CSV_CONTENTS)
        expected_val = ('2014/05/31', '01:00', '89.7')
        return_val = self.daminfo.get_latest_storage()
        self.assertEqual(return_val, expected_val)

    @patch('daminfo.DamInfo.get_realtime_daminfo')
    def test_calc_latest_storage(self, m):
        m.return_value =  self.daminfo._format_csv(CSV_CONTENTS)
        expected_val = ('2014/05/31', '01:10', '91.8')
        self.daminfo.maximum_storage = 172000
        return_val = self.daminfo.calc_latest_storage()
        self.assertEqual(return_val, expected_val)

if __name__ == '__main__':
    unittest.main()
