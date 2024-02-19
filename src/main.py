import time

import psycopg2.errors
import sqlalchemy
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .async_database import AsyncSessionLocal
from .models import Cliente, Transacao

app = FastAPI()


async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


@app.post("/clientes/{cliente_id}/transacoes", response_model=schemas.ClienteBase)
async def post_transacao(cliente_id: int, transacao: schemas.TransactionBase, session: AsyncSession = Depends(get_session)):
    cliente = await session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    try:
        session.add(
            Transacao(**transacao.model_dump(),
                        cliente_id=cliente_id)
        )
        await session.commit()
        await session.refresh(cliente)
    except DBAPIError as e:
        if isinstance(e.orig, sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.IntegrityError):
            raise HTTPException(status_code=422, detail="Limite insuficiente")
        raise HTTPException(status_code=500, detail="Erro interno")

    return {
        "limite": cliente.limite,
        "saldo": cliente.saldo,
    }


@app.get("/clientes/{id}/extrato")
async def get_extrato(id: int, session: AsyncSession = Depends(get_session)):
    client = await session.get(Cliente, id)

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transactions = await session.execute(
        select(Transacao)
        .where(Transacao.cliente_id == id)
        .order_by(Transacao.id.desc()).limit(10)
    )


    return {
        "saldo": {
            "total": client.saldo,
            "data_extrato": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "limite": client.limite
        },
        "ultimas_transacoes": [
            schemas.Transaction.model_validate(t) for t in transactions.scalars()
        ]
    }
