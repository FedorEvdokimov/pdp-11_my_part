import pyparsing as pp
import re


#.venv\Scripts\activate
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

mode_reg = (
    pp.Regex(r'^R[1-7]$')('000') | # R3, mode = '000'
    pp.Regex(r'^\(R[1-7]\)$')('001') |  # (R3), mode = '001'
    pp.Regex(r'^\(R[1-7]\)\+$')('010') | # (R3)+, mode = '010'
    pp.Regex(r'^@\(R[1-7]\)\+$')('011') | # @(R3)+, mode = '011'
    pp.Regex(r'^-\(R[1-7]\)$')('100') | # -(R3), mode = '100'
    pp.Regex(r'^@-\(R[1-7]\)$')('101') | # @-(R3), mode = '101',
    pp.Regex(r'^[1-7]+\(R[1-7]\)$')('110') | # 2(R3), mode = '110'
    pp.Regex(r'^@[1-7]+\(R[1-7]\)$')('111') | # @2(R3), mode = '111'
    #Ниже регистр у всех равен '111'
    pp.Regex(r'^#[0-7]+$')('010' + '111') | # #3, mode = '010'
    pp.Regex(r'^@#[0-7]+')('011' + '111') | # @#100, mode = '011'
    pp.Regex(r'^[0-7]+')('110' + '111') | # 100, mode = '110'
    pp.Regex(r'^@[0-7]+')('111' + '111')  # @100, mode = '111'

)
#runtests!

mode_reg.runTests('''
R3
(R3)
(R3)+
@(R3)+
-(R3)
@-(R3)
277(R3)
@26(R3)
#7777
@#100
100
@100
''' )



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
