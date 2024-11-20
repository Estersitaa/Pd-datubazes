from flask import Flask, render_template, request, redirect, url_for, flash
import data

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Lai strādātu Flash ziņojumi

# Inicializē datubāzi
data.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        if not first_name or not last_name or not username:
            flash("Visi lauki ir obligāti!", "error")
        else:
            try:
                data.add_user(first_name, last_name, username)
                flash("Reģistrācija veiksmīga!", "success")
                return redirect(url_for('register'))
            except ValueError as e:
                flash(str(e), "error")
    return render_template('registration.html')

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        user_id = request.form['user_id']
        message = request.form['message']
        try:
            data.add_message(user_id, message)
            flash("Ziņa pievienota!", "success")
        except ValueError as e:
            flash(str(e), "error")
    users = data.get_users()
    messages = data.get_messages()
    return render_template('messages.html', users=users, messages=messages)

@app.route('/stats')
def stats():
    statistics = data.get_user_statistics()
    return render_template('stats.html', statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True)
