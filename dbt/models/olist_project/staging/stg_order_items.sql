with source as (
    select * from {{ source('raw', 'order_items') }}
),

order_items_stg as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
    from source
)

select * from order_items_stg