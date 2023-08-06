
# 巨大オブジェクトのデバッグ表示 [sout]

import sys
import json

indent_str = "  "

# コンテナ的な型の表示
def container_stringify(
	iter_target,	# イテレート対象
	element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
	brackets,	# 括弧
	indent_depth,	 # インデント深さ
	element_limit	# 省略の度合い
):
	if element_limit is None: element_limit = len(iter_target)
	bra, ket = brackets
	show_ls = []
	show_ls.append(bra)
	for i,e in enumerate(iter_target):
		if i >= element_limit:
			show_ls.append("%s... (all_n = %d)"%(indent_str*(indent_depth+1), len(iter_target)))
			break
		show_ls.append("%s%s,"%(
			indent_str*(indent_depth+1),	# インデント
			element_str_func(e)
		))
	show_ls.append("%s%s"%(indent_str*indent_depth, ket))
	show_str = "\n".join(show_ls)
	return show_str

# show_strが短いときは一行で表示する
def one_line(show_str, limit_n):
	# 改行やタブを省略してみる
	rep_str = show_str
	for sep in ["\n", "\t"]:
		rep_str = rep_str.replace(sep, " ")
	ls = rep_str.split(" ")
	ls = [e for e in ls if len(e) > 0]
	short_s = " ".join(ls)
	# 文字長判断
	if len(short_s) > limit_n:
		return show_str
	else:
		return short_s

# 再帰的に可視化につかうオブジェクトを作る
def gen_show_str(data, element_limit, indent_depth):
	if type(data) == type({}):
		def element_str_func(key):
			return "%s: %s"%(
				gen_show_str(key, element_limit, indent_depth+1),	# キー
				gen_show_str(data[key], element_limit, indent_depth+1)	# 値
			)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["{", "}"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit	# 省略の度合い
		)
	elif type(data) == type([]):
		# リストの場合
		def element_str_func(elem):
			return gen_show_str(elem, element_limit, indent_depth+1)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["[", "]"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit	# 省略の度合い
		)
	elif type(data) == type(()):
		# タプルの場合
		def element_str_func(elem):
			return gen_show_str(elem, element_limit, indent_depth+1)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["(", ")"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit	# 省略の度合い
		)
	elif type(data) == type(""):
		# 文字列の場合
		show_str = json.dumps(data, ensure_ascii = False)
	else:
		show_str = str(data)
	# show_strが短いときは一行で表示する
	show_str = one_line(show_str, limit_n = 20)
	return show_str

# 巨大オブジェクトのデバッグ表示 [sout]
def sout(
	data,	# 表示すべきデータ
	element_limit = 5	# 省略の度合い (None指定で全表示)
):
	show_str = gen_show_str(data, element_limit, indent_depth = 0)	# 再帰的に可視化につかうオブジェクトを作る
	print(show_str)
