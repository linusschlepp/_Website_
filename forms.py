from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")
