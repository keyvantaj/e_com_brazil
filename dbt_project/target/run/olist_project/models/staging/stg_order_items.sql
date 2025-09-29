
  create view "olist"."analytics_staging"."stg_order_items__dbt_tmp"
    
    
  as (
    

SELECT
    order_id,
    product_id,
    seller_id,
    price,
    freight_value
FROM "olist"."public"."order_items"
  );