select
    data,
    municipio,
    classe,
    subclasse,
    vitima_fatal,
    vitima_grave,
    vitima_leve
from {{ ref('stg_acidentes') }}