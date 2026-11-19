-- Initial staging model for the sales source.
-- The local Parquet path will be configured separately.

select
    *
from read_parquet(
    '{{ env_var("SALES_PARQUET_PATH") }}'
)
