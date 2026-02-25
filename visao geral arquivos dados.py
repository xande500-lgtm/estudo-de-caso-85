import pandas as pd

caminho_arquivo = r'dados_saida.csv'

# Carregar os dados
df = pd.read_csv(caminho_arquivo)

# 1. Estrutura geral e tipos de dados
print("=== Estrutura do DataFrame ===")
print(df.info())

# 2. Valores nulos por coluna
print("\n=== Valores nulos por coluna ===")
print(df.isnull().sum())

# 3. Linhas duplicadas
print("\n=== Número de linhas duplicadas ===")
print(df.duplicated().sum())

# 4. Estatísticas descritivas (para detectar outliers)
print("\n=== Estatísticas descritivas ===")
print(df.describe(include='all'))

# 5. Valores negativos em colunas que não deveriam ter
print("\n=== Preços negativos ===")
print(df[df['price'] < 0])

print("\n=== Vendas negativas ===")
print(df[df['sales'] < 0])

print("\n=== Estoque negativo ===")
print(df[df['stock_quantity'] < 0])

print("\n=== Descontos fora da faixa lógica (menor que 0 ou maior que 100) ===")
print(df[(df['discount'] < 0) | (df['discount'] > 100)])

# 6. Conferir se datas estão válidas
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print("\n=== Datas inválidas convertidas para NaT ===")
print(df[df['date'].isnull()])