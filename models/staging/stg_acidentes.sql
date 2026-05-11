select
    cast("DATA" as date) as data,
    cast("HORA" as time) as hora,
    "CONCESSIONARIA" as concessionaria,
    "RODOVIA" as rodovia,
    cast("KM" as numeric) as km,
    "SENTIDO" as sentido,
    cast("LATITUDE" as numeric) as latitude,
    cast("LONGITUDE" as numeric) as longitude,
    "CLASSE" as classe,
    "SUBCLASSE" as subclasse,
    "CAUSA_PROVAVEL" as causa_provavel,

    coalesce("VITIMA_ILESA",0) as vitima_ilesa,
    coalesce("VITIMA_LEVE",0) as vitima_leve,
    coalesce("VITIMA_MODERADA",0) as vitima_moderada,
    coalesce("VITIMA_GRAVE",0) as vitima_grave,
    coalesce("VITIMA_FATAL",0) as vitima_fatal,

    "VEICULOS_ENVOLVIDOS" as veiculos_envolvidos,
    "VISIBILIDADE" as visibilidade,
    "CONDICAO_METERIOLOGICA" as condicao_meteriologica,
    "MUNICIPIO" as municipio,
    "REGIAO_ADMINISTRATIVA" as regiao_administrativa,
    "REGIONAL_DER" as regional_der,
    "JURISDICAO" as jurisdicao

from {{ ref('acidentes_rodovias_2026') }}