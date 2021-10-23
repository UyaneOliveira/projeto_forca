#Importando bibliotecas a serem usadas
import os
import csv
from random import choice, shuffle
from time import sleep

#Lista contendo desenhos da forca, que serão mostrados de acordo com o número de erros do jogador
forca = ('''
 _ _ _ _  
|      / 
|      
|        
|        
-''',
''' 
_ _ _ _  
|      / 
|     O
|        
|        
-''',
''' 
_ _ _ _  
|      / 
|     O
|     |   
|        
-''',
''' 
_ _ _ _  
|      / 
|     O
|    /|   
|        
-''',
''' 
_ _ _ _  
|      / 
|     O
|    /|\ 
|        
-''',
''' 
_ _ _ _  
|      / 
|     O
|    /|\  
|    / 
-''',
''' 
_ _ _ _  
|      / 
|     O
|    /|\  
|    / \    
-'''
)


def sortearPalavra(quantidade, palavrasSorteadas):

    #Chama o arquivo de palavras salvas e guarda numa lista
    with open("PalavrasParaForca.csv", "r", encoding="utf-8-sig") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";", lineterminator="\n")
        lista = [linha for linha in leitor]

    #Analisando se a pessoa quer escolher alguma categoria
    while True:
        esc = input("\n\033[mVocê quer escolher uma categoria (S/N): ").title().strip()


        #Se a pessoa quer escolher uma categoria para jogar
        if esc=="S":
            #Mostrando as categorias disponíveis
            todascategorias = [cat[0] for cat in lista]
            print('\n\033[36mCategorias:')
            for index, categoria in enumerate(todascategorias):
                print(f'- {categoria}')
            
            print()
            while True:
                #Recebendo as categorias escolhidas e fazendo análise das mesmas
                escolhidas =  input("\n\033[mColoque as categorias que você deseja separadas por vírgula: ").split(",")
                escolhidas = [escolha.strip().title() for escolha in escolhidas]
                
                #Se alguma categoria escolhida não estiver na lista, informar erro
                if False in [item in todascategorias for item in escolhidas]:
                    print("\033[31mAo menos uma das categorias informadas não está disponível!")
                #Se todas estão na lista, segue
                else:
                    listanova = [l for l in lista if l[0] in escolhidas]
                    lista = listanova
                    break

            break

        #Se a pessoa não quer escolher uma categoria para jogar
        elif esc == "N":
            break
        else:
            print("\033[31mOpção inválida!")
    
    #Sorteando uma categoria da lista de categorias e salvando a dica
    categoria = choice(lista)
    dica = categoria[0].strip()

    #Sorteando uma palavra da categoria sorteada
    while True:
        palavra = choice(categoria[1:]).strip()
        #Confere se a palavra é maior que quantidade de jogadores e se já não foi sorteada antes
        if len(palavra)>=quantidade and palavra not in palavrasSorteadas:
            break

    #Retornando a palavra sorteada e a dica
    return palavra.upper(), dica   

def dadosJogadores(num):

    print("")
    #Criando dicionário vazio de jogadores
    jogadores = {}

    #Pegando nomes dos jogadores e salvando numa lista
    listaNomes = []
    for i in range(num):
        while True:
            nome = input(f"\033[mNome do {i+1}º jogador: ").strip()
            nome = " ".join(nome.split())
            #Validando caracteres inseridos no nome
            if False in [letra.isalpha() or letra.isspace() for letra in nome]:
                print("\033[31mCaracteres inválidos para nome. ")
            else:
                break
        listaNomes.append(nome)
    
    #Sorteando aleatoriamente os nomes para ver a ordem de jogada
    shuffle(listaNomes)
    
    #Adicionando jogadores ao dicionário
    for i,nome in enumerate(listaNomes):
        jogadores[f"Jogador {i+1}"]={"Nome":nome.title(), "Pontos":0, "Vencedor":False, "Vitórias":0}
    
    #Retornando dicionário contendo informações dos jogadores
    return jogadores

def desenha(rodada, dica, dicionarioDeLetras, forca, palavra):

    #Limpando o terminal
    os.system("cls")

    #Mostrando cabeçalho da rodada
    print(f"\n\033[36mRodada {rodada}")
    print("-"*20)
    print(f"\n\033[36mDica: {dica}")
    
    #print(f"\033[36mPalavra: {palavra}")

    # Será utilizado para printar a forca que está armazenada
    # em uma lista, conforme o index da lista:
    print(f"\033[m{forca[len(dicionarioDeLetras['Erradas'])]}")

    #Mostrando os tracinhos da letra (ou letras se já tiverem sido inseridas)
    for letra in palavra:
        if letra in dicionarioDeLetras["Corretas"]:
            print(letra, end= " ")
        else:
            print("_", end= " ")

    #Mostrando lista de letras corretas e erradas
    print()
    if len(dicionarioDeLetras["Corretas"]) > 0:
        print(f'\nLetras corretas já informadas:', end =' ')
        for letra in dicionarioDeLetras["Corretas"]:
            if letra not in [" ","-"]:
                print(letra, end = ' ')
    if len(dicionarioDeLetras["Erradas"]) > 0:
        print(f'\nLetras erradas já informadas:', end =' ')
        for letra in dicionarioDeLetras["Erradas"]:
            print(letra, end = ' ')
    
    print()

def adicionaDicionario(letra, dicionarioDeLetras, palavra):

    #Se a letra informada estiver na palavra é uma letra correta
    if letra in palavra:
        dicionarioDeLetras['Corretas'].append(letra)
    #Se a letra informada não estiver na palavra é uma letra errada
    else:
        dicionarioDeLetras['Erradas'].append(letra)

    return dicionarioDeLetras

def jogada(rodada, dica, jogador, dicionarioDeLetras, palavra, forca):
    
    #Chamando função de desenhar cabeçalho, forca e letras já inseridas
    desenha(rodada, dica, dicionarioDeLetras, forca, palavra)
    
    print(f"\n\033[34mVez de {jogador['Nome']}: ")

    while True:
        while True:
            #Recebendo letra, verificando o tipo do caractere e seu tamanho
            letra = input("\033[34mEscolha uma letra: ").strip().upper()
            if letra.isalpha() and len(letra)==1:
                break
            print("\033[31mCaractere não aceito")

        #Se a letra não estiver nem no dicionário das corretas e nem no das erradas, iniciar
        # processo de inserção da letra no dicionário
        if letra not in dicionarioDeLetras["Corretas"] and letra not in dicionarioDeLetras["Erradas"]: 
            adiciona = False 

            #Inserindo a letras com acentuação (caso possua na palavra)
            dicionario = {'A':['Ã','Á','Â'], 'E':['É','Ê'], 'I':['Í'], 'O':['Ó','Ô'], 'U':['Ú'], 'C':['Ç']}
            for chave,dado in dicionario.items():
                for letraEspecial in dado:
                    if letraEspecial in palavra and chave==letra: 
                        dicionarioDeLetras = adicionaDicionario(letraEspecial, dicionarioDeLetras, palavra)
                        adiciona = 2
            
            #Se a letra estiver na palavra, inserir letra
            if letra in palavra:
                dicionarioDeLetras = adicionaDicionario(letra, dicionarioDeLetras, palavra)
                adiciona = 3
            
            #Se a letra não foi adicionada é porque é uma letra errada
            if adiciona==False:
                dicionarioDeLetras = adicionaDicionario(letra, dicionarioDeLetras, palavra)
            
            break
        
        # Se a letra já estiver no dicionário, informar o jogador e pedir outra letra
        print("\033[31mLetra já inserida!. Escolha outra letra.")
    
    #Chamando função de desenhar cabeçalho, forca e letras já inseridas
    desenha(rodada, dica, dicionarioDeLetras, forca, palavra)

    #Se a letra inserida estiver correta, jogador ganha pontos e pode chutar a palavra
    if letra in dicionarioDeLetras["Corretas"] or adiciona==2: #adiciona == 2 é o caso em que há caracter especial
        if not False in [i in dicionarioDeLetras["Corretas"] for i in palavra]:
            return jogador["Pontos"]+1, True
        
        #Verificando se o jogador quer chutar
        while True:
            chute = input(f"\n\033[34m{jogador['Nome']} acertou a letra, quer chutar (S/N): ").strip().upper()
            if chute=="S":
                #Se o jogador acertar, temos um vencedor
                if input("\033[35mQual seu palpite? ").upper()==palavra:
                    print("\n\033[32mParabéns! Você acertou! :D", end="")
                    #Aumenta pontos e o vencedor
                    return jogador["Pontos"]+1, True
                else:
                    print("\033[31mErrou! Não é essa palavra.")
                    sleep(3)
                break
            elif chute=="N":
                break
            else:
                print("\033[31mOpção inválida!")
        #Caso o jogador erre, ainda sim recebe seu ponto, mas não recebe o critério True para vencedor
        return jogador["Pontos"]+1, False

    #Retorna pontos e não vencedor caso erre a letra
    else:
        return jogador["Pontos"], False
    
def classificacao(jogadores):

    #Limpa o terminal
    os.system("cls")

    print("\n\n\033[35mClassificação Geral: ")
    classificacao = {}
    texto = ''

    #Recebe os dados dos jogadores e os organiza por vitórias e pontos
    for jogador in list(jogadores.values()):
        classificacao[jogador['Nome']] = (jogador['Vitórias'], jogador["Pontos"])
        # Primeiro critério para classificação são as vitórias e depois a pontuação do jogador
        sortedClass = sorted(classificacao.items(), key=lambda kv: (kv[1][0], kv[1][1]), reverse = True)

    #Salva no texto as vitórias e os pontos dos jogadores 
    for tuplas in sortedClass:
        texto += f'\n {tuplas[0]:<{10}} = {tuplas[1][0]} vitórias e {tuplas[1][1]} pontos'

    #Mostra texto com vitórias e pontuações de cada jogador
    print("\033[m"+texto+"\n")

def funcaoPrincipal(rodada, quantidade, jogadores, palavrasSorteadas):

    #Criando dicionário com letras corretas e erradas
    dicionarioDeLetras = {"Corretas":[ ], "Erradas":[ ]}

    #Recebendo a palavra sorteada da rodada e a dica
    palavra, dica = sortearPalavra(quantidade, palavrasSorteadas)

    #Armazena palavra sorteada na lista   
    palavrasSorteadas.append(palavra) 

    #Se na palavra tiver espaço ou hífen já inserir esses caracteres
    if " " in palavra:
        dicionarioDeLetras["Corretas"].append(" ")
    if "-" in palavra:
        dicionarioDeLetras["Corretas"].append("-")
    
    #Chamando função de desenhar cabeçalho, forca e letras já inseridas
    desenha(rodada, dica, dicionarioDeLetras, forca, palavra)

    #Criando variável de controle para a palavra descoberta
    palavraDescoberta = False

    #Chamando o jogadores enquanto a palavra não tiver sido descoberta
    while not palavraDescoberta:
        
        #Para cada jogador chamar a função jogada
        for jogador in jogadores.values():
            jogador["Pontos"], jogador["Vencedor"] = jogada(rodada, dica, jogador, dicionarioDeLetras, palavra, forca)

            #Se já tivermos um vencedor ou todas as letras já tiverem sido descobertas:
            if True in [jogador["Vencedor"] for jogador in jogadores.values()] or not False in [i in dicionarioDeLetras["Corretas"] for i in palavra]:
                
                #Designar vitória ao jogador da vez
                palavraDescoberta = True
                jogador["Vitórias"] += 1
                print(f"\n\033[32m{jogador['Nome']} ganhou a rodada!")
                sleep(3)
                break
                
            #Se já possui 6 erros, finalizar chamadas
            elif len(dicionarioDeLetras["Erradas"])>=6:
                break
        
        #Se já possui 6 erros, finalizar as chamadas 
        if len(dicionarioDeLetras["Erradas"])>=6:
            break
    
    #Se a palavra não foi descoberta, mostrar qual era a palavra
    if palavraDescoberta==False:
        print(f"\n\n\033[33mQue pena, a palavra era {palavra}")
        sleep(3)
    
    print()

    return jogadores, palavrasSorteadas
    
def inicio():

    #Limpa o terminal e mostra nome do jogo
    os.system("cls")
    print("\n\033[36m"+"-"*20)
    print(f"{'JOGO DA FORCA':^20}")
    print("-"*20)

    print("""\n\033[m    O objetivo deste jogo é descobrir uma palavra adivinhando as letras que ela possui. 
    A cada rodada, os jogadores irão simultaneamente escolher uma letra que suspeitem fazer parte da palavra. 
    Caso a palavra contenha esta letra, será mostrado em que posição(ões) ela está. 
    Entretanto, caso esta letra não exista na palavra, será desenhada uma parte do corpo do boneco do jogador. 
    Se todas as 6 partes do corpo do boneco estiverem desenhadas, o jogador estará fora da partida.""")
    print("""\n    Instruções adicionais: 
    1. Ao acertar uma letra o jogador pode chutar a palavra.
    2. Ao chutar a palavra, ela deve vim com suas acentuações, mas ao chutar a letra o acento será colocado automaticamente.
    3. O número de vitórias por rodada e o número de pontos feitos são contabilizados na classificação final""")

    #Recebendo a quantidade de jogadores e validando o número inserido
    while True:
        quantidade = input("\n\033[37mQuantos jogadores (Máximo 6)? ")
        if quantidade.isdigit() and 0<int(quantidade)<=6:
            break
        print("\033[31mNúmero inválido. ")
    quantidade = int(quantidade)

    #Recebendo o dicionário com dados dos jogadores
    jogadores = dadosJogadores(quantidade)

    #Perguntando número de rodadas e fazendo sua validação
    while True:
        numRodadas = input("\n\033[37mQuantas rodadas? ")
        if numRodadas.isdigit() and 0<int(numRodadas):
            break
        print("\033[31mNúmero inválido. ")

    palavrasSorteadas = []

    #Para cada rodada chamar a função principal
    for rodada in range(int(numRodadas)):

        #Limpa o terminal e mostra qual é a rodada atual
        os.system("cls")
        print(f"\n\033[36mIniciando Rodada {rodada+1}")
        print("-"*20)

        #Chama a função principal
        jogadores, palavrasSorteadas = funcaoPrincipal(rodada+1, quantidade, jogadores, palavrasSorteadas)

        #Ao final da rodada todos os jogadores recebem falso como vencedor da rodada
        for jogador in jogadores.values():
            jogador["Vencedor"]=False
    
    #Chama função de classificação
    classificacao(jogadores)
    sleep(5)
    
#Chama a função de inicio do jogo
inicio()