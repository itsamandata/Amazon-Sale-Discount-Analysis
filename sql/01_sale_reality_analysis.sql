-- ==============================================================================
-- PROJECT: Amazon & Flipkart Big Sale Discount Reality Check
-- AUTHOR: Aman (itsamandata)
-- PURPOSE: Analyze pricing manipulation, genuine vs artificial discounts, 
--          and identify product quality traps during major e-commerce sales.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. OVERVIEW & TABLE SCHEMA PREVIEW
-- ------------------------------------------------------------------------------
SELECT *
FROM ecommerce_sales
LIMIT 10;


-- ------------------------------------------------------------------------------
-- 2. OVERALL DISCOUNT REALITY SUMMARY
-- Compare Advertised Discount (MRP based) vs Real Discount (30-day Avg based)
-- ------------------------------------------------------------------------------
SELECT 
    platform,
    COUNT(product_id) AS total_products,
    ROUND(AVG(advertised_discount_pct), 2) AS avg_advertised_discount_pct,
    ROUND(AVG(actual_real_discount_pct), 2) AS avg_real_discount_pct,
    ROUND(AVG(discount_inflation_pct), 2) AS avg_discount_inflation_pct
FROM ecommerce_sales
GROUP BY platform;


-- ------------------------------------------------------------------------------
-- 3. DEAL CLASSIFICATION: GENUINE VS ARTIFICIAL VS FAKE MARKUPS
-- How many deals are actually giving real savings vs deceptive marketing?
-- ------------------------------------------------------------------------------
SELECT 
    deal_type,
    COUNT(product_id) AS product_count,
    ROUND(COUNT(product_id) * 100.0 / (SELECT COUNT(*) FROM ecommerce_sales), 2) AS percentage_of_total_catalog,
    ROUND(AVG(advertised_discount_pct), 2) AS avg_advertised_discount,
    ROUND(AVG(actual_real_discount_pct), 2) AS avg_real_discount,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
    ROUND(AVG(return_rate_pct), 2) AS avg_return_rate_pct
FROM ecommerce_sales
GROUP BY deal_type
ORDER BY product_count DESC;


-- ------------------------------------------------------------------------------
-- 4. CATEGORY BREAKDOWN: WHERE ARE THE BEST & WORST DEALS?
-- Which categories provide true savings vs the highest discount inflation?
-- ------------------------------------------------------------------------------
SELECT 
    category,
    COUNT(product_id) AS total_items,
    ROUND(AVG(mrp_inr), 0) AS avg_mrp,
    ROUND(AVG(sale_price_inr), 0) AS avg_sale_price,
    ROUND(AVG(advertised_discount_pct), 2) AS avg_advertised_discount_pct,
    ROUND(AVG(actual_real_discount_pct), 2) AS avg_real_discount_pct,
    ROUND(AVG(discount_inflation_pct), 2) AS avg_inflation_gap
FROM ecommerce_sales
GROUP BY category
ORDER BY avg_real_discount_pct DESC;


-- ------------------------------------------------------------------------------
-- 5. THE "DISCOUNT TRAP": PRODUCTS WITH HUGE DISCOUNTS BUT POOR RATINGS
-- High advertised discount (>= 40%) but low customer rating (< 3.5) & high return rate
-- ------------------------------------------------------------------------------
SELECT 
    product_id,
    product_name,
    category,
    platform,
    mrp_inr,
    sale_price_inr,
    advertised_discount_pct,
    actual_real_discount_pct,
    customer_rating,
    return_rate_pct
FROM ecommerce_sales
WHERE advertised_discount_pct >= 40 
  AND customer_rating < 3.5
  AND return_rate_pct > 15.0
ORDER BY return_rate_pct DESC
LIMIT 20;


-- ------------------------------------------------------------------------------
-- 6. TOP 10 BEST VALUE PRODUCTS (GENUINE SAVINGS & TOP RATINGS)
-- True discount > 20%, Customer Rating >= 4.5, Return Rate < 6%
-- ------------------------------------------------------------------------------
SELECT 
    product_name,
    category,
    sub_category,
    regular_price_30d_avg,
    sale_price_inr,
    (regular_price_30d_avg - sale_price_inr) AS net_rupee_savings,
    actual_real_discount_pct,
    customer_rating,
    review_count
FROM ecommerce_sales
WHERE actual_real_discount_pct >= 20.0
  AND customer_rating >= 4.5
  AND return_rate_pct <= 6.0
ORDER BY net_rupee_savings DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- 7. ADVANCED WINDOW FUNCTION: RANKING TOP VALUE DEALS PER CATEGORY
-- Using DENSE_RANK() to find the #1 best deal in each category
-- ------------------------------------------------------------------------------
WITH RankedDeals AS (
    SELECT 
        category,
        product_name,
        regular_price_30d_avg,
        sale_price_inr,
        actual_real_discount_pct,
        customer_rating,
        DENSE_RANK() OVER (
            PARTITION BY category 
            ORDER BY actual_real_discount_pct DESC, customer_rating DESC
        ) as category_rank
    FROM ecommerce_sales
    WHERE deal_type = 'Genuine Deal'
)
SELECT 
    category,
    product_name,
    regular_price_30d_avg,
    sale_price_inr,
    actual_real_discount_pct,
    customer_rating
FROM RankedDeals
WHERE category_rank <= 3
ORDER BY category, category_rank;
