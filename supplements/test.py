# # Search test
# from flask import Flask, render_template
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Integer, DateTime, ForeignKey, text, Boolean
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# db = SQLAlchemy(model_class=Base)
#
#
# class Person(db.Model):
#     __tablename__ = "people"
#     id: Mapped[int] = mapped_column(Integer(), primary_key=True)
#     name: Mapped[str] = mapped_column(String())
#     number: Mapped[int] = mapped_column(Integer())
#
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pegasus"
# db.init_app(app)
#
#
# with app.app_context():
#     db.create_all()
#
#
# @app.route("/")
# def index():
#     query = Person.query.filter(Person.name.ilike(f'%chloe%')).all()
#     return render_template("test.html", query=query)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
# # End of search test


# # Pagination test
# from flask import Flask, render_template
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Integer, DateTime, ForeignKey, text, Boolean
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# db = SQLAlchemy(model_class=Base)
#
#
# class Person(db.Model):
#     __tablename__ = "people"
#     id: Mapped[int] = mapped_column(Integer(), primary_key=True)
#     name: Mapped[str] = mapped_column(String())
#     number: Mapped[int] = mapped_column(Integer())
#
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pegasus"
# db.init_app(app)
#
#
# with app.app_context():
#     db.create_all()
#
#
# @app.route("/<int:page_number>")
# def index(page_number):
#     people = db.select(Person).order_by(Person.id)
#     book = db.paginate(select=people, page=page_number, per_page=6)
#     sub_people = book.items
#     link_helpers = book.iter_pages(left_current=1, right_current=2)
#     return render_template("test.html", page_number=page_number, book=book, people=sub_people, pages=link_helpers)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

# # End of pagination test


# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(email, password)
#     connection.sendmail(
#         from_addr=email,
#         to_addrs=e_mail,
#         msg=f"Subject:{unconfirmed_person.verification_code} is your verification code for WebBuildHQ\n\n"
#             f"Dear user,\n\nYour verification code is {unconfirmed_person.verification_code}. Please "
#             f"note that it will expire in 14 minutes.\n\nBest Regards,\nWebBuildHQ"
#     )


    # with smtplib.SMTP("smtp.ethereal.email", 587) as connection:
    #     connection.starttls()
    #     connection.login("era99@ethereal.email", "vqr3dG8HWUHu23AMhY")
    #     connection.sendmail(
    #         from_addr="reply@webbuildhq.com",
    #         to_addrs=e_mail,
    #         msg=f"Subject:Password reset for WebBuildHQ account ({password_changer.verification_code})\n\n"
    #             f"Dear user,\n\nYour verification code to use in changing your password "
    #             f"is {password_changer.verification_code}. Please note it will expire in "
    #             f"14 minutes.\n\nBest Regards,\nWebBuildHQ"
    #     )


# from flask import Flask, render_template
# # from flask_cors import CORS
# import os
# from dotenv import load_dotenv
# import markdown2
# from bs4 import BeautifulSoup

# load_dotenv()

# gemini_key = os.environ.get("GEMINI_API_KEY")

# import requests
# import json

# url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# headers = {
#     "Content-Type": "application/json",
#     "X-goog-api-key": gemini_key
# }

# data = {
#     "contents": [
#         {
#             # "role": "user",
#             "parts": [
#                 {
#                     "text": "How hot does antartica get in the summer?"
#                 }
#             ]
#         },
#         # {
#         #     "role": "model",
#         #     "parts": [
#         #         {
#         #             "text": '"OluwaFolajimi" is a Yoruba name (a language spoken in Nigeria). Here\'s a breakdown of its meaning:\n\n*   **Oluwa:** God, Lord\n*   **Folajimi:** Crown is given to me\n\nTherefore, **OluwaFolajimi** roughly translates to:\n\n*   **God gave me a crown**\n*   **God has given me honor/glory**\n*   **God bestowed a crown upon me**\n\nIt\'s a name expressing gratitude to God for a gift or blessing, symbolized by a crown.\n'
#         #         }
#         #     ]
#         # },
#         # {
#         #     "role": "user",
#         #     "parts": [
#         #         {
#         #             "text": "Great. Can you use it in a sentence?"
#         #         }
#         #     ]
#         # }
#     ]
# }

# response = requests.post(url, headers=headers, data=json.dumps(data))

# print(response.json()["candidates"][0]["content"]["parts"][0]["text"])

# # print({'candidates': [{'content': {'parts': [{'text': 'Here are a few sentences using the name OluwaFolajimi:\n\n*   OluwaFolajimi\'s parents chose the name as a testament to their faith and gratitude for his safe arrival.\n*   We celebrate OluwaFolajimi\'s achievements, knowing they are a reflection of the blessings inherent in his name.\n*   OluwaFolajimi carries his name with pride, understanding its meaning as "God has given me a crown."\n'}], 'role': 'model'}, 'finishReason': 'STOP', 'avgLogprobs': -0.27636760912443464}], 'usageMetadata': {'promptTokenCount': 139, 'candidatesTokenCount': 95, 'totalTokenCount': 234, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 139}], 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 95}]}, 'modelVersion': 'gemini-2.0-flash', 'responseId': 'LVqsaOv_NbDikdUP7v_a2Qg'}["candidates"][0]["content"]["parts"][0]["text"])


# # md_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

# mdown_text = 'Here are a few sentences using the name OluwaFolajimi:\n\n*   OluwaFolajimi\'s parents chose the name as a testament to their faith and gratitude for his safe arrival.\n*   We celebrate OluwaFolajimi\'s achievements, knowing they are a reflection of the blessings inherent in his name.\n*   OluwaFolajimi carries his name with pride, understanding its meaning as "God has given me a crown."\n'

# html_output = markdown2.markdown(md_text)

# print(html_output)

# Parse with BeautifulSoup
# soup = BeautifulSoup(html_output, "html.parser")

# # Example: add a class to <strong> tags
# for strong_tag in soup.find_all("strong"):
#     strong_tag["style"] = "color: red;"

# # Example: add an id to the first <li>
# first_li = soup.find("li")
# if first_li:
#     first_li["style"] = "color: blue;"
    
# for p_tag in soup.find_all("p"):
#     p_tag["style"] = "color: green;"

# html = soup.prettify()


# app = Flask(__name__)

# CORS(app)

# @app.route("/")
# def test():
#     return html


# if __name__ == "__main__":
#     app.run(debug=True)



# print(lambda x=2, y=3: x + y)