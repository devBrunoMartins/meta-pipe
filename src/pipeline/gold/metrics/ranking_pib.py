import pandas as pd

def build_gold_ranking_pib(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_pib = fact_pib[columns['fact_pib']]

    ranking_pib = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
    )
  
    ranking_pib = ranking_pib.sort_values(['pib'], ascending=False).reset_index()

    return ranking_pib