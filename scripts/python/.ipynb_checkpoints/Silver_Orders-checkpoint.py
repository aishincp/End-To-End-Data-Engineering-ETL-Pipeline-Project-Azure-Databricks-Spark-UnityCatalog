# Databricks notebook source
# MAGIC %md
# MAGIC ### Data Processing & Transformation

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window


# COMMAND ----------

df = spark.read.format("parquet")\
  .load("abfss://bronze@databricksetldatastorage.dfs.core.windows.net/orders")
display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df = df.drop('_rescued_data')
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Date Transformation ['Order_Date'] to get TimeStamp

# COMMAND ----------

from pyspark.sql.functions import to_timestamp, col
df = df.withColumn("order_date", to_timestamp(col("order_date")))
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Creating New column to the Orders Data File

# COMMAND ----------

from pyspark.sql.functions import year, month, monthname, dayofmonth, col

df = df.withColumn("year", year(col('order_date')))
df = df.withColumn("month", monthname(col('order_date')))
df = df.withColumn("day", dayofmonth(col('order_date')))
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Display col='Total Amount' (Desc to Asc) according to Year (Desc to Asc)

# COMMAND ----------

df_1 = df.withColumn("flag", dense_rank().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
df_1.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Making diffrence from dense_rank to rank_flag for better flagging

# COMMAND ----------

df1 = df_1.withColumn("rank_flag", rank().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
df1.display()

# COMMAND ----------

df1 = df_1.withColumn("row_flag", row_number().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
df1.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating Class (OOP's Concept) to [reuse](url) Functions Efficiently

# COMMAND ----------

class windows:

  def dense_rank(self, df):
    df_dense_rank = df.withColumn("flag", dense_rank().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
    return df_dense_rank

  def rank(self, df):
    df_rank_flag = df.withColumn("rank_flag", rank().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
    return df_rank_flag

  def row_number(self, df):
    df_row_flag = df.withColumn("row_flag", row_number().over(Window.partitionBy("year").orderBy(col("total_amount").desc())))
    return df_row_flag




# COMMAND ----------

df_new = df
df_new.display()

# COMMAND ----------

object = windows()
df_result = object.dense_rank(df_new)
df_result.display()    

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Writing

# COMMAND ----------

df.write.format("delta").mode("overwrite").save("abfss://silver@databricksetldatastorage.dfs.core.windows.net/orders")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Creating Schema for Silver,  Tables: 'Order'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS databricks_etl_catalog.silver.orders_silver
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@databricksetldatastorage.dfs.core.windows.net/orders'

# COMMAND ----------

# MAGIC %sql
# MAGIC Select * from databricks_etl_catalog.silver.orders_silver