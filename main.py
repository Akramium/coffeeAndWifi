from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name',
                       validators=[DataRequired()])
    location = StringField(label='Location URL',
                           validators=[DataRequired(), URL()])
    open_time = StringField(label='Open time',
                            validators=[DataRequired()])
    closing_time = StringField(label='Closing time',
                               validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee rating',
                                validators=[DataRequired()],
                                choices=[('0', '☕'), ('1', '☕☕'), ('2', '☕☕☕'), ('3', '☕☕☕☕'), ('4', '☕☕☕☕☕')])
    wifi_rating = SelectField('Wifi rating',
                              validators=[DataRequired()],
                              choices=[('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'),
                                       ('5', '💪💪💪💪💪')])
    power = SelectField('Power outlet rating',
                        validators=[DataRequired()],
                        choices=[('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'),
                                 ('5', '🔌🔌🔌🔌🔌')])

    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a') as data:
            data.write(f"\n{form.cafe.data},"
                       f"{form.location.data},"
                       f"{form.open_time.data},"
                       f"{form.closing_time.data},"
                       f"{form.coffee_rating.data},"
                       f"{form.wifi_rating.data},"
                       f"{form.power.data}")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(f"{row}")
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
