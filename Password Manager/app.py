from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(256), nullable=False)
    passwords = db.relationship('Password', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Password model
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    encrypted_password = db.Column(db.String(256), nullable=False)
    encryption_key = db.Column(db.String(256), nullable=False)  # Store the key for this password
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Password {self.name}>'

@app.route('/register', methods=['POST'])
def register_user():
    try:
        email = request.json['email']
        password = request.json['password']

        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 400

        encrypted_password = Fernet(Fernet.generate_key()).encrypt(password.encode()).decode('utf-8')

        user = User(email=email, encrypted_password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User successfully registered'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email=email).first()
        print("User:", user)
        if not user:
            return {'error': 'User not found'}, 404

        print("User password:", user.encrypted_password)
        
        return {'message': 'Login successful'}, 200
    except Exception as e:
        return {'error': str(e)}, 400
    
@app.route('/add_password', methods=['POST'])
def add_password():
    try:
        email = request.json['email']
        name = request.json['name']
        password = request.json['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'error': 'User not found'}, 404

        encryption_key = Fernet.generate_key()
        encrypted_password = Fernet(encryption_key).encrypt(password.encode()).decode('utf-8')

        password = Password(name=name, encrypted_password=encrypted_password, encryption_key=encryption_key, user_id=user.id)
        db.session.add(password)
        db.session.commit()

        return {'message': 'Password successfully added'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

@app.route('/get_password/<email>/<name>', methods=['GET'])
def get_password(email, name):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return {'error': 'User not found'}, 404
        
        password = Password.query.filter_by(user_id=user.id, name=name).first()
        if not password:
            return {'error': 'Password not found'}, 404
        
        decrypted_password = Fernet(password.encryption_key).decrypt(password.encrypted_password.encode()).decode('utf-8')
        return {'password': decrypted_password}, 200
    except Exception as e:
        return {'error': str(e)}, 400
    
@app.route('/get_passwords/<email>', methods=['GET'])
def get_passwords(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return {'error': 'User not found'}, 404
        
        passwords = Password.query.filter_by(user_id=user.id).all()
        data = {
            'passwords': [
                {
                    'name': password.name,
                    'decrypted_password': Fernet(password.encryption_key).decrypt(password.encrypted_password.encode()).decode('utf-8')
                }
                for password in passwords
            ]
        }
        return data, 200
    except Exception as e:
        return {'error': str(e)}, 400
    
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        users = User.query.all()
        data = []
        for user in users:
            user_data = {
                'email': user.email,
                'passwords': [
                    {
                        'name': password.name,
                        'decrypted_password': Fernet(password.encryption_key).decrypt(password.encrypted_password.encode()).decode('utf-8'),
                        # 'encrypted_password': str(password.encrypted_password),
                        # 'encryption_key': password.encryption_key
                    }
                    for password in user.passwords
                ]
            }
            data.append(user_data)
        return {'data': data}, 200
    except Exception as e:
        return {'error': str(e)}, 400

    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)