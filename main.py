from fastapi import FastAPI


from routers import request_body


app = FastAPI()


app.include_router(request_body.router, tags=["request body"])

