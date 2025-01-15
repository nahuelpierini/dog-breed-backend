from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import selected_env
from src.routes.predict_routes import predict_bp
from src.routes.auth_routes import auth
from src.routes.dog_routes import dog_bp
from src.routes.user_routes import profile_bp
from src.routes.prueba import prueba_bp

app = Flask(__name__)
app.config.from_object(selected_env)
FRONTEND_URL="FRONTEND_URL"
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})
jwt = JWTManager(app)

app.register_blueprint(prueba_bp)
app.register_blueprint(auth)  
app.register_blueprint(predict_bp)  
app.register_blueprint(dog_bp)     
app.register_blueprint(profile_bp)  

if __name__ == '__main__':
    app.run()