import re
import os

def avalia_instrucoes(instrucoes, pilha, output_file):
    comando = ""
    valor = ""
    index = 0
    fbr = 0
    while index < len(instrucoes):
        x = instrucoes[index]
        if (len(x)>1):
            comando = x[0]
            output_file.write(f"{comando}\n")
            valor = x[1]
            output_file.write(f"{valor}\n")
        else:
            comando = x[0]
            output_file.write(f"{comando}\n")

        # Inserção de valores
        if comando == "PUSHIMM":
            output_file.write("Valor inserido\n")
            pilha.append(int(valor))
        # Manipulação de pilha
        elif comando == "ADDSP":
            output_file.write("Aloca espaco na pilha\n")
            for x in range(abs(int(valor))):
                if int(valor) > 0:
                    pilha.append(0)
                else:
                    pilha.pop()
        elif comando == "STOREABS":
            output_file.write("Armazena valor em posicao absoluta\n")
            pilha[int(valor)] = pilha.pop()
        elif comando == "STOREOFF":
            output_file.write("Armazena valor em posicao relativa\n")
            pilha[int(fbr) + int(valor)] = pilha.pop()
        elif comando == "PUSHABS":
            output_file.write("Pega valor de posicao absoluta\n")
            pilha.append(pilha[int(valor)])
        elif comando == "PUSHOFF":
            output_file.write("Pega valor de posicao relativa\n")
            pilha.append(pilha[int(fbr) + int(valor)])
        
        # Operações aritméticas com inteiros
        elif comando == "ADD":
            output_file.write("Soma\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (pilha[tam_pilha-2] + pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "SUB":
            output_file.write("Subtracao\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (pilha[tam_pilha-2] - pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "TIMES":
            output_file.write("Multiplicacao\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (pilha[tam_pilha-2] * pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "DIV":
            output_file.write("Divisao\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (pilha[tam_pilha-2] / pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "MOD":
            output_file.write("Modulo\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (pilha[tam_pilha-2] % pilha[tam_pilha-1])
            pilha.pop()

        # Operações com números de ponto flutuante (reais)
        elif comando == "PUSHIMMF":
            output_file.write("Valor real inserido\n")
            pilha.append(float(valor))
        elif comando == "ADDF":
            output_file.write("Soma de reais\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = float(pilha[tam_pilha-2]) + float(pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "SUBF":
            output_file.write("Subtração de reais\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = float(pilha[tam_pilha-2]) - float(pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "TIMESF":
            output_file.write("Multiplicação de reais\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = float(pilha[tam_pilha-2]) * float(pilha[tam_pilha-1])
            pilha.pop()
        elif comando == "DIVF":
            output_file.write("Divisão de reais\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = float(pilha[tam_pilha-2]) / float(pilha[tam_pilha-1])
            pilha.pop()

        # Operações lógicas
        elif comando == "AND":
            output_file.write("E\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if ((pilha[tam_pilha-2] != 0) & (pilha[tam_pilha-1] != 0)) else 0)
            pilha.pop()
        elif comando == "NAND":
            output_file.write("Nao E\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (0 if ((pilha[tam_pilha-2] != 0) & (pilha[tam_pilha-1] != 0)) else 1)
            pilha.pop()
        elif comando == "OR":
            output_file.write("Ou\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if ((pilha[tam_pilha-2] != 0) | (pilha[tam_pilha-1] != 0)) else 0)
            pilha.pop()
        elif comando == "NOR":
            output_file.write("Nao Ou\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (0 if ((pilha[tam_pilha-2] != 0) | (pilha[tam_pilha-1] != 0)) else 1)
            pilha.pop()
        elif comando == "NOT":
            output_file.write("Nao\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-1] = (1 if pilha[tam_pilha-1] == 0 else 0)
        elif comando == "XOR":
            output_file.write("Ou exclusivo\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if ((pilha[tam_pilha-2] != 0) ^ (pilha[tam_pilha-1] != 0)) else 0)
            pilha.pop()

        # Operações de comparação
        elif comando == "EQUAL":
            output_file.write("Igualdade\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if pilha[tam_pilha-2] == pilha[tam_pilha-1] else 0)
            pilha.pop()
        elif comando == "GREATER":
            output_file.write("Maior\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if pilha[tam_pilha-2] > pilha[tam_pilha-1] else 0)
            pilha.pop()
        elif comando == "LESS":
            output_file.write("Menor\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if pilha[tam_pilha-2] < pilha[tam_pilha-1] else 0)
            pilha.pop()
        elif comando == "ISNIL":
            output_file.write("Nulo\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-1] = (1 if pilha[tam_pilha-1] == 0 else 0)
        elif comando == "CMP":
            output_file.write("Compara\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-2] = (1 if pilha[tam_pilha-2] < pilha[tam_pilha-1] else (-1 if pilha[tam_pilha-2] > pilha[tam_pilha-1] else 0))
            pilha.pop()
        elif comando == "ISPOS":
            output_file.write("Positivo\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-1] = (1 if pilha[tam_pilha-1] > 0 else 0)
        elif comando == "ISNEG":
            output_file.write("Negativo\n")
            tam_pilha = len(pilha)
            pilha[tam_pilha-1] = (1 if pilha[tam_pilha-1] < 0 else 0)

        # Comandos de fluxo
        elif comando == "JUMP":
            output_file.write("Pula\n")
            index = instrucoes.index([valor])
            output_file.write(f"{index}\n")
            x = instrucoes[index]
        elif comando == "JUMPC":
            output_file.write("Pula condicional\n")
            tam_pilha = len(pilha)
            if pilha[tam_pilha-1] == 1:
                index = instrucoes.index([valor])
                output_file.write(f"{index}\n")
                x = instrucoes[index]
                pilha.pop()
            else:
                pilha.pop()
        elif comando == "JUMPIND":
            output_file.write("Pula indireto\n")
            index = int(pilha.pop())
            output_file.write(f"{index}\n")
            x = instrucoes[index]
        elif comando == "RST":
            output_file.write("Pula indireto\n")
            index = int(pilha.pop())
            output_file.write(f"{index}\n")
            x = instrucoes[index]
        elif comando == "JSR":
            output_file.write("Chama rotina\n")
            pilha.append(f"{index}\n")
            index = instrucoes.index([valor])
            output_file.write(f"{index}\n")
            x = instrucoes[index]
        
        # Comandos de manipulação de registradores e FBR
        elif comando == "LINK":
            output_file.write("Adiciona o FBR na pilha e FBR = SP - 1\n")
            pilha.append(fbr)
            fbr = len(pilha)-1
            output_file.write(f"fbr = {fbr}\n")
        elif comando == "UNLINK":
            output_file.write("Retira o FBR da pilha e FBR = SP\n")
            fbr = pilha.pop()
            output_file.write(f"fbr = {fbr}\n")
        elif comando == "POPFBR":
            output_file.write("Retira o FBR da pilha e FBR = SP\n")
            fbr = pilha.pop()
            output_file.write(f"fbr = {fbr}\n")

        # Operações de escrita
        elif comando == "WRITE":
            output_file.write("Escreve valor inteiro ou lógico\n")
            valor = pilha.pop()
            output_file.write(f"{int(valor)}\n")
        elif comando == "WRITEF":
            output_file.write("Escreve valor real\n")
            valor = pilha.pop()
            output_file.write(f"{float(valor)}\n")
                
        # Comandos de parada
        elif comando == "STOP":
            output_file.write("Finalizou com\n")
            output_file.write(f"{pilha[0]}\n")
            if len(pilha) > 1:
                output_file.write(f"Aviso: Ainda tem {len(pilha)-1} valores na pilha\n")
            break

        index += 1
        output_file.write(f"Pilha: {pilha}\n")

def trata_instrucao(instrucao):
    regex = r"^(\w+)(?:\s([A-Z0-9-]+))?"
    match = re.match(regex, instrucao)
    try:
        return match.group(0)
    except AttributeError:
        return 0

def executa_vm_sam(input_file):
    instrucoes = []
    pilha = []

    base_name = os.path.splitext(input_file)[0]
    output_file_name = f"{base_name}_result.txt"

    with open(input_file) as f:
        for x in f:
            instrucao = trata_instrucao(x.strip())
            if instrucao == 0:
                continue
            instrucoes.append(instrucao.split(' '))

    with open(output_file_name, 'w') as output_file:
        output_file.write("Executando código SAM:\n")
        output_file.write(f"{instrucoes}\n")
        avalia_instrucoes(instrucoes, pilha, output_file)

    return output_file_name

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        executa_vm_sam(sys.argv[1])
    else:
        print("Usage: python vm_sam.py <input_file>\n")