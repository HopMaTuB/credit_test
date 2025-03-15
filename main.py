from fastapi import FastAPI
from src.routes import credit_router,plans_inserts
import uvicorn


app = FastAPI()


app.include_router(credit_router)
app.include_router(plans_inserts)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)