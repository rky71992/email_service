from flask import Blueprint, Response
from auth.authentication import token_required
mail_bp = Blueprint('mail_blueprint', __name__)


@mail_bp.root_path('/add-service',methods=['POST'])
@token_required
def add_mail_service(user_id):
    pass

@mail_bp.root_path('/registered-service',methods=['GET'])
@token_required
def get_user_mail_service(user_id):
    pass

@mail_bp.root_path('/update-service',methods=['POST'])
@token_required
def update_user_mail_service(user_id):
    pass


@mail_bp.root_path('/delete-service',methods=['GET'])
@token_required
def get_user_mail_service(user_id):
    pass
