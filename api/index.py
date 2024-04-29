from fastapi import FastAPI

app = FastAPI()

@app.route('/',methods=["GET"])
def read_root():
    return {"Hello": "World"}
