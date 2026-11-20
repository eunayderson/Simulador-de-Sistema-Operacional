# Simulador de Sistema Operacional

Trabalho da disciplina de Estruturas de Dados. A ideia foi juntar as quatro estruturas que a gente estudou (Lista, Pilha, Fila e Árvore) em um programa só, simulando algumas partes de um sistema operacional. Os dados ficam salvos em um arquivo texto, então dá pra fechar o programa e depois carregar tudo de novo.

## Como executar

Precisa ter o **Python 3** instalado (testei no 3.10 pra cima). O projeto não usa nenhuma biblioteca externa, só o que já vem com o Python, então não precisa instalar nada.

1. Baixe ou clone o repositório:

   ```bash
   git clone https://github.com/eunayderson/Simulador-de-Sistema-Operacional.git
   cd Simulador-de-Sistema-Operacional
   ```

2. Rode o programa:

   ```bash
   python3 main.py
   ```

   No Windows normalmente o comando é `python main.py`.

3. Vai aparecer o menu principal. É só digitar o número da opção e apertar ENTER.

O programa começa vazio, sem nenhum dado. Para testar, o caminho mais rápido é cadastrar alguns itens em cada menu, usar a opção **5 (Salvar dados)**, fechar o programa, abrir de novo e usar a opção **6 (Carregar dados)**. Tudo volta do jeito que estava.

## O que tem no menu

**1. Fila de escalonamento da CPU:** adicionar processo no fim da fila, listar, atualizar os dados de um processo pelo PID e executar o próximo (que tira o processo do início da fila).

**2. Pilha de chamadas e interrupções:** empilhar uma chamada no topo, listar (o topo aparece primeiro), atualizar a chamada do topo e desempilhar.

**3. Tabela de processos ativos:** adicionar processo, listar com o índice de cada um, atualizar pelo índice e remover pelo índice.

**4. Sistema de arquivos e diretórios:** criar pasta ou arquivo dentro de um caminho, mostrar a árvore inteira, ver o conteúdo de uma pasta, renomear e remover um item. Os caminhos são digitados separando as pastas por barra, por exemplo `home/aluno`. Para criar algo direto na raiz é só apertar ENTER quando ele pedir a pasta.

**5. Salvar dados:** grava tudo que está na memória no arquivo `dados_sistema.txt`.

**6. Carregar dados:** lê o `dados_sistema.txt` e monta as estruturas de novo na memória (o que estava antes na memória é substituído).

**0. Sair:** fecha o programa. Lembrando que ele não salva sozinho, então salve antes de sair.

## Por que cada estrutura foi usada onde foi

**Fila (collections.deque) para o escalonamento da CPU.** Num escalonamento simples, o primeiro processo que chega é o primeiro que usa a CPU (FIFO). Então o processo novo entra no fim e o próximo a executar sai do início. Usei o `deque` em vez de lista comum porque tirar do início de uma lista com `pop(0)` obriga o Python a mover todos os outros elementos, já o `popleft()` do deque faz isso direto.

**Pilha (list) para as chamadas de sub-rotinas e interrupções.** Quando uma função chama outra, a última que foi chamada é a primeira que termina, e com interrupção é igual: o sistema para o que estava fazendo, atende a interrupção e depois volta. Isso é exatamente o comportamento LIFO da pilha. A lista do Python já funciona como pilha usando `append()` para empilhar e `pop()` para desempilhar, sempre no final, que é o topo.

**Lista (list) para a tabela de processos ativos.** Os processos em segundo plano não têm uma ordem obrigatória de entrada e saída, qualquer um pode ser encerrado a qualquer momento. Por isso faz sentido acessar pelo índice, que é o ponto forte da lista: dá pra ler, alterar ou remover qualquer posição diretamente.

**Árvore (dicionários aninhados) para o sistema de arquivos.** Pastas e arquivos são naturalmente uma hierarquia: a raiz tem pastas, que têm outras pastas, que têm arquivos. Como o Python não tem árvore pronta, cada item é uma chave de dicionário e o valor dele é outro dicionário com o que está dentro. Um dicionário vazio quer dizer que o item não tem nada dentro. Para andar na árvore o programa vai entrando de dicionário em dicionário seguindo o caminho digitado.

## Como os dados são salvos

Tudo fica em um único arquivo texto chamado `dados_sistema.txt`, criado na mesma pasta do `main.py`. Não usei banco de dados, JSON, CSV nem pickle. Cada linha começa com o nome da estrutura e depois vêm os campos separados por `|`. Um exemplo de como o arquivo fica:

```text
LISTA|301|spotify|200|Executando
LISTA|302|slack|150|Suspenso
FILA|101|kernel_init|30
FILA|102|firefox|40
PILHA|CALL01|main|Subrotina
PILHA|IRQ07|teclado|Interrupção
ARVORE|home|aluno|notas.txt
ARVORE|etc|config
```

Os campos de cada tipo são:

1. `LISTA|PID|nome|memória em MB|estado`
2. `FILA|PID|nome|tempo de CPU em ms`
3. `PILHA|ID da chamada|rotina|tipo`
4. `ARVORE|pasta|subpasta|...|item`

Algumas coisas que eu cuidei para o arquivo voltar igual:

* A fila é gravada do início para o fim e a pilha da base para o topo, assim quando carrega a ordem continua a mesma.
* Na árvore cada linha é o caminho completo até um item que não tem nada dentro. Na hora de carregar, o programa vai criando as pastas do caminho se elas ainda não existirem, e com isso a hierarquia inteira é remontada.
* O programa não deixa digitar o caractere `|` nos campos, porque ele é o separador e iria bagunçar as linhas do arquivo.
