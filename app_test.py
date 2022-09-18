from api.compair import Compair
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
import requests
import numpy as np
from selenium import webdriver

PATH = "C:\chromedriver.exe"
app = FastAPI()
sp = Compair()


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    vec = requests.request("POST", "http://127.0.0.1:4050/", headers={}, data={},
                           files=[('file', (file.filename, file.file, 'image/jpeg'))])
    c = np.array(vec.json(), dtype=np.float32)
    # my_dict = {"similar_posts": sp.similar_postid(a)}
    # return my_dict
    driver = webdriver.Chrome(PATH)
    hel = {}
    b = sp.similar_postid(c)
    for j, i in enumerate(b):
        driver.get(f"https://www.kukala.ir/product/{i}")
        a = input("Would you like to save it? ")
        if a == 'y':
            hel[i] = input("your comments: ")
        if a == 'break':
            break
        if a == "undo":
            driver.get(f"https://www.kukala.ir/product/{b[j - 1]}")
            c = input("Would you like to save it? ")
            if c == 'y':
                hel[b[j - 1]] = input("your comments: ")
    return {"bugs": hel}


@app.get("/")
async def read_index():
    return FileResponse('api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
