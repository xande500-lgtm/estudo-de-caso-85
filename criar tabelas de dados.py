import pandas as pd
import random
import os
from faker import Faker

os.system('cls')

fake = Faker()

n = 2000

store_names, dates, prices, sales = [], [], [], []
product_ids, product_names, categories = [], [], []
customer_ids, customer_names, regions = [], [], []
payment_methods, discounts, stock_quantities = [], [], []

for i in range(n):
    # Loja
    store_names.append(random.choice([
        fake.company(),
        fake.company() + " Str.",
        fake.company().lower(),
        fake.company().strip()
    ]))
    
    # Datas
    dates.append(random.choice([
        fake.date(),
        fake.date_time().strftime("%d/%m/%Y"),
        fake.date_time().strftime("%Y-%m-%d %H:%M:%S")
    ]))
    
    # Preço e vendas
    prices.append(random.choice([round(random.uniform(-100, 500), 2), None]))
    sales.append(random.choice([random.randint(-50, 200), None]))
    
    # Produto
    product_ids.append(i+1)
    product_names.append(random.choice([
        "Notebook", "Smartphone", "Camisa", "Tênis", "Chocolate", "Café"
    ]) + random.choice(["", " ", "!!"]))  # erros
    
    categories.append(random.choice(["Eletrônicos", "Roupas", "Alimentos"]))
    
    # Cliente
    customer_ids.append(fake.random_int(min=1000, max=9999))
    customer_names.append(random.choice([
        fake.name(),
        fake.name().lower(),
        fake.name().strip()
    ]))
    
    # Região
    regions.append(random.choice(["SP", "RJ", "MG", "BA", "RS"]))
    
    # Pagamento
    payment_methods.append(random.choice(["Cartão", "Boleto", "Pix", "cartao"]))
    
    # Desconto e estoque
    discounts.append(random.choice([round(random.uniform(-10, 30), 2), None]))
    stock_quantities.append(random.choice([random.randint(-5, 100), None]))

# Criar DataFrame
df = pd.DataFrame({
    "store_name": store_names,
    "date": dates,
    "price": prices,
    "sales": sales,
    "product_id": product_ids,
    "product_name": product_names,
    "category": categories,
    "customer_id": customer_ids,
    "customer_name": customer_names,
    "region": regions,
    "payment_method": payment_methods,
    "discount": discounts,
    "stock_quantity": stock_quantities
})

# Adicionar duplicados
df = pd.concat([df, df.sample(50, random_state=1)], ignore_index=True)

#imprimir a tabela gerada
print(df)

# Exportar para CSV
df.to_csv("dados.csv", index=False)