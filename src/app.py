from BancoDIO import BancoDIO
from Menu import Menu

def main():
    nome_banco = 'Banco DIO'
    valor_limite_saque = 500  # Limite por saque individual

    banco_dio = BancoDIO(nome_banco=nome_banco, valor_limite_saque=valor_limite_saque)
    menu = Menu(banco_dio)
    menu.executar()

if __name__ == '__main__':
    main()
