from sqlalchemy import Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class Cat(Base):
    __tablename__ = "cat"
    __table_args__ = {"schema": "cat8rat"}

    id = mapped_column(Integer, primary_key=True, index=True)
    birth_date = mapped_column(Date, nullable=False)
    paws_quantity = mapped_column(Integer, nullable=False)
    name = mapped_column(String, nullable=False)
    gender = mapped_column(String(1), nullable=False)
    tails_quantity = mapped_column(Integer, nullable=False)

   # rats = relationship("Rat", back_populates="cat") todo make relationships work



class Rat(Base):
    __tablename__ = "rat"
    __table_args__ = {"schema": "cat8rat"}

    id = mapped_column(Integer, primary_key=True, index=True)
    birth_date = mapped_column(Date, nullable=False)
    courage = mapped_column(Integer, nullable=False)
    stupidity = mapped_column(Integer, nullable=False)
    is_eaten = mapped_column(Boolean, default=False)
    cat_id = mapped_column(Integer, ForeignKey('Cat.id'), nullable=True)

    # cat = relationship("Cat", back_populates="rats")
