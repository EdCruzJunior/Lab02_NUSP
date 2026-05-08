select *
from {{ ref('fct_acidentes') }}
where vitima_fatal < 0