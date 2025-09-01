# Import necessary libraries and modules
# sqlalchemy creates the relational database where information like usernames, emails, testimonies are stored
# https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, text, Boolean
from flask_sqlalchemy import SQLAlchemy
# The UserMixin class helps to link a database user to a login session
# https://flask-login.readthedocs.io/en/latest/
from flask_login import UserMixin
# The python datetime module
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class UnverifiedUser(UserMixin, db.Model):
    __tablename__ = "unverified users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())
    verification_code: Mapped[int] = mapped_column(Integer(), nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    mail_sent: Mapped[bool] = mapped_column(Boolean(), nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())
    picture_number: Mapped[int] = mapped_column(Integer(), default=0, server_default=text("0"))
    picture_url: Mapped[str] = mapped_column(String(), nullable=True)
    testimonies = relationship("Testimony", back_populates="user")
    items = relationship("Item", back_populates="user")
    cart_products = relationship("CartProduct", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Testimony(UserMixin, db.Model):
    __tablename__ = "testimonies"
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime())
    website: Mapped[str] = mapped_column(String(), nullable=True)
    testimony: Mapped[str] = mapped_column(String())
    is_visible: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=text("false"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="testimonies")


class PasswordChanger(UserMixin, db.Model):
    __tablename__ = "password changers"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(), unique=True)
    verification_code: Mapped[int] = mapped_column(Integer(), nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    mail_sent: Mapped[bool] = mapped_column(Boolean(), nullable=True)


class Item(UserMixin, db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String())
    unique_name: Mapped[str] = mapped_column(String())
    name: Mapped[str] = mapped_column(String())
    price: Mapped[int] = mapped_column(Integer())
    description: Mapped[str] = mapped_column(String())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="items")
    cart_product = relationship("CartProduct", back_populates="item")
    order = relationship("Order", back_populates="item")
    

class CartProduct(UserMixin, db.Model):
    __tablename__ = "cart products"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item = relationship("Item", back_populates="cart_product")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="cart_products")
    

class Order(UserMixin, db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item = relationship("Item", back_populates="order")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    datetime: Mapped[datetime] = mapped_column(DateTime())
