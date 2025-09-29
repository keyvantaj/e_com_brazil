{{ config(schema='staging') }}

SELECT
    order_id,
    payment_type,
    payment_value
FROM {{ source('olist', 'order_payments') }}