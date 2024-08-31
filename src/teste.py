

def informacao_transacao(self, transacao=None, dicionario=None):
    # Defina o caminho para o arquivo
    caminho_arquivo = 'data/historico.txt'
    
    # Abra o arquivo para escrita
    with open(caminho_arquivo, 'a+') as informacao_transacao:
        texto_transacao = f"""
        Nome do banco: {self.nome_banco}
        Tipo de Operação: {transacao}
        Saldo Atual: {self.saldo:.2f}
        """

        texto_transacao += ''.join(f"{chave.capitalize()} : {valor}\n" for chave, valor in dicionario.items())
        print(texto_transacao)
        informacao_transacao.write(f'{texto_transacao}\n{"".center(40, "=")}\n')