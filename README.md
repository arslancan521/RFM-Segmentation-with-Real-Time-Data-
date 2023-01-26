# RFM-Segmentation-with-Real-Time-Data-
RFM Segmentation with real time data using kafka on docker and storing the data in database

In this project, steps are following below:
- The real time customer transaction data is created randomly by using python
- These data is sent to the kafka via docker
- Then the data is read from the kafka
- After that the RFM segmentation processes are applied to the data
- A database and table are created by using sqlalchemy
- Then the transaction data and its segment are inserted to the table in the database

The data flow process is repeated constantly.
