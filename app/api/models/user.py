from ..models import db
from datetime import datetime
from ..common.utils import format_datetime_to_json

class UserModel(db.Model):
    """
        用户表
    """
    __tablename__ = 'user'
    # 主键
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, comment='主键id')
    # 用户名
    username = db.Column(db.String(50), nullable=False, default='', comment='用户名')
    # 密码
    password = db.Column(db.String(300), comment='密码')
    # salt
    salt = db.Column(db.String(50), comment='salt')
    # 创建时间
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 更新时间
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 新增用户
    def addUser(self):
        db.session.add(self)
        db.session.commit()

    # 用户字典
    def dictUser(self):
        return {
            'id': self.id,
            'username': self.username,
            'create_time': format_datetime_to_json(self.create_time),
            'update_time': format_datetime_to_json(self.update_time)
        }
    
    # 获取密码和salt
    def getPwd(self):
        return {
            'password': self.password,
            'salt': self.salt
        }

    # 按username查找用户
    @classmethod
    def findByUsername(cls, username):
        return db.session.execute(db.select(cls).filter_by(username=username)).first()
    
    # 按id查找用户
    @classmethod
    def findById(cls, id):
        return db.session.execute(db.select(cls).filter_by(id=id)).first()
    
    # 查询所有用户
    @classmethod
    def findAll(cls):
        return db.session.query(cls).all()
