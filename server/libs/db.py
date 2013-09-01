# coding: utf8

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

_db = None

_POOL_SIZE = 5
_POOL_RECYCLE = 3600


def get_db(db_url, debug=False):
    global _db
    if _db and str(_db.url) == db_url:
        return _db
    _db = create_engine(db_url, echo=debug,
                        pool_size=_POOL_SIZE, pool_recycle=_POOL_RECYCLE)
    return _db


def get_db_session(database_uri):
    global _db
    if not _db or str(_db.url) != database_uri:
        _db = get_db(database_uri)
    db_session = scoped_session(sessionmaker(bind=_db, autocommit=False,
                                             autoflush=False))
    return db_session