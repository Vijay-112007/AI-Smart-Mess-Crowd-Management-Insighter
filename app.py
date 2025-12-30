from flask import Flask, render_template, request, redirect, url_for, session, flash
from authentication import SignIn, SignUp
import os

app = Flask(__name__)
app.secret_key = 'ai_smart_mess_secret_key_2025'  # Change this to a secure secret key

@app.route('/')
def index():
    """Landing page with options to sign in or sign up"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('signin.html')
        
        # Use the existing SignIn class
        signin_obj = SignIn(username, password)
        result = signin_obj.sign_in()
        
        if result == "Authentication Successfull":
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result, 'error')
            return render_template('signin.html')
    
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password or not email:
            flash('Please fill in all fields', 'error')
            return render_template('signup.html')
        
        # Use the existing SignUp class
        signup_obj = SignUp(username, password, email)
        result = signup_obj.sign_up()
        
        if result == "Account Successfully Created":
            recovery_code = signup_obj.recovery_code()
            flash(f'Account created successfully! Your recovery code is: {recovery_code}. Please save it securely.', 'success')
            return redirect(url_for('signin'))
        else:
            flash(result, 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page after successful login"""
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('signin'))
    
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    """Logout route"""
    session.pop('user', None)
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
