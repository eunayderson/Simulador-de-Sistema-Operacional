"""Simulador de Sistema Operacional.

Trabalho de Estruturas de Dados que usa Lista, Pilha, Fila e Árvore
para simular partes de um sistema operacional, salvando tudo em um
arquivo texto.
"""

from collections import deque

ARQUIVO_DADOS = "dados_sistema.txt"
SEPARADOR = "|"
LARGURA = 60


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


def menu_principal():
    opcoes = {
    }
    executar_menu("SIMULADOR DE SISTEMA OPERACIONAL", opcoes, "Sair")
    print("\n  Sistema encerrado. Até a próxima!\n")


if __name__ == "__main__":
    menu_principal()
