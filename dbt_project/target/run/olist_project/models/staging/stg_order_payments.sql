
  create view "olist"."analytics_staging"."stg_order_payments__dbt_tmp"
    
    
  as (
    

SELECT
    order_id,
    payment_type,
    payment_value
FROM "olist"."public"."order_payments"
  );