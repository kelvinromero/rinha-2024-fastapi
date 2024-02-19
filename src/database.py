from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql://admin:123@db/rinha"

# Engine é uma fábrica de conexões, ele guarda as conexões numa pool
# para serem reutilizadas rapidamente.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Precisamos definir as tabelas do banco
# E precisamos definir classes que mapeam as tabelas do banco
# Essa classe base permite ao SQLAlchemy ter um catalogo de classes
# que mapeiam as tabelas do banco
# Geralmente só se tem uma. Também é importante saber que o SQLAlchemy
# não presume nada, e você precisará cada detalhe nas suas classes de modelo.
class Base(DeclarativeBase):
    pass

# Session solicita uma conexão à pool de conexões (engine)
# quando é solicita uma query ou uma persistência
# Estabelece uma transação na conexão até que faça o commit ou rollback
# Quando conclui, liberar a conexão de volta para a pool
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Sources:
# https://docs.sqlalchemy.org/en/14/orm/quickstart.html