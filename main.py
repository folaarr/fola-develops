# Import necessary libraries and modules
# flask creates the server that communicates with users
# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, abort, send_from_directory
# os is where the secrets are saved, like developer passwords and api keys
import os
# Import forms from the forms.py file
from supplements.forms import LoginForm, SignupForm, NoteForm, PictureForm, SettingsForm, VerifyForm, EmailForm, NewPasswordForm, ItemForm, AmountForm
# CSRFProtect protects from cross-site-request-forgery https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
from flask_wtf.csrf import CSRFProtect
# Import database tables from the entities.py file
from supplements.entities import db, UnverifiedUser, User, PasswordChanger, Note, Item, CartProduct, Order, AiChat, AiMessage, Payment
from sqlalchemy import func, desc
# werkzeug.security hashes passwords
# https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
# flask_login logs users in and out https://flask-login.readthedocs.io/en/latest/
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# The python datetime module is used for getting the time that testimonies were made
from datetime import datetime, timezone, timedelta
# API requests are made through the requests module
import requests
# load_dotenv loads data stored as environment variables(e.g. secrets like the developer passwords or api keys)
from dotenv import load_dotenv
# cloudinary stores pictures uploaded by users
# https://cloudinary.com/documentation/dev_kickstart
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
# The random module is used to generate a random number
import random
# The simple-mail-transfer-protocol library(smtplib) is used send emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supplements.email_templates import verify_one, verify_two, reset_one, reset_two, email_brand, before_greeting, before_datetime, after_datetime, before_number, before_image, before_name, before_quantity, before_price, after_price, before_total, after_total
from functools import wraps
from supplements.items_data import things
# from flask_cors import CORS
from supplements.ai_skeleton import system_instructions, chat_ai, identify_chat, accumulate_chat, message_ai
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import uuid
import hashlib
import hmac


load_dotenv()

app = Flask(__name__)

csrf = CSRFProtect(app)

app.config["SECRET_KEY"] = os.environ.get("FLASK-SECRET-KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE-URI")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db.init_app(app)

app.config["UPLOAD_FOLDER"] = "static/images/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "jfif"}
# app.config["MAX_CONTENT_LENGTH"] = 8 * 1000 * 1000

url = os.environ.get("API-URL")
i_d_ = os.environ.get("ID-INSTANCE")
key = os.environ.get("API-TOKEN-INSTANCE")
number = os.environ.get("NUMBER")

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

video_url = os.environ.get("VIDEO-URL")

gemini_key = os.environ.get("GEMINI_API_KEY")

config = cloudinary.config(secure=True)  # Signed up with the Google account

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

admin_email = os.environ.get("ADMIN-EMAIL")

admin_emails = [admin_email, "view@foladevelops.onrender.com"]

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=14)
jwt = JWTManager(app)

PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_LIVE_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_LIVE_PUBLIC_KEY")

FLUTTERWAVE_SECRET_KEY = os.environ.get("FLUTTERWAVE_TEST_SECRET_KEY")
FLUTTERWAVE_PUBLIC_KEY = os.environ.get("FLUTTERWAVE_TEST_PUBLIC_KEY")
# FLUTTERWAVE_ENCRYPTION_KEY = os.environ.get("FLUTTERWAVE_LIVE_ENCRYPTION_KEY")
FLUTTERWAVE_SECRET_HASH = os.environ.get("FLASK-SECRET-KEY")

# CORS(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the current user is not the admin then return abort with a 403 error
        if current_user.email not in admin_emails:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("index.html", video_url=video_url)


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/flow")
# @login_required
# def flow():
#     return render_template("flow.html")
#
#
# @app.route("/flow/api")
# @login_required
# def flow_api():
#     return jsonify({
#         "first name": current_user.first_name,
#         "last name": current_user.last_name,
#         "email": current_user.email,
#         "picture url": current_user.picture_url,
#     })


@app.route("/projects")
def categories():
    return render_template("projects.html")


@app.route("/professional")
def professional():
    return render_template("professional.html")


@app.route("/personal")
def designs():
    return render_template("personal.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# @app.route("/testimonies")
# def testimonies():
#     # Display all the testimonies in the database on the web page, starting with the most recent
#     posts = db.session.execute(db.select(Testimony).order_by(Testimony.id.desc())).scalars().all()
#     return render_template("testimonies.html", testimonies=posts)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    signup_form = SignupForm()
    if request.method == "POST":
        if signup_form.validate_on_submit():
            data = request.form
            db_emails = db.session.query(User.email).all()
            for email in db_emails:
                if data["email"] == email[0]:
                    flash("This Account Already Exists Here.")
                    return redirect(url_for("sign_up"))
            if data["password"] == data["second_password"]:
                hashed_password = generate_password_hash(
                    password=data["second_password"],
                    method="pbkdf2",
                    salt_length=8
                )
                unvalidated_user = db.session.execute(db.select(UnverifiedUser).where(UnverifiedUser.email == data["email"])).scalar()
                if unvalidated_user:
                    db.session.delete(unvalidated_user)
                    db.session.commit()
                unverified_user = UnverifiedUser(
                    first_name=data["first_name"].title(),
                    last_name=data["last_name"].title(),
                    email=data["email"],
                    password=hashed_password,
                    verification_code=random.randint(1000, 9999),
                    sent_at = datetime.now()
                )
                db.session.add(unverified_user)
                db.session.commit()
                return redirect(url_for("verify_email", e_mail=data["email"]))
            else:
                flash("Passwords do not match, please try again.")
                return redirect(url_for("sign_up"))
    return render_template("sign-up.html", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            data = request.form
            user = db.session.execute(db.select(User).where(User.email == data["email"].lower())).scalar()
            if user:
                if check_password_hash(user.password, data["password"]):
                    login_user(user)
                    # 👇 Try to get it first from hidden field
                    next_page = login_form.next.data or request.args.get("next")
                    # security check: only allow relative URLs
                    if not next_page or not next_page.startswith("/"):
                        next_page = url_for("account")
                    return redirect(next_page)
                flash("Invalid Password, Please Try Again.")
                return redirect(url_for("login"))
            flash("Account Not Found.")
            return redirect(url_for("login"))
    else: 
        next_page = request.args.get("next")
        login_form.next.data = next_page
    return render_template("login.html", form=login_form, next=next_page)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/account")
@login_required
def account():
    return render_template("account.html", admin_email=admin_email)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = db.session.execute(db.select(User).where(User.id == current_user.id)).scalar()
    settings_form = SettingsForm(
        first_name=user.first_name,
        last_name=user.last_name
    )
    if request.method == "POST":
        if settings_form.validate_on_submit():
            data = request.form
            with app.app_context():
                user = db.session.execute(db.select(User).where(User.id == current_user.id)).scalar()
                user.first_name = data["first_name"].title()
                user.last_name = data["last_name"].title()
                db.session.commit()
            return redirect(url_for("account"))
    return render_template("settings.html", form=settings_form, email=user.email, admin_email=admin_email)


@app.route("/add-note", methods=["GET", "POST"])
@login_required
def add_note():
    note_form = NoteForm()
    if request.method == "POST":
        if note_form.validate_on_submit():
            data = request.form
            with app.app_context():
                note = Note(
                    datetime=datetime.now(timezone.utc),
                    title=data["title"],
                    content=data["content"],
                    user_id = current_user.id
                )
                db.session.add(note)
                db.session.commit()
            flash("Your note has been added.")
            return redirect(url_for("account"))
    return render_template("add-note.html", form=note_form, admin_email=admin_email)


@app.route("/edit-note/<int:i_d>", methods=["GET", "POST"])
@login_required
def edit_note(i_d):
    note = db.session.execute(db.select(Note).where(Note.id == i_d)).scalar()
    note_form = NoteForm(title=note.title, content=note.content)
    if request.method == "POST":
        if note_form.validate_on_submit():
            data = request.form
            with app.app_context():
                note = db.session.execute(db.select(Note).where(Note.id == i_d)).scalar()
                note.title = data["title"]
                note.content = data["content"]
                db.session.commit()
            flash("Your note has been updated.")
            return redirect(url_for("account"))
    return render_template("edit-note.html", i_d=i_d, form=note_form)


@app.route("/confirm-delete/<int:i_d>")
@login_required
def confirm_delete(i_d):
    pending_note = db.session.execute(db.select(Note).where(Note.id == i_d)).scalar()
    return render_template("confirm-delete.html", note=pending_note)


@app.route("/delete/<int:i_d>")
@login_required
def delete(i_d):
    note = db.session.execute(db.select(Note).where(Note.id == i_d)).scalar()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("account"))


@app.route("/profile-picture")
@login_required
def profile_picture():
    return render_template("profile-picture.html")


def valid_picture(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload-picture", methods=["GET", "POST"])
@login_required
def upload_picture():
    # if not current_user.is_authenticated:
    #     return redirect(url_for("login"))
    picture_form = PictureForm()
    if request.method == "POST":
        if "picture" not in request.files:
            flash("No file part")
            return redirect(url_for("upload_picture"))
        profile_pic = request.files["picture"]
        pic_name = profile_pic.filename
        if pic_name == "":
            flash("No file selected")
            return redirect(url_for("upload_picture"))
        if profile_pic and valid_picture(pic_name):
            if current_user.picture_url:
                cloudinary.uploader.destroy(f"{current_user.id}-{current_user.picture_number - 1}", invalidate=True)
            lad = db.get_or_404(User, current_user.id)
            picture_no = lad.picture_number
            cloudinary.uploader.upload(profile_pic, public_id=f"{current_user.id}-{picture_no}", unique_filename=False, overwrite=True)
            pic_url = CloudinaryImage(f"{current_user.id}-{picture_no}").build_url()
            user = db.get_or_404(User, current_user.id)
            user.picture_url = pic_url.rsplit("/", 1)[0] + "/q_auto/f_auto/c_scale,w_500/" + pic_url.rsplit("/", 1)[1]
            user.picture_number = picture_no + 1
            db.session.commit()
            requests.post(
                f"{url}/waInstance{i_d_}/sendFileByUrl/{key}",
                json={
                    "chatId": f"{number}@c.us",
                    "urlFile": f"{current_user.picture_url}",
                    "fileName": f"{current_user.first_name}-{current_user.last_name}.png",
                    "caption": f"{current_user.first_name} {current_user.last_name} uploaded a picture to FolaDevelops."
                },
                headers={'Content-Type': 'application/json'}
            )
        else:
            flash("File format not supported")
            return redirect(url_for("upload_picture"))
        return redirect(url_for("profile_picture"))
    return render_template("upload-picture.html", form=picture_form)


@app.route("/confirm-delete-picture")
@login_required
def confirm_remove():
    return render_template("confirm-remove.html")


@app.route("/delete-picture")
@login_required
def delete_picture():
    user = db.get_or_404(User, current_user.id)
    user.picture_url = None
    db.session.commit()
    return redirect(url_for("profile_picture"))


@app.route("/verify-email/<e_mail>", methods=["GET", "POST"])
def verify_email(e_mail):
    verify_form = VerifyForm()
    unconfirmed_person = db.session.execute(db.select(UnverifiedUser).where(UnverifiedUser.email == e_mail)).scalar()
    if unconfirmed_person.mail_sent != True:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{unconfirmed_person.verification_code} is your verification code for FolaDevelops."
        message["From"] = email
        message["To"] = e_mail
        message.attach(MIMEText(f"""{verify_one}{unconfirmed_person.verification_code}{verify_two}""", "html"))
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(email, password)
            connection.sendmail(message["From"], message["To"], message.as_string())
    unconfirmed_person.mail_sent = True
    db.session.commit()
    if verify_form.validate_on_submit():
        data = request.form
        if datetime.now() < (unconfirmed_person.sent_at + timedelta(minutes=14)):
            if int(data["input"]) == unconfirmed_person.verification_code:
                user = User(
                    first_name=unconfirmed_person.first_name,
                    last_name=unconfirmed_person.last_name,
                    email=unconfirmed_person.email,
                    password=unconfirmed_person.password
                )
                db.session.add(user)
                db.session.commit()
                user = db.session.execute(db.select(User).where(User.email == e_mail)).scalar()
                login_user(user)
                requests.post(
                    f"{url}/waInstance{i_d_}/sendMessage/{key}",
                    json={
                        "chatId": f"{number}@c.us",
                        "message": f"{user.first_name} {user.last_name} Signed Up to FolaDevelops with a successful verification!"
                    },
                    headers={'Content-Type': 'application/json'}
                )
                flash("Your email has been verified successfully, Welcome.")
                return redirect(url_for("account"))
            else:
                flash("Wrong verification code, please try again", "error")
                return redirect(url_for("verify_email", e_mail=e_mail))
        else:
            flash("This verification code is no longer valid, kindly check your email for a new one.", "error")
            unconfirmed_person.verification_code = random.randint(1000, 9999)
            unconfirmed_person.sent_at = datetime.now()
            unconfirmed_person.mail_sent = False
            db.session.commit()
            return redirect(url_for("verify_email", e_mail=e_mail))
    return render_template("verify-email.html", form=verify_form, e_mail=e_mail)


@app.route("/resend-email/<e_mail>")
def resend_email(e_mail):
    unconfirmed_person = db.session.execute(db.select(UnverifiedUser).where(UnverifiedUser.email == e_mail)).scalar()
    unconfirmed_person.verification_code = random.randint(1000, 9999)
    unconfirmed_person.sent_at = datetime.now()
    unconfirmed_person.mail_sent = True
    db.session.commit()
    person = db.session.execute(db.select(UnverifiedUser).where(UnverifiedUser.email == e_mail)).scalar()
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{unconfirmed_person.verification_code} is your verification code for FolaDevelops."
    message["From"] = email
    message["To"] = e_mail
    message.attach(MIMEText(f"""{verify_one}{person.verification_code}{verify_two}""", "html"))
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(message["From"], message["To"], message.as_string())
    flash(f"A verification code has been resent to '{e_mail}'.", "success")
    return redirect(url_for("verify_email", e_mail=e_mail))


@app.route("/email", methods=["GET", "POST"])
def your_email():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        data = request.form
        password_editor = db.session.query(PasswordChanger).filter_by(email=data["email"]).first()
        if password_editor:
            db.session.delete(password_editor)
            db.session.commit()
        possible_user = db.session.query(User).filter_by(email=data["email"]).first()
        if possible_user:
            the_user = PasswordChanger(
                email=data["email"],
                verification_code=random.randint(1000, 9999),
                sent_at=datetime.now()
            )
            db.session.add(the_user)
            db.session.commit()
            return redirect(url_for("reset_password", e_mail=data["email"]))
        else:
            flash("This email address does not exist in WebBuildHQ's database")
            return redirect(url_for("email"))
    return render_template("your-email.html", form=email_form)


@app.route("/reset-password/<e_mail>", methods=["GET", "POST"])
def reset_password(e_mail):
    password_form = NewPasswordForm()
    password_changer = db.session.execute(db.select(PasswordChanger).where(PasswordChanger.email == e_mail)).scalar()
    if password_changer.mail_sent != True:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{password_changer.verification_code} is the code to reset your password for your FolaDevelops account."
        message["From"] = email
        message["To"] = e_mail
        message.attach(MIMEText(f"""{reset_one}{password_changer.verification_code}{reset_two}""", "html"))
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
            connection.starttls()
            connection.login(email, password)
            connection.sendmail(message["From"], message["To"], message.as_string())
    password_changer.mail_sent = True
    db.session.commit()
    if password_form.validate_on_submit():
        data = request.form
        if datetime.now() < (password_changer.sent_at + timedelta(minutes=14)):
            if int(data["code"]) == password_changer.verification_code:
                if data["password"] == data["second_password"]:
                    hashed_password = generate_password_hash(
                        password=data["second_password"],
                        method="pbkdf2",
                        salt_length=8
                    )
                    user = db.session.execute(db.select(User).where(User.email == e_mail)).scalar()
                    user.password = hashed_password
                    db.session.commit()
                    flash("Your password has been changed successfully, you may now log in.")
                    return redirect(url_for("login"))
                else:
                    flash("Passwords do not match, please try again.")
                    return redirect(url_for("reset_password", e_mail=e_mail))
            else:
                flash("Wrong verification code, please try again", "error")
                return redirect(url_for("reset_password", e_mail=e_mail))
        else:
            flash("This verification code is no longer valid, kindly check your email for a new one.")
            password_changer.verification_code = random.randint(1000, 9999)
            password_changer.sent_at = datetime.now()
            password_changer.mail_sent = False
            db.session.commit()
            return redirect(url_for("reset_password", e_mail=e_mail))
    return render_template("reset-password.html", form=password_form, e_mail=e_mail)


@app.route("/resend-password/<e_mail>")
def resend_password(e_mail):
    password_changer = db.session.execute(db.select(PasswordChanger).where(PasswordChanger.email == e_mail)).scalar()
    password_changer.verification_code = random.randint(1000, 9999)
    password_changer.sent_at = datetime.now()
    password_changer.mail_sent = True
    db.session.commit()
    someone = db.session.execute(db.select(PasswordChanger).where(PasswordChanger.email == e_mail)).scalar()
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{someone.verification_code} is the code to reset your password for your FolaDevelops account."
    message["From"] = email
    message["To"] = e_mail
    message.attach(MIMEText(f"""{reset_one}{someone.verification_code}{reset_two}""", "html"))
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(message["From"], message["To"], message.as_string())
    flash(f"A verification code has been resent to '{e_mail}'.")
    return redirect(url_for("reset_password", e_mail=e_mail))


@app.route("/api/active")
def active():
    return jsonify({"status": "active"})


# @app.route("/admin")
# @login_required
# @admin_only
# def admin():
#     testimonials = db.session.execute(db.select(Testimony).order_by(Testimony.id.desc())).scalars().all()
#     return render_template("admin.html", testimonies=testimonials, admin_email=admin_email)


# @app.route("/show-testimony/<i_d>")
# @login_required
# @admin_only
# def show_testimony(i_d):
#     testimony = db.session.execute(db.select(Testimony).where(Testimony.id == i_d)).scalar()
#     testimony.is_visible = True
#     db.session.commit()
#     with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
#         connection.starttls()
#         connection.login(email, password)
#         connection.sendmail(
#             from_addr=email,
#             to_addrs=testimony.user.email,
#             msg=f"Subject:Your testimony has been published on the FolaDevelops testimonies section\n\n"
#                 f"Dear user,\n\nYour testimony '{testimony.testimony}' for '{testimony.website}' has "
#                 f"been published on the FolaDevelops testimonies section, you can view your testimony "
#                 f"among others on https://webbuildhq.com/testimonies, thank you for leaving a testimony." 
#                 f"\n\nBest Regards,\nFolaDevelops"
#         )
#     return redirect(url_for("admin"))


# @app.route("/hide-testimony/<i_d>")
# @login_required
# @admin_only
# def hide_testimony(i_d):
#     testimony = db.session.execute(db.select(Testimony).where(Testimony.id == i_d)).scalar()
#     testimony.is_visible = False
#     db.session.commit()
#     return redirect(url_for("admin"))


# @app.route("/projects")
# def projects():
#     return render_template("projects.html")


@app.route("/ap")
def add_placeholders():
    # Add all the placeholder entities to the database, only use when you are creating a new database
    with app.app_context():
    # Add users
        user = User(
        first_name="User",
        last_name="Account",
        email="view@foladevelops.onrender.com",
        password="pbkdf2:sha256:1000000$STNIsWCs$ba157c62d3a12e324789fe094dbd42a6589832f8a1909b9e4f4beb3ccbd0f359",
        picture_number=0
        )
        user_2 = User(
        first_name="Jimi",
        last_name="Abolade",
        email="folajimiabolade@gmail.com",
        password="pbkdf2:sha256:1000000$LnEVrUJt$924cc433408925189620f4254f00e2001b7911f38440d75bbb6735135498c2e4",
        picture_number=0
        )
        user_3 = User(
        first_name="Eniola",
        last_name="Abolade",
        email="i.eniolaabolade@gmail.com",
        password="pbkdf2:sha256:1000000$ELa3VoLQ$d40360f04e6f5f5d20145a4eb1dd3747b1881988e7766d9129c16bed2f3742fe",
        picture_number=0
        )
        db.session.add(user)
        db.session.add(user_2)
        db.session.add(user_3)
        db.session.commit()
        # Add store items
        for thing in things:
            item = Item(
            picture_url=thing["picture_url"],
            unique_name=thing["unique_name"],
            name=thing["name"],
            price=thing["price"],
            description=thing["description"],
            user_id=thing["user_id"]
            )
            db.session.add(item)
            db.session.commit()
    return "<h2>All placeholders have been added successfully!</h2>"


@app.route("/store")
@login_required
def store():
    # if not current_user.is_authenticated:
    #     return redirect(url_for("login"))
    items = db.session.execute(db.select(Item).order_by(Item.id.desc())).scalars().all()
    return render_template("store.html", items=items, page_name="store", admin_email=admin_email)


@app.route("/load-store/api")
@login_required
def load_store():
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    product_ids = [cart_product.item_id for cart_product in cart_products]
    buyer_ids = [cart_product.user_id for cart_product in cart_products]
    users_items = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    items_ids = [cart_product.item_id for cart_product in users_items]
    return jsonify({
        "cart_length": len(cart_products),
        "product_ids": product_ids,
        "buyer_ids": buyer_ids,
        "items_ids": items_ids
        })


@app.route("/add-item", methods=["GET", "POST"])
@login_required
@admin_only
def add_item():
    item_form = ItemForm()
    if request.method == "POST":
        if item_form.validate_on_submit():
            if "picture" not in request.files:
                flash("No file part")
                return redirect(url_for("add_item"))
            item_pic = request.files["picture"]
            pic_name = item_pic.filename
            if pic_name == "":
                flash("No file selected")
                return redirect(url_for("add_item"))
            item_data = request.form
            if item_pic and valid_picture(pic_name):
                item_name = item_data["name"].replace(" ", "_").replace("|", "-")
                cloudinary.uploader.upload(item_pic, public_id=f"{item_name}",
                                           unique_filename=False, overwrite=True)
                pic_url = CloudinaryImage(f"{item_name}").build_url()
                picture_url = pic_url.rsplit("/", 1)[0] + "/q_auto/f_auto/c_scale,w_500/" + pic_url.rsplit("/", 1)[
                    1]
                item = Item(
                    picture_url=picture_url,
                    unique_name=item_name,
                    name=item_data["name"],
                    price=item_data["price"],
                    description=item_data["description"],
                    user_id=current_user.id
                )
                db.session.add(item)
                db.session.commit()
                flash("Your item has been added successfully.")
        return redirect(url_for("store"))
    return render_template("add-item.html", form=item_form, admin_email=admin_email)


@app.route("/item/<unique_name>")
@login_required
def item(unique_name):
    item = db.session.execute(db.select(Item).where(Item.unique_name == unique_name)).scalar()
    item_id = item.id
    count = 0
    cart_products = db.session.query(CartProduct).filter(CartProduct.item_id == item_id, CartProduct.user_id == current_user.id).all()
    if cart_products:
        # count = (
        #     db.session.query(func.count(CartProduct.id))
        #     .filter(CartProduct.item_id == item_id)
        #     .scalar()
        # )
        count = len(cart_products)
    return render_template("item.html", item=item, page_name="item", admin_email=admin_email, count=count)


@app.route("/load-item/api")
@login_required
def load_item():
    return jsonify({})


@app.route("/add-to-cart/api", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json()
    item_id = data.get("item_id")
    cart_product = CartProduct(
        item_id=item_id,
        user_id=current_user.id
    )
    db.session.add(cart_product)
    db.session.commit()
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    items = db.session.query(CartProduct).filter(
        CartProduct.item_id == item_id, 
        CartProduct.user_id == current_user.id
        ).all()
    return jsonify({
        "cart_length": len(cart_products),
        "quantity": len(items)
        })


@app.route("/reduce-quantity/api", methods=["POST"])
@login_required
def reduce_quantity():
    data = request.get_json()
    item_id = data.get("item_id")
    cart_product = db.session.query(CartProduct).filter(CartProduct.item_id == item_id, CartProduct.user_id == current_user.id).first()
    db.session.delete(cart_product)
    db.session.commit()
    products = db.session.query(CartProduct).filter(
        CartProduct.user_id == current_user.id, 
        CartProduct.item_id == item_id
        ).all()
    quantity = len(products)
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    items_details = (
        db.session.query(CartProduct.item_id, func.count(CartProduct.item_id))
        .filter(CartProduct.user_id == current_user.id)
        .group_by(CartProduct.item_id).all()
    )
    cart_items = [{"item_id": value, "quantity": frequency} for value, frequency in items_details]
    items = db.session.execute(db.select(Item).order_by(Item.id)).scalars().all()
    total_price = 0
    for item in items:
        for thing in cart_items:
            if item.id == thing["item_id"]:
                total_price += (item.price * thing["quantity"])
    return jsonify({
        "cart_length": len(cart_products),
        "quantity": quantity,
        "total_price": total_price
        })


@app.route("/increase-quantity/api", methods=["POST"])
@login_required
def increase_quantity():
    data = request.get_json()
    item_id = data.get("item_id")
    cart_product = CartProduct(item_id=item_id, user_id=current_user.id)
    db.session.add(cart_product)
    db.session.commit()
    products = db.session.query(CartProduct).filter(
        CartProduct.user_id == current_user.id, 
        CartProduct.item_id == item_id
        ).all()
    quantity = len(products)
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    items_details = (
        db.session.query(CartProduct.item_id, func.count(CartProduct.item_id))
        .filter(CartProduct.user_id == current_user.id)
        .group_by(CartProduct.item_id).all()
    )
    cart_items = [{"item_id": value, "quantity": frequency} for value, frequency in items_details]
    items = db.session.execute(db.select(Item).order_by(Item.id)).scalars().all()
    total_price = 0
    for item in items:
        for thing in cart_items:
            if item.id == thing["item_id"]:
                total_price += (item.price * thing["quantity"])
    return jsonify({
        "cart_length": len(cart_products),
        "quantity": quantity,
        "total_price": total_price
        })


@app.route("/cart")
@login_required
def cart():
    items_details = (
        db.session.query(CartProduct.item_id, func.count(CartProduct.item_id))
        .filter(CartProduct.user_id == current_user.id)
        .group_by(CartProduct.item_id).all()
    )
    cart_products = [{"item_id": value, "quantity": frequency} for value, frequency in items_details]
    items = db.session.execute(db.select(Item).order_by(Item.id)).scalars().all()
    total_price = 0
    for item in items:
        for cart_product in cart_products:
            if item.id == cart_product["item_id"]:
                total_price += (item.price * cart_product["quantity"])
    cart_items = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    return render_template(
        "cart.html", 
        page_name="cart", 
        cart_products=cart_products, 
        items=items,
        total_price=total_price,
        cart_length=len(cart_items)
        )


@app.route("/delete-item/api", methods=["POST"])
@login_required
def delete_item():
    data = request.get_json()
    item_id = data.get("item_id")
    products = db.session.query(CartProduct).filter(
        CartProduct.user_id == current_user.id, 
        CartProduct.item_id == item_id
        ).all()
    for product in products:
        db.session.delete(product)
        db.session.commit()
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    return jsonify({
        "cart_length": len(cart_products)
        })


@app.route("/add-to-trolley/api", methods=["POST"])
@login_required
def add_to_trolley():
    data = request.get_json()
    item_id = data.get("item_id")
    cart_product = CartProduct(
        item_id=item_id,
        user_id=current_user.id
    )
    db.session.add(cart_product)
    db.session.commit()
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    items = db.session.query(CartProduct).filter(
        CartProduct.item_id == item_id, 
        CartProduct.user_id == current_user.id
        ).all()
    return jsonify({
        "cart_length": len(cart_products),
        "quantity": len(items)
        })


@app.route("/checkout")
def checkout():
    now = datetime.now()
    cart_products = db.session.query(CartProduct).filter(CartProduct.user_id == current_user.id).all()
    for cart_product in cart_products:
        order = Order(
            item_id=cart_product.item_id,
            user_id=cart_product.user_id,
            datetime=now
        )
        db.session.add(order)
        db.session.delete(cart_product)
        db.session.commit()
    items_details = (
        db.session.query(Order.item_id, func.count(Order.item_id))
        .filter(Order.user_id == current_user.id, Order.datetime == now)
        .group_by(Order.item_id).all()
    )
    orders = [{"item_id": value, "quantity": frequency} for value, frequency in items_details]
    items = db.session.execute(db.select(Item).order_by(Item.id)).scalars().all()
    total_price = 0
    for item in items:
        for order in orders:
            if item.id == order["item_id"]:
                total_price += (item.price * order["quantity"])
    items_html = ""
    for order in orders:
        for item in items:
            if order["item_id"] == item.id:
                items_html += f"{before_number}{orders.index(order) + 1}{before_image}{item.picture_url}{before_name}{item.name}{before_quantity}{order["quantity"]}{before_price}{"₦{:,.0f}".format(item.price)}{after_price}"
    order_datetime = f"{now.strftime("%B %d, %Y")} at {now.strftime("%H:%M:%S UTC")}"
    html_email = f"""{email_brand}{before_greeting}{current_user.first_name}{before_datetime}{order_datetime}{after_datetime}{items_html}{before_total}{"₦{:,.0f}".format(total_price)}{after_total}"""
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your order made on {order_datetime} has been confirmed."
    message["From"] = email
    message["To"] = current_user.email
    message.attach(MIMEText(html_email, "html"))
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(email, password)
        connection.sendmail(message["From"], message["To"], message.as_string())
    return render_template("checkout.html", page_name="checkout")


@app.route("/orders")
def orders():
    order_points = (
        db.session.query(Order.datetime)
        .filter(Order.user_id == current_user.id)
        .group_by(Order.datetime)
        .order_by(desc(Order.datetime)).all()
    )
    return render_template("orders.html", order_points=order_points, page_name="orders")


@app.route("/order/<order_point>")
def order(order_point):
    order_instance = datetime.fromisoformat(order_point)
    orders = db.session.query(Order).filter(Order.datetime == order_instance).all()
    items_details = (
        db.session.query(Order.item_id, func.count(Order.item_id))
        .filter(Order.user_id == current_user.id, Order.datetime == order_instance)
        .group_by(Order.item_id).all()
    )
    orders = [{"item_id": value, "quantity": frequency} for value, frequency in items_details]
    items = db.session.execute(db.select(Item).order_by(Item.id)).scalars().all()
    total_price = 0
    for item in items:
        for order in orders:
            if item.id == order["item_id"]:
                total_price += (item.price * order["quantity"])
    return render_template(
        "order.html", 
        orders=orders, 
        items=items, 
        total_price=total_price, 
        page_name="order", 
        order_point=order_instance
        )


@app.route("/ai-assistant")
@login_required
def ai_assistant():
    ai_chats = db.session.execute(db.select(AiChat).order_by(AiChat.datetime.desc())).scalars().all()
    return render_template("ai.html", ai_chats=ai_chats, page_name="a.i.")


@app.route("/ping-ai/api", methods=["POST"])
@login_required
def ping_ai():
    data = request.get_json()
    message = data.get("message")
    chats = current_user.ai_chats
    no_chats = not chats
    now = datetime.now()
    chat = AiChat(datetime=now, user_id=current_user.id)
    db.session.add(chat)
    db.session.commit()
    ai_chat = db.session.execute(db.select(AiChat).where(AiChat.datetime == now)).scalar()
    system_instruction = AiMessage(role="user", message=system_instructions, chat_id=ai_chat.id)
    db.session.add(system_instruction)
    user_message = AiMessage(role="user", message=message, chat_id=ai_chat.id)
    db.session.add(user_message)
    ai_reply = chat_ai(message)
    assistant_message = AiMessage(role="model", message=ai_reply["raw_output"], message_html=ai_reply["html_output"], chat_id=ai_chat.id)
    db.session.add(assistant_message)
    chat_title = identify_chat(ai_chat.id)
    ai_chat.title = chat_title
    db.session.commit()
    return jsonify({
        "output": ai_reply["html_output"], 
        "chat_id": ai_chat.id, 
        "chat_title": chat_title, 
        "no_chats": no_chats
        })


@app.route("/open-chat/api", methods=["POST"])
@login_required
def open_chat():
    data = request.get_json()
    chat_id = data.get("chat_id")
    ai_chat = db.session.execute(db.select(AiChat).where(AiChat.id == chat_id)).scalar()
    ai_chat.datetime = datetime.now()
    db.session.commit()
    chat_messages = ai_chat.messages
    messages = [{"role": message.role, "message": message.message} if message.role == "user" else {"role": message.role, "message": message.message_html} for message in chat_messages if chat_messages.index(message) != 0]
    return jsonify({"messages": messages, "chat_id": ai_chat.id})


@app.route("/update-ai/api", methods=["POST"])
@login_required
def update_ai():
    data = request.get_json()
    chat_id = data.get("chat_id")
    message = data.get("message")
    initial_contents = accumulate_chat(chat_id)
    ai_reply = message_ai(initial_contents, message)
    user_message = AiMessage(role="user", message=message, chat_id=chat_id)
    db.session.add(user_message)
    statement = db.session.execute(db.select(AiMessage).where(AiMessage.message == message)).scalar()
    assistant_message = AiMessage(role="model", message=ai_reply["raw_output"], message_html=ai_reply["html_output"], chat_id=chat_id)
    db.session.add(assistant_message)
    db.session.commit()
    return jsonify({"output": ai_reply["html_output"], "message_id": statement.id})


@app.route("/monnify-test")
def monnify_test():
    return render_template("monnify-test.html")
    
@app.route("/gallery-test")
def gallery_test():
    return render_template("gallery-test.html")


# Mobile app start

@csrf.exempt
@app.route("/api-login", methods=["POST"])
def api_login():
    data = request.get_json()
    user = db.session.execute(db.select(User).where(User.email == data["email"].lower())).scalar()
    if user:
        if check_password_hash(user.password, data["password"]):
            access = create_access_token(identity=str(user.id))
            refresh = create_refresh_token(identity=str(user.id))
            return jsonify({
                "status": 'success', 
                'access': access, 
                'refresh': refresh
            })
        return jsonify({
            "status": 'error',
            "message": "Incorrect Password, Please Try Again!"
        })
    return jsonify({
        "status": 'error',
        "message": "Account Not Found."
    })


@csrf.exempt
@app.route("/api-picture", methods=['GET'])
@jwt_required()
def api_picture():
    jwt_id = int(get_jwt_identity())
    user_id = db.get_or_404(User, jwt_id)
    return jsonify({'imageURL': user_id.picture_url}) 




# Payment gateways start
@app.route('/input-amount', methods=["GET", "POST"])
@login_required
def input_amount():
    amount_form = AmountForm()
    if amount_form.validate_on_submit():
        data = request.form
        amount = data['amount']
        gateway = data['amount']
        if gateway == "paystack":
            return redirect(url_for('pay', amount=amount))
        elif gateway == "flutterwave":
            return redirect(url_for('f_pay', amount=amount))
    return render_template('input-amount.html', form=amount_form)


def expire_old_payments():
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    old_payments = Payment.query.filter(
        Payment.status == "pending",
        Payment.created_at < one_hour_ago
    ).all()
    for payment in old_payments:
        payment.status = "expired"
    db.session.commit()


# Paystack start
@app.route('/pay/<int:amount>', methods=["GET", "POST"])
@login_required
def pay(amount):
    expire_old_payments()
    reference = str(uuid.uuid4())
    payment = Payment(
        email=current_user.email,
        amount=amount,
        reference=reference,
        gateway="paystack",
        currency="NGN",
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(payment)
    db.session.commit()
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": current_user.email,
        "amount": amount * 100,
        "reference": reference,
        "currency": "NGN",
        "callback_url": url_for("payment_callback", _external=True)
    }
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()

    if not response_json.get("status"):
        return f"Error: {response_json.get('message')}", 400
    
    return redirect(response_json["data"]["authorization_url"])


@app.route("/payment/callback")
def payment_callback():
    reference = request.args.get("reference")
    return redirect(url_for("verify_payment", reference=reference))


@app.route("/verify/<reference>")
def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    payment = Payment.query.filter_by(reference=reference).first()
    if not payment:
        return "Payment record not found", 404
    if payment.status == "expired":
        return "Payment expired"
    if payment.status == "success":
        return "Payment already marked as success (probably from webhook)", 200
    if response_json["data"]["status"] == "success":
        payment.status = "success"
        payment.paid_at = datetime.now(timezone.utc)
        db.session.commit()
        return "Payment successful"
    payment.status = "failed"
    db.session.commit()
    return "Payment failed"


@app.route("/paystack/webhook", methods=["POST"])
@csrf.exempt
def paystack_webhook():
    print('WEBHOOK FIRED BY PAYSTACK!')
    signature = request.headers.get("x-paystack-signature")
    payload = request.data
    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(),
        payload,
        hashlib.sha512
    ).hexdigest()
    if computed_signature != signature:
        return "Invalid signature", 400
    event = request.get_json()
    if event["event"] == "charge.success":
        reference = event["data"]["reference"]
        payment = Payment.query.filter_by(reference=reference).first()
        if not payment:
            return "", 200
        if payment and payment.status == "expired":
            return "Payment expired"
        if payment and payment.status != "success":
            url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if response_json["data"]["status"] == "success":
                payment.status = "success"
                payment.paid_at = datetime.now(timezone.utc)
                db.session.commit()
    return "", 200


# Flutterwave start
@app.route('/f-pay/<int:amount>', methods=["GET", "POST"])
@login_required
def f_pay(amount):
    expire_old_payments()
    reference = str(uuid.uuid4())
    payment = Payment(
        email=current_user.email,
        amount=amount,
        reference=reference,
        gateway="flutterwave",
        currency="USD",
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(payment)
    db.session.commit()
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "tx_ref": reference,
        "amount": amount,
        "currency": "USD",
        "redirect_url": url_for("f_payment_callback", _external=True),
        "customer": {
            "email": current_user.email
        },
        "customizations": {
            "title": "FolaDevelops",
            "description": "Payment Checkout"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()

    if not response_json.get("status"):
        return f"Error: {response_json.get('message')}", 400
    
    return redirect(response_json["data"]["link"])


@app.route("/f-payment/callback")
def f_payment_callback():
    tx_ref = request.args.get("tx_ref")
    return redirect(url_for("verify_f_payment", reference=tx_ref))


@app.route("/verify/f/<reference>")
def verify_f_payment(reference):
    url = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={reference}"
    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    payment = Payment.query.filter_by(reference=reference).first()
    if not payment:
        return "Payment record not found", 404
    if payment.status == "expired":
        return "Payment expired"
    if payment.status == "success":
        return "Payment already marked as success (probably from webhook)", 200
    if response_json.get("status") == "success":
        payment.status = "success"
        payment.paid_at = datetime.now(timezone.utc)
        db.session.commit()
        return "Payment successful"
    payment.status = "failed"
    db.session.commit()
    return "Payment failed"


@app.route("/flutterwave/webhook", methods=["POST"])
@csrf.exempt
def flutterwave_webhook():
    print('WEBHOOK FIRED BY FLUTTERWAVE!')
    signature = request.headers.get("verif-hash")
    if not signature or signature != FLUTTERWAVE_SECRET_HASH:
        return "Invalid webhook source", 400
    
    event = request.get_json()
    if not event:
        return "Invalid payload", 400
    
    event_type = event.get("type") or event.get("event")
    if event_type != "charge.completed":
        return "", 200

    data = event.get("data", {})

    reference = data.get("reference") or data.get("tx_ref")
    if not reference:
        return "", 200
    payment = Payment.query.filter_by(reference=reference).first()
    if not payment:
        return "", 200
    if payment.status in ["expired", "success"]:
        return "", 200
    
    url = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={reference}"
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get("data", {}).get("status") == "successful":
            payment.status = "success"
            payment.paid_at = datetime.now(timezone.utc)
            db.session.commit()
    except Exception as e:
        print(f"Flutterwave verify failed with API error: {e}")
        return "Retry", 500

    return "", 200


# For crawl

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")


@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favico.ico')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
