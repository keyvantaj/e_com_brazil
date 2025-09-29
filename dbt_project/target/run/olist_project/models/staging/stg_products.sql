
  create view "olist"."analytics_staging"."stg_products__dbt_tmp"
    
    
  as (
    

SELECT
    product_id,
    product_category_name,
    product_name_length,
    product_description_length,
    product_photos_qty
FROM "olist"."public"."products"
  );