select distinct
    municipio,
    regiao_administrativa,
    regional_der,
    jurisdicao
from {{ ref('stg_acidentes') }}