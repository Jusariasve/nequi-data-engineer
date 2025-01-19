WITH cleaned_data AS (
    SELECT
        id::STRING AS card_id,
        client_id::STRING,
        card_number::STRING,
        cvv::STRING,
        credit_limit::FLOAT,
        CAST(expires AS TIMESTAMP) AS expiration_date,
        CAST(acct_open_date AS TIMESTAMP) AS account_open_date,
        card_type
    FROM {{ source('processed', 'cards') }}
)

SELECT * FROM cleaned_data;
