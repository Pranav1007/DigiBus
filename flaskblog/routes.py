import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Pass
from flaskblog.forms import RegistrationForm, LoginForm, ContactForm, PassbookingForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Jayesh Travels',
        'title': 'Chennai to Hyderabad - 20:30 to 08:10',
        'date_posted': '29 March 2021'
    },
    {
        'author': 'Pranav Travels',
        'title': 'Chennai to Hyderabad - 20:30 to 08:10',
        'date_posted': '29 March 2021'
    }
]

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@app.route('/')
@app.route('/home',  methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template( 'index.html', title='Book Tickets Online', image_file=image_file)
    return render_template('index.html', title='Book Tickets Online')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Thank you for Contacting. We will get back to you soon.', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('contact.html', title='Contact Us', form=form, image_file=image_file)

@app.route('/support')
def support():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('support.html', title='Support', image_file=image_file)


@app.route('/ticketbooking')
@login_required
def ticketbooking():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('ticketbooking.html', posts=posts, title='Ticket Booking', image_file=image_file)

@app.route('/passbooking', methods=['GET', 'POST'])
@login_required
def passbooking():
    form = PassbookingForm()
    if form.validate_on_submit():
        user_pass = Pass(city=form.city.data, source=form.fromaddress.data, dest=form.toaddress.data, date=form.date.data, user_id=current_user.id)
        db.session.add(user_pass)
        db.session.commit()
        flash(f'Continue your payment', 'primary')
        return redirect(url_for('payment'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('passbooking.html', title='Pass Booking', form=form, image_file=image_file)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/payment')
def payment():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('payment.html', title='Payment', image_file=image_file)
