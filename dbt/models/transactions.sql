WITH cleaned_data AS (
    SELECT
        id::STRING AS transaction_id,
        client_id::STRING,
        card_id::STRING,
        merchant_id::STRING,
        mcc::STRING,
        amount::FLOAT,
        CAST(date AS TIMESTAMP) AS transaction_date
    FROM {{ source('processed', 'transactions') }}
)

SELECT * FROM cleaned_data;
