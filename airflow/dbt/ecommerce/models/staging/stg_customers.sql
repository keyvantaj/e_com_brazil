
{{ config(
    materialized = 'view',
    schema = 'staging'
) }}

with raw_customers as (

    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    from {{ source('raw', 'customers') }}

),

renamed as (

    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix as zip_code_prefix,
        lower(customer_city) as city,
        upper(customer_state) as state
    from raw_customers

)

select * from renamed