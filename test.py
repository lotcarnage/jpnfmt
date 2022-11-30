import jpnfmt

JAPANESE_TEXT = '''
MSRとはMean Square Rootの略である。
'''[1:-1]


def _main():
    print('123|567890T')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 4, True))
    print('123|567890F')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 4, False))
    print('1234|67890T')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 5, True))
    print('12345|7890F')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 5, False))
    print('12345|7890T')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 6, True))
    print('12345|7890F')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 6, False))
    print('123456789|T')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 10, True))
    print('123456789|F')
    print(jpnfmt.textwrap_force(JAPANESE_TEXT, 10, False))

    print('123|567890T')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 4, True))
    print('123|567890F')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 4, False))
    print('1234|67890T')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 5, True))
    print('12345|7890F')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 5, False))
    print('12345|7890T')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 6, True))
    print('12345|7890F')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 6, False))
    print('123456789|T')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 10, True))
    print('123456789|F')
    print(jpnfmt.textwrap_overrun(JAPANESE_TEXT, 10, False))

    return None


if __name__ == '__main__':
    _main()
