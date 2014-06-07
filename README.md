pydaminfo
=======
Python2.7対応。  
国土交通省 川の防災情報(river.go.jp)からダムの情報（貯水率等）を取得するためのPythonモジュールです。  
ダムbot(https://twitter.com/sameura_dam )で使用しているものと同じものです。

How to use
-------
DamInfoのコンストラクタに観測所記号を指定してください。観測所記号はリアルタイムダム諸量一覧表(DspDamData.exe)に記載されています。  
例：早明浦ダム 1368080700010 （2014年6月現在）
あるいは引数のIDにある値と同じです。

    >>> from daminfo import DamInfo
    >>> sameura = DamInfo('1368080700010')
    >>> sameura.getRecentPerOfStorage()
    (u'2014/06/07', u'20:00', u'87.9')


dependency
------
標準モジュールのみ

license
------ 
GNU AFFERO GENERAL PUBLIC LICENSE Version 3


TODO
-------
* 任意期間ダム諸量検索（過去のダム情報）への対応
* Python3への対応
