import pandas as pd

t_sp_25_ddm = pd.read_csv('arquivos/ddm/t_sp_25_ddm.csv')
t_sp_26_ddm = pd.read_csv('arquivos/ddm/t_sp_26_ddm.csv')



t_sp_25_ddm["Data"] = pd.to_datetime(
        t_sp_25_ddm["Data"],
        format="%Y-%m-%d",
        errors="raise"
    )

t_sp_26_ddm["Data"] = pd.to_datetime(
        t_sp_26_ddm["Data"],
        format="%Y-%m-%d",
        errors="raise"
    )

tabelas = {
    "25": t_sp_25_ddm,
    "26": t_sp_26_ddm
}

def analise(nome, df):
    linha = "-" * 60

    print("\n" + "="*60)
    print(f"📊 ANÁLISE DA TABELA: {nome.upper()}")
    print("="*60)

    print(f"\n{linha}")
    print("🔎 INFORMAÇÕES GERAIS:")
    print(linha)
    df.info()

    print(f"\n{linha}")
    print("📌 PRIMEIRAS LINHAS:")
    print(linha)
    print(df.head())


    print(f"\n{linha}")
    print("📌 ÚLTIMAS LINHAS:")
    print(linha)
    print(df.tail())

    print(f"\n{linha}")
    print("🧾 TIPOS DE DADOS:")
    print(linha)
    print(df.dtypes)

    print(f"\n{linha}")
    print("📂 COLUNAS:")
    print(linha)
    print(list(df.columns))

    print(f"\n{linha}")
    print("📏 FORMATO (linhas, colunas):")
    print(linha)
    print(df.shape)

    print(f"\n{linha}")
    print("📊 ESTATÍSTICAS:")
    print(linha)
    print(df.describe())

    print(f"\n{linha}")
    print("⚠️ VALORES NULOS POR COLUNA:")
    print(linha)
    print(df.isnull().sum())


    print("\n" + "="*60 + "\n")

for nome, df in tabelas.items():
    analise(nome, df)