import os 
import WConio2 as WConio2
from arquivos import *

# Classe base para as telas
class TelaBase:
    def limpar_tela(self):
        os.system('cls')

    def aguardar_tecla(self):
        input("Pressione Enter para continuar...")

# Tela inicial do jogo
class TelaInicial(TelaBase):
    def mostrar_tela_inicial(self, opcao_jogador):
        self.limpar_tela()

        # Impressão do título e opções
        print("__" * 30)
        print("__" * 30)
        print("__" + 22 * " " + "PAC MAN" + 27 * " " + "__")
        print("__" * 30)
        print("__    1 - Novo Jogo" + 39 * " " + "__")
        print("__    2 - High Scores" + 37 * " " + "__")
        print("__    3 - Sair" + 44 * " " + "__")
        print("__" + 56 * " " + "__")
        print("__    Digite sua opção:" + 35 * " " + "__")
        print("__" * 30)
        print("__" * 30)

        # Posicionar o cursor na tela
        WConio2.gotoxy(24, 8)
        opcao_jogador = input()

        # Validar a entrada do jogador
        while opcao_jogador not in ["1", "2", "3"]:
            self.limpar_tela()
            print("__" * 30)
            print("__" * 30)
            print("__" + 22 * " " + "PAC MAN" + 27 * " " + "__")
            print("__" * 30)
            print("__    1 - Novo Jogo" + 39 * " " + "__")
            print("__    2 - High Scores" + 37 * " " + "__")
            print("__    3 - Sair" + 44 * " " + "__")
            print("__" + 56 * " " + "__")
            print("__    Digite sua opção:" + 35 * " " + "__")
            print("__" * 30)
            print("__" * 30)

            # Posicionar o cursor na tela
            WConio2.gotoxy(24, 8)
            opcao_jogador = input()

        return opcao_jogador

# Tela para um novo jogo
class TelaNovoJogo(TelaBase):
    def mostrar_tela_novo_jogo(self):
        self.limpar_tela()

        # Solicitar o nome do jogador
        print("__" * 30)
        print("__" * 30)
        print("__    Digite seu nome: " + 35 * " " + "__")
        for _ in range(6):
            print("__" + 56 * " " + "__")
        print("__" * 30)
        print("__" * 30)
        print("")
            
        # Posicionar o cursor na tela
        WConio2.gotoxy(23, 2)

        nome_jogador = input()

        return nome_jogador

# Tela para exibir as pontuações mais altas
class TelaHighScores(TelaBase):
    def mostrar_tela_high_scores(self):
        self.limpar_tela()

        # Obter pontuações ordenadas
        pontuacoes_ordenadas = ordenar_pontuacoes()

        # Mostrar Maiores pontuações
        print("__" * 30)
        print("__" * 30)
        print("__    MAIORES PONTUAÇÕES: " + 32 * " " + "__")

        # Se não existir o arquivo
        if not pontuacoes_ordenadas:
            print("__" + 56 * " " + "__")
        else:
            # Iterar sobre as pontuações e imprimir formatado
            for i, (nome, pontuacao) in enumerate(pontuacoes_ordenadas, start=1):  # A função enumerate iterar sobre uma sequência
                # Calcular o número de espaços necessários para alinhar a pontuação
                espacos_pontuacao = 30 - len(nome) - len(str(pontuacao))

                # Imprimir a linha formatada com base no tamanho do nome e pontuação
                print(f"__    {i}. {nome}: {pontuacao}" + espacos_pontuacao * " " + 17 * " "  + "__")

        print("__" + 56 * " " + "__")
        print("__" * 30)
        print("__" * 30)

        self.aguardar_tecla()

# Gerenciador do jogo
class Game:
    def __init__(self):
        self.opcao_jogador = "1"
        self.tela_inicial = TelaInicial()
        self.tela_novo_jogo = TelaNovoJogo()
        self.tela_high_scores = TelaHighScores()

    def executar_jogo(self):
        while self.opcao_jogador != "3":
            self.opcao_jogador = self.tela_inicial.mostrar_tela_inicial(self.opcao_jogador)

            # Opção 1
            if self.opcao_jogador == "1":
                nome_jogador = self.tela_novo_jogo.mostrar_tela_novo_jogo()


                ''' Colocar aqui o loop principal do jogo '''

                ''' Após terminar o jogo ele deve retorna a pontuacao, e o input abaixo pode ser desconsiderada(Ela é só para teste)
                    sendo substituido pela pontuação do jogo'''
                pontuacao = input("Digite uma pontuação: ")

                # Verifica se é uma string 0 até 100
                while not (pontuacao.isdigit() and 0 <= int(pontuacao) <= 100):
                    print("A pontuação deve ser um número entre 0 e 100.")
                    pontuacao = input("Digite uma pontuação: ")


                # Grava nome do jogador e em seguida a sua pontuacao em um arquivo PontuacaoJogadores.txt 
                gravaNomeJogador(nome_jogador)
                gravaPontuacao(pontuacao)

            # Opção 2
            if self.opcao_jogador == "2":
                self.tela_high_scores.mostrar_tela_high_scores()

        self.tela_inicial.limpar_tela()
        print("Fim do Jogo!")

if __name__ == "__main__":
    jogo = Game()
    jogo.executar_jogo()