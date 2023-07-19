# path of file on local disk
file_path_movie = "D:\DE\A_PROJECT_LIST/3_DW_Movies\data_source\movies_metadata.csv"

# connect to postgres:
dbname = "Immigration"
user = "postgres"
password = "postgres"
server = "localhost"
port = "5432"
url = f"jdbc:postgresql://{server}:{port}/{dbname}"
driver = "org.postgresql.Driver"
# query postgres:
query_postgres = " select * from db_state"

#----------------------------------------------------------------------------------------
# connect to Oracle:

dbname_dw = "Immigration"
table_dw_port = "TM_PORT_D"
user_dw = "c##odi_demo"
password_dw = "welcome"
server_dw = "127.0.0.1"
port_dw = 1521
service_name_dw = "ORCL"
url_dw = f"jdbc:oracle:thin:@{server_dw}:{port_dw}:{service_name_dw}"
driver_dw = "oracle.jdbc.OracleDriver"

# query oracle:
query_oracle = "select * from TM_VISA_D"

# GCS KEY:
gcs_key_path = "D:\DE\key_connect_GCP\key_conn_gcp_2.json"
dest_lake_01 = "gs://movies_project_hien_v2/Data_lake"
