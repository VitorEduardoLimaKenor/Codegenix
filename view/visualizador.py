import seaborn as sns
import json
import pandas as pd
import matplotlib.pyplot as plt

with open('historico_avaliacoes.json', 'r', encoding='utf-8') as arquivo:
    historico_avaliacoes = json.load(arquivo)
    df = pd.DataFrame(historico_avaliacoes)
   
df = pd.json_normalize(arquivo)

df.rename(columns={
    'metricas.eficiencia': 'Eficiencia',
    'metricas.clareza': 'Clareza',
    'metricas.boas_praticas': 'BoasPraticas'
}, inplace=True)

sns.set_theme(style="darkgrid")

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.lineplot(data=df, x='geracao', y='fitness', color="black", marker='o')
plt.title('Evolução do Fitness')
plt.xlabel('Geração')
plt.ylabel('Fitness')

plt.subplot(2, 2, 2)
sns.lineplot(data=df, x='geracao', y='Eficiencia',   color="orange", marker='o')
plt.title('Evolução da Eficiência')
plt.xlabel('Geração')
plt.ylabel('Eficiência')

plt.subplot(2, 2, 3)
sns.lineplot(data=df, x='geracao', y='Clareza', color="green",  marker='o')
plt.title('Evolução da Clareza')
plt.xlabel('Geração')
plt.ylabel('Clareza')

plt.subplot(2, 2, 4)
sns.lineplot(data=df, x='geracao', y='BoasPraticas', color="blue",   marker='o')
plt.title('Evolução das Boas Práticas')
plt.xlabel('Geração')
plt.ylabel('Boas Práticas')

plt.tight_layout()
plt.show()