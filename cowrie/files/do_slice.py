# -*- coding: utf-8 -*-


def trim(s):
    sindex = 0
    word = s[sindex:sindex+1]
    while word == ' ':
        sindex = sindex + 1
        word = s[sindex:sindex + 1]
    ecount = -1
    word = s[ecount:]
    if word == ' ':
        while word == ' ':
            ecount = ecount-1
            word = s[ecount:]
    else:
        ecount=s.__len__()
    return s[sindex:ecount]


# 测试:
if trim('hello  ') != 'hello':
    print('测试失败!  1')
elif trim('  hello') != 'hello':
    print('测试失败!  2')
elif trim('  hello  ') != 'hello':
    print('测试失败!  3')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!  4')
elif trim('') != '':
    print('测试失败!  5')
elif trim('    ') != '':
    print('测试失败!  6')
else:
    print('测试成功!')