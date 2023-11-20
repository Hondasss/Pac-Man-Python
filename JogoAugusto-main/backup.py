#Bibliotecas a serem usadas
import os
import cursor
import msvcrt
import WConio2 as WConio2
import random
import time
import sys

#Importação de classes
from telaInicial import TelaInicial, TelaNovoJogo, TelaHighScores, TelaGameOver
from mapa import Mapa
from pacman import Pacman
from paredesMapa import Paredes
from fantasmas import Fantasmas
from arquivos import *
from pontuacao import Pontuacao

def main():
    telaInicial = TelaInicial()
    opcaoJogador = telaInicial.showTelaInicial("1")

    if opcaoJogador == "1":
        telaNovoJogo = TelaNovoJogo()
        nomeJogador = telaNovoJogo.mostrarNovoJogo()
        iniciarJogo(nomeJogador,"1")
    if opcaoJogador == "2":
        telaNovoJogo = TelaNovoJogo()
        nomeJogador = telaNovoJogo.mostrarNovoJogo()
        iniciarJogo(nomeJogador,"2")

    elif opcaoJogador == "3":
        telaHighScore = TelaHighScores()
        telaHighScore.mostrarHighscore()

    os.system('cls')  # Limpa a tela antes de sair do jogo
    print("Fim do Jogo!")

# Função para salvar a pontuação
def salvarPontuacao(nome_jogador, pontuacao):
    with open('ranking.txt', 'a') as arquivo:
        arquivo.write(f"{nome_jogador}: {pontuacao}\n")

# Função para mostrar os high scores
def mostrarHighScore():
    try:
        with open('ranking.txt', 'r') as arquivo:
            pontuacoes = []
            for linha in arquivo:
                nome, pontuacao = linha.strip().split(': ')
                pontuacoes.append((nome, int(pontuacao)))
            
            pontuacoesOrdenadas = sorted(pontuacoes, key=lambda x: x[1], reverse=True)
            
            print("Pontuações mais altas:")
            for idx, (nome, pontuacao) in enumerate(pontuacoesOrdenadas, start=1):
                print(f"{idx}. {nome}: {pontuacao}")
    except FileNotFoundError:
        print("Ainda não há pontuações salvas.")

def iniciarJogo(nomeJogador, opcaoJogador):
    os.system('cls')
    #Declarando instâncias das classes
    dimensoesMapa = Mapa(largura=23, altura=23) #Definindo um mapa 23x23
    pacman = Pacman("C", 4, 11) #Definindo o simbolo do pacman e sua posição inicial
    fantasmas = [
        Fantasmas("R", 1, 1),
        Fantasmas("G", 1, 21),
        Fantasmas("B", 21, 1),
        Fantasmas("Y", 21, 21)
    ]
    simbolo = ''
    paredes = Paredes(dimensoesMapa.plano)
    pontuacaoTotal = 0 

    if opcaoJogador == "1":
        paredes.configurarMapa() #Aqui colocamos as paredes do mapa
    elif opcaoJogador == "2":
        paredes.configurarMapa2()
    
    dimensoesMapa.colocar_frutas(3)

    while (simbolo != "o"):
        #Posiciona o cursor no começo do terminal
        WConio2.gotoxy(0,0)
        cursor.hide() #Esconde o cursor
        dimensoesMapa.atualizaCaractere(pacman.pacman, pacman.linha, pacman.coluna) #Atualiza o caractere do pacman
        dimensoesMapa.atualizaFantasma(fantasmas)

        dimensoesMapa.imprimir() #Imprime o mapa
        
        time.sleep(0.1)
        
        #Captação e movimentação usando a biblioteca msvcrt
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode()
            if tecla == 'a' or tecla == 'A':
                pacman.moverEsquerda(dimensoesMapa.plano)
            elif tecla == 'd' or tecla == 'D':
                pacman.moverDireita(dimensoesMapa.plano)
            elif tecla == 'w' or tecla == 'W':
                pacman.moverCima(dimensoesMapa.plano)
            elif tecla == 's' or tecla == 'S':
                pacman.moverBaixo(dimensoesMapa.plano)
        
    
        #gerado um numero aleatorio entre 1 e 4
        #1 cima, 2 direita, 3 baixo, 4 esquerdo
        for i in range(len(fantasmas)):
            dir = random.randint(1,4)
            if dir == 1:
                fantasmas[i].moverCima(dimensoesMapa.plano)
            elif dir == 2:
                fantasmas[i].moverDireita(dimensoesMapa.plano)
            elif dir == 3:
                fantasmas[i].moverBaixo(dimensoesMapa.plano)
            else:
                fantasmas[i].moverEsquerda(dimensoesMapa.plano)

        pontuacaoAtual = Pontuacao.atualizarPontuacao(pacman, dimensoesMapa.plano)
        if dimensoesMapa.coletar_fruta(pacman.linha, pacman.coluna):
            pontuacaoAtual += 10  # Incrementa a pontuação se uma fruta foi coletada

        #Atualizando a pontuação:
        pontuacaoAtual = Pontuacao.atualizarPontuacao(pacman, dimensoesMapa.plano)
        pontuacaoTotal += pontuacaoAtual
        print(f"\nPontuação: {pontuacaoTotal}", end='', flush=True)
        

        #Verifica colisão com fantasmas
        for i, fantasma in enumerate(fantasmas):
            if pacman.linha == fantasma.linha and pacman.coluna == fantasma.coluna:
                gameOver(nomeJogador, pontuacaoTotal)
                return

def gameOver(nomeJogador, pontuacaoTotal):
    telaGameOver = TelaGameOver()
    opcaoGameOver = telaGameOver.showGameOver()
    
    if opcaoGameOver == "1":
        salvarPontuacao(nomeJogador, pontuacaoTotal)  # Salvar pontuação ao final da partida
        WConio2.gotoxy(12, 2)
        opcaoHighscore = input("Deseja ver os high scores? (S/N): ")
        while opcaoHighscore.upper() == "S":
            os.system('cls') 
            telaHighScore = TelaHighScores()
            telaHighScore.mostrarHighscore()
            break
        
        main()  # Reiniciar o jogo
        return  # Sai da função gameOver após reiniciar o jogo

    elif opcaoGameOver == "2":
        os.system('cls')
        print("Fim do Jogo!")
        sys.exit()  # Sair do jogo
        return 
        
if __name__ == "__main__":
    main()

import random

class Mapa:
    #Definição da função INIT, que armazenará variáveis de controle da largura e altura
    def __init__(self, largura, altura):
        #Iniciando altura e largura
        self.largura = largura 
        self.altura = altura

        #Iniciando uma matriz que representará toda a área do jogo, sendo essa ALTURA x LARGURA
        self.plano = [['.' for coluna in range(largura)] for linha in range(altura)] #O ponto representa o valor inicial de cada célula na matriz
        self.bordas() #O método é chamado aqui para criar as bordas desde o inicio do jogo, garantindo solidez e evitando erros
        self.linhaPacmanAnterior = 0  
        self.colunaPacmanAnterior = 0  
        self.FantasmaAnterior = {
            "LinhaFantasma1": 0,
            "ColunaFantasma1": 0,
            "LinhaFantasma2": 0,
            "ColunaFantasma2": 0,
            "LinhaFantasma3": 0,
            "ColunaFantasma3": 0,
            "LinhaFantasma4": 0,
            "ColunaFantasma4": 0
        }
        self.frutas = []
            

    def bordas(self):
        #Método que adiciona as bordas delimitadas por #
        for i in range(self.largura):
            self.plano[0][i] = '#' #Tampa
            self.plano[self.altura - 1][i] = '#' #Fundo

        for i in range(self.altura):
            self.plano[i][0] = '#' #Lateral esquerda
            self.plano[i][self.largura - 1] = '#' #Lateral direita 

    def atualizaCaractere(self, caractere, linha, coluna):
        # Limpa a posição anterior do Pacman
        self.limparPosicao(self.linhaPacmanAnterior, self.colunaPacmanAnterior)

        # Proteção do script para verificação da linha e coluna dentro do limite máximo
        if 0 <= linha < self.altura and 0 <= coluna < self.largura:
            self.linhaPacmanAnterior, self.colunaPacmanAnterior = linha, coluna
            self.plano[linha][coluna] = caractere

    def atualizaFantasma(self, fantasmas):
        for i in range(len(fantasmas)):
            f = fantasmas[i]
            # Verifica se a próxima posição está vazia ou é o símbolo do Pac-Man antes de mover o fantasma
            if self.plano[f.linha][f.coluna] == ' ' or self.plano[f.linha][f.coluna] == 'C':
                self.plano[self.FantasmaAnterior[f"LinhaFantasma{i+1}"]][self.FantasmaAnterior[f"ColunaFantasma{i+1}"]] = ' '  # Limpa a posição anterior do fantasma
            else:
                self.plano[self.FantasmaAnterior[f"LinhaFantasma{i+1}"]][self.FantasmaAnterior[f"ColunaFantasma{i+1}"]] = '.'  # Volta o caractere original
            self.plano[f.linha][f.coluna] = f.fantasma
            self.FantasmaAnterior[f"LinhaFantasma{i+1}"] = f.linha
            self.FantasmaAnterior[f"ColunaFantasma{i+1}"] = f.coluna
            
    def limparPosicao(self, linha,  coluna):
        # Limpa a posição anterior do Pacman para dar impressao de movimento
        self.plano[linha][coluna] = ' '

    def colocar_frutas(self, quantidade):
        for i in range(quantidade):
            linha = random.randint(1, self.altura - 2)
            coluna = random.randint(1, self.largura - 2)
            if self.plano[linha][coluna] == ' ':
                self.plano[linha][coluna] = 'O'
                self.frutas.append((linha, coluna)) 

    def coletar_fruta(self, linha, coluna):
        # Verifica se o Pac-Man está na posição de uma fruta
        if (linha, coluna) in self.frutas:
            self.frutas.remove((linha, coluna))  # Remove a fruta da lista
            return True  # Retorna True se uma fruta foi coletada
        return False  # Retorna False se não houve coleta de fruta

    def imprimir(self): #Impressão
        for linha in self.plano:
            for caractere in linha:
                print(caractere, end=' ')
            print()