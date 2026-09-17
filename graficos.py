"""
Comparação climática São Paulo: 2025 vs 2026 (Jun-Ago)
--------------------------------------------------------
Objetivo: comparar o período jun-ago de 2025 com o mesmo período de 2026
(ano de El Niño) para ver em quais variáveis o efeito do El Niño aparece:
temperatura, vento ou chuva.

Entradas (relativas à pasta do projeto):
  - arquivos/ddm/t_sp_25_ddm.csv
  - arquivos/ddm/t_sp_26_ddm.csv
  (colunas: Data, Temperatura_media, Temperatura_maxima, Temperatura_minima,
   Direcao_vento, Velocidade_vento, Soma_chuva, direcao_cardinal)

Saídas (em ./outputs/, criada automaticamente):
  1_serie_temporal.png  -> temperatura e chuva dia a dia, 2025 sobreposto a 2026
  2_boxplots.png        -> distribuição (mediana/quartis/outliers) de cada variável
  3_rosa_ventos.png      -> frequência da direção do vento em cada ano
  4_chuva_resumo.png     -> total de chuva, dias com chuva e maior chuva em 1 dia
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 0. Pasta de saída (criada automaticamente se não existir)
# ---------------------------------------------------------------
PASTA_SAIDA = 'outputs'
os.makedirs(PASTA_SAIDA, exist_ok=True)

# ---------------------------------------------------------------
# 1. Carregar os dois anos e criar um índice comum "dia do período"
#    (0 = 1º de junho), para poder sobrepor as duas séries no mesmo eixo X
#    mesmo com os anos sendo diferentes.
# ---------------------------------------------------------------
df25 = pd.read_csv('arquivos/ddm/t_sp_25_ddm.csv', parse_dates=['Data'])
df26 = pd.read_csv('arquivos/ddm/t_sp_26_ddm.csv', parse_dates=['Data'])
df25['dia'] = range(len(df25))
df26['dia'] = range(len(df26))

c25, c26 = '#2E86AB', '#E76F51'  # cores fixas: azul = 2025, laranja = 2026

# ---------------------------------------------------------------
# 2. Estatísticas resumo (média, desvio padrão, min, max) + chuva total
#    Isso é o que confirma numericamente o que os gráficos mostram depois.
# ---------------------------------------------------------------
print("=== Estatísticas resumo ===")
for nome, df in [('2025', df25), ('2026', df26)]:
    resumo = df[['Temperatura_media', 'Temperatura_maxima', 'Temperatura_minima',
                 'Velocidade_vento', 'Soma_chuva']].describe().loc[['mean', 'std', 'min', 'max']]
    print(f"\n--- {nome} ---")
    print(resumo)
    print(f"Chuva total no período: {df['Soma_chuva'].sum():.1f} mm")
    print(f"Dias com chuva: {(df['Soma_chuva'] > 0).sum()} de {len(df)}")

print("\nDistribuição da direção do vento (%) - 2025:")
print((df25['direcao_cardinal'].value_counts(normalize=True) * 100).round(1))
print("\nDistribuição da direção do vento (%) - 2026:")
print((df26['direcao_cardinal'].value_counts(normalize=True) * 100).round(1))

# ---------------------------------------------------------------
# 3. Gráfico 1: série temporal sobreposta
#    Painel de cima = temperatura média dia a dia (2025 x 2026)
#    Painel de baixo = chuva diária dia a dia (2025 x 2026)
#    Mostra a evolução ao longo da estação, não só a média do período.
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

axes[0].plot(df25['dia'], df25['Temperatura_media'], label='2025', color=c25, linewidth=1.5)
axes[0].plot(df26['dia'], df26['Temperatura_media'], label='2026 (El Niño)', color=c26, linewidth=1.5)
axes[0].set_ylabel('Temperatura média (°C)')
axes[0].set_title('Temperatura média diária: 2025 vs 2026 (Jun-Ago)')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].bar(df25['dia'] - 0.2, df25['Soma_chuva'], width=0.4, label='2025', color=c25, alpha=0.8)
axes[1].bar(df26['dia'] + 0.2, df26['Soma_chuva'], width=0.4, label='2026 (El Niño)', color=c26, alpha=0.8)
axes[1].set_ylabel('Chuva (mm)')
axes[1].set_xlabel('Dia do período (0 = 1º jun)')
axes[1].set_title('Precipitação diária: 2025 vs 2026')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, '1_serie_temporal.png'), dpi=130)
plt.close()

# ---------------------------------------------------------------
# 4. Gráfico 2: boxplots lado a lado
#    Compara mediana, quartis e outliers de cada variável entre os dois anos
#    -> revela se a diferença é só na média ou na distribuição toda.
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(14, 5))
variaveis = [
    ('Temperatura_media', 'Temp. média (°C)'),
    ('Temperatura_maxima', 'Temp. máxima (°C)'),
    ('Temperatura_minima', 'Temp. mínima (°C)'),
    ('Velocidade_vento', 'Vel. vento (m/s)'),
]
for ax, (col, label) in zip(axes, variaveis):
    bp = ax.boxplot([df25[col], df26[col]], tick_labels=['2025', '2026'],
                     patch_artist=True, widths=0.5)
    for patch, color in zip(bp['boxes'], [c25, c26]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_title(label)
    ax.grid(alpha=0.3, axis='y')
plt.suptitle('Distribuição das variáveis: 2025 vs 2026', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, '2_boxplots.png'), dpi=130, bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------
# 5. Gráfico 3: rosa dos ventos
#    Frequência (%) de cada direção cardinal do vento em cada ano,
#    num gráfico polar -> revela mudanças no padrão de circulação atmosférica.
# ---------------------------------------------------------------
dirs_order = ['Norte', 'Nordeste', 'Leste', 'Sudeste', 'Sul', 'Sudoeste', 'Oeste', 'Noroeste']
angles = np.linspace(0, 2 * np.pi, len(dirs_order), endpoint=False)

freq25 = df25['direcao_cardinal'].value_counts(normalize=True).reindex(dirs_order, fill_value=0) * 100
freq26 = df26['direcao_cardinal'].value_counts(normalize=True).reindex(dirs_order, fill_value=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), subplot_kw={'projection': 'polar'})
for ax, freq, ano, color in zip(axes, [freq25, freq26], ['2025', '2026 (El Niño)'], [c25, c26]):
    vals = freq.values.tolist()
    vals += vals[:1]  # fecha o polígono
    ang = angles.tolist() + [angles[0]]
    ax.plot(ang, vals, color=color, linewidth=2)
    ax.fill(ang, vals, color=color, alpha=0.3)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(dirs_order, fontsize=8)
    ax.set_title(f'Rosa dos ventos {ano}', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, '3_rosa_ventos.png'), dpi=130)
plt.close()

# ---------------------------------------------------------------
# 6. Gráfico 4: resumo de chuva
#    Três indicadores lado a lado: chuva total, nº de dias com chuva,
#    e a maior chuva registrada em um único dia -> mostra se a chuva é
#    mais frequente ou mais concentrada em eventos intensos.
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
metricas = ['Total de chuva\n(mm)', 'Dias com\nchuva', 'Maior chuva\nem 1 dia (mm)']
v25 = [df25['Soma_chuva'].sum(), (df25['Soma_chuva'] > 0).sum(), df25['Soma_chuva'].max()]
v26 = [df26['Soma_chuva'].sum(), (df26['Soma_chuva'] > 0).sum(), df26['Soma_chuva'].max()]
x = np.arange(len(metricas))
ax.bar(x - 0.2, v25, width=0.4, label='2025', color=c25)
ax.bar(x + 0.2, v26, width=0.4, label='2026 (El Niño)', color=c26)
ax.set_xticks(x)
ax.set_xticklabels(metricas)
ax.set_title('Precipitação: 2025 vs 2026')
ax.legend()
ax.grid(alpha=0.3, axis='y')
for i, (a, b) in enumerate(zip(v25, v26)):
    ax.text(i - 0.2, a, f'{a:.1f}', ha='center', va='bottom', fontsize=9)
    ax.text(i + 0.2, b, f'{b:.1f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, '4_chuva_resumo.png'), dpi=130)
plt.close()

print(f"\nOK - 4 gráficos salvos em ./{PASTA_SAIDA}/")