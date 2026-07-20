-- Example analytical queries for portfolio

-- 1. Performance: last close per asset
SELECT ticker, date, close_price
FROM fact_prices
WHERE (ticker, date) IN (
  SELECT ticker, MAX(date) FROM fact_prices GROUP BY ticker
);

-- 2. Monthly average close price
SELECT 
  d.year_month,
  f.ticker,
  AVG(f.close_price) as avg_close
FROM fact_prices f
JOIN dim_calendar d ON f.date = d.date
GROUP BY d.year_month, f.ticker
ORDER BY d.year_month;

-- 3. Cumulative return vs IBOVESPA
WITH base AS (
  SELECT ticker, MIN(date) as first_date FROM fact_prices GROUP BY ticker
),
first_price AS (
  SELECT f.ticker, f.close_price as base_price
  FROM fact_prices f JOIN base b ON f.ticker=b.ticker AND f.date=b.first_date
)
SELECT 
  f.date,
  f.ticker,
  (f.close_price / fp.base_price - 1) * 100 as cumulative_return_pct
FROM fact_prices f
JOIN first_price fp ON f.ticker = fp.ticker
ORDER BY f.ticker, f.date;

-- 4. Join with asset dimension for sector analysis
SELECT 
  a.sector,
  COUNT(DISTINCT f.ticker) as num_assets,
  AVG(f.close_price) as avg_price
FROM fact_prices f
JOIN dim_asset a ON f.ticker = a.ticker
GROUP BY a.sector;