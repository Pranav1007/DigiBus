from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ContactForm, PassbookingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '925709c46e120ecd46eb5aa502757785'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



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


@app.route('/')
@app.route('/home',  methods=['GET', 'POST'])
def home():
    return render_template('index.html', title='Book Tickets Online')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Thankyou for Contacting. We will get back to you soon.', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html', title='Contact Us', form=form)

@app.route('/support')
def support():
    return render_template('support.html', title='Support')

@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@app.route('/ticketbooking')
def ticketbooking():
    return render_template('ticketbooking.html', posts=posts, title='Ticket Booking')

@app.route('/passbooking', methods=['GET', 'POST'])
def passbooking():
    form = PassbookingForm()
    if form.validate_on_submit():
        flash(f'Continue your payment', 'primary')
        return redirect(url_for('payment'))
    return render_template('passbooking.html', title='Pass Booking', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@digibus.com' and form.password.data == 'password':
            flash('Logged in Successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/payment')
def payment():
    return render_template('payment.html', title='Payment')


if __name__ == "__main__":
    app.run(debug=True)
