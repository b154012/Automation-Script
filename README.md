# Automation-Script
The scripts are open-source for educational purposes, and do not involve in any confidential data. The scripts are written during the course of my employment in the event of the 2nd COVID wave at EVYD Technology Sdn Bhd.

There are 3 scripts that have been developed to process and automate data processing. It includes obtaining real-time swab datasets from the database at MOH , Brunei, which will be ingesting into the EVYD database; retrieving Entry Travel Permit datasets using Rest API through Remote Desktop Connection protocol; and performing data cleansing on medical datasets which are required to be cleaned for further checked at EVYDresearch system. In addition, crontab is used to help automate the process of running the script without running a command, for example for swab data extration.

Below are the descriptions of each file for its functionalities:-

1. Swab Data Extraction.py - It retrieves all swab info using SparkSQL, then compresses the data into parquet and finally, sends it using the following library such as email.mime.multipart to support the transferring of parquet data.

2. parquet_to_csv.py - Since outlook does not support receiving attachments which are over 50 mb in size, this script allows the conversion of parquet into csv.

3. config.json - The information required to be used by swab_data_extration.py for transfering files and attachments.

4. ETP Data Extraction.py - It collects entry travel permit datasets using Rest API, which requires the following info such as grant_type, client_id, content-type, access_token, expires_in and authorization. This is to fufill the execution of extracting data via Remote Desktop Protocol by signing in and then opening a terminal to access a remote database. The script has to be run in Remote Desktop Protocol.

5. data_transformation.py - It transforms medical datasets which can be used in EVYDresearch. There are several issues found in the datasets such as replacing string data into numerical values, changing the format of the data in specified columns of the respective datasets, removing particular words in the records and making it NaN instead, seperating two records in one line and converting specific values in its respective categories.
