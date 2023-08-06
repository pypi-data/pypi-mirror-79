
# local log (globalスコープを汚さないログツール) [llog]

import sys
from sout import sout

# local log (globalスコープを汚さないログツール) [llog]
class LLog:
	# 初期化処理
	def __init__(self, filename):
		self.filename = filename
	# ログ出力 (level: debug) [llog]
	def debug(self, log_obj):
		# debug出力
		sout(log_obj)
