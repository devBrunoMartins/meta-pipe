POPULACAO_CONFIG = {
    'label': 'População',
    'name': 'populacao',
    'url': (
        'https://servicodados.ibge.gov.br/api/v3/'
        'agregados/4714/periodos/2022/'
        'variaveis/93?localidades=N6'
    ),

    'normalize': {

        'record_path': ['resultados', 'series'],

        'meta': [
            ['id'],
            ['variavel'],
            ['unidade']
        ],

        'errors': 'ignore',
        'sep': '.'
    },

    'columns': [

        {
            'source': ['localidade', 'id'],
            'target': 'city_id'
        },

        {
            'source': ['localidade', 'nome'],
            'target': 'city_name'
        },

        {
            'source': ['serie', '2022'],
            'target': 'population'
        }
    ],

    'static_columns': {
        'year': 2022
    },

    'dtypes': {

        'city_id': 'Int64',
        'city_name': 'string',
        'population': 'Int64',
        'year': 'Int64'
    },

    'constraints': {

        'not_null': [
            'city_id',
            'city_name',
            'population',
            'year'
        ],

        'unique': [],

        'primary_key': [
            'city_id',
            'year'
        ]
    }
}