from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import Product, User  # Make sure User model is defined with password methods
import os
import barcode
from barcode.writer import ImageWriter
from flask import flash
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)

# Neon PostgreSQL connection string (fallback included)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 
    "postgresql://neondb_owner:npg_Rsu7od9cApKP@ep-lively-dust-a2am9qf3-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
app.config['UPLOAD_FOLDER'] = 'static/barcodes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")  # Needed for sessions

# Initialize DB
db.init_app(app)

# Create tables & folder on first run
with app.app_context():
    db.create_all()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        description = request.form['description']
        telephone = request.form['telephone']
        instagram = request.form['instagram']
        email = request.form['email']

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{code}.png')

        ean = barcode.get('code128', code, writer=ImageWriter())
        ean.save(file_path[:-4])  # remove .png extension

        product = Product(
            name=name,
            code=code,
            description=description,
            telephone=telephone,
            instagram=instagram,
            email=email,
            barcode_path=f'barcodes/{code}.png'
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/product/<code>')
def product_info(code):
    product = Product.query.filter_by(code=code).first_or_404()
    return render_template('product_info.html', product=product)

# This route is open to everyone (no login required)
@app.route('/check', methods=['GET', 'POST'])
def check_code():
    if request.method == 'POST':
        code = request.form['code'].strip()
        return redirect(url_for('product_info', code=code))
    return render_template('check_code.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "User already exists."

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')
# EDIT PRODUCT
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.code = request.form['code']
        product.description = request.form.get('description')
        product.telephone = request.form.get('telephone')
        product.instagram = request.form.get('instagram')
        product.email = request.form.get('email')
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product)

# DELETE PRODUCT
@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
