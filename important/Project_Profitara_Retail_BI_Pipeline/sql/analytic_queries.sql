-- =============================================================================
-- PROFITARA ANALYTICAL SQL LAYER (DuckDB & PostgreSQL Compatible)
-- =============================================================================
-- Author: Senior Analytics Engineer & Data Scientist
-- Database: profitara.duckdb
-- Tables Queried: india_orders, real_transactions, customer_segments,
--                 clv_predictions, winback_targets, association_rules
-- =============================================================================

-- =============================================================================
-- QUERY 1: Monthly Cohort Retention Matrix
-- Business Goal: Measure what percentage of customers acquired in each signup
-- month return to place an order in subsequent months (Months 0 to 11).
-- =============================================================================
WITH customer_first_order AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM india_orders
    GROUP BY customer_id
),
customer_orders AS (
    SELECT 
        o.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS order_month,
        DATEDIFF('month', c.cohort_month, DATE_TRUNC('month', o.order_date)) AS month_number
    FROM india_orders o
    JOIN customer_first_order c ON o.customer_id = c.customer_id
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_order
    GROUP BY cohort_month
),
retention_counts AS (
    SELECT 
        c.cohort_month,
        c.month_number,
        COUNT(DISTINCT c.customer_id) AS active_customers
    FROM customer_orders c
    GROUP BY c.cohort_month, c.month_number
)
SELECT 
    STRFTIME(r.cohort_month, '%Y-%m') AS cohort,
    s.cohort_size,
    r.month_number,
    r.active_customers,
    ROUND((r.active_customers * 100.0) / s.cohort_size, 2) AS retention_pct
FROM retention_counts r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
WHERE r.month_number <= 11
ORDER BY cohort, month_number;


-- =============================================================================
-- QUERY 2: Quarterly Signup Cohort Repeat Purchase Rate
-- Business Goal: Determine the conversion rate from 1-time to multi-order buyers
-- across acquisition quarters.
-- =============================================================================
WITH customer_orders_summary AS (
    SELECT 
        customer_id,
        DATE_TRUNC('quarter', MIN(order_date)) AS acquisition_quarter,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS total_spend
    FROM india_orders
    GROUP BY customer_id
)
SELECT 
    CONCAT(CAST(EXTRACT('year' FROM acquisition_quarter) AS VARCHAR), '-Q', CAST(EXTRACT('quarter' FROM acquisition_quarter) AS VARCHAR)) AS signup_quarter,
    COUNT(customer_id) AS total_acquired_customers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) AS repeat_buyers,
    ROUND(SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(customer_id), 2) AS repeat_rate_pct,
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer,
    ROUND(AVG(total_spend), 2) AS avg_customer_spend
FROM customer_orders_summary
GROUP BY acquisition_quarter
ORDER BY signup_quarter;


-- =============================================================================
-- QUERY 3: Pareto 80/20 Customer Revenue Concentration
-- Business Goal: Quantify customer concentration by computing cumulative revenue
-- share across descending spend percentiles.
-- =============================================================================
WITH customer_spend AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders
    FROM india_orders
    GROUP BY customer_id, customer_name
),
spend_ranked AS (
    SELECT 
        customer_id,
        customer_name,
        total_revenue,
        total_orders,
        ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS spend_rank,
        COUNT(*) OVER () AS total_customers,
        SUM(total_revenue) OVER () AS grand_total_revenue,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue
    FROM customer_spend
)
SELECT 
    spend_rank,
    customer_id,
    customer_name,
    total_revenue,
    ROUND(spend_rank * 100.0 / total_customers, 2) AS customer_percentile,
    ROUND(running_revenue * 100.0 / grand_total_revenue, 2) AS cumulative_revenue_pct
FROM spend_ranked
WHERE spend_rank <= 20 OR spend_rank % 100 = 0
ORDER BY spend_rank;


-- =============================================================================
-- QUERY 4: RFM Segment Revenue Share & Unit Economics
-- Business Goal: Profile the 4 behavioral segments identified by K-Means on the
-- real retail dataset (revenue share, AOV, frequency, recency).
-- =============================================================================
SELECT 
    segment_name,
    COUNT(customerid) AS customer_count,
    ROUND(COUNT(customerid) * 100.0 / SUM(COUNT(customerid)) OVER (), 2) AS customer_share_pct,
    ROUND(SUM(monetary), 2) AS segment_revenue,
    ROUND(SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER (), 2) AS revenue_share_pct,
    ROUND(AVG(monetary), 2) AS avg_spend_per_customer,
    ROUND(AVG(frequency), 2) AS avg_order_frequency,
    ROUND(AVG(recency), 1) AS avg_recency_days
FROM customer_segments
GROUP BY segment_name
ORDER BY segment_revenue DESC;


-- =============================================================================
-- QUERY 5: Month-over-Month (MoM) Revenue Growth & Margin Trend
-- Business Goal: Use LAG() window function to calculate sequential monthly
-- revenue growth and net margin shifts.
-- =============================================================================
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS order_month,
        ROUND(SUM(sales), 2) AS monthly_revenue,
        ROUND(SUM(profit), 2) AS monthly_profit,
        COUNT(DISTINCT order_id) AS order_count
    FROM india_orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    STRFTIME(order_month, '%Y-%m') AS month,
    monthly_revenue,
    monthly_profit,
    ROUND(monthly_profit / NULLIF(monthly_revenue, 0) * 100, 2) AS margin_pct,
    order_count,
    LAG(monthly_revenue, 1) OVER (ORDER BY order_month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY order_month)) 
        * 100.0 / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY order_month), 0), 2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY month;


-- =============================================================================
-- QUERY 6: Moving 30-Day Trailing Revenue Window
-- Business Goal: Calculate 30-day moving average of daily sales to smooth out
-- weekly demand spikes and seasonality.
-- =============================================================================
WITH daily_sales AS (
    SELECT 
        CAST(order_date AS DATE) AS sale_date,
        ROUND(SUM(sales), 2) AS daily_revenue,
        COUNT(DISTINCT order_id) AS daily_orders
    FROM india_orders
    GROUP BY CAST(order_date AS DATE)
)
SELECT 
    sale_date,
    daily_revenue,
    daily_orders,
    ROUND(
        AVG(daily_revenue) OVER (
            ORDER BY sale_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 2
    ) AS moving_avg_30d_revenue,
    ROUND(
        SUM(daily_revenue) OVER (
            ORDER BY sale_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 2
    ) AS trailing_30d_revenue_sum
FROM daily_sales
ORDER BY sale_date DESC
LIMIT 60;


-- =============================================================================
-- QUERY 7: Customer Churn Risk Exposure
-- Business Goal: Identify customers inactive for >90 days, quantifying total
-- historical revenue at stake per segment.
-- =============================================================================
WITH latest_date AS (
    SELECT MAX(order_date) AS max_date FROM india_orders
),
customer_recency AS (
    SELECT 
        o.customer_id,
        o.customer_name,
        o.segment,
        o.city,
        DATEDIFF('day', MAX(o.order_date), (SELECT max_date FROM latest_date)) AS days_since_last_order,
        COUNT(DISTINCT o.order_id) AS lifetime_orders,
        ROUND(SUM(o.sales), 2) AS lifetime_revenue
    FROM india_orders o
    GROUP BY o.customer_id, o.customer_name, o.segment, o.city
)
SELECT 
    segment,
    COUNT(customer_id) AS at_risk_customers_count,
    ROUND(AVG(days_since_last_order), 1) AS avg_inactivity_days,
    ROUND(SUM(lifetime_revenue), 2) AS total_revenue_at_risk,
    ROUND(AVG(lifetime_revenue), 2) AS avg_customer_revenue_at_risk
FROM customer_recency
WHERE days_since_last_order > 90
GROUP BY segment
ORDER BY total_revenue_at_risk DESC;


-- =============================================================================
-- QUERY 8: Category Margin Decay by Discount Band
-- Business Goal: Identify structurally unprofitable discount tiers across
-- categories to flag margin erosion.
-- =============================================================================
WITH discounted_orders AS (
    SELECT 
        category,
        sub_category,
        sales,
        profit,
        CASE 
            WHEN discount = 0 THEN '0% (Full Price)'
            WHEN discount <= 0.10 THEN '1-10%'
            WHEN discount <= 0.20 THEN '11-20%'
            WHEN discount <= 0.30 THEN '21-30%'
            ELSE '31%+' 
        END AS discount_band
    FROM india_orders
)
SELECT 
    category,
    discount_band,
    COUNT(*) AS order_line_items,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS net_margin_pct
FROM discounted_orders
GROUP BY category, discount_band
ORDER BY category, discount_band;


-- =============================================================================
-- QUERY 9: Priority Win-Back Action Queue (from Decision Engine)
-- Business Goal: Retrieve the top 15 churned candidates ranked by expected net
-- recovery value for CRM direct action.
-- =============================================================================
SELECT 
    customerid,
    ROUND(prob_churn * 100, 1) AS churn_probability_pct,
    ROUND(pred_clv, 2) AS predicted_future_spend_gbp,
    ROUND(expected_gross_recovery, 2) AS expected_gross_recovery_gbp,
    ROUND(expected_net_value, 2) AS expected_net_value_gbp
FROM winback_targets
ORDER BY expected_net_value DESC
LIMIT 15;


-- =============================================================================
-- QUERY 10: Quick-Commerce Delivery Speed Performance & Unit Economics
-- Business Goal: Compare order volume, sales, and profit margin across delivery
-- SLA modes (Instant 10-15 min vs Express 30-60 min vs Scheduled Slot).
-- =============================================================================
SELECT 
    ship_mode AS delivery_sla,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(COUNT(DISTINCT order_id) * 100.0 / SUM(COUNT(DISTINCT order_id)) OVER (), 2) AS order_share_pct,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM india_orders
GROUP BY ship_mode
ORDER BY total_revenue DESC;


-- =============================================================================
-- QUERY 11: Regional Performance & DENSE_RANK() by State Revenue
-- Business Goal: Rank states by revenue contribution while evaluating regional
-- margin consistency.
-- =============================================================================
SELECT 
    state,
    region,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS state_revenue,
    ROUND(SUM(profit), 2) AS state_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS state_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(sales) DESC) AS revenue_rank
FROM india_orders
GROUP BY state, region
ORDER BY revenue_rank
LIMIT 15;
