PIB_CONFIG = {
    'label': 'PIB',
    'name': 'pib',
    'url': ('https://apisidra.ibge.gov.br/values/'
    't/5938/n6/all/v/37/p/2021'),

    'normalize': {
        'errors': 'ignore'
    },

    'pre_processing': {
        'skip_rows': 1
    },

    'columns': [

        {
            'source': ['D1C'],
            'target': 'city_id'
        },

        {
            'source': ['D3C'],
            'target': 'year'
        },

        {
            'source': ['V'],
            'target': 'pib'
        },

        {
            'source': ['D1N'],
            'target': 'city_name'
        },

        {
            'source': ['MN'],
            'target': 'unit'
        },

        {
            'source': ['D2N'],
            'target': 'variable_name'
        }
    ],

    'dtypes': {

        'city_id': 'Int64',

        'year': 'Int64',

        'pib': 'Float64',

        'city_name': 'string',

        'unit': 'string',

        'variable_name': 'string'
    },

    'constraints': {

        'not_null': [
            'city_id',
            'year',
            'pib'
        ],

        'unique': [],

        'primary_key': [
            'city_id',
            'year'
        ]
    }
}