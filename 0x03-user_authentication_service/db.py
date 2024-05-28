#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        method that adds new user to database and returns the object
        '''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Receives keyword arguments and returns the first
        user matching all criteria.
        """
        filters = []
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError("Invalid field: {}".format(key))
            filters.append(getattr(User, key) == value)
        query = self._session.query(User).filter(*filters).first()
        if not query:
            raise NoResultFound
        return query

    def update_user(self, user_id, **kwargs) -> None:
        '''
        recievs user id and datat,
        then updated the user at given id
        '''
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            user.key = value
        self.__session.commit()
        return None
