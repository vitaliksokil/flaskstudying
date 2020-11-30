from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Regexp


class FriendForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=4, max=25, message='Min:4 , max 25 symbols'),
                                                   DataRequired(message='This field is required'),
                                                   Regexp('^[A-Za-z]+$', 0,
                                                          'Name must have only letters')])
    last_name = StringField('Last Name', validators=[Length(min=4, max=25, message='Min:4 , max 25 symbols'),
                                                   DataRequired(message='This field is required'),
                                                   Regexp('^[A-Za-z]+$', 0,
                                                          'Last name must have only letters')])
    phone = StringField('Phone', validators=[DataRequired(), Regexp('^\+[0-9]{12}$', 0,
                                                          'Phone must be in format +************ (plus symbol + 12 digits)')])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])

    birth_day = DateField('Birth day', format='%m/%d/%y', render_kw={'placeholder': '6/20/15 for June 20, 2015'})

    friend_rank = SelectField('Friend rank', choices=[('acquaintance', 'Acquaintance'),('good_acquaintance', 'Good Acquaintance'), ('friend', 'Friend')], validators=[DataRequired()])

    hobby = StringField('Hobby', validators=[DataRequired()])

    submit = SubmitField('Save')