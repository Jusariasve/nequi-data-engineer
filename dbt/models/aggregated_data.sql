WITH transactions AS (
    SELECT *
    FROM {{ ref('transactions') }}
),
users AS (
    SELECT *
    FROM {{ ref('users') }}
),
cards AS (
    SELECT *
    FROM {{ ref('cards') }}
),
combined_data AS (
    SELECT
        t.transaction_id,
        t.amount,
        t.transaction_date,
        u.user_id,
        u.name AS user_name,
        u.email,
        u.yearly_income,
        c.card_id,
        c.credit_limit,
        c.card_type
    FROM transactions t
    INNER JOIN users u
        ON t.client_id = u.user_id
    INNER JOIN cards c
        ON t.card_id = c.card_id
)

SELECT * FROM combined_data;
