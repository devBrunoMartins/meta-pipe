import pandas as pd

def build_gold_estados_resumo(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios  = dim_municipios[columns['dim_municipios']]
    fact_populacao  = fact_populacao[columns['fact_populacao']]
    fact_pib        = fact_pib[columns['fact_pib']]

    estados_resumo = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
        .merge(
            fact_populacao,
            on='city_id',
            how='left'
            )
    )
    estados_resumo = (
        estados_resumo
        .groupby(['state_id', 'state_name', 'state_sigla'])
        .agg(
            total_populacao=('population', 'sum'),
            total_pib=('pib', 'sum'),
            total_cities=('city_id', 'count')
        )
        .reset_index()

    )

    estados_resumo['avg_pib_per_capita'] = estados_resumo['total_pib'] / estados_resumo['total_populacao']

    return estados_resumo
