import inspect
from grammar import Grammar
from predict import predict_algorithm
from token_sequence import token_sequence
from var_control import var_control
from file_control import open_file, write_to_file, close_file

sp = 1 
label_control = 0
var_manager = var_control()

def get_func_name():
    return inspect.stack()[1][3]

def increment_sp():
    global sp
    sp += 1

def decrement_sp():
    global sp
    sp -= 1

def label_manager():
    global label_control
    label_control += 1
    return f'L{label_control}'

def arithmetic_operation(op, type1, type2):
    if type1 == 'real' and type2 == 'real':
        if op == '+':
            return 'ADDF'
        elif op == '-':
            return 'SUBF'
        elif op == '*':
            return 'TIMESF'
        elif op == '/':
            return 'DIVF'
    else:
        if op == '+':
            return 'ADD'
        elif op == '-':
            return 'SUB'
        elif op == '*':
            return 'TIMES'
        elif op == '/':
            return 'DIV'

def simple_fortran()->Grammar:
    G = Grammar()

    # Não terminais
    G.add_nonterminal('PROGRAM')
    G.add_nonterminal('BODY')
    G.add_nonterminal('STATEMENT')
    G.add_nonterminal('DECLARATION')
    G.add_nonterminal('ASSIGNMENT')
    G.add_nonterminal('IF_STATEMENT')
    G.add_nonterminal('END_IF')
    G.add_nonterminal('DO_LOOP')
    G.add_nonterminal('EXPRESSION')
    G.add_nonterminal('END_EXPRESSION')
    G.add_nonterminal('TERM')
    G.add_nonterminal('END_TERM')
    G.add_nonterminal('FACTOR')
    G.add_nonterminal('PRINT_STATEMENT')
    G.add_nonterminal('RELATIONAL_OPERATOR')
    G.add_nonterminal('LOGICAL_OPERATOR')

    # Terminais
    G.add_terminal('program')
    G.add_terminal('end')
    G.add_terminal('integer')
    G.add_terminal('real')
    G.add_terminal('logical')
    G.add_terminal('if')
    G.add_terminal('then')
    G.add_terminal('else')
    G.add_terminal('endif')
    G.add_terminal('do')
    G.add_terminal('while')
    G.add_terminal('enddo')
    G.add_terminal('print')
    G.add_terminal('::')
    G.add_terminal('=')
    G.add_terminal('(')
    G.add_terminal(')')
    G.add_terminal(',')
    G.add_terminal('+')
    G.add_terminal('-')
    G.add_terminal('*')
    G.add_terminal('/')
    G.add_terminal('.and.')
    G.add_terminal('.or.')
    G.add_terminal('.not.')
    G.add_terminal('.true.')
    G.add_terminal('.false.')
    G.add_terminal('==')
    G.add_terminal('/=')
    G.add_terminal('>')
    G.add_terminal('<')
    G.add_terminal('>=')
    G.add_terminal('<=')
    G.add_terminal('identifier')
    G.add_terminal('number')
    G.add_terminal('$')

    # Produções básicas
    G.add_production('PROGRAM', ['program', 'identifier', 'BODY', 'end'])
    G.add_production('BODY', ['STATEMENT', 'BODY'])
    G.add_production('BODY', [])
    G.add_production('STATEMENT', ['DECLARATION'])
    G.add_production('STATEMENT', ['ASSIGNMENT'])
    G.add_production('STATEMENT', ['IF_STATEMENT'])
    G.add_production('STATEMENT', ['DO_LOOP'])
    G.add_production('STATEMENT', ['PRINT_STATEMENT'])
    G.add_production('DECLARATION', ['integer', '::' , 'identifier'])
    G.add_production('DECLARATION', ['real', '::' , 'identifier'])
    G.add_production('DECLARATION', ['logical', '::' , 'identifier'])
    G.add_production('ASSIGNMENT', ['identifier', '=', 'EXPRESSION'])

    # Produções condicionais
    G.add_production('IF_STATEMENT', ['if', '(', 'EXPRESSION', ')', 'BODY', 'END_IF'])
    G.add_production('END_IF', ['else', 'BODY', 'endif'])
    G.add_production('END_IF', ['endif'])

    # Produções de laço
    G.add_production('DO_LOOP', ['do', 'while', '(','EXPRESSION',')', 'BODY', 'enddo'])
    G.add_production('PRINT_STATEMENT', ['print', '*', ',', 'identifier'])
    
    # Produções lógicas e aritméticas
    # Justificativa para como simplifiquei a precedencia: https://www.tutorialspoint.com/fortran/fortran_operators_precedence.htm
    G.add_production('EXPRESSION', ['TERM', 'END_EXPRESSION'])
    G.add_production('END_EXPRESSION', ['+', 'TERM', 'END_EXPRESSION'])
    G.add_production('END_EXPRESSION', ['-', 'TERM', 'END_EXPRESSION'])
    G.add_production('END_EXPRESSION', ['RELATIONAL_OPERATOR', 'TERM', 'END_EXPRESSION'])
    G.add_production('END_EXPRESSION', ['LOGICAL_OPERATOR', 'TERM', 'END_EXPRESSION'])
    G.add_production('END_EXPRESSION', [])

    G.add_production('TERM', ['FACTOR', 'END_TERM'])
    G.add_production('END_TERM', ['*', 'FACTOR', 'END_TERM'])
    G.add_production('END_TERM', ['/', 'FACTOR', 'END_TERM'])
    G.add_production('END_TERM', [])
    
    G.add_production('FACTOR', ['(', 'EXPRESSION', ')'])
    G.add_production('FACTOR', ['identifier'])
    G.add_production('FACTOR', ['number'])
    G.add_production('FACTOR', ['.true.'])
    G.add_production('FACTOR', ['.false.'])
    G.add_production('FACTOR', ['.not.', 'FACTOR'])

    # Operadores lógicos e relacionais
    G.add_production('RELATIONAL_OPERATOR', ['=='])
    G.add_production('RELATIONAL_OPERATOR', ['/='])
    G.add_production('RELATIONAL_OPERATOR', ['>'])
    G.add_production('RELATIONAL_OPERATOR', ['<'])
    G.add_production('RELATIONAL_OPERATOR', ['>='])
    G.add_production('RELATIONAL_OPERATOR', ['<='])

    G.add_production('LOGICAL_OPERATOR', ['.and.'])
    G.add_production('LOGICAL_OPERATOR', ['.or.'])

    G.add_nonterminal('RETURN')
    G.add_production('RETURN', ['identifier'])
    G.add_production('RETURN', ['number'])
    G.add_production('RETURN', [])

    return G

def RETURN(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(94):
        ts.match('identifier')
    elif ts.peek() in p.predict(95):
        ts.match('number')
    elif ts.peek() in p.predict(96):
        return
    else:
        print('Syntax error at',get_func_name())
        exit(0)


def LOGICAL_OPERATOR(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(91):
        ts.match('.and.')
        return 'AND'
    elif ts.peek() in p.predict(92):
        ts.match('.or.')
        return 'OR'
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def RELATIONAL_OPERATOR(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(85):
        ts.match('==')
        return 'EQUAL'
    elif ts.peek() in p.predict(86):
        ts.match('/=')
        return 'EQUAL\nNOT'
    elif ts.peek() in p.predict(87):
        ts.match('>')
        return 'GREATER'
    elif ts.peek() in p.predict(88):
        ts.match('<')
        return 'LESS'
    elif ts.peek() in p.predict(89):
        ts.match('>=')
        #Se a < b, ISNEG coloca 1, NOT (0)
        #Se a = b, ISNEG coloca 0, NOT (1)
        #Se a > b, ISNEG coloca 0, NOT (1)
        return 'SUB\nISNEG\nNOT'
    elif ts.peek() in p.predict(90):
        ts.match('<=')
        #Se a > b, ISPOS coloca 1, NOT (0)
        #Se a = b, ISPOS coloca 0, NOT (1)
        #Se a < b, ISPOS coloca 0, NOT (1)
        return 'SUB\nISPOS\nNOT'
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def FACTOR(ts: token_sequence, p: predict_algorithm) -> str:
    if ts.peek() in p.predict(79):
        ts.match('(')
        expr_type = EXPRESSION(ts, p)
        ts.match(')')
        return expr_type
    elif ts.peek() in p.predict(80):
        var = ts.value()
        var_type = var_manager.get_variable_type(var)
        value = var_manager.get_variable(var)
        ts.match('identifier')
        write_to_file(f'PUSHABS {value}')
        return var_type
    elif ts.peek() in p.predict(81):
        value = ts.value()
        if '.' in value:
            write_to_file(f'PUSHIMMF {value}')
            ts.match('number')
            return 'real'
        else:
            write_to_file(f'PUSHIMM {value}')
            ts.match('number')
            return 'integer'
    elif ts.peek() in p.predict(82):
        ts.match('.true.')
        write_to_file('PUSHIMM 1')
        return 'logical'
    elif ts.peek() in p.predict(83):
        ts.match('.false.')
        write_to_file('PUSHIMM 0')
        return 'logical'
    elif ts.peek() in p.predict(84):
        ts.match('.not.')
        factor_type = FACTOR(ts, p)
        if factor_type != 'logical':
            raise TypeError(f'NOT. operator expects logical type, but received: {factor_type}')
        write_to_file('NOT')
        return 'logical'
    else:
        print('Syntax error at', get_func_name())
        exit(0)
        
def END_TERM(ts: token_sequence, p: predict_algorithm, term_type) -> str:
    if ts.peek() in p.predict(76):
        ts.match('*')
        factor_type = FACTOR(ts, p)
        op = arithmetic_operation('*', term_type, factor_type)
        write_to_file(op)
        end_type = END_TERM(ts, p, 'real' if (term_type == 'real' or factor_type == 'real') else 'integer')
        return end_type
    elif ts.peek() in p.predict(77):
        ts.match('/')
        factor_type = FACTOR(ts, p)
        op = arithmetic_operation('/', term_type, factor_type)
        write_to_file(op)
        end_type = END_TERM(ts, p, 'real' if (term_type == 'real' or factor_type == 'real') else 'integer')
        return end_type
    elif ts.peek() in p.predict(78):
        return term_type
    else:
        print('Syntax error at', get_func_name())
        exit(0)
    
def TERM(ts: token_sequence, p: predict_algorithm) -> str:
    if ts.peek() in p.predict(75):
        factor_type = FACTOR(ts, p)
        term_type = END_TERM(ts, p, factor_type)
        return term_type
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def END_EXPRESSION(ts: token_sequence, p: predict_algorithm, expr_type) -> str:
    if ts.peek() in p.predict(70):
        ts.match('+')
        term_type = TERM(ts, p)
        if expr_type != term_type:
            raise TypeError(f'Incompatible types: {expr_type} e {term_type}')
        op = arithmetic_operation('+', expr_type, term_type)
        write_to_file(op)
        end_type = END_EXPRESSION(ts, p, expr_type)
        return end_type
    elif ts.peek() in p.predict(71):
        ts.match('-')
        term_type = TERM(ts, p)
        if expr_type != term_type:
            raise TypeError(f'Incompatible types: {expr_type} e {term_type}')
        op = arithmetic_operation('-', expr_type, term_type)
        write_to_file(op)
        end_type = END_EXPRESSION(ts, p, expr_type)
        return end_type
    elif ts.peek() in p.predict(72):
        OP = RELATIONAL_OPERATOR(ts, p)
        term_type = TERM(ts, p)
        if expr_type != term_type:
            raise TypeError(f'Incompatible types: {expr_type} e {term_type}')
        write_to_file(OP)
        END_EXPRESSION(ts, p, 'logical')
        return 'logical'
    elif ts.peek() in p.predict(73):
        op = LOGICAL_OPERATOR(ts, p)
        if expr_type != 'logical':
            raise TypeError(f'Logical operator expects logical type, but received: {expr_type}')
        term_type = TERM(ts, p)
        if term_type != 'logical':
            raise TypeError(f'Logical operator expects logical type, but received: {term_type}')
        write_to_file(op)
        END_EXPRESSION(ts, p, 'logical')
        return 'logical'
    elif ts.peek() in p.predict(74):
        return expr_type
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def EXPRESSION(ts: token_sequence, p: predict_algorithm) -> str:
    if ts.peek() in p.predict(69):
        term_type = TERM(ts, p)
        expr_type = END_EXPRESSION(ts, p, term_type)
        return expr_type
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def PRINT_STATEMENT(ts: token_sequence, p: predict_algorithm) -> None:
    if ts.peek() in p.predict(68):
        ts.match('print')
        ts.match('*')
        ts.match(',')
        var = ts.value()
        value = var_manager.get_variable(var)
        write_to_file(f'PUSHABS {value}')
        var_type = var_manager.get_variable_type(var)
        if var_type == 'real':
            write_to_file('WRITEF')
        elif var_type == 'logical':
            write_to_file('WRITE')
        else:
            write_to_file('WRITE')
        ts.match('identifier')
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def DO_LOOP(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(67):
        ts.match('do')
        ts.match('while')
        loop_start = label_manager()
        loop_end = label_manager()
        write_to_file(f'{loop_start}:')
        ts.match('(')
        EXPRESSION(ts,p)
        ts.match(')')
        write_to_file('ISNIL')
        write_to_file(f'JUMPC {loop_end}')
        BODY(ts,p)
        write_to_file(f'JUMP {loop_start}')
        write_to_file(f'{loop_end}:')
        ts.match('enddo')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def END_IF(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(65):
        ts.match('else')
        BODY(ts,p)
        ts.match('endif')
    elif ts.peek() in p.predict(66):
        ts.match('endif')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def IF_STATEMENT(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(64):
        ts.match('if')
        ts.match('(')
        EXPRESSION(ts,p)
        ts.match(')')
        ts.match('then')
        else_label = label_manager()
        end_if_label = label_manager()
        write_to_file('ISNIL')
        write_to_file(f'JUMPC {else_label}')
        BODY(ts,p)
        write_to_file(f'JUMP {end_if_label}')
        write_to_file(f'{else_label}:')
        END_IF(ts,p)
        write_to_file(f'{end_if_label}:')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def ASSIGNMENT(ts: token_sequence, p: predict_algorithm) -> None:
    if ts.peek() in p.predict(63):
        var = ts.value()
        ts.match('identifier')
        ts.match('=')
        var_type = var_manager.get_variable_type(var)
        expr_type = EXPRESSION(ts, p)
        if var_type != expr_type:
            raise TypeError(f'Incompatible type: attempt to assign {expr_type} to variable {var} of type {var_type}')
        value = var_manager.get_variable(var)
        write_to_file(f'STOREABS {value}')
        var_manager.set_variable(var, value, var_type)
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def DECLARATION(ts: token_sequence, p: predict_algorithm) -> None:
    global sp
    if ts.peek() in p.predict(60):
        ts.match('integer')
        ts.match('::')
        var = ts.value()
        if var_manager.is_variable_declared(var):
            raise ValueError(f"Error: Variable '{var}' is already declared")
        ts.match('identifier')
        write_to_file('ADDSP 1')
        var_manager.set_variable(var, sp, 'integer')
        write_to_file(f'// VAR {var}: integer, address = {sp}')
        sp += 1
    elif ts.peek() in p.predict(61):
        ts.match('real')
        ts.match('::')
        var = ts.value()
        if var_manager.is_variable_declared(var):
            raise ValueError(f"Error: Variable '{var}' is already declared")
        ts.match('identifier')
        write_to_file('ADDSP 1')
        var_manager.set_variable(var, sp, 'real')
        write_to_file(f'// VAR {var}: real, address = {sp}')
        sp += 1
    elif ts.peek() in p.predict(62):
        ts.match('logical')
        ts.match('::')
        var = ts.value()
        if var_manager.is_variable_declared(var):
            raise ValueError(f"Error: Variable '{var}' is already declared")
        ts.match('identifier')
        write_to_file('ADDSP 1')
        var_manager.set_variable(var, sp, 'logical')
        write_to_file(f'// VAR {var}: logical, address = {sp}')
        sp += 1
    else:
        print('Syntax error at', get_func_name())
        exit(0)

def STATEMENT(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(55):
        DECLARATION(ts,p)
    elif ts.peek() in p.predict(56):
        ASSIGNMENT(ts,p)
    elif ts.peek() in p.predict(57):
        IF_STATEMENT(ts,p)
    elif ts.peek() in p.predict(58):
        DO_LOOP(ts,p)
    elif ts.peek() in p.predict(59):
        PRINT_STATEMENT(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def BODY(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(53):
        STATEMENT(ts,p)
        BODY(ts,p)
    elif ts.peek() in p.predict(54):
        return
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def PROGRAM(ts:token_sequence,p:predict_algorithm, output_file: str)->None:
    open_file(output_file)
    if ts.peek() in p.predict(52):
        ts.match('program')
        ts.match('identifier')
        write_to_file('PUSHIMM 0')
        BODY(ts,p)
        ts.match('end')
        ts.match('program')
        ts.match('identifier')
        var = sp
        write_to_file(f'ADDSP -{sp-1}')
        write_to_file('STOP')
        close_file()
    else:
        write_to_file('Syntax error at',get_func_name())
        close_file()
        exit(0)
