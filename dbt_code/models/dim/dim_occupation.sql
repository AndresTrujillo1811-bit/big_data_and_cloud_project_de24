with src_occupation as (
    select
        occupation,
        occupation_group,
        occupation_field
    from {{ ref('src_occupation') }}
    where occupation is not null
),

agg as (
    select
        occupation,
        max(occupation_group) as occupation_group,
        max(occupation_field) as occupation_field
    from src_occupation
    group by occupation
)

select
    {{ dbt_utils.generate_surrogate_key(['occupation']) }} as occupation_id,
    occupation,
    occupation_group,
    occupation_field
from agg
