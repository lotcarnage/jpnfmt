""" 日本語整形モジュール
日本語を整形するためのモジュールです。
"""
import unicodedata
from enum import Enum


def _正規化(日本語混じり文字列: str):
    return ''.join([行 for 行 in 日本語混じり文字列.split('\n')])


def _文字幅(文字: str):
    return 2 if unicodedata.east_asian_width(文字[0]) in 'FWA' else 1


def _文字幅配列を日本語混じり文字列から作る(日本語混じり文字列: str):
    文字幅配列 = [_文字幅(文字) for 文字 in 日本語混じり文字列]
    return 文字幅配列


def _全角文字列と半角文字列を分離する(正規化済み日本語混じり文字列: str) -> list[str]:
    文字幅配列 = _文字幅配列を日本語混じり文字列から作る(正規化済み日本語混じり文字列)
    segments = []
    head_index = 0
    is_asian = (文字幅配列[0] == 2)
    for i in range(len(文字幅配列)):
        if is_asian:
            if 文字幅配列[i] != 2 and 正規化済み日本語混じり文字列[i] != ' ':
                segments.append({'sentence': 正規化済み日本語混じり文字列[head_index:i], 'is_asian': is_asian})
                head_index = i
                is_asian = False
        else:
            if 文字幅配列[i] == 2:
                スペース区切り半角文字列 = 正規化済み日本語混じり文字列[head_index:i]
                半角文字列配列 = [文字列断片.strip() for 文字列断片 in スペース区切り半角文字列.split()]
                for 半角文字列 in 半角文字列配列:
                    segments.append({'sentence': 半角文字列, 'is_asian': False})
                head_index = i
                is_asian = True
    else:
        segments.append({'sentence': 正規化済み日本語混じり文字列[head_index:i + 1], 'is_asian': is_asian})
    return segments


class WrapType(Enum):
    UNDERRUN = 0,
    OVERRUN = 1,
    FORCE = 2,


def _textwrap_overrun(文字列断片配列: list[dict[str, bool]], 行表示幅: int, 端数はみだし有効: bool):
    新しい文字列 = []
    行幅 = 0
    for i, 文字列断片 in enumerate(文字列断片配列):
        if 文字列断片['is_asian']:
            if (行表示幅 - 行幅) < (2 if 端数はみだし有効 else 3):
                新しい文字列.append('\n')
                行幅 = 0
            else:
                if 0 < i and 0 < 行幅:
                    新しい文字列.append(' ')
                    行幅 += 1
            for 文字 in 文字列断片['sentence']:
                if (not 端数はみだし有効) < (行表示幅 - 行幅):
                    新しい文字列.append(文字)
                    行幅 += 2
                else:
                    if 文字 == '。':
                        新しい文字列.append(文字)
                        新しい文字列.append('\n')
                    else:
                        新しい文字列.append('\n')
                        新しい文字列.append(文字)
                    行幅 = 2
        else:
            if (行表示幅 - 行幅) < 2:
                新しい文字列.append('\n')
                行幅 = 0
            else:
                if 0 < i and 0 < 行幅:
                    新しい文字列.append(' ')
                    行幅 += 1
            新しい文字列.append(文字列断片['sentence'])
            行幅 += len(文字列断片['sentence'])

    return 新しい文字列


def textwrap_overrun(japanese_text: str, line_width: int, allow_fraction_over: bool):
    """ 日本語文章を整形する関数（英語行末はみだし）

    :arg japanese_text: 日本語文章文字列
    :line_width １行で許容できる表示幅
    :allow_fraction_over 行末の半端な文字のはみだしを許容するか
    """

    normalized = _正規化(japanese_text)
    文字列断片配列 = _全角文字列と半角文字列を分離する(normalized)
    新しい文字列 = _textwrap_overrun(文字列断片配列, line_width, allow_fraction_over)
    return ''.join(新しい文字列)


def _textwrap_force(文字列断片配列: list[dict[str, bool]], 行表示幅: int, 端数はみだし有効: bool):
    新しい文字列 = []
    行幅 = 0
    for i, 文字列断片 in enumerate(文字列断片配列):
        if 文字列断片['is_asian']:
            if (行表示幅 - 行幅) < (2 if 端数はみだし有効 else 3):
                新しい文字列.append('\n')
                行幅 = 0
            else:
                if 0 < i and 0 < 行幅:
                    新しい文字列.append(' ')
                    行幅 += 1
            for 文字 in 文字列断片['sentence']:
                if (not 端数はみだし有効) < (行表示幅 - 行幅):
                    新しい文字列.append(文字)
                    行幅 += 2
                else:
                    新しい文字列.append('\n')
                    新しい文字列.append(文字)
                    行幅 = 2
        else:
            if (行表示幅 - 行幅) < (2 if 端数はみだし有効 else 3):
                新しい文字列.append('\n')
                行幅 = 0
            else:
                if 0 < i and 0 < 行幅:
                    新しい文字列.append(' ')
                    行幅 += 1
            for 文字 in 文字列断片['sentence']:
                if 行幅 < (行表示幅 - int(not 端数はみだし有効) * 1):
                    新しい文字列.append(文字)
                    行幅 += 1
                else:
                    新しい文字列.append('-\n')
                    新しい文字列.append(文字)
                    行幅 = 1
    return 新しい文字列


def textwrap_force(japanese_text: str, line_width: int, allow_fraction_over: bool):
    """ 日本語文章を整形する関数（英語強制折り返し）

    :arg japanese_text: 日本語文章文字列
    :line_width １行で許容できる表示幅
    :allow_fraction_over 行末の半端な文字のはみだしを許容するか
    """
    normalized = _正規化(japanese_text)
    文字列断片配列 = _全角文字列と半角文字列を分離する(normalized)
    新しい文字列 = _textwrap_force(文字列断片配列, line_width, allow_fraction_over)
    return ''.join(新しい文字列)
