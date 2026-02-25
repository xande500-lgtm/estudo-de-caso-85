import os

# (1) A equipe para poder tratar os dados precisou antes instalar a biblioteca Pandas, 
# importar a biblioteca e importar o dataframe. Qual o código para instalar a biblioteca 
# Pandas? E para importá-la? E para importar o dataframe?
try:
    import pandas as pd
    print("Pandas está instalado!")
except ImportError:
    print("Pandas não está instalado.\nInstalando pandas...")
    os.system('pip install pandas')
    import pandas as pd

from datetime import datetime

clean_store_name_counter = 0
def clean_store_name(store_name):
    global clean_store_name_counter
    clean_store_name_counter += 1
    store_name = store_name.strip()
    store_name = store_name.replace("Str.", "Store") 
    return store_name

def converter_datas(series):
    formatos = [
        "%d/%m/%Y",         # 24/10/2009
        "%Y-%m-%d",         # 1995-02-28
        "%Y-%m-%d %H:%M:%S" # 2001-12-31 17:09:55
        # basta adicionar mais formatos aqui conforme necessário
    ]
    
    def parse_data(valor):
        if pd.isna(valor) or str(valor).strip() == "":
            return None
        for fmt in formatos:
            try:
                return datetime.strptime(str(valor), fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
        return None  # se não conseguir converter
    
    return series.apply(parse_data)

#limpar o terminal
os.system('cls')

nome_arquivo_original = 'dados.csv'

nome_arquivo_saida = 'dados_saida.csv'

print(f'Será processado o arquivo\n{nome_arquivo_original}\n')
print(f'O resultado será salvo em \n{nome_arquivo_saida}\n')


# (1) E para importar o dataframe?
dados = pd.read_csv(nome_arquivo_original, header = 0)

# Verificar valores ausentes antes
print("Valores ausentes antes do tratamento:\n")
print(dados.isnull().sum())

media = []
mediana = []

for coluna, qtd in dados.isnull().sum().items():
    if qtd > 0:
        if pd.api.types.is_numeric_dtype(dados[coluna]): #processa apenas se a coluna for numérica
            # preencher os valores nulos considerando o comportamento estatístico da coluna
            # media distribuição simétrica e mediana para distribuição assimétrica
            if abs(dados[coluna].skew()) < 1:  # skew próximo de 0 a distribuição é simétrica
                media.append(coluna)
                dados[coluna] = dados[coluna].fillna(dados[coluna].mean())
            else:  # distribuição assimétrica
                mediana.append(coluna)   
                dados[coluna] = dados[coluna].fillna(dados[coluna].median())


print(f"\nColuna(s) tratado(s) usando média: {media}\n")
print(f"Coluna(s) tratado(s) usando mediana: {mediana}\n")  

# Verificar novamente após o tratamento
print("\nValores ausentes depois do tratamento:")
print(dados.isnull().sum())

#excluir as linhas restantes que possuem valores nulos em colunas textuais, não tratadas anteriormente
excluida = []
qt_excluida = 0
print(f'\nExcluindo linhas com valores nulos em colunas textuais não tratadas anteriormente...\n')
for coluna, qtd in dados.isnull().sum().items():
    if qtd > 0:
        excluida.append(coluna)
        qt_excluida += dados[coluna].isnull().sum()
        dados = dados.dropna(subset=[coluna])
print(f"\nLinha(s) excluida(s) por devido à valores nulos nas colunas: {excluida}",'\n')
print(f"Quantidade de linhas excluídas: {qt_excluida}",'\n')

# Verificar novamente após o tratamento
print("Valores ausentes depois do tratamento:\n")
print(dados.isnull().sum())
print('\n')

#processa a coluna store_name utilizando a função clean_store_name
#retira espaços em branco do inicio e do final e substitui "Str." por "Store"
clean_store_name_counter = 0    
dados['store_name'] = dados['store_name'].apply(clean_store_name)    
print(f"Quantidade de vezes que a função clean_store_name foi chamada: {clean_store_name_counter}\n")


#converte campos string que apresentam datas em diversos formatos para um formato único dd/mm/yyyy
print('Convertendo str em diversos formatos para um formato único dd/mm/yyyy\n')    
dados['date'] = converter_datas(dados['date'])

print(f'===== Removendo linhas duplicadas =====\n')
# (2) A equipe esqueceu de remover duplicados, como você pode fazer isso no Pandas?
print('total de linhas antes da remocao de linhas duplicadas', len(dados),'\n')
print('total de linhas duplicadas', dados.duplicated().sum(),'\n') 
dados.drop_duplicates(inplace=True)
print('total de linhas após da remocao de linhas duplicadas', len(dados),'\n')
print(f'=======================================\n')

# (3) Em geral, para que serve a função lambda no python?

# A função lambda em Python serve para criar funções anônimas 
# sem precisar usar def. Ela é usada principalmente quando é 
# preciso uma função simples e temporária.
# De maneira geral é utilizada em operações como ordenação, 
# filtragem ou transformação de dados. 
# A seguir, um exemplo da sintaxe e de utilização:

#retirando os sinais negativos da coluna price
print('Retirando os sinais negativos da coluna price\n')
dados['price'] = dados['price'].apply(lambda x: abs(x))

#retirando os sinais negativos da coluna sales
print('Retirando os sinais negativos da coluna sales\n')
dados['sales'] = dados['sales'].apply(lambda x: abs(x))

#retirando os caracteres especiais da coluna product_name
print('Retirando os caracteres especiais da coluna product_name\n')
dados['product_name'] = dados['product_name'].str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)

#retirando os sinais negativos e casas decimais da coluna stock_quantity
print('Retirando os sinais negativos da coluna stock_quantity\n')
dados['stock_quantity'] = dados['stock_quantity'].apply(lambda x: abs(x))
dados['stock_quantity'] = dados['stock_quantity'].round().astype(int)


print('Retirando os sinais negativos e casas decimais da coluna discount\n')
dados['discount'] = dados['discount'].apply(lambda x: abs(x))
dados['discount'] = dados['discount'].round(2)


# Salvando o resultado em um novo arquivo
try:
    if os.path.exists(nome_arquivo_saida):
        os.remove(nome_arquivo_saida)
    dados.to_csv(nome_arquivo_saida, index=False)
    print(f"Arquivo salvo com sucesso em {nome_arquivo_saida}\n") 
except (OSError, IOError, PermissionError,ValueError) as e:
    print(f"Erro ao salvar o arquivo: {e}")
    exit()

print('\n')
print(type(dados))
print(dados)