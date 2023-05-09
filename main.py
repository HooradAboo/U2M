'''
    pip install uvicorn
    uvicorn main:app --reload --host 0.0.0.0
    lsof -i :8000
    kill -9 
'''

from fastapi import Request, FastAPI

app = FastAPI()

@app.post("/")
async def get_body(request: Request):
    if request.body:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8")
        print(body_str)
        return body_str
    else:
        return "No request body found"
    