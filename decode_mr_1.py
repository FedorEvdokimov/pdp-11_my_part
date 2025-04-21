import pyparsing as pp
import re


def to3bit(x):
    res = str(bin(int(x))[2:])
    while len(res) < 3:
        res = '0' + res
    return res

def to_four_digit_hex_number(x):
    res = str(hex(int(x)))[2:]
    while len(res) < 4:
        res = '0' + res
    return res

#Пока без label (лейблы могут быть, но они никак не обрабатываются и не записываются в машинный код)

command_description = {
    # Однобайтовые команды
    'halt': {
        'opcode': '0' * 16,  #Код операции MOV (в hex)
        'args': []
    },
    # Двухадресные команды
    'mov': {
        'opcode': '0001',
        'args': ['mr', 'mr']  #ss = mr, dd = mr - mode, register
    },
    'add': {
        'opcode': '0110',
        'args': ['mr', 'mr']
    },
}

def get_command_by_name(name):
    return command_description[name]

def to16bit(x):
    res = bin(x)[2:]
    while len(res) < 16:
        res = '0' + res
    return res

def from8to10(s):
    x = 0
    s = s[::-1]
    for i in range(len(s)):
        x += int(s[i]) * 8**i
    return x

def from8to16bit(s):
    return  to16bit(from8to10(s))

modes = (
    pp.Regex(r'^R.')('000') | # R3, mode = '000'
    pp.Regex(r'^\(R.\)$')('001') |  # (R3), mode = '001'
    pp.Regex(r'^')
)

result = modes.parseString('(R3)', parseAll=True)
print(result)
print(next(name for name in ['000', '001', '010', '011', '100', '101', '110', '111'] if name in result))



"""
def decode_mr_arg(arg):
    additional_word = ''
    mode = ''
    register = ''
    if arg[0] == 'r': # R3
        mode = '000'
        register = to3bit(arg[1])
    elif  arg[0] == '(' and arg[-1] == ')': # (R3)
        mode = '001'
        register = to3bit(arg[2])
    elif arg[0] == '(' and arg[-1] == '+': # (R3)+
        mode = '010'
        register = to3bit(arg[2])
    elif arg[0] == '@' and arg[-1] == '+': # @(R3)+
        mode = '011'
        register = to3bit(arg[3])
    elif arg[0] == '-':  # -(R3)
        mode = '100'
        register = to3bit(arg[3])
    elif arg[0] == '@' and arg[1] == '-': # @-(R3)
        mode = '101'
        register = to3bit(arg[4])
    elif arg[0] == '@' and arg[-1] == ')': # @2(R3)
        mode = '111'
        register = to3bit(arg[-2])
        additional_word = from8to16bit(arg[1:-4])
    elif arg[0] in '01234567' and arg[-1] == ')': # 2(R3)
        mode = '110'
        register = to3bit(arg[-2])
        additional_word = from8to16bit(arg[:-4])
    elif arg[0] == '#': # #3
        mode = '010'
        register = '111'
        additional_word = from8to16bit(arg[1:])
    elif arg[0] == '@' and arg[1] == '#': # @#100
        mode = '011'
        register = '111'
        additional_word = from8to16bit(arg[2:])
    elif arg[0] == '@' and arg[1] != '#': # @100
        mode = '111'
        register = '111'
        additional_word = from8to16bit(arg[1:])
    elif arg[0] in '01234567': # 100
        mode = '110'
        register = '111'
        additional_word = from8to16bit(arg)
    code_arg = mode + register
    return code_arg, additional_word
"""


"""
import pyparsing as pp
import re

# Создаем парсеры для каждой моды с сохранением типа
modes = (
    pp.Regex(r'^a', re.IGNORECASE)('mode0') |  # mode0 если начинается на a/A
    pp.Regex(r'^b', re.IGNORECASE)('mode1') |  # mode1 если начинается на b/B
    pp.Regex(r'^c', re.IGNORECASE)('mode2')    # mode2 если начинается на c/C
)

# Функция для определения моды
def determine_mode(word):
    try:
        result = modes.parseString(word, parseAll=False)
        print("result:",result)
        return next(name for name in ['mode0', 'mode1', 'mode2'] if name in result)
    except:
        return "UNKNOWN"

# Тестирование
test_words = ["apple", "Banana", "cherry", "123", " dog", "Carrot", "boat"]
for word in test_words:
    print(f"{word!r}: {determine_mode(word)}")
    print()
"""