from pyspark.sql import SparkSession
from parameter import *


## 1. CREATE SPARKSESSION 
def create_sparksession():
    spark = SparkSession.builder \
            .master("local[1]") \
            .appName("ETL SPARK TO GCS") \
            .config("spark.jars", "D:\Spark\jdbc\gcs-connector-hadoop2-latest.jar,D:\Spark\jdbc\ojdbc8.jar,D:\Spark\jdbc\postgresql-42.6.0.jar") \
            .getOrCreate()
    spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
    spark._jsc.hadoopConfiguration().set('fs.gs.auth.service.account.enable', 'true')
    spark._jsc.hadoopConfiguration().set('google.cloud.auth.service.account.json.keyfile', gcs_key_path)
    
    return spark
# Call spark: 
spark = create_sparksession()

# 2. EXTRACT DATA FROM SOURCE TO DATAFRAME:
# 2.1  FROM LOCAL DISK:
def extract_disk(file_path):
    df_movie_meta = spark.read.csv(file_path,sep = ',', header= True)
    print("already extracted diskfile")
    return df_movie_meta

# 2.2 FROM POSTGRES:
def extract_postgre():
    df_state = spark.read.format('jdbc') \
                    .option("url", url) \
                    .option("query", query_postgres) \
                    .option("user", user) \
                    .option("password", password) \
                    .option("driver", driver) \
                    .load()
    print("already extracted state data")
    return df_state

# 2.3 FROM ORACLE: 
def extract_oracle():
    df_imgt = spark.read.format('jdbc') \
                    .option("url", url_dw) \
                    .option("query", query_oracle) \
                    .option("user", user_dw) \
                    .option("password", password_dw) \
                    .option("driver", driver_dw) \
                    .load()
    print('already extract df_oracle')
    return df_imgt

# LOAD DF TO GCS:
def load_to_gcs(df_movie_meta,df_state, df_imgt, dest_lake):
    df_list = [df_movie_meta,df_state, df_imgt]
    check = ["df_movie_meta","df_state", "df_imgt"]
    df_list_load = zip(df_list, check)
    for df, name in df_list_load:
        df.write.option("header",True) \
        .mode("append") \
        .csv(dest_lake)
    print(f"already load {name} on to GCS")

# create main function:
def main():
    df_movie_meta = extract_disk(file_path_movie)
    df_state = extract_postgre()
    df_imgt = extract_oracle() 
    load_to_gcs(df_movie_meta,df_state, df_imgt, dest_lake_01)

if __name__ =="__main__":
    main()


