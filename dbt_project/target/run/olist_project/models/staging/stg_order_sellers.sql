
  create view "olist"."analytics_staging"."stg_order_sellers__dbt_tmp"
    
    
  as (
    

SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city
FROM "olist"."public"."sellers"
  );