select
    data,
    hora,
    municipio,
    regiao_administrativa as estado,  -- ✔ ajuste aqui
    classe,
    subclasse,
    vitima_fatal,
    vitima_grave,
    vitima_leve,
    vitima_ilesa
from {{ source('raw', 'acidentes_raw') }}