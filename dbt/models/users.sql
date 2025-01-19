WITH cleaned_data AS (
    SELECT
        id::STRING AS user_id,
        name,
        email,
        age::INT,
        per_capita_income::FLOAT,
        yearly_income::FLOAT,
        total_debt::FLOAT
    FROM {{ source('processed', 'users') }}
)

SELECT * FROM cleaned_data;
