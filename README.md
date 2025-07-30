# End-To-End-Data-Engineering-ETL-Pipeline-Project-Azure-Databricks-Spark-UnityCatalog

$${\color{red}Color \space Yellow \space Red}$$

## *A. Project Overview:*
This project demonstrates the design, development, & implementation of a robust, scalable & fully automated end-to-end data engineering ETL pipeline built on **Microsoft Azure and Databricks**. The pipeline processes raw data (parquet files), transforms it through a **Medallion Architecture (Bronze, Silver & Gold Layers)**, and prepares it for analytical consumption, which can ultimately connect to Power BI for business reporting.

## *B. Architecture Diagram:*
Below is the high-level architecture diagram of data pipeline, illustrating the flow of data from ingestion to consumption across various Azure & Databricks services.

![AzureDatabricksArchitecture_Big](https://github.com/user-attachments/assets/9b6a26cf-6ae0-4383-8326-11e6257fbe1b)


This diagram clearly outlines the key components. I have specifically highlighted the **Medallion Architecture** and the integration points between **Azure Data Factory, Delta Lake, Databricks, Unity Catalog, and Synapse Analytics.** 

## *C. Key Technologies Used:*

#### *1. Azure Data Lake Storage Gen2 (ADLS Gen2):* 
This serves as the scalable & secure foundation for our data lakehouse. Its hierarchical namespace and cost-effective **storage were crucial for housing all data layers (raw, processed, & curated), and handling large volumes of diverse data.** 

#### *2. Azure Data Factory (ADF):* 
As a primary orchestration tool, $${\color{yellow}ADF \space was \space instrumental \space in \space automating \space the \space data \space ingestion \space process}$$. It allows the creation of robust pipelines to effectively move raw data from source locations into ADLS Gen2, ensuring reliable and scheduled data loading.

#### *3. Azure Databricks:* 
This powerful, **cloud-based Apache Spark analytics platform was central to our data transformation efforts**. It provided the compute power & collaborative environment necessary to execute complex **data processing logic on massive datasets, from cleaning to aggregation.**

#### *4. Delta Lake:* 
Implemented as storage format across our Silver & Gold layers, Delta Lake brought critical reliability features to our data lake. Its ACID properties (Atomicity, Consistency, Isolation, Durability) ensured **data integrity, while features like schema enforcement and time travel capabilities simplified schema management & enabled robust error recovery.**

#### *5. Delta Live Tables (DLT):* 
A declarative framework **significantly streamlined the development & maintenance of the ETL pipelines on Databricks**. DLT allowed me to define transformations with simple Python/SQL syntax. automatically managing dependencies, error handling, and incremental data updates, thereby ensuring the reliability and testability of data flow.

#### *6. Medallion Architecture:* 
This logical layering strategy (Bronze, Silver & Gold layers) is fundamental to organizing and refining our data. It provided a structured approach to progressively improve data quality, apply transformations, & prepare data for specific analytical use cases, promoting data governance & reusability.

#### *7. Azure Synapse Analytics (SQL Pool):* 
This service was used to provide a highly efficient and cost-effective query endpoint over the curated Gold layer data stored in ADLS Gen2. It allowed for direct SQL querying of large datasets without provisioning dedicated resources, making the data easily accessible for downstream applications and Power BI for business reporting. 

#### 8. *Power BI:* 
This business intelligence tool was used for interactive data visualization and reporting, serving as the final consumption layer. Notably, I leveraged the Power BI connector available through the Databricks marketplace to establish a seamless and optimized connection to the curated Gold layer tables. This enabled easy sharing of the Power BI extension file with analysts, allowing them to connect directly and build insightful dashboards and business reports on top of the high-quality data.

## *D. Data Ingestion & Storage (Source to Bronze Layer):*
The initial phase of the pipeline focuses on efficiently ingesting raw data from source into a raw data zone within Azure Data Lake Storage Gen2, forming our Bronze layer.

#### 1. *Raw Data Source:*
My project utilized the following transactional data, provided as Parquet files:

    customers.parquet

    products.parquet

    orders.parquet

    regions.parquet

These files were initially placed in a designated source container within our Azure Storage Account.

![SourceContainers](https://github.com/user-attachments/assets/36b1d0f6-eb52-4b33-a5a1-7081516ee6a8)

#### 2. *Azure Data Lake Storage Gen2 Setup:*
Azure Data Lake Storage Gen2 serves as the backbone of our data lakehouse, providing a highly scalable and secure storage solution for all data layers.

    Resource Group: RG_Databricks_ETL_Pipeline_Project

    Storage Account: databricksetldatastorage

    Containers Created: source, bronze, silver, gold (for Medallion Architecture layers), and a logs container.

![ResourceGroup](https://github.com/user-attachments/assets/3f51d3af-e4ed-4308-bfbe-9f955f366a85)


![ADLSGen2_Containers](https://github.com/user-attachments/assets/8f0bbf90-5351-4989-993c-d42ea6e791c2)

#### 3. *Data Ingestion with ADF:*
Azure Data Factory (ADF) was orchestrated to automate the process of moving the raw Parquet files from the source container into the bronze container within ADLS Gen2. This ensures an immutable copy of the raw data is retained.

Key ADF Activities:

    Copy Data Activity: Used to perform the direct transfer of files.

    Linked Services: Configured to connect ADF to the ADLS Gen2 storage account.


![UnityCatalog](https://github.com/user-attachments/assets/7dc9ad22-ebb4-4e37-af8e-b6f15167db69)


#### 3. *Bronze Layer: Landing Zone:*
This layer stores raw data in ADLS Gen 2, in its original, untransformed state, exactly as it was received from the source. Bronze layer acts as an immutable history record, crucial for auditing & reprocessing if needed.

```
Location: abfss://bronze@databricksetldatastorage.dfs.core.windows.net/

Data Format: Raw Parquet files (same as source).

Characteristics: Schema-on-read, no data transformations applied yet.
```

![Bronze_Containers](https://github.com/user-attachments/assets/825a3af9-fbae-417c-a552-a86849f5e109)

**Data Streaming (Reading) from Source containers using parameters** 

![BronzeLayer_Code1](https://github.com/user-attachments/assets/401bd4e5-1b69-4bc1-8604-0c2a0636caf6)

**Data Streaming (Writing) to Bronze Layer containers for each file as parameters**

![BronzeLayer_Code2](https://github.com/user-attachments/assets/6cb1fa5d-9eef-4498-b833-ffcaefd5a781)


## *E. Data Transformation with Databricks (Bronze to Silver):*
This stage involves leveraging Azure Databricks to process the raw data from the Bronze layer, applying initial cleansing and standardization, and storing the result in the Silver layer as Delta Lake tables.

#### *1. Azure Databricks Setup & Connectivity:*
```
Azure Databricks Workspace: databricks

Access Connector: databricks_datalake_connector
```
This connector ensures secure & seamless access for Databricks (as shown in the architecture figure)

![DatabricksAccessConnector](https://github.com/user-attachments/assets/42778ec1-9ad3-43a8-8832-2096c35ccee3)


#### *2. Silver Layer: Cleansing & Conforming:*
The Silver layer is where data from the Bronze layer undergoes initial transformations to become clean, conformed, and ready for further integration. This involved:

**Retrieving Files from Bronze to Silver Layer**

<img width="796" height="110" alt="image" src="https://github.com/user-attachments/assets/3e74d9e6-8a19-4b59-83c8-3d76b6fabdff" />

**Dropping unnecessary col**

<img width="360" height="66" alt="image" src="https://github.com/user-attachments/assets/531e6742-2e85-476e-922a-74980fbd7cb7" />

**Filtering top three domains**

<img width="598" height="316" alt="image" src="https://github.com/user-attachments/assets/f416931e-958c-4b70-b643-87b35e47e387" />

**Concatenation of First & Last Names**

<img width="795" height="127" alt="image" src="https://github.com/user-attachments/assets/83164bd7-0e28-4cb6-818b-6caefc6a2769" />

**OUTPUT**

![SilverCustomers_TableView](https://github.com/user-attachments/assets/8bc80a9f-7118-4966-adb5-ab7b7646650b)


#### *3. Silver Layer: Delta Lake Tables (CUSTOMERS):*
The output of our Bronze to Silver transformations is Delta Lake tables stored in the silver container. Delta Lake provides ACID properties, schema enforcement, and time travel capabilities, making the Silver layer reliable and queryable.

```
Location: abfss://silver@databricksetldatastorage.dfs.core.windows.net/

Data Format: Delta Lake tables.

Characteristics: Schema enforced, cleaned, and conformed.
```

![Silver_Containers](https://github.com/user-attachments/assets/a0ed5b4b-f01d-4cba-93eb-ebf530cb9a42)


![SilverCatalog](https://github.com/user-attachments/assets/e0f0b0ed-f6c8-4d68-9b71-d0f2a4452540)

#### 4. *Silver Layer: Delta Lake Tables (PRODUCTS):* 
Here need to give every detail for the Products file (from Silver to Gold layer)

#### *5. Silver Layer: Delta Lake Tables (ORDERS):* 
Here need to give every detail for the Orders file (from Silver to Gold layer}

## *F. Data Transformation with Databricks (Bronze to Silver):*
This crucial stage focuses on transforming the cleaned Silver layer data into a highly optimized, business-ready format – specifically, a Star Schema for analytical querying.

#### *1. Gold Layer: Star Schema Design:*

For this project, I designed a star schema to provide an intuitive and high-performance model for business intelligence. This involved creating dimension tables that describe entities (DimCustomerKey, DimProductKey) and fact tables that record measurements/events (FactOrders).

**Example Star Schema (based on Parquet files):**

- Dimension Tables:
  ```
    DimCustomerKey: customer_id
    DimProductKey:  product_id
  ```

- Fact Table:
  ```
    FactOrders = order_id, customer_id, product_id, order_date, etc.
  ```

#### *2. Building Gold Layer with Delta Live Tables (CUSTOMERS):*
Using Delta Live Tables to build and maintain the Gold layer tables. DLT pipelines automatically handle dependencies, error handling, and incremental data processing, ensuring that our analytical data is always up-to-date.














