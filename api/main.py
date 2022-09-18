from compair import Compair
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
import requests
import numpy as np

app = FastAPI()
sp = Compair()


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    vec = requests.request("POST", "http://192.168.2.10:4050/", headers={}, data={},
                           files=[('file', (file.filename, file.file, 'image/jpeg'))])
    a = np.array(vec.json(), dtype=np.float32)
    my_dict = {"similar_posts": sp.similar_postid(a)}
    return my_dict


@app.get("/")
async def read_index():
    return FileResponse('api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4040)
