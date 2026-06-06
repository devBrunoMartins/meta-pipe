import pandas as pd

def build_gold_municipios_indicadores(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]
    fact_pib = fact_pib[columns['fact_pib']]

    municipios_indicadores = (
        
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
    
    municipios_indicadores['pib_per_capita'] = municipios_indicadores['pib'] / municipios_indicadores['population']

    return municipios_indicadores.reset_index()