import pandas as pd

def build_gold_ranking_populacao(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao       = datasets['fact_populacao']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]

    ranking_populacao = (
        
        dim_municipios

        .merge(
            fact_populacao,
            on='city_id',
            how='left'
               )
    )
  
    ranking_populacao = ranking_populacao.sort_values(['population'], ascending=False).reset_index()

    return ranking_populacao