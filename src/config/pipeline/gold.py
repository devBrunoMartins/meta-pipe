GOLD_DATASET_CONFIG = {
    'gold_municipios_indicadores':{
        'columns': {
            'dim_municipios': [
                'city_id',
                'city_name',
                'microregion_name',
                'mesoregion_name',
                'state_sigla',
                'state_name'            
                ],
            'fact_populacao': [
                'city_id',
                'population'
                ],
            'fact_pib': [
                'city_id',
                'year',
                'pib'
                ]
        }
    },
    
    'gold_estados_resumo':{
        'columns': {
            'dim_municipios': [
                'city_id',
                'state_id',
                'state_name',
                'state_sigla'
            ],
            'fact_populacao': [
                'city_id',
                'population'
            ],
            'fact_pib': [
                'city_id',
                'year',
                'pib'
            ]
        },
        'order': [
            'state_id', 
            'state_name', 
            'state_sigla', 
            'total_populacao', 
            'total_pib', 
            'avg_pib_per_capita', 
            'total_cities'
        ]
    },

    'gold_ranking_pib':{
        'columns': {
            'dim_municipios': [
                'city_id',
                'city_name',
                'state_sigla'
            ],
            'fact_pib': [
                'city_id',
                'year',
                'pib'
            ]
        }
    },

    'gold_ranking_populacao':{
        'columns': {
            'dim_municipios': [
                'city_id',
                'city_name',
                'state_sigla'
            ],
            'fact_populacao': [
                'city_id',
                'year',
                'population'
            ]
        }
    },

    'gold_ranking_pib_per_capita':{
        'columns': {
            'dim_municipios': [
                'city_id',
                'city_name',
                'state_sigla'
            ],
            'fact_populacao': [
                'city_id',
                'population'
            ],
            'fact_pib': [
                'city_id',
                'year',
                'pib'
            ]
        }
    }

}