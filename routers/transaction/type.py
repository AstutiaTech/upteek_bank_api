from fastapi import APIRouter, Request, Depends, Query
from modules.authentication.auth import auth
from modules.postings.trans_type import create_new_transaction_type, update_existing_transaction_type, delete_existing_transaction_type, retrive_transaction_type, retrieve_single_transaction_type, retrieve_single_transaction_type_by_code
from database.schema import ErrorResponse, PlainResponse, TransactionTypeModel, CreateTransTypeModel, UpdateTransTypeModel, TransTypeResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/transaction_types",
    tags=["transaction_types"]
)

@router.post("/create", response_model=TransTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateTransTypeModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_new_transaction_type(db=db, user_id=user['id'], corresponding_gl_id=fields.corresponding_gl_id, charge_gl_id=fields.charge_gl_id, name=fields.name, description=fields.description, action=fields.action, chargeable=fields.chargeable, charge_type=fields.charge_type, charge_percentage=fields.charge_percentage, charge_flat=fields.charge_flat, require_approval=fields.require_approval, require_approval_amount=fields.require_approval_amount)
    return req

@router.post("/update/{type_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateTransTypeModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), type_id: int=0):
    values = fields.model_dump()
    req = update_existing_transaction_type(db=db, type_id=type_id, values=values)
    return req

@router.get("/delete/{type_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return delete_existing_transaction_type(db=db, type_id=type_id)

@router.get("/", response_model=Page[TransactionTypeModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), name: str = Query(None), code: str = Query(None), action: int = Query(None), chargeable: int = Query(None), charge_type: int = Query(None), require_approval: int = Query(None), is_system: int = Query(None), status: int = Query(None), created_by: int = Query(None)):
    filters = {}
    if action:
        filters['action'] = action
    if name:
        filters['name'] = name
    if code:
        filters['code'] = code
    if status:
        filters['status'] = status
    if created_by:
        filters['created_by'] = created_by
    if chargeable:
        filters['chargeable'] = chargeable
    if charge_type:
        filters['charge_type'] = charge_type
    if require_approval:
        filters['require_approval'] = require_approval
    if is_system:
        filters['is_system'] = is_system
    return retrive_transaction_type(db=db, filters=filters)

@router.get("/get_single/{type_id}", response_model=TransTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return retrieve_single_transaction_type(db=db, type_id=type_id)

@router.get("/get_single_by_code/{code}", response_model=TransTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_by_code(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), code: str = None):
    return retrieve_single_transaction_type_by_code(db=db, code=code)

