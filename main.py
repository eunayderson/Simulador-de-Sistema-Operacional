"""Simulador de Sistema Operacional.

Trabalho de Estruturas de Dados que usa Lista, Pilha, Fila e Árvore
para simular partes de um sistema operacional, salvando tudo em um
arquivo texto.
"""

from collections import deque

ARQUIVO_DADOS = "dados_sistema.txt"
SEPARADOR = "|"
LARGURA = 60

# Fila de processos esperando a CPU: entra pelo fim e sai pelo início
fila_processos = deque()


def imprimir_titulo(texto):
    print()
    print("╔" + "═" * LARGURA + "╗")
    print("║" + texto.center(LARGURA) + "║")
    print("╚" + "═" * LARGURA + "╝")


def imprimir_aviso(texto):
    print(f"\n  >> {texto}")


def ler_texto(mensagem):
    # Repete a pergunta até o usuário digitar um texto válido
    while True:
        valor = input(f"  {mensagem}: ").strip()
        # Bloqueia o separador porque ele quebraria as linhas do arquivo de dados
        if SEPARADOR in valor:
            imprimir_aviso(f"O caractere '{SEPARADOR}' não é permitido.")
        elif valor:
            return valor
        else:
            imprimir_aviso("Este campo não pode ficar vazio.")


def ler_inteiro(mensagem):
    while True:
        valor = input(f"  {mensagem}: ").strip()
        if valor.isdigit():
            return int(valor)
        imprimir_aviso("Digite um número inteiro positivo.")


def esta_vazia(estrutura, nome):
    if not estrutura:
        imprimir_aviso(f"{nome} está vazia.")
        return True
    return False


def executar_menu(titulo, opcoes, texto_saida):
    # O dicionário liga o número digitado à função que faz a operação
    while True:
        imprimir_titulo(titulo)
        for numero, (descricao, _) in opcoes.items():
            print(f"  [{numero}] {descricao}")
        print(f"  [0] {texto_saida}")

        escolha = input("\n  Escolha uma opção: ").strip()
        if escolha == "0":
            return
        if escolha in opcoes:
            opcoes[escolha][1]()
        else:
            imprimir_aviso("Opção inválida, tente novamente.")


def fila_adicionar():
    pid = ler_texto("PID do processo")
    nome = ler_texto("Nome do processo")
    tempo = ler_inteiro("Tempo de CPU necessário (ms)")
    # Na fila o processo novo sempre entra no final e espera a sua vez
    fila_processos.append({"pid": pid, "nome": nome, "tempo": tempo})
    imprimir_aviso(f"Processo {pid} entrou na fila na posição {len(fila_processos)}.")


def fila_listar():
    if esta_vazia(fila_processos, "A fila de escalonamento"):
        return
    print(f"\n  {'POS':<6}{'PID':<10}{'NOME':<26}{'TEMPO CPU':>12}")
    for posicao, processo in enumerate(fila_processos, start=1):
        print(f"  {posicao:<6}{processo['pid']:<10}{processo['nome']:<26}{processo['tempo']:>9} ms")


def fila_atualizar():
    if esta_vazia(fila_processos, "A fila de escalonamento"):
        return
    fila_listar()
    pid = ler_texto("PID do processo que será atualizado")
    # Procura o primeiro processo com esse PID, se não achar devolve None
    processo = next((p for p in fila_processos if p["pid"] == pid), None)
    if processo is None:
        imprimir_aviso(f"Nenhum processo com PID {pid} na fila.")
        return
    # Os dados mudam mas o processo continua na mesma posição da fila
    processo["nome"] = ler_texto("Novo nome")
    processo["tempo"] = ler_inteiro("Novo tempo de CPU (ms)")
    imprimir_aviso(f"Processo {pid} atualizado.")


def fila_executar_proximo():
    if esta_vazia(fila_processos, "A fila de escalonamento"):
        return
    # O popleft tira o processo do início da fila, que é o próximo a usar a CPU
    processo = fila_processos.popleft()
    imprimir_aviso(f"Processo {processo['pid']} ({processo['nome']}) foi enviado para a CPU.")


def menu_fila():
    executar_menu("FILA DE ESCALONAMENTO DA CPU", {
        "1": ("Adicionar processo no fim da fila", fila_adicionar),
        "2": ("Listar fila", fila_listar),
        "3": ("Atualizar processo", fila_atualizar),
        "4": ("Executar próximo processo (sai do início)", fila_executar_proximo),
    }, "Voltar")


def menu_principal():
    opcoes = {
        "1": ("Fila de escalonamento da CPU", menu_fila),
    }
    executar_menu("SIMULADOR DE SISTEMA OPERACIONAL", opcoes, "Sair")
    print("\n  Sistema encerrado. Até a próxima!\n")


if __name__ == "__main__":
    menu_principal()
