## Basic Design:

### 4 layers of encapsulation:

Rest Endpoint( InfluxCore( InfluxDBClient( Http Requests to DB ) ) ) )

InfluxDBClient manages lower level requests with the DB over HTTP. The open source influx python client is wrapped to
allow for use case specific functions.

### Architecture

#### Single Instance

Write: Data file is received by the REST endpoint, data file is parsed and time stamps with associated data are
extracted and written to the relevant bucket in influx db. There db and web server have a one to one relationship.

Read: Queries are passed received by the REST endpoint and passed directly to the db for execution, data is structured
into a dictionary that can be converted into a dataframe.

Performance: Optimal for small low read and write volumes.

#### Multi instance

Write: Similar to the single instance design accept parsed data is written across all databases  
in the cluster (write mirroring).

Read: Handled the same way as the single instance design accept data can be requested from any db.

Performance: Low write throughput but extremely high read throughput. 