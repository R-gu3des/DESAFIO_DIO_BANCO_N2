from datetime import datetime
from Usuario import Usuario
from DataBasePandas import DataBasePandas

class BancoDIO:
    def __init__(self, nome_banco, valor_limite_saque):
        self.nome_banco = nome_banco
        self.valor_limite_saque = valor_limite_saque
        self.data_base = DataBasePandas('historico_banco_dio', ['CPF', 'Tipo', 'Valor', 'Data'])
        self.usuarios_db = DataBasePandas('usuarios', ['CPF', 'Nome', 'Endereco', 'Email', 'Saldo', 'Tipo_Conta'])

    @staticmethod
    def formatar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf.strip())).zfill(11)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def buscar_usuario(self, cpf):
        usuarios_dados = self.usuarios_db.get_table()
        return usuarios_dados[usuarios_dados['CPF'] == cpf]

    def cadastrar_usuario(self):
        usuario = Usuario.criar_usuario()
        if usuario:
            Usuario.salvar_usuario(usuario)
            print("Usuário cadastrado com sucesso!")
        else:
            print("Erro ao cadastrar o usuário.")

    def realizar_saque(self):
        cpf = self.formatar_cpf(input("Digite o CPF do usuário: ").strip())
        valor = self._solicitar_valor("Digite o valor do saque: ", self.valor_limite_saque)

        if not valor:
            return

        usuario = self.buscar_usuario(cpf)
        if usuario.empty:
            print("Usuário não encontrado.")
            return

        saldo = usuario['Saldo'].values[0]
        if saldo < valor:
            print("Saldo insuficiente.")
            return

        if self._limite_saques_excedido(cpf):
            print("Limite diário de saques atingido.")
            return

        self._atualizar_saldo(usuario, -valor)
        self._registrar_transacao(cpf, 'Saque', valor)

        print("Saque realizado com sucesso!")

    def realizar_deposito(self):
        cpf = self.formatar_cpf(input("Digite o CPF do usuário: ").strip())
        valor = self._solicitar_valor("Digite o valor do depósito: ")

        if not valor:
            return

        usuario = self.buscar_usuario(cpf)
        if usuario.empty:
            print("Usuário não encontrado.")
            return

        self._atualizar_saldo(usuario, valor)
        self._registrar_transacao(cpf, 'Depósito', valor)

        print("Depósito realizado com sucesso!")

    def historico_transacao(self):
        cpf = self.formatar_cpf(input("Digite o CPF do usuário para consultar o histórico: ").strip())
        transacoes = self.data_base.get_table()
        transacoes_usuario = transacoes[transacoes['CPF'] == cpf]

        if transacoes_usuario.empty:
            print("Nenhuma transação encontrada para o CPF informado.")
        else:
            Usuario.exibir_dados_usuario(cpf)
            print("Histórico de Transações:")
            print(transacoes_usuario)

    def _solicitar_valor(self, mensagem, limite=None):
        while True:
            valor_input = input(mensagem).strip()
            try:
                valor = float(valor_input)
                if valor <= 0:
                    print("O valor deve ser positivo.")
                elif limite and valor > limite:
                    print(f"Valor excede o limite de {limite} reais.")
                else:
                    return valor
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")

    def _limite_saques_excedido(self, cpf):
        hoje = datetime.now().strftime('%Y-%m-%d')
        historico_saques = self.data_base.get_table()
        saques_hoje = historico_saques[
            (historico_saques['CPF'] == cpf) & 
            (historico_saques['Tipo'] == 'Saque') & 
            (historico_saques['Data'] == hoje)
        ]
        return len(saques_hoje) >= 3

    def _atualizar_saldo(self, usuario, valor):
        usuarios_dados = self.usuarios_db.get_table()
        usuarios_dados.loc[usuario.index, 'Saldo'] += valor
        usuarios_dados.to_csv(self.usuarios_db.file_path, index=False)

    def _registrar_transacao(self, cpf, tipo, valor):
        dados_transacao = [[cpf, tipo, valor, datetime.now().strftime('%Y-%m-%d')]]
        self.data_base.inserir_dados(dados_transacao)
