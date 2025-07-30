# End-To-End-Data-Engineering-ETL-Pipeline-Project-Azure-Databricks-Spark-UnityCatalog

$${\color{red}Color \space Yellow \space Red}$$

## *A. Project Overview:*
This project demonstrates the design, development, & implementation of a robust, scalable & fully automated end-to-end data engineering ETL pipeline built on **Microsoft Azure and Databricks**. The pipeline processes raw data (parquet files), transforms it through a **Medallion Architecture (Bronze, Silver & Gold Layers)**, and prepares it for analytical consumption, which can ultimately connect to Power BI for business reporting.

## *B. Architecture Diagram:*
Below is the high-level architecture diagram of data pipeline, illustrating the flow of data from ingestion to consumption acroos various Azure & Databricks services.

![AzureDatabricksArchitecture_Big](https://github.com/user-attachments/assets/9b6a26cf-6ae0-4383-8326-11e6257fbe1b)


This diagram clearly outlines the key components. I have specifically highlighted the **Medallion Architecture** and the integration points between **Azure Data Factory, Delta Lake, Databricks, Unity Catalog, and Synapse Analytics.** 

## *C. Key Technologies Used:*

#### *1. Azure Data Lake Storage Gen2 (ADLS Gen2):* 
This serves as the scalable & secure foundation for our data lakehouse. Its hierarchical namespace and cost-effective **storage were crucial for housing all data layers (raw, processed, & curated), and handling large volumes of diverse data.** 

#### *2. Azure Data Factory (ADF):* 
As primary orchestration tool, $${\color{yellow}ADF \space was \space instrumental \space in \space automating \space the \space data \space ingestion \space process}$$. It allows creation of robust pipelines to effectively move raw data from source locations into ADLS Gen2, ensuring reliable and scheduled data loading.

#### *3. Azure Databricks:* 
This powerful, **cloud-based Apache Spark analytics platform was central to our data transformation efforts**. It provided the compute power & collaborative environment necessary to execute complex **data processing logi on massive datasets, from cleaning to aggregation.**

#### *4. Delta Lake:* 
Implemented as storage format across our Silver & Gold layers, Delta Lake brought critical reliability features to our data lake. Its ACID properties (Atomicity, Consistency, Isolation, Durability) ensured **data integrity, while features like schema enforcement and time travel capabiulities simplified schema management & enabled robust error recovery.**

#### *5. Delta Live Tables (DLT):* 
A declarative framework **significantly streamlined the development & maintenance of the ETL pipelines on Databricks**. DLT allowed me to define transformations with simple Python/SQL syntax. automatically managing dependencies, error handling, and incremental data updates, thereby ensuring the reliability and testability of data flow.

#### *6. Medallion Architecture:* 
This logical layering strategy (Bronze, Silver & Gold) layers is a fundamental to organizing and refining our data. It provided a structured approach to progressively improve data quality, apply transformations, & prepare data for specific analytical use cases, promoting data governance & reusability.

#### *7. Azure Synapse Analytics (SQL Pool):* 
This service was used to provide highly efficient and cost-effective query endpoint over the curated Gold layer data stored in ADLS Gen2. It allowed for direct SQL querying of large datasets without provisioning dedicated resources, making the data easily accessible for downstream applications and Power BI for business reporting. 

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




