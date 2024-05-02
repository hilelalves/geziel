import PySimpleGUI as sg
import json
import random
import string

# Definindo o tema e cores personalizadas
sg.theme('DarkBlue14')
cor_azul_marinho = '#173f5f'
cor_cinza_claro = '#FFFFFF'
cor_verde = '#2ca02c'
cor_vermelha = '#d62728'
cor_fundo = '#edf6f9'

# Variáveis globais para armazenar informações do usuário logado
usuario_logado = None  # Inicialmente nenhum usuário está logado

# Função para gerar número de agência aleatório
def gerar_agencia():
    return ''.join(random.choices(string.digits, k=4))

# Função para gerar número de conta aleatório
def gerar_conta():
    return ''.join(random.choices(string.digits, k=6))

# Função para cadastrar uma nova conta
def cadastrar_conta():
    layout = [
        [sg.Text('Nome:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF')],
        [sg.InputText(key='-NOME-')],
        [sg.Text('Data de Nascimento (DD/MM/AAAA):', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF')],
        [sg.InputText(key='-DATA_NASCIMENTO-')],
        [sg.Text('CPF:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF')],
        [sg.InputText(key='-CPF-')],
        [sg.Text('Endereço', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF', key='-LABEL_ENDERECO-', visible=False)],
        [sg.Text('Logradouro:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF', visible=False)],
        [sg.InputText(key='-LOGRADOURO-', visible=False)],
        [sg.Text('Bairro:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF', visible=False)],
        [sg.InputText(key='-BAIRRO-', visible=False)],
        [sg.Text('Cidade:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF', visible=False)],
        [sg.InputText(key='-CIDADE-', visible=False)],
        [sg.Text('Estado (Sigla):', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF', visible=False)],
        [sg.InputText(key='-ESTADO-', visible=False)],
        [sg.Button('Cadastrar', button_color=(cor_cinza_claro, cor_azul_marinho), size=(10, 1), font=('Helvetica', 12, 'bold'), key='-CADASTRAR-')]
    ]

    window = sg.Window('Cadastrar Nova Conta', layout, background_color=cor_fundo)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-CADASTRAR-':
            nome = values['-NOME-']
            data_nascimento = values['-DATA_NASCIMENTO-']
            cpf = values['-CPF-']
            logradouro = values['-LOGRADOURO-']
            bairro = values['-BAIRRO-']
            cidade = values['-CIDADE-']
            estado = values['-ESTADO-']

            # Verifica se as informações pessoais foram preenchidas
            if nome and data_nascimento and cpf:
                # Gerar número de agência e conta aleatórios
                agencia = gerar_agencia()
                conta = gerar_conta()

                # Montando o dicionário com os dados da conta
                nova_conta = {
                    "nome": nome,
                    "data_nascimento": data_nascimento,
                    "cpf": cpf,
                    "agencia": agencia,
                    "conta": conta,
                    "endereco": {
                        "logradouro": logradouro,
                        "bairro": bairro,
                        "cidade": cidade,
                        "estado": estado
                    },
                    "saldo": 0,  # Saldo inicial definido como zero
                    "limite_diario": 3,  # Define um limite diário inicial de 3 saques
                    "extrato": []  # Lista vazia para armazenar transações
                }

                # Salvando os dados da nova conta em um arquivo JSON
                with open("contas.json", "a") as arquivo:
                    json.dump(nova_conta, arquivo)
                    arquivo.write("\n")
                sg.popup("Conta cadastrada com sucesso! Agência: " + agencia + " Conta: " + conta, font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_verde)
            else:
                sg.popup("Preencha todas as informações pessoais antes de cadastrar.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_vermelha)
            break

    window.close()

# Função para fazer login com agência e conta
def fazer_login():
    global usuario_logado
    layout = [
        [sg.Text('Agência:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF')],
        [sg.InputText(key='-AGENCIA-')],
        [sg.Text('Conta:', font=('Helvetica', 12, 'bold'), text_color='#FFFFFF')],
        [sg.InputText(key='-CONTA-')],
        [sg.Button('Login', button_color=(cor_cinza_claro, cor_azul_marinho), size=(10, 1), font=('Helvetica', 12, 'bold'), key='-LOGIN-')]
    ]

    window = sg.Window('Login', layout, background_color=cor_fundo)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-LOGIN-':
            agencia = values['-AGENCIA-']
            conta = values['-CONTA-']

            # Verificando se a conta existe no arquivo JSON
            with open("contas.json", "r") as arquivo:
                for linha in arquivo:
                    conta_info = json.loads(linha)
                    if conta_info["agencia"] == agencia and conta_info["conta"] == conta:
                        sg.popup(f"\nLogin bem-sucedido! Bem-vindo, {conta_info['nome']}!", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_verde)
                        usuario_logado = conta_info  # Armazenar informações do usuário logado
                        window.close()
                        return True
                sg.popup("Falha no login. Agência ou conta incorretas.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_vermelha)
            break

    window.close()
    return False

# Função para exibir o menu principal
def menu_principal():
    layout = [
        [sg.Text('MENU PRINCIPAL', justification='center', size=(30, 1), font=('Helvetica', 14, 'bold'), text_color=cor_azul_marinho)],
        [sg.Button('Depositar', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-DEPOSITAR-')],
        [sg.Button('Sacar', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-SACAR-')],
        [sg.Button('Extrato', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-EXTRATO-')],
        [sg.Button('Sair', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-SAIR-')]
    ]

    window = sg.Window('Menu Principal', layout, background_color=cor_fundo)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-SAIR-':
            break
        elif event == '-DEPOSITAR-':
            depositar()
        elif event == '-SACAR-':
            sacar()
        elif event == '-EXTRATO-':
            exibir_extrato()

    window.close()

# Função para realizar um depósito
def depositar():
    global usuario_logado
    if usuario_logado:
        layout = [
            [sg.Text('Digite o valor de depósito:', font=('Helvetica', 12, 'bold'), text_color=cor_azul_marinho)],
            [sg.InputText(key='-VALOR_DEPOSITO-')],
            [sg.Button('Depositar', button_color=(cor_cinza_claro, cor_azul_marinho), size=(10, 1), font=('Helvetica', 12, 'bold'), key='-DEPOSITAR-')]
        ]

        window = sg.Window('Depositar', layout, background_color=cor_fundo)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-DEPOSITAR-':
                deposito = float(values['-VALOR_DEPOSITO-'])
                if deposito <= 0:
                    sg.popup("Valor de depósito inválido", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)
                else:
                    # Atualizar o saldo do usuário logado
                    usuario_logado["saldo"] += deposito
                    usuario_logado["extrato"].append(f"Depósito +R$ {deposito}")
                    sg.popup("DEPÓSITO FEITO COM SUCESSO!", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_verde)
                break

        window.close()
    else:
        sg.popup("Faça login antes de realizar operações.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)

# Função para realizar um saque
def sacar():
    global usuario_logado
    if usuario_logado:
        layout = [
            [sg.Text('Digite o valor de saque:', font=('Helvetica', 12, 'bold'), text_color=cor_azul_marinho)],
            [sg.InputText(key='-VALOR_SAQUE-')],
            [sg.Button('Sacar', button_color=(cor_cinza_claro, cor_azul_marinho), size=(10, 1), font=('Helvetica', 12, 'bold'), key='-SACAR-')]
        ]

        window = sg.Window('Sacar', layout, background_color=cor_fundo)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-SACAR-':
                saque = float(values['-VALOR_SAQUE-'])
                if saque <= 0:
                    sg.popup("Valor inválido", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)
                elif saque > 500:
                    sg.popup("NEGADO: valor do saque excede o limite.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_vermelha)
                elif usuario_logado["limite_diario"] == 0:
                    sg.popup("NEGADO: Você excedeu o limite de saques diários.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_vermelha)
                elif saque <= usuario_logado["saldo"]:
                    usuario_logado["limite_diario"] -= 1
                    usuario_logado["saldo"] -= saque
                    usuario_logado["extrato"].append(f"Saque -R$ {saque}")
                    sg.popup("SAQUE APROVADO", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_verde)
                else:
                    sg.popup("Saldo Insuficiente", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_vermelha)
                break

        window.close()
    else:
        sg.popup("Faça login antes de realizar operações.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)

# Função para exibir o extrato do usuário logado
def exibir_extrato():
    global usuario_logado
    if usuario_logado:
        extrato = usuario_logado.get("extrato", [])
        if len(extrato) == 0:
            sg.popup("Não há transações a serem exibidas.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)
        else:
            extrato_str = '\n'.join(extrato)
            sg.popup(extrato_str + "\nSaldo atual: R$ " + str(usuario_logado['saldo']), font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)
    else:
        sg.popup("Faça login antes de exibir o extrato.", font=('Helvetica', 12, 'bold'), background_color=cor_fundo, text_color=cor_azul_marinho)

# Chamada inicial do programa
def main():
    global usuario_logado
    while True:
        layout = [
            [sg.Text('MENU INICIAL', justification='center', size=(30, 1), font=('Helvetica', 14, 'bold'), text_color=cor_azul_marinho)],
            [sg.Button('Fazer Login', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-FAZER_LOGIN-')],
            [sg.Button('Criar Conta', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-CRIAR_CONTA-')],
            [sg.Button('Sair', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=(cor_cinza_claro, cor_azul_marinho), key='-SAIR-')]
        ]

        window = sg.Window('Menu Inicial', layout, background_color=cor_fundo)

        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-SAIR-':
            break
        elif event == '-FAZER_LOGIN-':
            if fazer_login():
                menu_principal()  # Se o login for bem-sucedido, exibe o menu principal
        elif event == '-CRIAR_CONTA-':
            cadastrar_conta()

    window.close()

if __name__ == "__main__":
    main()
