WITH 
    fct_table AS (SELECT * FROM {{ ref('fct_table') }}),
    dim_employer AS (SELECT * FROM {{ ref('dim_employer') }}),
    dim_auxilliary AS (SELECT * FROM {{ ref('dim_auxilliary_attributes') }}),
    dim_job_details AS (SELECT * FROM {{ ref('dim_job_details') }}),
    dim_occupation AS (SELECT * FROM {{ ref('dim_occupation') }})

SELECT
    d_occ.occupation,
    d_occ.occupation_field,
    d_occ.occupation_group,
    dj.headline,
    dj.description,
    dj.employment_type,
    dj.duration,
    dj.salary_type,
    da.experience_required,
    da.access_to_own_car,
    da.driving_license_required,
    de.employer_name,
    de.employer_workplace,
    de.workplace_street_address,
    de.workplace_region,
    de.workplace_city,
    de.workplace_postcode,
    de.workplace_country,
    ft.vacancies,
    ft.application_deadline,
    ft.publication_date
FROM
    fct_table ft
LEFT JOIN dim_employer de ON de.employer_id = ft.employer_id
LEFT JOIN dim_auxilliary da ON da.auxilliary_attribute_id = ft.auxilliary_attribute_id
LEFT JOIN dim_job_details dj ON dj.job_details_id = ft.job_details_id
LEFT JOIN dim_occupation d_occ ON d_occ.occupation_id = ft.occupation_id
WHERE LOWER(d_occ.occupation_field) LIKE '%data%'
   OR LOWER(d_occ.occupation_field) LIKE '%it%'
