import pyparsing as pp

# Улучшенные определения элементов
identifier = pp.Word(pp.alphas, pp.alphanums + "_")
mnemonic = pp.oneOf("mov add sub halt", caseless=True)  # Список команд
command_name = mnemonic("command")

# Числа: #10 или 10 (целые)
number = pp.Combine(pp.Optional('#') + pp.Word(pp.nums))
# Регистры: r0, r1, ..., r15
register = pp.Combine(pp.CaselessLiteral('r') + pp.Word(pp.nums, max=2))
argument = number | register | identifier
arguments = pp.Group(pp.delimitedList(argument, delim=pp.Suppress(',')))("args")

label = (identifier + pp.Suppress(":"))("label")
comment = (pp.Suppress(';') + pp.restOfLine.setParseAction(lambda t: t[0].strip()))("comment")

# Основное правило
rule = (
    pp.Optional(label, default='')
    + pp.Optional(command_name, default='')
    + pp.Optional(arguments, default=[])
    + pp.Optional(comment, default='')
)

debug_mode = False

def parse_line(s):
    s = s.lower().strip()
    if s[0] == '.':
        s = s.replace(" ", "")
        return {'label': '', 'command_name': 'start_from_address', 'arguments': [ s[2:] ], 'comment': ''}
    parsed = rule.parseString(s, parseAll=True)
    args = []
    if len(parsed.args) != 0:
        args = parsed.args.asList()
    comment = ''
    if parsed.comment  != '':
        comment = parsed.comment[0]
    label = ''
    if parsed.label != '':
        label = parsed.label[0]
    result = {
        'label': label,
        'command_name': parsed.command if 'command' in parsed else '',
        'arguments': args,
        'comment': comment
    }
    return result

assembler_code = []
blocks = []
dict_machine_code = {'start': '', 'data': []}

filename = 'asm_code.txt'
with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.lower().strip()
        assembler_code.append(parse_line(line))

print("assembler_code:", assembler_code)

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

def decode_mr_arg(arg):
    """
    :param arg:
    :return:
    только для ss и dd: mode, register
    """
    print("decode_mr_arg")
    print("arg:", arg)
    mode_reg = (
            pp.Regex(r'^r[0-7]$').setParseAction(lambda t: f'000{to3bit(t[0][1])}')('code') |  # R3, mode = '000'
            pp.Regex(r'^\(r[0-7]\)$').setParseAction(lambda t: f'001{to3bit(t[0][2])}')('code') |  # (R3), mode = '001'
            pp.Regex(r'^\(r[0-7]\)\+$').setParseAction(lambda t: f'010{to3bit(t[0][2])}')(
                'code') |  # (R3)+, mode = '010'
            pp.Regex(r'^@\(r[0-7]\)\+$').setParseAction(lambda t: f'011{to3bit(t[0][3])}')(
                'code') |  # @(R3)+, mode = '011'
            pp.Regex(r'^-\(r[0-7]\)$').setParseAction(lambda t: f'100{to3bit(t[0][3])}')(
                'code') |  # -(R3), mode = '100'
            pp.Regex(r'^@-\(r[0-7]\)$').setParseAction(lambda t: f'101{to3bit(t[0][4])}')(
                'code') |  # @-(R3), mode = '101',
            pp.Regex(r'^[1-7]+\(r[0-7]\)$').setParseAction(
                lambda t: f'110{to3bit(t[0][-2]) + from8to16bit(t[0][:-4])}')('code') |  # 2(R3), mode = '110'
            pp.Regex(r'^@[1-7]+\(r[0-7]\)$').setParseAction(
                lambda t: f'111{to3bit(t[0][-2]) + from8to16bit(t[0][1:-4])}')('code') |  # @2(R3), mode = '111'
            pp.Regex(r'^#[0-7]+$').setParseAction(lambda t: f'010111{from8to16bit(t[0][1:])}')(
                'code') |  # #3, mode = '010'
            pp.Regex(r'^@#[0-7]+').setParseAction(lambda t: f'011111{from8to16bit(t[0][2:])}')(
                'code') |  # @#100, mode = '011'
            pp.Regex(r'^[0-7]+').setParseAction(lambda t: f'110111{from8to16bit(t[0])}')('code') |  # 100, mode = '110'
            pp.Regex(r'^@[0-7]+').setParseAction(lambda t: f'111111{from8to16bit(t[0][1:])}')('code') # @100, mode = '111'
    )
    res = (mode_reg.parseString(arg))[0]
    print("mode_reg.parseString(arg):", res)
    print("type:", type(res))
    if len(res) == 6:
        res = [res, '']
    elif len(res) == 6 + 16:
        res = [res[:6], res[6:]]
    return res


#def decode_mr_arg()






#на случай # у нас есть переменные additional...
def cmd_to_raw_machine_code(command, start_address=None):
    """
    Перевод {'label': 'label1', 'command_name': 'mov', 'arguments': ['#3', 'r1'], 'comment': 'comment2'}
     в ['0001010111000001', '0003'], только вмсто 0003 тавим 16 бит которые соответствуют 0003 или как? в принципеможно просто
     0003 оставить и потом просто на длину смотртеь? было бы прощ
    """

    """
        Перевод ['mov', '#2', 'r0'] в [0o012700, 2]
        """
    # по имени команды записываешь в результирующее слово опкод команды
    print()
    print("command:", command)
    command_name = command['command_name']
    print("command_name:", command_name)
    if command_name == 'start_from_address':
        return [command['arguments'][0], 'num_of_bytes_in_file']

    cmd = get_command_by_name(command_name)
    """return {
        'opcode': '1000',
        'args': ['ss', 'dd'],  # source, destination
    }"""
    print("cmd:", cmd)
    parse_args = command['arguments'] #['#2', 'r1']
    command_code = cmd['opcode']
    additional_words = []
    print("parse_args:", parse_args)
    for arg, parse_arg in zip(cmd['args'], parse_args):
        # arg='mr', parse_arg='#2'
        code_arg = ''
        additional_word = ''
        match arg:
            case 'mr':
                print("parse_arg:", parse_arg)
                print("decoded:", decode_mr_arg(parse_arg))
                code_arg = decode_mr_arg(parse_arg)[0]
                additional_word = decode_mr_arg(parse_arg)[1]
                print("code_arg:", code_arg)
                print("additional_word:", additional_word)
                command_code += code_arg
                if additional_word != '':
                    additional_words.append(additional_word)
            # code_arg = '010111'  27
            # additional_word = '...'   2  вот тут может быть использование лейбла и его посчитаем во второй проход
            # code_arg добавляем в кодировку текущей команды
            # если дополнительное слово есть, его присоедняем к списку слов
    res = [command_code]
    for w in additional_words:
        res.append(w)
    print("return:", res)
    print()
    return res

def asm_to_binary_code(asm_code):
    res = []
    for line in asm_code:
        bin_numbers = cmd_to_raw_machine_code(line)
        for bin_num in bin_numbers:
            res.append(bin_num)
    return res

binary_code = asm_to_binary_code(assembler_code)
print("binary_code:", binary_code)

def from2to10(s):
    s = s[::-1]
    x = 0
    for i in range(len(s)):
        x += int(s[i]) * 2**i
    return x

def bits_to_bytes(bin_command_code):
    piece1 = bin_command_code[:4]
    piece2 = bin_command_code[4:8]
    piece3 = bin_command_code[8:12]
    piece4 = bin_command_code[12:]
    # print("pieces", piece1, piece2, piece3, piece4)
    num1 = hex(int(piece1, 2))[2:] + hex(int(piece2, 2))[2:]
    num2 = hex(int(piece3, 2))[2:] + hex(int(piece4, 2))[2:]
    machine_command = [num2, num1]
    return machine_command


machine_code = []
for line in binary_code:
    if len(line) != 16:
        machine_code.append(line)
        continue
    byte1, byte2 = bits_to_bytes(line)
    machine_code.append(byte1)
    machine_code.append(byte2)
print("machine_code:", machine_code)
