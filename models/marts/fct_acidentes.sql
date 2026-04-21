{{ config(
    materialized='incremental',
    unique_key='id_acidente'
) }}

select
    md5(concat(cast(data as text), cast(hora as text), rodovia, cast(km as text))) as id_acidente,
    data,
    hora,
    rodovia,
    km,
    sentido,
    municipio,

    vitima_ilesa,
    vitima_leve,
    vitima_moderada,
    vitima_grave,
    vitima_fatal,

    veiculos_envolvidos

from {{ ref('stg_acidentes') }}

{% if is_incremental() %}
where data > (select max(data) from {{ this }})
{% endif %}