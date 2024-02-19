import time

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import schemas
from .database import SessionLocal
from .models import Cliente, Transacao

app = FastAPI()


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post("/clientes/{cliente_id}/transacoes", response_model=schemas.ClienteBase)
async def post_transacao(cliente_id: int, transacao: schemas.TransactionBase, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    try:
        session.add(
            Transacao(**transacao.model_dump(),
                        cliente_id=cliente_id)
        )
        session.commit()
        session.refresh(cliente)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Limite insuficiente")

    return {
        "limite": cliente.limite,
        "saldo": cliente.saldo,
    }


@app.get("/clientes/{id}/extrato")
async def get_extrato(id: int, session: Session = Depends(get_session)):
    client = session.get(Cliente, id)

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transactions = session.execute(
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
