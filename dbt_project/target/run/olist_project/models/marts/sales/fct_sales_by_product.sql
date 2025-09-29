
  
    

  create  table "olist"."analytics_analytics"."fct_sales_by_product__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    p.product_category_name,
    SUM(op.payment_value) AS total_sales,
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM "olist"."analytics_staging"."stg_order_items" oi
JOIN "olist"."analytics_staging"."stg_order_payments" op
  ON oi.order_id = op.order_id
JOIN "olist"."analytics_staging"."stg_products" p
  ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC
  );
  