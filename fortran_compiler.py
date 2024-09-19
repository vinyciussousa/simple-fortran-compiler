import sys
from grammar import Grammar
from lexical_analyzer import lexical_analyzer
import fortran
from ll1_check import is_ll1
from predict import predict_algorithm
from token_sequence import token_sequence
from vm_sam import executa_vm_sam 

def print_grammar(G: Grammar) -> None:
    for x in G.productions():
        print(x,G.lhs(x),'->',G.rhs(x))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 fortran_compiler.py <input_file> <output_file>")
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        tokens = lexical_analyzer(input_file)
        ts = token_sequence(tokens)
        G = fortran.simple_fortran()
        #print_grammar(G)
        predict_alg = predict_algorithm(G)
        #print('LL(1) ?',is_ll1(G, predict_alg))
        print("Compilando código Fortran para SAM\n")
        fortran.PROGRAM(ts,predict_alg, output_file)
        print(f"Código Fortran compilado para SAM Assembly em: {output_file}\n")

        print("Executando código SAM compilado\n")
        output_file_name = executa_vm_sam(output_file)
        print(f"Código SAM Assembly executado em: {output_file_name}\n")

    except ValueError as e:
        print(f"Erro de compilação: {e}")
        sys.exit(0)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(0)