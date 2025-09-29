{{ config(schema='staging') }}

SELECT
    order_id,
    product_id,
    seller_id,
    price,
    freight_value
FROM {{ source('olist', 'order_items') }}