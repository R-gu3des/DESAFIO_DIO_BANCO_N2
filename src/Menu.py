import os
import sys
from time import sleep
from BancoDIO import BancoDIO

class Menu:
    def __init__(self, banco: BancoDIO):
        self.banco = banco

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu(self):
        print(f"""
=========\033[94m Bem Vindo ao {self.banco.nome_banco} \033[0m=========
        
Escolha uma das opções a seguir:

[0] Desejo sair
[1] Cadastrar Usuário
[2] Depósito
[3] Saque
[4] Histórico de Atividade

============================================================
""")

    def executar(self):
        while True:
            self.clear_screen()
            self.mostrar_menu()
            opcao = input('Digite a opção desejada (0-4): ').strip()

            if opcao.isdigit() and int(opcao) in range(5):
                opcao = int(opcao)

                if opcao == 0:
                    print("\nSaindo do sistema...")
                    sleep(1)
                    sys.exit()

                elif opcao == 1:
                    print("\nIniciando operação de cadastro de usuário...")
                    self.banco.cadastrar_usuario()
                    sleep(2)

                elif opcao == 2:
                    print("\nIniciando operação de depósito...")
                    self.banco.realizar_deposito()
                    sleep(2)

                elif opcao == 3:
                    print("\nIniciando operação de saque...")
                    self.banco.realizar_saque()
                    sleep(2)

                elif opcao == 4:
                    print("\nConsultando histórico de atividades...")
                    self.banco.historico_transacao()
                    input("\nPressione Enter para continuar...")

            else:
                print(f"\n\033[91mOpção inválida! Tente novamente.\033[0m")
                sleep(2)
