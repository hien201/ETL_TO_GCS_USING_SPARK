# ETL Pipeline to GCS Using Spark 
### 1. Giới thiệu:
Ngày nay, việc lưu trữ và xử lý không chỉ ở "mặt đất" mà xu thế là đưa chúng "lên mây". 
Trong Repo này tôi sẽ cung cấp ETL đơn giản để upload csv file lên GCS từ các nguồn sau:
* Local Disk
* PostgreSQL
* Oracle
## 2. Yêu cầu:
- Cài đặt spark (pyspark)
- Cài đặt oracle sqldeveloper, PostgeSQL
- Tạo tài khoản Google Cloud
### 3. Kết nối GCS: 
- Đầu tiên, tôi cần tải trình kết nối GCP, truy cập link: https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage#clusters
- Tiếp theo, tạo Service Account và nhận Key connect .json:
  ![image](https://github.com/hien201/ETL_TO_GCS_USING_SPARK/assets/90466915/e52940da-116e-41f9-938b-772a54f27d83)
- Thiết lập môi trường windows qua câu lệnh sau:
      set GOOGLE_APPLICATION_CREDENTIALS="path/to/your/keyfile.json"


### 4. Tạo và cấu hình SparkSession:
Điều quan trọn là sparksession phải kết nối được với GCS, PostgreSQL và oracle. Tôi thực hiện như sau:

def create_sparksession():
    spark = SparkSession.builder \
            .master("local[1]") \
            .appName("ETL SPARK TO GCS") \
            .config("spark.jars", "your_path_file_to_jars_postgres,your_path_file_to_jars_gcs,your_path_file_to_jars_poracle  ") \
            .getOrCreate()
    spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
    spark._jsc.hadoopConfiguration().set('fs.gs.auth.service.account.enable', 'true')
    spark._jsc.hadoopConfiguration().set('google.cloud.auth.service.account.json.keyfile', "your_path_file_to_key)

Trong ví dụ này, tôi thiết lập code như sau:
![image](https://github.com/hien201/ETL_TO_GCS_USING_SPARK/assets/90466915/8b88b24c-0bca-4722-8e76-1db9bab2d302)

==> Bước cấu hình đã xong

### 5. Extract data from source: 
Bây giờ, tôi cần extract dữ liệu từ nguồn, trong ví dụ này tôi sẽ trích xuát từ 3 nguồn sau đó kết quả trả về các  Spark DataFrame: 
##### FROM LOCAL DISK:
def extract_disk(file_path):
    df_movie_meta = spark.read.csv(file_path,sep = ',', header= True)
    print("already extracted diskfile")
    return df_movie_meta

##### FROM POSTGRES:
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

##### FROM ORACLE: 
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

### 6. Load to GCS:
Giờ là bước cuối cùng, tôi thực hiện load các Spark DataFrame đã trích xuất ở phần 5 lên GCS như sau:

def load_to_gcs(df_movie_meta,df_state, df_imgt, dest_lake):
    df_list = [df_movie_meta,df_state, df_imgt]
    check = ["df_movie_meta","df_state", "df_imgt"]
    df_list_load = zip(df_list, check)
    for df, name in df_list_load:
        df.write.option("header",True) \
        .mode("append") \
        .csv(dest_lake)
    print(f"already load {name} on to GCS")

  
Lưu ý: khi sử dụng vòng lặp for, ta cần sử dụng phương thức mode("append")

### 7. Demo kết quả:
Sau khi chạy ETL trên, đây là kết quả tôi thu được:
![image](https://github.com/hien201/ETL_TO_GCS_USING_SPARK/assets/90466915/b47ae5b0-fbec-4219-a956-9774d203c1fa)



  
