import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config
from .api.models import db
from .api import api_blueprint
from .manage import migrate


# 导入模型
from .api.models.user import UserModel
from .api.models.revoked_token import RevokedTokenModel

def create_app(config_name):
    app = Flask(__name__)

    # 解决跨域
    CORS(app)

    # 加载配置项
    app.config.from_object(config[config_name])
    
    # 初始化数据库ORM
    db.init_app(app)
    
    # 初始化数据库ORM迁移插件
    migrate.init_app(app,db)

    # 注册蓝图
    app.register_blueprint(api_blueprint)
    
    # 初始化 JWT
    jwt = JWTManager(app)
    # 注册 JWT 钩子
    registerJwtHooks(jwt)

    return app
def registerJwtHooks(jwt):
    # 注册 JWT 钩子 用于检查 token 是否在黑名单中
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

#初始化项目
app = create_app(os.getenv('FLASK_ENV', 'development')) 
