#!/usr/bin/env python
# coding: utf-8

import urllib2
import re

class DamInfo(object):
    BASE_URL = 'http://www1.river.go.jp'
    REALTIME_URL = '/cgi-bin/DspDamData.exe?ID={damid}&KIND=3&PAGE=0'
    DEFAULT_ENCODE = 'euc-jp'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
    REGXP_CSV_URL = r'<A href="(/dat/dload/download/\d+\.dat)" target="_blank">'

    def __init__(self, damid, maximum_storage=0):
        self.damid = damid
        self.maximum_storage = maximum_storage

    def get_latest_storage(self):
        info = self.get_realtime_daminfo()
        for line in reversed(info):
            attribute = line[11]
            if not attribute.strip():
                date = line[0]
                time = line[1]
                percent = line[10]
                break
        else:
            raise Exception("Could not find storage information")
        return date, time, percent

    def calc_latest_storage(self):
        info = self.get_realtime_daminfo()
        date = info[-1][0]
        time = info[-1][1]
        percent = "{:.1f}".format(float(info[-1][4]) / self.maximum_storage * 100)
        return date, time, percent

    def get_realtime_daminfo(self):
        contents = self._fetch_contents(self._get_realtime_url, 'euc-jp',
                                        self._get_csv_url, 'cp932')
        info = self._format_csv(contents)
        return info

    def _format_csv(self, data):
        lines = data.strip().split('\r\n')[9:]
        table = [l.split(',') for l in lines]
        return table

    def _fetch_contents(self, get_outer, outer_charset, get_inner, inner_charset):
        outer_url = get_outer()
        outer_contents = self._http_get(outer_url, outer_charset)
        inner_url = get_inner(outer_contents)
        try:
            contents = self._http_get(inner_url, inner_charset)
        except urllib2.HTTPError:
            # retry
            outer_contents = self._http_get(outer_url, outer_charset)
            inner_url = get_inner(outer_contents)
            contents = self._http_get(inner_url, inner_charset)
        return contents

    def _http_get(self, url, encode=DEFAULT_ENCODE):
        headers = {'User-Agent': self.USER_AGENT}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        contents = response.read().decode(encode)
        return contents

    def _get_realtime_url(self):
        url = self.BASE_URL + self.REALTIME_URL.format(damid=self.damid)
        return url

    def _get_csv_url(self, contents):
        c_regxp = re.compile(self.REGXP_CSV_URL)
        mached = c_regxp.search(contents)
        if mached is not None:
            url = self.BASE_URL + mached.group(1)
            return url
        else:
            raise Exception("Could not find csv url")
