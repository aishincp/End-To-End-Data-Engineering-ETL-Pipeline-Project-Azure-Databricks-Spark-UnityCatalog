# Databricks notebook source
# MAGIC %md
# MAGIC # **Fact Orders Table**

# COMMAND ----------

# MAGIC %md
# MAGIC Data Reading

# COMMAND ----------

# MAGIC %md
# MAGIC ### In Fact Tables -> only put dimension keys & numeric values

# COMMAND ----------

df = spark.sql("select * from databricks_etl_catalog.silver.orders_silver")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Replacing columns 'customer_id' & 'product_id' with DimCustomerKey

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from databricks_etl_catalog.gold.dimcustomers

# COMMAND ----------

# MAGIC %md
# MAGIC #### As this table was created using DLT so some columns are named by DLT such as _START_AT & _END_AT, which are basically the create_date & update_date. Also here below the product_id would be the DimProductKey"

# COMMAND ----------

# MAGIC %sql  
# MAGIC select * from databricks_etl_catalog.gold.dimproducts

# COMMAND ----------

df_dim_customers = spark.sql("select DimCustomerKey, customer_id as DimCustomerID from databricks_etl_catalog.gold.dimcustomers")

df_dim_products = spark.sql("select product_id as DimProductKey from databricks_etl_catalog.gold.dimproducts")

# COMMAND ----------

df_dim_customers.display()

# COMMAND ----------

df_dim_products.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **Fact Dataframe**

# COMMAND ----------

df_fact = df.join(df_dim_customers, df.customer_id == df_dim_customers.DimCustomerID, how="left").join(df_dim_products, df.product_id == df_dim_products.DimProductKey, how="left")

df_fact.display()


# COMMAND ----------

df_fact_new = df_fact.drop('customer_id', 'product_id', 'DimCustomerID')

# COMMAND ----------

df_fact_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC # **Upserting this Fact Table to Gold Layer**

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

if spark.catalog.tableExists("databricks_etl_catalog.gold.FactOrders"):
  dlt_obj = DeltaTable.forName(spark, "databricks_etl_catalog.gold.FactOrders")

  dlt_obj.alias("trg").merge(df_fact_new.alias("src"), "trg.order_id = src.order_id AND trg.DimCustomerKey = src.DimCustomerKey AND trg.DimProductKey = src.DimProductKey")\
              .whenMatchedUpdateAll()\
              .whenNotMatchedInsertAll()\
                .execute()
else:
  df_fact_new.write.format("delta")\
              .option("path", "abfss://gold@databricksetldatastorage.dfs.core.windows.net/FactOrders")\
              .saveAsTable("databricks_etl_catalog.gold.FactOrders")


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from databricks_etl_catalog.gold.FactOrders

# COMMAND ----------

