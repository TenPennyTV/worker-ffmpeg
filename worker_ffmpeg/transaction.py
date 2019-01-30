# -*- coding: utf-8 -*-
from .db import session


class Transaction(object):

    def __init__(self, tx):
        """
        :type tx: sqlalchemy.orm.session.Session
        """
        self.tx = tx

    def __enter__(self):
        """
        :rtype: sqlalchemy.orm.session.Session
        """
        return self.tx

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_type is not None:
            self.rollback()
        self.commit()

    def rollback(self):
        try:
            self.tx.rollback()
        finally:
            self.tx.close()

    def commit(self):
        try:
            self.tx.commit()
        finally:
            self.tx.close()


class TxManager(object):

    def __init__(self, session):
        """
        :type engine: sqlalchemy.orm.session.Session
        """
        self.session = session

    def begin(self):
        """
        :rtype: Transaction
        """
        return Transaction(self.session)


tx_manager = TxManager(session)
