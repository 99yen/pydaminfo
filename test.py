#!/usr/bin/env python
# coding: utf-8

import unittest
import daminfo

outerHtml = u'''<HTML>
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

csvContents = u'''リアルタイムダム諸量一覧表
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
'''.replace('\n','\r\n')

class DamInfoTest(unittest.TestCase):
	def setUp(self):
		self.daminfo = daminfo.DamInfo('1368080700010')

	def test_getRealtimeUrl(self):
		ru = 'http://www1.river.go.jp/cgi-bin/DspDamData.exe?ID=1368080700010&KIND=3&PAGE=0'
		tu = self.daminfo._getRealtimeUrl()
		self.assertEqual(tu, ru)

	def test_getCsvUrl(self):
		ru = 'http://www1.river.go.jp/dat/dload/download/5313680807000102014053117221.dat'
		tu = self.daminfo._getCsvUrl(outerHtml)
		self.assertEqual(tu, ru)

	def test_format_Csv(self):
		ru = [['2014/05/31', '00:50', '0.0', ' ', '158020', ' ', '9.94', ' ', '22.50', ' ', '0.0', '-'], \
 		      ['2014/05/31', '01:00', '0.0', ' ', '158020', ' ', '8.56', ' ', '22.30', ' ', '89.7', ' '], \
		      ['2014/05/31', '01:10', '0.0', ' ', '157970', ' ', '8.46', ' ', '23.80', ' ', '0.0', '-']]
 		tu = self.daminfo._formatCsv(csvContents)
 		self.assertEqual(tu, ru)

 	def test_getRecentPerOfStorage(self):
 		ru = ('2014/05/31', '01:00', '89.7')
 		self.daminfo.getRealtimeDaminfo = lambda: self.daminfo._formatCsv(csvContents)
 		tu = self.daminfo.getRecentPerOfStorage()
 		self.assertEqual(tu, ru)

if __name__ == '__main__':
	unittest.main()
