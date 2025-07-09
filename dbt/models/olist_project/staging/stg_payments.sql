with source as (
    select * from {{ source('raw', 'order_payments') }}
),

order_payments_stg as (
    select
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
    from source
)

select * from order_payments_stg