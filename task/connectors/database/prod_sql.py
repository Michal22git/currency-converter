from typing import Any

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from task.connectors.base_classes import DatabaseConnector

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    price_in_pln = Column(Float, nullable=False)
    date = Column(String, nullable=False)


class SqliteDatabaseConnector(DatabaseConnector):
    def __init__(self, db_url='sqlite:///database.sqlite3') -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save(self, entity: dict[str, Any]) -> int:
        session = self.Session()
        new_entry = CurrencyRate(
            currency=entity['currency'],
            rate=entity['rate'],
            price_in_pln=entity['price_in_pln'],
            date=entity['date']
        )
        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)
        session.close()
        return new_entry.id

    def get_all(self) -> list[dict[str, Any]]:
        session = self.Session()
        results = session.query(CurrencyRate).all()
        session.close()
        return [
            {
                'id': result.id,
                'currency': result.currency,
                'rate': result.rate,
                'price_in_pln': result.price_in_pln,
                'date': result.date
            } for result in results
        ]

    def get_by_id(self, id: int) -> dict[str, Any] | None:
        session = self.Session()
        result = session.query(CurrencyRate).filter_by(id=id).first()
        session.close()
        if result:
            return {
                'id': result.id,
                'currency': result.currency,
                'rate': result.rate,
                'price_in_pln': result.price_in_pln,
                'date': result.date
            }
        return None
