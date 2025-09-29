{{ config(schema='analytics') }}

SELECT
    p.product_category_name,
    SUM(op.payment_value) AS total_sales,
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_order_payments') }} op
  ON oi.order_id = op.order_id
JOIN {{ ref('stg_products') }} p
  ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC