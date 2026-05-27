MUNICIPIOS_CONFIG = {
    'label': 'Municípios',
    'name': 'municipios',
    'url': (
        'https://servicodados.ibge.gov.br/api/v1/'
        'localidades/municipios'
    ),

    'normalize': {

        'sep': '.',
        'errors': 'ignore'
    },

    'columns': [

        {
            'source': ['id'],
            'target': 'city_id'
        },

        {
            'source': ['nome'],
            'target': 'city_name'
        },

        {
            'source': ['microrregiao', 'id'],
            'target': 'microregion_id'
        },

        {
            'source': ['microrregiao', 'nome'],
            'target': 'microregion_name'
        },

        {
            'source': ['microrregiao', 'mesorregiao', 'id'],
            'target': 'mesoregion_id'
        },

        {
            'source': ['microrregiao', 'mesorregiao', 'nome'],
            'target': 'mesoregion_name'
        },

        {
            'source': ['microrregiao', 'mesorregiao', 'UF', 'id'],
            'target': 'state_id'
        },

        {
            'source': ['microrregiao', 'mesorregiao', 'UF', 'sigla'],
            'target': 'state_sigla'
        },

        {
            'source': ['microrregiao', 'mesorregiao', 'UF', 'nome'],
            'target': 'state_name'
        }
    ],

    'dtypes': {

        'city_id': 'Int64',

        'city_name': 'string',

        'microregion_id': 'Int64',

        'microregion_name': 'string',

        'mesoregion_id': 'Int64',

        'mesoregion_name': 'string',

        'state_id': 'Int64',

        'state_sigla': 'string',

        'state_name': 'string'
    },

    'constraints': {

        'not_null': [
            'city_id'
        ],

        'unique': [
            'city_id'
        ],

        'primary_key': [
            'city_id'
        ]
    }
}