from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import AddForm, DeleteForm, SearchForm, LoginForm, ChangePasswordForm
from app import db
from app.models import City, User
import sys

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login failed', file=sys.stderr)
            return redirect(url_for('login'))
        # login_user is a flask_login function that starts a session
        login_user(user)
        print('Login successful', file=sys.stderr)
        return redirect(url_for('view'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/change_password',  methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user:
            if form.old_pass.data is None or not current_user.check_password(form.old_pass.data):
                print('password incorrect', file=sys.stderr)
                return render_template('change_password.html', form = form)
            elif form.new_pass.data != form.new_pass_retype.data:
                print('passwords do not match', file=sys.stderr)
                return render_template('change_password.html', form = form)
            else:
                current_user.set_password(form.new_pass_retype.data)
                db.session.add(current_user)
                db.session.commit()
                print("Password Changed succesfully", file=sys.stderr)
                return logout()
    return render_template('change_password.html', form = form)

def is_admin():
    '''
    Helper function to determine if authenticated user is an admin.
    '''
    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


# Adding a city requires that a user be logged in
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_record():
    form = AddForm()
    if form.validate_on_submit():
        # Extract values from form
        city_name = form.city.data
        population = form.population.data

        # Create a city record to store in the DB
        c = City(city=city_name, population=population)

        # add record to table and commit changes
        db.session.add(c)
        db.session.commit()

        form.city.data = ''
        form.population.data = ''
        return redirect(url_for('add_record'))
    return render_template('add.html', form=form)

# Adding a city requires that a user be logged in AND is an admin
@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_record():
    # Verifying that user is an admin
    if is_admin():
        form = DeleteForm()
        if form.validate_on_submit():
            # Query DB for matching record (we'll grab the first record in case
            # there's more than one).
            to_delete = db.session.query(City).filter_by(city = form.city.data).first()

            # If record is found delete from DB table and commit changes
            if to_delete is not None:
                db.session.delete(to_delete)
                db.session.commit()

            form.city.data = ''
            # Redirect to the view_all route (view function)
            return redirect(url_for('view'))
        return render_template('delete.html', form=form)
    # Tell non-admin user they're not authorized to access route.
    else:
        return render_template('unauthorized.html')


@app.route('/search', methods=['GET', 'POST'])
def search_by_name():
    form = SearchForm()
    if form.validate_on_submit():
        # Query DB table for matching name
        record = db.session.query(City).filter_by(city = form.city.data).all()
        if record:
            return render_template('view_cities.html', cities=record)
        else:
            return render_template('not_found.html')
    return render_template('search.html', form=form)


@app.route('/view_all')
def view():
    all = db.session.query(City).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)


@app.route('/sort_by_name')
def sort_by_name():
    all = db.session.query(City).order_by(City.city).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)
