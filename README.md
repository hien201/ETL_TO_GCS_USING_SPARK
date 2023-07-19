## Load csv file from source( local disk, postgreSQL, Oracle) to GCS using Spark 
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


### Tạo và cấu hình SparkSession:
Điều quan trọn là sparksession phải kết nối được với GCS, PostgreSQL và oracle. Tôi thực hiện như sau:
![image](https://github.com/hien201/ETL_TO_GCS_USING_SPARK/assets/90466915/f538fbc0-defe-4864-a046-b582829f734e)

    spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
    spark._jsc.hadoopConfiguration().set('fs.gs.auth.service.account.enable', 'true')
    spark._jsc.hadoopConfiguration().set('google.cloud.auth.service.account.json.keyfile', gcs_key_path)

  
