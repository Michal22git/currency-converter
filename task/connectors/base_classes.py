from abc import ABC, abstractmethod
from typing import Any


class RateProvider(ABC):
    @abstractmethod
    def get_rate(self, currency: str) -> tuple[float, str] | None:
        """
        Retrieves the exchange rate for the specified currency.

        Args:
            currency (str): The currency code in ISO 4217 format.

        Returns:
            tuple[float, str] | None: A tuple containing the exchange rate and date or None if not found.
        """
        pass


class DatabaseConnector(ABC):
    @abstractmethod
    def save(self, entity: dict[str, Any]) -> int:
        """
        Saves the given entity to the appropriate database and returns the record ID.

        Args:
            entity (Dict[str, Any]): A dictionary representing the entity to be saved.

        Returns:
            int: The ID of the saved record.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[dict[str, Any]]:
        """
        Retrieves all records from the database.

        Returns:
            list[dict[str, Any]]: List of dictionaries which represent records.
        """
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> dict[str, Any] | None:
        """
        Retrieves an entity by its ID from the database.

        Args:
            id (int): The ID of the entity to retrieve.

        Returns:
            dict[str, Any] | None: A dictionary representing the entity or None if not found.
        """
        pass
