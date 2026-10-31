SELECT COUNT(*) As total_customers From credit_risk;
SELECT sum(loan_amnt) As total_loan_amount From credit_risk;
SELECT ROUND(AVG(person_income), 2) AS average_income FROM credit_risk;


-- 4. Average Interest Rate
SELECT ROUND(AVG(loan_int_rate), 2) AS average_interest_rate
FROM credit_risk;

-- 5. Total Default Customers
SELECT COUNT(*) AS default_customers
FROM credit_risk
WHERE loan_status = 1;

-- 6. Total Non-Default Customers
SELECT COUNT(*) AS non_default_customers
FROM credit_risk
WHERE loan_status = 0;

-- 7. Overall Default Rate
SELECT
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS default_rate_percentage
FROM credit_risk;

-- 8. Loan Amount by Loan Grade
SELECT
    loan_grade,
    SUM(loan_amnt) AS total_loan_amount
FROM credit_risk
GROUP BY loan_grade
ORDER BY total_loan_amount DESC;

-- 9. Customer Distribution by Loan Purpose
SELECT
    loan_intent,
    COUNT(*) AS total_customers
FROM credit_risk
GROUP BY loan_intent
ORDER BY total_customers DESC;

-- 10. Default Customers by Loan Grade
SELECT
    loan_grade,
    COUNT(*) AS default_customers
FROM credit_risk
WHERE loan_status = 1
GROUP BY loan_grade
ORDER BY default_customers DESC;
