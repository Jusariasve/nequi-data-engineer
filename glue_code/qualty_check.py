from pyspark.sql import SparkSession

# Inicialización de Spark
spark = SparkSession.builder.appName("ETL_Quality_Checks").getOrCreate()

# Rutas de las capas de datos
processed_path = "s3://your-bucket-name/processed/"

# Función para validar duplicados
def check_duplicates(df, unique_columns, table_name):
    duplicates = df.groupBy(unique_columns).count().filter("count > 1").count()
    if duplicates > 0:
        print(f"ERROR: La tabla {table_name} contiene {duplicates} filas duplicadas.")
    else:
        print(f"SUCCESS: La tabla {table_name} no contiene duplicados.")

# Función para validar nulos en columnas obligatorias
def check_nulls(df, required_columns, table_name):
    for column in required_columns:
        null_count = df.filter(df[column].isNull()).count()
        if null_count > 0:
            print(f"ERROR: La columna {column} en la tabla {table_name} contiene {null_count} valores nulos.")
        else:
            print(f"SUCCESS: La columna {column} en la tabla {table_name} no contiene valores nulos.")

# Leer y validar datos procesados
transactions_df = spark.read.parquet(f"{processed_path}/transactions/")
users_df = spark.read.parquet(f"{processed_path}/users/")
cards_df = spark.read.parquet(f"{processed_path}/cards/")

check_duplicates(transactions_df, ["transaction_id"], "transactions")
check_duplicates(users_df, ["user_id"], "users")
check_duplicates(cards_df, ["card_id"], "cards")

check_nulls(transactions_df, ["transaction_id", "user_id", "amount"], "transactions")
check_nulls(users_df, ["user_id", "email"], "users")
check_nulls(cards_df, ["card_id", "card_type"], "cards")

spark.stop()
