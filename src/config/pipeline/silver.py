SILVER_DATASET_CONFIG = {

    'municipios': {
        
        'label': 'Municípios',
        'table_prefix': 'dim',
        'payload': {
                'type': 'flat'
            },

        'columns': [
            {'source': ['id'], 'target': 'city_id'},
            {'source': ['nome'], 'target': 'city_name'},
            {'source': ['microrregiao', 'id'], 'target': 'microregion_id'},
            {'source': ['microrregiao', 'nome'], 'target': 'microregion_name'},
            {'source': ['microrregiao', 'mesorregiao', 'id'], 'target': 'mesoregion_id'},
            {'source': ['microrregiao', 'mesorregiao', 'nome'], 'target': 'mesoregion_name'},
            {'source': ['microrregiao', 'mesorregiao', 'UF', 'id'], 'target': 'state_id'},
            {'source': ['microrregiao', 'mesorregiao', 'UF', 'sigla'], 'target': 'state_sigla'},
            {'source': ['microrregiao', 'mesorregiao', 'UF', 'nome'], 'target': 'state_name'}
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
            'not_null': ['city_id'],
            'unique': ['city_id'],
            'primary_key': ['city_id']
        },
    },

    'populacao': {

        'label': 'População',
        'table_prefix': 'fact',

        'payload': {
            'type': 'json_normalize',
            'record_path': ['resultados', 'series']
        },

        'static_columns': {
            'year': 2022
        },

        'columns': [
            {'source': ['localidade', 'id'], 'target': 'city_id'},
            {'source': ['localidade', 'nome'], 'target': 'city_name'},
            {'source': ['serie', '2022'], 'target': 'population'}
        ],

        'dtypes': {
            'city_id': 'Int64',
            'city_name': 'string',
            'population': 'Int64',
            'year': 'Int64'
        },

        'constraints': {
            'not_null': ['city_id', 'city_name', 'population', 'year'],
            'unique': [],
            'primary_key': ['city_id', 'year']
        }
    },

    'pib': {

        'label': 'PIB',
        'table_prefix': 'fact',

        'payload': {
            'type': 'flat'
        },

        'pre_processing': {
            'skip_rows': 1
        },

        'columns': [
            {'source': ['D1C'], 'target': 'city_id'},
            {'source': ['D3C'], 'target': 'year'},
            {'source': ['V'], 'target': 'pib'},
            {'source': ['D1N'], 'target': 'city_name'},
            {'source': ['MN'], 'target': 'unit'},
            {'source': ['D2N'], 'target': 'variable_name'}
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
            'not_null': ['city_id', 'year', 'pib'],
            'unique': [],
            'primary_key': ['city_id', 'year']
        }
    }
}