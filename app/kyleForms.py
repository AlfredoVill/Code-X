from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

"""
Sprint1:
Home Page (logged out)
Login
Change Password

Sprint2:
HR Dashboard - LoggedIn
  - All Processes Displayed (Interviews/Disciplinary - ID, Stage (HR/Manager), Status (Approved, Denied, Information Request, Pending Review))
  - "Sort-by" - Action Required Button displaying processes requiring attention
  - Print Reports 
    - User Types by Numbers (Applicant, Employee, HR, Manager)
    - Users by Disciplinary Standing (Good Standing, Performance Review, Appeal Pending, Terminated)

Process Actions Form
 - Approve, Deny, Information Request

Applicant/Employee Dashboard 
 - 
  
Sprint3:
Connecting everything together - database, backend, etc.
  

"""

class AddForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    population = IntegerField('Population: ', validators=[DataRequired()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old password', validators=[DataRequired()])
    new_pass = PasswordField('New password', validators=[DataRequired()])
    new_pass_retype = PasswordField('Retype new password', validators=[DataRequired()])
    submit = SubmitField('Change password')
