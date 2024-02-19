from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class TransactionTypeEnum(str, Enum):
    credito = 'c'
    debito = 'd'

class TransactionBase(BaseModel):
    valor: int
    tipo: TransactionTypeEnum
    descricao: str = Field(max_length=10, min_length=1)

class TransactionCreate(TransactionBase):
    id: int
    cliente_id: int
    realizada_em: str

class Transaction(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    realizada_em: datetime

class LimiteSaldo(BaseModel):
    limite: int
    saldo: int

class ClienteBase(BaseModel):
    limite: int
    saldo: int

class ClientCreate(ClienteBase):
    id: int

class Client(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
