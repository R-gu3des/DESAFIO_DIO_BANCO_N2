import pandas as pd
import os

class Usuario:
    def __init__(self, cpf, nome, endereco, email, saldo, tipo_conta):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.saldo = saldo
        self.tipo_conta = tipo_conta

    @classmethod
    def criar_usuario(cls):
        while True:
            dados = input("Digite os dados do usuário separados por vírgula (cpf, nome, endereco, email, saldo, tipo_conta): ").strip()
            try:
                cpf, nome, endereco, email, saldo, tipo_conta = map(str.strip, dados.split(','))
                cpf = cls.formatar_cpf(cpf)
                saldo = float(saldo)
                return cls(cpf, nome, endereco, email, saldo, tipo_conta)
            except ValueError:
                print("Dados inválidos. Certifique-se de que todos os campos estão preenchidos corretamente.")

    @staticmethod
    def formatar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf.strip())).zfill(11)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def salvar_usuario(usuario):
        file_path = 'database/usuarios.csv'
        df = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame(columns=['CPF', 'Nome', 'Endereco', 'Email', 'Saldo', 'Tipo_Conta'])
        
        if usuario.cpf in df['CPF'].values:
            print("CPF já cadastrado.")
            return

        novo_usuario = pd.DataFrame([[usuario.cpf, usuario.nome, usuario.endereco, usuario.email, usuario.saldo, usuario.tipo_conta]], columns=df.columns)
        df = pd.concat([df, novo_usuario], ignore_index=True)
        df.to_csv(file_path, index=False)

    @staticmethod
    def exibir_dados_usuario(cpf):
        usuarios = pd.read_csv('database/usuarios.csv').set_index('CPF').to_dict(orient='index')
        if cpf not in usuarios:
            print("Usuário não encontrado.")
            return

        usuario = usuarios[cpf]
        print(f"CPF: {cpf}\nNome: {usuario['Nome']}\nEndereço: {usuario['Endereco']}\nEmail: {usuario['Email']}\nSaldo: {usuario['Saldo']}\nTipo de Conta: {usuario['Tipo_Conta']}")
        print("-" * 30)
