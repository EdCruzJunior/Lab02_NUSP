select *
from {{ ref('fct_acidentes') }}
where data > current_date