# Recriando o processor.py após reset com melhorias robustas
import pandas as pd

def tratar_dados(df_averis: pd.DataFrame, lista_df_fazendas: list[pd.DataFrame], mes: int) -> pd.DataFrame:
    """
    Trata os dados da planilha Averis cruzando com as planilhas das fazendas.
    Aplica filtro de ano = 2025 e mês = mes nas planilhas das fazendas.
    Para MG, ignora a fazenda no cruzamento.
    Adiciona colunas 'Situação' e 'Status da Verificação'.
    Garante tratamento robusto para campos OBS e fallback para datas.
    """
    df_resultado = df_averis.copy()
    situacoes = []
    status_verificacao = []

    for i in range(len(lista_df_fazendas)):
        df_faz = lista_df_fazendas[i]
        df_faz.columns = [col.strip().upper() for col in df_faz.columns]

        # Tenta identificar e converter a coluna de data
        data_col = None
        possible_date_cols = [col for col in df_faz.columns if 'DATA' in col]
        for col in possible_date_cols:
            try:
                df_faz[col] = pd.to_datetime(df_faz[col], errors='coerce')
                if pd.api.types.is_datetime64_any_dtype(df_faz[col]):
                    data_col = col
                    break
            except Exception:
                continue

        if data_col:
            df_filtered = df_faz[
                (df_faz[data_col].dt.year == 2025) &
                (df_faz[data_col].dt.month == mes)
            ]
            if df_filtered.empty:
                lista_df_fazendas[i] = df_faz  # fallback sem filtro
            else:
                lista_df_fazendas[i] = df_filtered
        else:
            lista_df_fazendas[i] = df_faz

    # Loop nas NFs da Averis
    for idx, row in df_resultado.iterrows():
        numero_nf = row['Nº NF-e']
        projeto = str(row['Projeto']).strip().upper()
        uf_emissor = str(row['UF emissor']).strip().upper()

        obs_encontrada = "em trânsito"
        encontrado = False

        for df_faz in lista_df_fazendas:
            if 'NF EMITIDA' not in df_faz.columns or 'OBS' not in df_faz.columns:
                continue

            if uf_emissor == "MG":
                df_match = df_faz[df_faz['NF EMITIDA'] == numero_nf]
            else:
                if 'FAZENDA' not in df_faz.columns:
                    continue
                df_match = df_faz[
                    (df_faz['NF EMITIDA'] == numero_nf) &
                    (df_faz['FAZENDA'].astype(str).str.strip().str.upper() == projeto)
                ]

            if not df_match.empty:
                encontrado = True
                obs = df_match.iloc[0]['OBS']
                if pd.notna(obs) and str(obs).strip() and str(obs).lower().strip() != "nan":
                    obs_encontrada = str(obs).strip()
                break

        situacoes.append(obs_encontrada)
        status_verificacao.append("OK" if encontrado else "NÃO ENCONTRADO")

    df_resultado.insert(1, "Situação", situacoes)
    df_resultado.insert(2, "Status da Verificação", status_verificacao)
    return df_resultado
