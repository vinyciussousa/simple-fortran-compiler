import re

regular_expression = {
    r'^program$': 'program',
    r'^end$': 'end',
    r'^integer$': 'integer',
    r'^real$': 'real',
    r'^logical$': 'logical',
    r'^if$': 'if',
    r'^then$': 'then',
    r'^else$': 'else',
    r'^endif$': 'endif',
    r'^do$': 'do',
    r'^while$': 'while',
    r'^enddo$': 'enddo',
    r'^print$': 'print',
    r'^::$': '::',
    r'^=$': '=',
    r'^\($': '(',
    r'^\)$': ')',
    r'^,$': ',',
    r'^\+$': '+',
    r'^-$': '-',
    r'^\*$': '*',
    r'^/$': '/',
    r'^\.and\.$': '.and.',
    r'^\.or\.$': '.or.',
    r'^\.not\.$': '.not.',
    r'^\.true\.$': '.true.',
    r'^\.false\.$': '.false.',
    r'^==$': '==',
    r'^/=$': '/=',
    r'^>$': '>',
    r'^<$': '<',
    r'^>=$': '>=',
    r'^<=$': '<=',
    r'^[a-zA-Z][a-zA-Z0-9_]*$': 'identifier',
    r'^[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?$': 'number'
}

def lexical_analyzer(filepath) -> str:
    with open(filepath, 'r') as f:
        token_sequence = []
        line_number = 1
        for line in f:
            line = line.strip()
            if not line:  
                continue
        
            tokens = re.findall(r'\S+|[()]', line)
            
            for t in tokens:
                found = False
                for regex, category in regular_expression.items():
                    if re.match(regex, t):
                        token_sequence.append((category,t))
                        #token_sequence.append(category)
                        found = True
                        break
                if not found:
                    print('Lexical error in line', line_number, ':',t)
                    exit(0)
            
            line_number += 1

    token_sequence.append('$')
    #print(token_sequence)
    return token_sequence