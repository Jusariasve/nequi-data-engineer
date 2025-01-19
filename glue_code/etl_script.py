import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from pyspark.sql.functions import col, to_timestamp

# Parseando los argumentos
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'RAW_BUCKET', 'PROCESSED_BUCKET'])
raw_bucket = args['RAW_BUCKET']
processed_bucket = args['PROCESSED_BUCKET']

# Inicialización de Glue Context y Job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Función para limpiar y transformar datos
def process_transactions(glueContext, raw_path, processed_path):
    # Leer datos desde la capa raw
    transactions_df = glueContext.create_dynamic_frame.from_options(
        connection_type='s3',
        connection_options={'paths': [f's3://{raw_path}/transactions/']},
        format='parquet'
    )
    
    # Convertir a DataFrame de Spark para manipulación avanzada
    transactions_df = transactions_df.toDF()
    
    # Limpieza y transformación
    transactions_df = transactions_df.dropDuplicates(['transaction_id'])
    transactions_df = transactions_df.fillna({'amount': 0.0})

    columns_to_string = ['id', 'client_id', 'card_id', 'merchant_id', 'mcc']
    for col_name in columns_to_string:
        transactions_df = transactions_df.withColumn(col_name, col(col_name).cast("string"))

    transactions_df = transactions_df.withColumn(
        "amount",
        col("amount").cast("string").substr(2, 15).cast("double")
    )

    transactions_df = transactions_df.withColumn(
        "date",
        to_timestamp(col("date"), "yyyy-MM-dd HH:mm:ss")
    )
    
    # Escribir datos en la capa processed
    transactions_dynamic_df = DynamicFrame.fromDF(transactions_df, glueContext, 'transactions_dynamic_df')
    glueContext.write_dynamic_frame.from_options(
        frame=transactions_dynamic_df,
        connection_type='s3',
        connection_options={'path': f's3://{processed_path}/transactions/'},
        format='parquet'
    )

def process_users(glueContext, raw_path, processed_path):
    # Leer datos desde la capa raw
    users_df = glueContext.create_dynamic_frame.from_options(
        connection_type='s3',
        connection_options={'paths': [f's3://{raw_path}/users/']},
        format='parquet'
    )
    
    # Convertir a DataFrame de Spark para manipulación avanzada
    users_df = users_df.toDF()
    
    # Limpieza y transformación
    users_df = users_df.dropDuplicates(['user_id'])
    users_df = users_df.fillna({'age': 0, 'email': 'unknown'})

    users_df = users_df.withColumn('id', col('id').cast("string"))

    columns_to_int = [
        'per_capita_income',
        'yearly_income',
        'total_debt',
    ]
    for col in columns_to_int:
        users_df = users_df.withColumn(
            col,
            col(col).cast("string").substr(2, 15).cast("double")
        )

    
    # Escribir datos en la capa processed
    users_dynamic_df = DynamicFrame.fromDF(users_df, glueContext, 'users_dynamic_df')
    glueContext.write_dynamic_frame.from_options(
        frame=users_dynamic_df,
        connection_type='s3',
        connection_options={'path': f's3://{processed_path}/users/'},
        format='parquet'
    )

def process_cards(glueContext, raw_path, processed_path):
    # Leer datos desde la capa raw
    cards_df = glueContext.create_dynamic_frame.from_options(
        connection_type='s3',
        connection_options={'paths': [f's3://{raw_path}/cards/']},
        format='parquet'
    )
    
    # Convertir a DataFrame de Spark para manipulación avanzada
    cards_df = cards_df.toDF()
    
    # Limpieza y transformación
    cards_df = cards_df.dropDuplicates(['card_id'])
    cards_df = cards_df.fillna({'card_type': 'unknown'})

    columns_to_string = ['id', 'client_id', 'card_number', 'cvv']
    for col_name in columns_to_string:
        cards_df = cards_df.withColumn(col_name, col(col_name).cast("string"))

    cards_df = cards_df.withColumn(
        "credit_limit",
        col("credit_limit").cast("string").substr(2, 15).cast("double")
    )

    columns_to_date = ['expires','acct_open_date']
    for col_name in columns_to_date:
        cards_df = cards_df.withColumn(col_name, to_timestamp(col("date"), "yyyy-MM-dd HH:mm:ss"))
    
    # Escribir datos en la capa processed
    cards_dynamic_df = DynamicFrame.fromDF(cards_df, glueContext, 'cards_dynamic_df')
    glueContext.write_dynamic_frame.from_options(
        frame=cards_dynamic_df,
        connection_type='s3',
        connection_options={'path': f's3://{processed_path}/cards/'},
        format='parquet'
    )

# Procesar cada tabla
process_transactions(glueContext, raw_bucket, processed_bucket)
process_users(glueContext, raw_bucket, processed_bucket)
process_cards(glueContext, raw_bucket, processed_bucket)


# Finalizar el trabajo
job.commit()
