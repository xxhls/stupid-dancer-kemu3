import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

NPY_PATH = "./data_zipped.npy"

data = np.load(NPY_PATH)

origins = [
    "http://127.0.0.1:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    """
    连通性测试
    """
    return {"data": "OK"}


@app.get("/data")
def get_data():
    """
    查询数据细节
    """
    if data is None:
        raise HTTPException(status_code=404, detail="The data was not loaded.")
    total, row, col = data.shape
    if total <= 0 or row <= 0 or col <= 0:
        raise HTTPException(status_code=404, detail="The data was empty.")
    return {"data": {
        "total": total,
        "row": row,
        "col": col
    }}


@app.get("/data/{data_index}")
def get_data_by_index(data_index: int):
    """
    分页查询数据
    """
    total, row, col = data.shape
    if data_index < 0 or data_index >= total:
        raise HTTPException(status_code=404, detail="The index is out of bounds.")
    return {"data": data[data_index].tolist()}
