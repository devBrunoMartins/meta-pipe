import pandas as pd

def build_gold_ranking_pib_per_capita(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]
    fact_pib = fact_pib[columns['fact_pib']]

    ranking_pib_per_capita = (
        
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
    
    ranking_pib_per_capita['pib_per_capita'] = ranking_pib_per_capita['pib'] / ranking_pib_per_capita['population']

    ranking_pib_per_capita = (
        ranking_pib_per_capita
        .sort_values(['pib'], ascending=False)
        .reset_index())


    return ranking_pib_per_capita