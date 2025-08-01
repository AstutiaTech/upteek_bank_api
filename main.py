from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import sys, traceback


from routers.authentication import auth
from routers import dashboard
from routers.user import profile
from routers.misc import geo
from routers.misc import merch
from routers.accounting import gl_type
from routers.accounting import gl
from routers.accounting import product
from routers.accounting import cust_acct
from routers.transaction import type
from routers.transaction import postings
from routers.user import main as user_main
from routers.loan import apply as loan_applications
from routers.loan import post as loans
from routers.deposit import fixed as fixed_deposits

# Main app section here
app = FastAPI(title="Upteek Bank")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dashboard.router)
app.include_router(geo.router)
app.include_router(merch.router)
app.include_router(gl_type.router)
app.include_router(gl.router)
app.include_router(product.router)
app.include_router(cust_acct.router)
app.include_router(type.router)
app.include_router(postings.router)
app.include_router(user_main.router)
app.include_router(loan_applications.router)
app.include_router(loans.router)
app.include_router(fixed_deposits.router)

#Test routers
# app.include_router(external.router)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        return response
    except Exception as e:
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        print(err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(err)}))


app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World! Upteek Bank"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, "url": request.base_url}),
    )

add_pagination(app)