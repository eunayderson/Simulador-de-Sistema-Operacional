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
# Pilha de chamadas: a última rotina chamada é a primeira a terminar
pilha_chamadas = []
# Lista de processos ativos em segundo plano, acessados pelo índice
lista_ativos = []
# Árvore do sistema de arquivos feita com dicionários dentro de dicionários
arvore_arquivos = {}


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


def ler_tipo_chamada():
    while True:
        opcao = input("  Tipo [1] Subrotina  [2] Interrupção: ").strip()
        if opcao == "1":
            return "Subrotina"
        if opcao == "2":
            return "Interrupção"
        imprimir_aviso("Escolha 1 ou 2.")


def pilha_empilhar():
    identificador = ler_texto("ID da chamada")
    rotina = ler_texto("Nome da rotina")
    tipo = ler_tipo_chamada()
    # Na pilha a chamada nova sempre vai para o topo, que é o final da lista
    pilha_chamadas.append({"id": identificador, "rotina": rotina, "tipo": tipo})
    imprimir_aviso(f"Chamada {identificador} empilhada no topo.")


def pilha_listar():
    if esta_vazia(pilha_chamadas, "A pilha de chamadas"):
        return
    print(f"\n  {'':<8}{'ID':<14}{'ROTINA':<26}{'TIPO'}")
    # Percorre a lista de trás pra frente para mostrar o topo primeiro
    for posicao, chamada in enumerate(reversed(pilha_chamadas)):
        marcador = "TOPO >" if posicao == 0 else ""
        print(f"  {marcador:<8}{chamada['id']:<14}{chamada['rotina']:<26}{chamada['tipo']}")


def pilha_atualizar_topo():
    if esta_vazia(pilha_chamadas, "A pilha de chamadas"):
        return
    # Na pilha só dá pra mexer no topo, que é o último item da lista
    chamada = pilha_chamadas[-1]
    print(f"\n  Topo atual: {chamada['id']} | {chamada['rotina']} | {chamada['tipo']}")
    chamada["rotina"] = ler_texto("Novo nome da rotina")
    chamada["tipo"] = ler_tipo_chamada()
    imprimir_aviso(f"Chamada {chamada['id']} atualizada.")


def pilha_desempilhar():
    if esta_vazia(pilha_chamadas, "A pilha de chamadas"):
        return
    # O pop sem índice remove o último item, ou seja, o topo da pilha
    chamada = pilha_chamadas.pop()
    imprimir_aviso(f"Chamada {chamada['id']} ({chamada['rotina']}) terminou e saiu do topo.")


def menu_pilha():
    executar_menu("PILHA DE CHAMADAS E INTERRUPÇÕES", {
        "1": ("Empilhar chamada no topo", pilha_empilhar),
        "2": ("Listar pilha", pilha_listar),
        "3": ("Atualizar chamada do topo", pilha_atualizar_topo),
        "4": ("Desempilhar chamada do topo", pilha_desempilhar),
    }, "Voltar")


def lista_adicionar():
    pid = ler_texto("PID do processo")
    nome = ler_texto("Nome do processo")
    memoria = ler_inteiro("Memória usada (MB)")
    estado = ler_texto("Estado (ex: Executando, Suspenso)")
    lista_ativos.append({"pid": pid, "nome": nome, "memoria": memoria, "estado": estado})
    imprimir_aviso(f"Processo {pid} adicionado no índice {len(lista_ativos) - 1}.")


def lista_listar():
    if esta_vazia(lista_ativos, "A lista de processos ativos"):
        return
    print(f"\n  {'ÍNDICE':<8}{'PID':<10}{'NOME':<22}{'MEMÓRIA':>10}  {'ESTADO'}")
    for indice, processo in enumerate(lista_ativos):
        print(f"  {indice:<8}{processo['pid']:<10}{processo['nome']:<22}"
              f"{processo['memoria']:>7} MB  {processo['estado']}")


def ler_indice_lista():
    lista_listar()
    indice = ler_inteiro("Índice do processo")
    # Confere se o índice existe antes de acessar a lista
    if indice >= len(lista_ativos):
        imprimir_aviso(f"O índice {indice} não existe na lista.")
        return None
    return indice


def lista_atualizar():
    if esta_vazia(lista_ativos, "A lista de processos ativos"):
        return
    indice = ler_indice_lista()
    if indice is None:
        return
    # Acessa o processo direto pela posição dele na lista
    processo = lista_ativos[indice]
    processo["nome"] = ler_texto("Novo nome")
    processo["memoria"] = ler_inteiro("Nova memória usada (MB)")
    processo["estado"] = ler_texto("Novo estado")
    imprimir_aviso(f"Processo do índice {indice} atualizado.")


def lista_remover():
    if esta_vazia(lista_ativos, "A lista de processos ativos"):
        return
    indice = ler_indice_lista()
    if indice is None:
        return
    # O pop com índice tira o processo exatamente daquela posição
    processo = lista_ativos.pop(indice)
    imprimir_aviso(f"Processo {processo['pid']} ({processo['nome']}) foi encerrado.")


def menu_lista():
    executar_menu("TABELA DE PROCESSOS ATIVOS", {
        "1": ("Adicionar processo", lista_adicionar),
        "2": ("Listar processos", lista_listar),
        "3": ("Atualizar processo pelo índice", lista_atualizar),
        "4": ("Remover processo pelo índice", lista_remover),
    }, "Voltar")


def ler_caminho(mensagem):
    while True:
        caminho = input(f"  {mensagem}: ").strip()
        if SEPARADOR in caminho:
            imprimir_aviso(f"O caractere '{SEPARADOR}' não é permitido.")
            continue
        # Transforma "home/aluno/docs" na lista ["home", "aluno", "docs"]
        return [parte.strip() for parte in caminho.split("/") if parte.strip()]


def arvore_buscar(partes):
    # Desce na árvore uma pasta por vez seguindo o caminho
    no = arvore_arquivos
    for parte in partes:
        if parte not in no:
            return None
        no = no[parte]
    return no


def nome_valido(nome, pasta):
    if "/" in nome:
        imprimir_aviso("O nome não pode ter '/'.")
        return False
    if nome in pasta:
        imprimir_aviso(f"Já existe um item chamado '{nome}' nessa pasta.")
        return False
    return True


def arvore_imprimir(no, nivel):
    for nome, filhos in no.items():
        print("  " + "    " * nivel + "└── " + nome)
        # A função chama ela mesma para mostrar o que existe dentro deste item
        arvore_imprimir(filhos, nivel + 1)


def arvore_listar():
    if esta_vazia(arvore_arquivos, "A árvore de arquivos"):
        return
    print("\n  /")
    arvore_imprimir(arvore_arquivos, 0)


def arvore_criar():
    if arvore_arquivos:
        arvore_listar()
    partes_pai = ler_caminho("Pasta onde criar (ex: home/aluno, ENTER para a raiz)")
    pai = arvore_buscar(partes_pai)
    if pai is None:
        imprimir_aviso("Caminho não encontrado.")
        return
    nome = ler_texto("Nome do novo item")
    if not nome_valido(nome, pai):
        return
    # Cada item é um dicionário vazio que pode receber outros itens dentro dele
    pai[nome] = {}
    imprimir_aviso(f"Item /{'/'.join(partes_pai + [nome])} criado.")


def arvore_ver_pasta():
    if esta_vazia(arvore_arquivos, "A árvore de arquivos"):
        return
    partes = ler_caminho("Caminho da pasta (ex: home/aluno)")
    pasta = arvore_buscar(partes)
    if pasta is None:
        imprimir_aviso("Caminho não encontrado.")
        return
    print(f"\n  /{'/'.join(partes)}")
    if not pasta:
        print("      (pasta vazia)")
    arvore_imprimir(pasta, 1)


def arvore_localizar_item():
    partes = ler_caminho("Caminho completo do item (ex: home/aluno/notas.txt)")
    if not partes:
        imprimir_aviso("A raiz não pode ser alterada.")
        return None, None
    # O pai é tudo menos a última parte do caminho, que é o nome do item
    pai = arvore_buscar(partes[:-1])
    if pai is None or partes[-1] not in pai:
        imprimir_aviso("Item não encontrado.")
        return None, None
    return pai, partes[-1]


def arvore_renomear():
    if esta_vazia(arvore_arquivos, "A árvore de arquivos"):
        return
    arvore_listar()
    pai, nome = arvore_localizar_item()
    if pai is None:
        return
    novo_nome = ler_texto("Novo nome")
    if not nome_valido(novo_nome, pai):
        return
    # O pop tira o item antigo e devolve o conteúdo dele, que fica guardado no novo nome
    pai[novo_nome] = pai.pop(nome)
    imprimir_aviso(f"'{nome}' renomeado para '{novo_nome}'.")


def arvore_remover():
    if esta_vazia(arvore_arquivos, "A árvore de arquivos"):
        return
    arvore_listar()
    pai, nome = arvore_localizar_item()
    if pai is None:
        return
    # Apagar a chave remove o item e tudo que estiver dentro dele
    del pai[nome]
    imprimir_aviso(f"'{nome}' e todo o seu conteúdo foram removidos.")


def menu_arvore():
    executar_menu("SISTEMA DE ARQUIVOS E DIRETÓRIOS", {
        "1": ("Criar pasta ou arquivo", arvore_criar),
        "2": ("Mostrar árvore completa", arvore_listar),
        "3": ("Ver conteúdo de uma pasta", arvore_ver_pasta),
        "4": ("Renomear item", arvore_renomear),
        "5": ("Remover item", arvore_remover),
    }, "Voltar")


def montar_linha(identificador, *campos):
    # Junta o identificador e os campos usando o separador, formando uma linha do arquivo
    return SEPARADOR.join([identificador] + [str(campo) for campo in campos])


def arvore_caminhos(no, caminho_atual):
    # Guarda o caminho completo até cada item que não tem nada dentro (as folhas)
    caminhos = []
    for nome, filhos in no.items():
        caminho = caminho_atual + [nome]
        if filhos:
            caminhos.extend(arvore_caminhos(filhos, caminho))
        else:
            caminhos.append(caminho)
    return caminhos


def salvar_dados():
    linhas = []
    for p in lista_ativos:
        linhas.append(montar_linha("LISTA", p["pid"], p["nome"], p["memoria"], p["estado"]))
    # A fila é gravada do início ao fim para manter a ordem de chegada
    for p in fila_processos:
        linhas.append(montar_linha("FILA", p["pid"], p["nome"], p["tempo"]))
    # A pilha é gravada da base até o topo para voltar na mesma ordem
    for c in pilha_chamadas:
        linhas.append(montar_linha("PILHA", c["id"], c["rotina"], c["tipo"]))
    for caminho in arvore_caminhos(arvore_arquivos, []):
        linhas.append(montar_linha("ARVORE", *caminho))

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")
    imprimir_aviso(f"{len(linhas)} registro(s) salvos em {ARQUIVO_DADOS}.")


def menu_principal():
    opcoes = {
        "1": ("Fila de escalonamento da CPU", menu_fila),
        "2": ("Pilha de chamadas e interrupções", menu_pilha),
        "3": ("Tabela de processos ativos", menu_lista),
        "4": ("Sistema de arquivos e diretórios", menu_arvore),
        "5": ("Salvar dados", salvar_dados),
    }
    executar_menu("SIMULADOR DE SISTEMA OPERACIONAL", opcoes, "Sair")
    print("\n  Sistema encerrado. Até a próxima!\n")


if __name__ == "__main__":
    menu_principal()
