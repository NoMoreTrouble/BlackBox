from plant_monitor import create_app
app = create_app()

# Define a simple login route for testing
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Handle the form data (authentication, etc.)
        # If successful, redirect to the home page
        return redirect(url_for('home'))
    
    # If it's a GET request, render the login form
    return render_template('login.html')

# A simple home route to test after login
@app.route('/home')
def home():
    return "Welcome to the Home Page!"

if __name__ == "__main__":
    app.run(debug=True)
