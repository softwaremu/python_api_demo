from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import UserModel
from ..common.utils import res

class UserService(Resource):
    @jwt_required()
    def get(self):
        userList = UserModel.findAll()
        result = []
        for user in userList:
            result.append(user.dictUser())
    
        return res(data=result)
