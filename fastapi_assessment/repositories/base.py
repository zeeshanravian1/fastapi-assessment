"""
Base Repository

Description:
- This module contains shared repository used by all repositories.

"""

from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.connection import BaseTable

Model = TypeVar("Model", bound=BaseTable)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseRepository(
    Generic[
        Model,
        CreateSchema,
        UpdateSchema,
    ]
):
    """
    Base Repository

    Description:
    - This class contains shared repository used by all repositories.
    - This is used to perform CRUD operations.

    """

    def __init__(self, model: Type[Model]) -> None:
        """
        Base Repository Constructor

        Description:
        - This is used to initialize base repository.

        Args:
        - `model (Model)`: Model object. **(Required)**

        Returns:
        - `None`

        """

        self.model: type[Model] = model

    def create(self, db_session: Session, entity: CreateSchema) -> Model:
        """
        Create Entity

        Description:
        - This method is used to create a single entity.

        Args:
        - `db_session (Session)`: Database session. **(Required)**
        - `entity (self.model)`: Entity object. **(Required)**

        Returns:
        - `entity (Model)`: Entity object.

        """

        db_instance: Model = self.model(**entity.model_dump())

        db_session.add(instance=db_instance)
        db_session.commit()
        db_session.refresh(instance=db_instance)

        return db_instance

    def read_by_id(self, db_session: Session, entity_id: int) -> Model | None:
        """
        Read Entity by ID

        Description:
        - This method is used to read entity by ID.

        Args:
        - `entity_id` (int): Entity ID. **(Required)**

        Returns:
        - `entity` (Model): Entity object.

        """

        return db_session.get(entity=self.model, ident=entity_id)

    def read_by_column(
        self, db_session: Session, entity_column, entity_value
    ) -> Model | None:
        """
        Read Entity by Column

        Description:
        - This method is used to read entity by column.

        Args:
        - `entity_column` (str): Entity column. **(Required)**
        - `entity_value` (str): Entity value. **(Required)**

        Returns:
        - `entity` (Model): Entity object.

        """

        return (
            db_session.query(self.model)
            .filter_by(**{entity_column: entity_value})
            .first()
        )

    def read_all(self, db_session: Session) -> list[Model]:
        """
        Read All Entities

        Description:
        - This method is used to read all entities.

        Args:
        - `db_session (Session)`: Database session. **(Required)**

        Returns:
        - `entities`: List of entity objects.

        """

        return db_session.query(self.model).all()

    def update(
        self, db_session: Session, entity_id: int, entity: UpdateSchema
    ) -> Model | None:
        """
        Update Entity

        Description:
        - This method is used to update entity.

        Args:
        - `db_session (Session)`: Database session. **(Required)**
        - `entity_id` (int): Entity ID. **(Required)**
        - `entity (self.model)`: Entity object. **(Required)**

        Returns:
        - `entity` (Model): Entity object.

        """

        db_instance: Model | None = self.read_by_id(
            db_session=db_session, entity_id=entity_id
        )

        if not db_instance:
            return None

        for key, value in entity.model_dump().items():
            setattr(db_instance, key, value)

        db_session.commit()
        db_session.refresh(instance=db_instance)

        return db_instance

    def delete(self, db_session: Session, entity_id: int) -> Model | None:
        """
        Delete Entity

        Description:
        - This method is used to delete entity.

        Args:
        - `db_session (Session)`: Database session. **(Required)**
        - `entity_id` (int): Entity ID. **(Required)**

        Returns:
        - `entity` (Model): Entity object.

        """

        db_instance: Model | None = self.read_by_id(
            db_session=db_session, entity_id=entity_id
        )

        if not db_instance:
            return None

        db_session.delete(instance=db_instance)
        db_session.commit()

        return db_instance
