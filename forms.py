from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Optional,URL,NumberRange


class AddCupcakeForm(FlaskForm):
    """Form for adding cupcakes."""

    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    rating = IntegerField("Rating", validators=[NumberRange(0,10,'select rating between 0-10'),InputRequired()])
    image = URLField("Image link", validators=[URL(message='url field'),Optional()])
