
# 巨大オブジェクトのデバッグ表示 [sout]
# 【動作確認 / 使用例】

import sys
from relpath import rel2abs
sys.path.append(rel2abs("../"))
# 巨大オブジェクトのデバッグ表示 [sout]
from sout import sout

# 使用例1
large_obj = [[1,2,3] for _ in range(9999)]
sout(large_obj)

# 使用例2

# 巨大辞書生成
def gen_huge_dic(n, gen_value_func):
	return {"key_%d"%i: gen_value_func(i)
		for i in range(n)}

# テスト用データ
temp_ls = 132
def gen_value_func(i):
	return gen_huge_dic(300, lambda i: temp_ls)	# 巨大辞書生成
dummy_huge_data = gen_huge_dic(300, gen_value_func)	# 巨大辞書生成

# 巨大オブジェクトのデバッグ表示 [sout]
sout(dummy_huge_data)
