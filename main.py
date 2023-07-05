import compair
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
import requests
import numpy as np

app = FastAPI()
find_similar = compair.FindSimilar()


@app.post("/")
async def upload_file(file: UploadFile = File(...), postid_count: int = 5):
    a = requests.request("POST", "http://192.168.110.45:4050/", headers={}, data={},
                         files=[('file', (file.filename, file.file, 'image/jpeg'))])
    vec = np.array(a.json(), dtype=np.float32)
    my_dict = {"similar_posts": find_similar.similar_postid(vec, postid_count)}
    return my_dict


@app.post("/find_exact_similar")
async def upload_file(file: UploadFile = File(...), postid_count: int = 5):
    a = requests.request("POST", "http://192.168.110.45:4050/", headers={}, data={},
                         files=[('file', (file.filename, file.file, 'image/jpeg'))])
    vec = np.array(a.json(), dtype=np.float32)
    my_dict = {"similar_posts": find_similar.similar_postid_exact(vec, postid_count)}
    return my_dict


@app.get("/")
async def read_index():
    return FileResponse('index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4040)
