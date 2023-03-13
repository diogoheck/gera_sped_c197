import os
from time import sleep
#  sao 33 itens com a condição esperada, terei que adicionar 33 c197


def gravar_linha(novo_sped):
    with open('sped_final.txt', 'a') as sped_final:
        for linha_sped in novo_sped:
            sped_final.write(linha_sped)


# def criar_registro_0460(linha):
#     try:
#         print(int(linha.split('|')[1]))
#         if int(linha.split('|')[1]) >= 450 and int(linha.split('|')[1] <= 500):
#             print(linha)
#     except:
#         pass


def inserir_c197_sped(linhas_sped):
    i = 0
    achou_item = False
    lista_c197 = []
    novo_sped = []
    soma_valor_apurado = 0
    primeiro_registro = True
    # soma_valor_apurado_rg2 = 0
    for linha in linhas_sped:

        # criar_registro_0460(linha)
        if linha.split('|')[1] == '0000':
            competencia = linha.split('|')[4][2:4]
            print(competencia)
        # print(linha)
        # achar item
        if linha.split('|')[1] != 'C170' and linha.split('|')[1] != 'C190' and linha.split('|')[1] != 'C195' and linha.split('|')[1] != 'C191' and achou_item:
            achou_item = False
            for c197 in lista_c197:

                novo_sped.append(c197)
                primeiro_registro = True

            lista_c197 = []

        if linha.split('|')[1] == 'C100':

            ultimo_c100 = linha.split('|')[10]
            # print(ultimo_c100[2:4])

            # 11 e 14
        elif linha.split('|')[1] == 'C170' and linha.split('|')[11] == '2102' and float(linha.split('|')[14].replace(',', '.')) == 4:
            achou_item = True
            codigo_item = linha.split('|')[3]
            base_icms_item_calculo = float(
                linha.split('|')[13].replace('.', '').replace(',', '.'))
            base_icms_item = linha.split('|')[13]
            imposto_calculado = round(float(base_icms_item_calculo * 0.13), 2)
            # print(linha)
            if ultimo_c100[2:4] == competencia:
                codigo_beneficio = 'RS99993006'
                # soma_valor_apurado_rg1 += imposto_calculado
            else:
                codigo_beneficio = 'RS99993005'
            soma_valor_apurado += imposto_calculado
            soma_valor_apurado = round(soma_valor_apurado, 2)
            # soma_valor_apurado_rg2 = round(soma_valor_apurado_rg2, 2)
            # print(ultimo_c100)
            imposto_calculado = str(imposto_calculado).replace('.', ',')

            if primeiro_registro:
                lista_c197.append(
                    f'|C195|1503|DEBITO ANTECIPACAO ICMS|\n')
                primeiro_registro = False
            lista_c197.append(
                f'|C197|{codigo_beneficio}||{codigo_item}|{base_icms_item}|13,00|{imposto_calculado}|0,00|\n')
            i += 1

        novo_sped.append(linha)
    # print(i)
    # print(soma_valor_apurado)
    return novo_sped, soma_valor_apurado


if __name__ == '__main__':
    try:

        if os.path.isfile('sped_final.txt'):
            os.remove('sped_final.txt')
        if os.path.isfile('REGISTRO_E111.txt'):
            os.remove('REGISTRO_E111.txt')

        with open('sped.txt', 'r') as banco_dados:
            linhas_sped = banco_dados.readlines()

        novo_sped, soma_valor_apurado = inserir_c197_sped(
            linhas_sped)
        soma_valor_apurado = str(soma_valor_apurado).replace('.', ',')

        gravar_linha(novo_sped)

        with open('REGISTRO_E111.txt', 'a') as registro:
            registro.write(f'|E111|RS001503||{soma_valor_apurado}|\n')

        print('finalizado com sucesso \o/')
        os.system("pause")

    except Exception as e:
        print(f'finalizado com erro => {e}')
