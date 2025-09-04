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
from fola_develops import db
from flask_migrate import Migrate


# class Base(DeclarativeBase):
#     pass


# db = SQLAlchemy(model_class=Base)


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
    notes = relationship("Note", back_populates="user")
    items = relationship("Item", back_populates="user")
    cart_products = relationship("CartProduct", back_populates="user")
    orders = relationship("Order", back_populates="user")
    ai_chats = relationship("AiChat", back_populates="user")


class Note(UserMixin, db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime())
    title: Mapped[str] = mapped_column(String(), nullable=True)
    content: Mapped[str] = mapped_column(String())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="notes")


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


class AiChat(UserMixin, db.Model):
    __tablename__ = "ai_chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime())
    title: Mapped[str] = mapped_column(String(), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="ai_chats")
    messages = relationship("AiMessage", back_populates="chat")


class AiMessage(UserMixin, db.Model):
    __tablename__ = "ai messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String())
    message: Mapped[str] = mapped_column(String())
    message_html: Mapped[str] = mapped_column(String(), nullable=True)
    chat_id: Mapped[int | None] = mapped_column(ForeignKey("ai_chats.id"), nullable=True)
    chat = relationship("AiChat", back_populates="messages")
