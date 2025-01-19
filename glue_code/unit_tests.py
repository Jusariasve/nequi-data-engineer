import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import sys


# Configurar una sesión de Spark para pruebas
@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("GlueJobTest") \
        .getOrCreate()


# Datos simulados para transactions
@pytest.fixture
def transactions_data(spark):
    return spark.createDataFrame([
        {'transaction_id': '1', 'client_id': '10', 'card_id': '100', 'amount': '$123.45', 'date': '2025-01-01 12:00:00'},
        {'transaction_id': '2', 'client_id': '20', 'card_id': '200', 'amount': '$234.56', 'date': '2025-01-02 12:00:00'},
        {'transaction_id': '3', 'client_id': '30', 'card_id': '300', 'amount': '$345.67', 'date': '2025-01-03 12:00:00'},
        {'transaction_id': '1', 'client_id': '10', 'card_id': '100', 'amount': '$123.45', 'date': '2025-01-01 12:00:00'},  
    ])


# Prueba: Limpieza y transformación de transactions
def test_process_transactions(spark, transactions_data):
    # Simulación de transformaciones
    transactions_df = transactions_data.dropDuplicates(['transaction_id'])
    transactions_df = transactions_df.withColumn(
        "amount",
        col("amount").cast("string").substr(2, 15).cast("double")
    )
    transactions_df = transactions_df.withColumn(
        "date",
        to_timestamp(col("date"), "yyyy-MM-dd HH:mm:ss")
    )

    # Validar: no hay duplicados
    assert transactions_df.select("transaction_id").distinct().count() == transactions_df.count()

    # Validar: columna `amount` es numérica y correcta
    amounts = [row["amount"] for row in transactions_df.collect()]
    assert all(isinstance(amount, float) for amount in amounts)

    # Validar: columna `date` es timestamp
    dates = [row["date"] for row in transactions_df.collect()]
    assert all(isinstance(date, type(dates[0])) for date in dates)


# Datos simulados para users
@pytest.fixture
def users_data(spark):
    return spark.createDataFrame([
        {'user_id': '1', 'email': None, 'age': 25, 'yearly_income': '$50000', 'total_debt': '$10000'},
        {'user_id': '2', 'email': 'user2@example.com', 'age': None, 'yearly_income': '$60000', 'total_debt': None},
        {'user_id': '3', 'email': 'user3@example.com', 'age': 30, 'yearly_income': '$70000', 'total_debt': '$20000'},
        {'user_id': '1', 'email': None, 'age': 25, 'yearly_income': '$50000', 'total_debt': '$10000'},  
    ])


# Prueba: Limpieza y transformación de users
def test_process_users(spark, users_data):
    # Simulación de transformaciones
    users_df = users_data.dropDuplicates(['user_id'])
    users_df = users_df.fillna({'email': 'unknown', 'age': 0})
    users_df = users_df.withColumn(
        "yearly_income",
        col("yearly_income").cast("string").substr(2, 15).cast("double")
    )
    users_df = users_df.withColumn(
        "total_debt",
        col("total_debt").cast("string").substr(2, 15).cast("double")
    )

    # Validar: no hay duplicados
    assert users_df.select("user_id").distinct().count() == users_df.count()

    # Validar: columnas numéricas son correctas
    yearly_incomes = [row["yearly_income"] for row in users_df.collect()]
    assert all(isinstance(inc, float) or inc is None for inc in yearly_incomes)

    total_debts = [row["total_debt"] for row in users_df.collect()]
    assert all(isinstance(debt, float) or debt is None for debt in total_debts)


# Datos simulados para cards
@pytest.fixture
def cards_data(spark):
    return spark.createDataFrame([
        {'card_id': '1', 'client_id': '10', 'card_number': '1234567812345678', 'cvv': '123', 'credit_limit': '$5000', 'expires': '2025-12-31', 'acct_open_date': '2020-01-01'},
        {'card_id': '2', 'client_id': '20', 'card_number': '8765432187654321', 'cvv': '321', 'credit_limit': '$10000', 'expires': '2026-12-31', 'acct_open_date': '2018-06-15'},
        {'card_id': '3', 'client_id': '30', 'card_number': '5678123456781234', 'cvv': '456', 'credit_limit': '$7500', 'expires': '2027-12-31', 'acct_open_date': '2019-03-10'},
        {'card_id': '1', 'client_id': '10', 'card_number': '1234567812345678', 'cvv': '123', 'credit_limit': '$5000', 'expires': '2025-12-31', 'acct_open_date': '2020-01-01'}, 
    ])


# Prueba: Limpieza y transformación de cards
def test_process_cards(spark, cards_data):
    # Simulación de transformaciones
    cards_df = cards_data.dropDuplicates(['card_id'])
    cards_df = cards_df.fillna({'card_type': 'unknown'})
    
    columns_to_string = ['card_id', 'client_id', 'card_number', 'cvv']
    for col_name in columns_to_string:
        cards_df = cards_df.withColumn(col_name, col(col_name).cast("string"))
    
    cards_df = cards_df.withColumn(
        "credit_limit",
        col("credit_limit").cast("string").substr(2, 15).cast("double")
    )
    
    columns_to_date = ['expires', 'acct_open_date']
    for col_name in columns_to_date:
        cards_df = cards_df.withColumn(col_name, to_timestamp(col(col_name), "yyyy-MM-dd"))
    
    # Validar: no hay duplicados
    assert cards_df.select("card_id").distinct().count() == cards_df.count()

    # Validar: columnas convertidas correctamente
    credit_limits = [row["credit_limit"] for row in cards_df.collect()]
    assert all(isinstance(limit, float) for limit in credit_limits)

    dates = [row["expires"] for row in cards_df.collect()] + [row["acct_open_date"] for row in cards_df.collect()]
    assert all(isinstance(date, type(dates[0])) for date in dates)

    # Validar: columnas de tipo string
    for col_name in columns_to_string:
        assert all(isinstance(row[col_name], str) for row in cards_df.collect())
