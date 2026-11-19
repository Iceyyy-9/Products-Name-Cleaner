with source as (

    select *
    from {{ source('sales_data', 'raw_sales') }}

),

renamed as (

    select
        商家名称 as merchant_name,
        设备编号 as device_id,
        设备型号 as device_model,
        设备激活时间 as device_activation_time,
        详细地址 as full_address,
        城市 as city,
        州 as state,
        对应销售 as salesperson,
        预授权金额 as preauthorization_amount,
        订单编号 as order_id,
        订单商品名称 as raw_product_name,
        商品数量 as quantity,
        商品单价 as unit_price,
        商品成本价 as unit_cost,
        合计 as line_total,
        销售税 as sales_tax,
        订单金额 as order_amount,
        实付金额 as paid_amount,
        订单创建时间 as order_created_at,
        订单支付时间 as order_paid_at
    from source

)

select * from renamed
