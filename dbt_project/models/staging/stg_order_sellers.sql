{{ config(schema='staging') }}

SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city
FROM {{ source('olist', 'sellers') }}