import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask import Flask
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


async def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite+aiosqlite:///./{db_file.strip()}"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_async_engine(conn_str, echo=True)
    __factory = async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    from . import __all_models

    async with async_session() as session:
        async with engine.begin() as conn:
            await conn.run_sync(SqlAlchemyBase.metadata.create_all)


def create_session() -> Session:
    global __factory
    return __factory
