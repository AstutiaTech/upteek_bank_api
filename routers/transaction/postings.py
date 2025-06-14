from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.postings.trans import retrieve_accounts, create_general_posting, retrieve_transactions, retrieve_transaction_by_id
from database.schema import ErrorResponse, PlainResponse, CreatePostingModel, TransactionAccountModel, TransactionModel, TransactionResponseModel, NewTransactionResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("/search_accounts/{search}", response_model=List[TransactionAccountModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search_accounts(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), search: str = None):
    return retrieve_accounts(db=db, search=search)

@router.post("/general_posting", response_model=NewTransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def general_posting(request: Request, fields: CreatePostingModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_general_posting(db=db, transaction_type_id=fields.transaction_type_id, from_account_number=fields.from_account_number, to_account_number=fields.to_account_number, amount=fields.amount, narration=fields.narration)
    if req is None:
        raise HTTPException(status_code=404, detail={'status': False, 'message': 'Posting failed', 'data': None})
    if req['status'] is False:
        raise HTTPException(status_code=404, detail=req)
    return req

@router.get("/", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), user_id: int = 0, merchant_id: int = 0, type_id: int = 0, action: int = 0, reference: str = None, external_reference: str = None, account_number: str = None, account_name: str = None, from_date: str = None, to_date: str = None, status: int = 0):
    filters = {}
    if user_id is not None:
        if  user_id > 0:
            filters['user_id'] = user_id
    if merchant_id is not None:
        if  merchant_id > 0:
            filters['merchant_id'] = merchant_id
    if type_id is not None:
        if  type_id > 0:
            filters['type_id'] = type_id
    if action is not None:
        if  action > 0:
            filters['action'] = action
    if reference is not None:
        filters['reference'] = reference
    if external_reference is not None:
        filters['external_reference'] = external_reference
    if account_number is not None:
        filters['account_number'] = account_number
    if account_name is not None:
        filters['account_name'] = account_name
    if from_date is not None:
        filters['from_date'] = from_date
    if to_date is not None:
        filters['to_date'] = to_date
    if status is not None:
        if  status > 0:
            filters['status'] = status
    return retrieve_transactions(db=db, filters=filters)

@router.get("/get_single/{transaction_id}", response_model=TransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), transaction_id: int = 0):
    return retrieve_transaction_by_id(db=db, transaction_id=transaction_id)
