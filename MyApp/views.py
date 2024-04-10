from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import db, User, ShortenedURL
from .url_shortener import shortenurl

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    shortened_url = None  # Define it here to ensure it's in scope at the render_template call
    if request.method == 'POST':
        url = request.form['url']
        shortened_url = shortenurl(url)
    return render_template('home.html', shortened_url=shortened_url)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first() is not None:
            flash('Username already taken. Please choose another one.', 'error')
            return redirect(url_for('main.register'))

        if User.query.filter_by(email=email).first() is not None:
            flash('Email already registered. Please use another email.', 'error')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('main.login'))
        session['user_id'] = user.id
        flash('Login successful.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))

    shortened_url = None
    if request.method == 'POST':
        url = request.form['url']
        shortened_url = shortenurl(url)
        if shortened_url and not "Error" in shortened_url:        
            new_shortened_url = ShortenedURL(original_url=url, shortened_url=shortened_url, user_id=user_id)
            db.session.add(new_shortened_url)
            db.session.commit()
            flash('URL successfully shortened.', 'success')

    user_shortened_urls = ShortenedURL.query.filter_by(user_id=user_id).all()
    shortened_urls = {s_url.shortened_url: s_url.original_url for s_url in user_shortened_urls}

    return render_template('dashboard.html', username=user.username, shortened_urls=shortened_urls)
