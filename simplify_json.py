import re


def parse_simplified_format(input_string: str) -> dict:
    """
    "key1: value1, key2: value2" のような単純化された形式の文字列をパースし、
    Pythonの辞書に変換します。

    JSONの "key1": value1, "key2": value2 の代わりに、より簡易的な
    key1: value1, key2: value2 形式を扱えます。

    特徴:
    - キーと値のペアはカンマ (,) で区切られます。
    - 各ペア内で、キーと値はコロン (:) で区切られます。
    - キー、値、区切り文字の周りの空白は無視されます。
    - キーは引用符で囲まず、Pythonの識別子に似た形式（英字またはアンダースコアで始まり、
      英数字またはアンダースコアが続く）である必要があります。
    - 値は整数または浮動小数点数として解釈されます。

    例:
    "x: 0.1, y: 2" -> {'x': 0.1, 'y': 2}
    "count:100, price:9.99" -> {'count': 100, 'price': 9.99}

    Args:
        input_string: パース対象の文字列。

    Returns:
        パース結果のPython辞書。

    Raises:
        ValueError: 文字列の形式が無効な場合（例: キーの形式が不正、値が数値でない等）。
    """
    result = {}

    # 空白のみの文字列や空文字列の場合は空の辞書を返す
    if not input_string.strip():
        return result

    # 1. カンマでキー・値ペアの候補に分割
    #    例: "x: 0.1 ,  y: 2" -> ["x: 0.1 ", "  y: 2"]
    raw_pairs = input_string.split(',')

    for pair_str_candidate in raw_pairs:
        # 各ペア候補の前後の空白を除去
        # 例: "x: 0.1 " -> "x: 0.1"
        pair_str = pair_str_candidate.strip()

        if not pair_str:  # カンマが連続している場合など (例: "a:1,,b:2") は無視
            continue

        # 2. コロンでキーと値の文字列に分割
        #    最初のコロンのみで分割する (キー名にコロンを含まない前提)
        #    例: "x: 0.1" -> ["x", " 0.1"]
        parts = pair_str.split(':', 1)
        if len(parts) != 2:
            raise ValueError(
                f"無効なキー・値ペアの形式です: '{pair_str}'. "
                f"各ペアは 'キー:値' の形式で、コロンで区切られている必要があります。"
            )

        key = parts[0].strip()
        value_str = parts[1].strip()

        # 3. キーのバリデーション
        #    英字またはアンダースコアで始まり、英数字またはアンダースコアのみ許容
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", key):
            raise ValueError(
                f"無効なキー名: '{key}'. キーは英字またはアンダースコアで始まり、"
                f"英数字またはアンダースコアのみ使用できます。"
            )

        # 値が空文字列でないことを確認 (例: "x:")
        if not value_str:
            raise ValueError(
                f"キー '{key}' に対する値が空です。"
            )

        # 4. 値の文字列を数値 (整数または浮動小数点数) に変換
        try:
            # まず整数として解釈を試みる
            value = int(value_str)
        except ValueError:
            try:
                # 整数でなければ浮動小数点数として解釈を試みる
                value = float(value_str)
            except ValueError:
                # どちらの数値型にも変換できない場合はエラー
                raise ValueError(
                    f"キー '{key}' の値 '{value_str}' を数値（整数または小数）に"
                    f"変換できませんでした。"
                )

        # 5. 結果の辞書に追加
        #    キーが重複した場合、後の値で上書きされます (Pythonのdictの標準的な挙動)
        if key in result:
            # 必要であれば重複キーに関する警告を出すこともできます
            # print(f"警告: キー '{key}' が重複しています。値を {result[key]} から {value} に上書きします。")
            pass
        result[key] = value

    return result


# --- 関数の使用例 ---
# if __name__ == '__main__':
#     # 正常系テスト
#     print("--- 正常系テスト ---")
#     test_strings_ok = [
#         "x: 0.1, y:2",
#         "x:0.1,y:2",
#         "  item_count  :  100  ,  price  :  9.99  ",
#         "z_index: -5, scale: 1.0",
#         "singleKey:123",
#         "a:1,b:2,c:3,d:4,e:5",
#         "value:0",
#         "",  # 空文字列
#         "   ",  # 空白のみ
#         "key1: 10 , key1: 20",  # 重複キー (後者で上書き)
#         " trailing_comma_test : 1 , ",  # 末尾のカンマ (結果は {'trailing_comma_test': 1})
#     ]
#
#     for s in test_strings_ok:
#         try:
#             parsed_dict = parse_simplified_format(s)
#             print(f"入力: \"{s}\" -> 出力: {parsed_dict}")
#         except ValueError as e:
#             print(f"入力: \"{s}\" -> エラー: {e} (これは予期せぬエラーです)")
#
#     # 異常系テスト (ValueErrorが発生することを期待)
#     print("\n--- 異常系テスト (ValueErrorを期待) ---")
#     test_strings_fail = [
#         "x:0.1,y",  # 値にコロンがない
#         "x:0.1,y:abc",  # 値が数値でない
#         "x:0.1,:2",  # キーが空
#         "1key:0.1,y:2",  # キーが数字で始まる
#         "key with space:1",  # キーにスペースが含まれる
#         "x:val1:val2",  # コロンが多すぎる (値部分にコロンは不可)
#         "x:",  # 値が空
#     ]
#
#     for s in test_strings_fail:
#         try:
#             parsed_dict = parse_simplified_format(s)
#             print(f"入力: \"{s}\" -> 出力: {parsed_dict} (エラーが発生しませんでした)")
#         except ValueError as e:
#             print(f"入力: \"{s}\" -> 期待通りのエラー: {e}")