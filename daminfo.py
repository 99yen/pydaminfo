#!/usr/bin/env python
# coding: utf-8

import urllib2
import re

class DamInfo:
	BASE_URL = 'http://www1.river.go.jp'
	REALTIME_URL = '/cgi-bin/DspDamData.exe?ID={damid}&KIND=3&PAGE=0'
	DEFAULT_ENCODE = 'euc-jp'
	USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'

	def __init__(self, damid):
		self.damid = damid

	def getRecentPerOfStorage(self):
		info = self.getRealtimeDaminfo()
		for line in reversed(info):
			attribute = line[11]
			if attribute != '-':
				date = line[0]
				time = line[1]
				pos = line[10]
				break
		else:
			raise "Can't find PerOfStorage"
		return date, time, pos

	def getRealtimeDaminfo(self):
		contents = self._fetchContents(self._getRealtimeUrl, 'euc-jp', self._getCsvUrl, 'cp932')
		info = self._formatCsv(contents)
		return info

	def _formatCsv(self, data):
		lines = data.strip().split('\r\n')[9:]
		table = [l.split(',') for l in lines]
		return table

	def _fetchContents(self, getOuterUrl, outerCharset, getInnerUrl, innerCharset):
		outer_url = getOuterUrl()
		outer_contents = self._httpGet(outer_url, outerCharset)
		inner_url = getInnerUrl(outer_contents)
		try:
			contents = self._httpGet(inner_url, innerCharset)
		except urllib2.HTTPError:
			# retry
			outer_contents = self._httpGet(outer_url, outerCharset)
			inner_url = getInnerUrl(outer_contents)
			contents = self._httpGet(inner_url, innerCharset)
		return contents

	def _httpGet(self, url, encode = DEFAULT_ENCODE):
		headers = {'User-Agent': self.USER_AGENT}
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)
		contents = response.read().decode(encode)
		return contents

	def _getRealtimeUrl(self):
		url = self.BASE_URL + self.REALTIME_URL.format(damid = self.damid)
		return url

	def _getCsvUrl(self, contents):
		p = re.compile(r'<A href="(/dat/dload/download/\d+\.dat)" target="_blank">')
		m = p.search(contents)
		if m is not None:
			url = self.BASE_URL + m.group(1)
			return url
		else:
			raise "Can't find csv url"
