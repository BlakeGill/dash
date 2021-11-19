from fastapi import FastAPI, UploadFile, File, Form

from sync.api import InfluxAPI

"""
upload_file
path: /api/{device}/upload/datafile 
"""

app = FastAPI()
api = InfluxAPI()


@app.route("/")
async def landing():
    pass


@app.get("/api/config/nodes")
def get_influx_nodes():
    """End point for listing influx nodes
    """
    return api.get_influx_nodes()


@app.post("/api/config/add/node")
def add_influx_node(node: str = Form(...)):
    """End point for appending influx.
    """
    return api.add_influx_node(node)


@app.post("/api/{bucket}/{asset}/upload/datafile")
def create_upload_file(bucket: str, asset: str, file: UploadFile = File(...)):
    """
    End point for file upload
    """
    return api.ingest_data_file(bucket, asset, file)


@app.post("/api/query")
def create_query(query: str = Form(...)):
    """
    End point for data query
    """
    return api.send_raw_query(query)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
