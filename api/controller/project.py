# -*- coding: utf-8 -*-
'''项目管理接口

@author: Wang Qianxiang
'''
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                get_jwt_claims, fresh_jwt_required,
                                set_access_cookies, unset_jwt_cookies)
from marshmallow import Schema, fields
from flask import jsonify, request, abort, Blueprint, session
from rbac.context import PermissionDenied

from model import project
app = Blueprint('project', __name__, url_prefix='/api')  # pylint: disable=c0103


# @app.route("/project/<int:project_id>", methods=['GET'])
@fresh_jwt_required
def project_info(project_id):
    '''获取项目信息

    GET /api/project/<int:project_id>
    '''
    return project.find_project(project_id)


# @app.route("/project/<int:project_id>", methods=['PUT'])
@fresh_jwt_required
def project_update(project_id):
    '''更新项目信息

    PUT /api/project/<int:project_id>
    '''
    if not request.json or\
    not 'name' in request.json or\
    not 'detail' in request.json:
        abort(400)
    session['project_id'] = project_id
    # try:
    return {
        "message": "项目更新成功",
        "data": project.update_project(project_id, request.json)
    }

# @app.route("/userlist", methods=['GET'])
@fresh_jwt_required
def user_list():
    '''获取所有用户列表

    GET /api/user
    '''
    return jsonify(project.find_users())


# @app.route("/project/<int:project_id>/user", methods=['GET'])
@fresh_jwt_required
def project_user(project_id):
    '''获取项目成员
    
    GET /api/project/<int:project_id>/user
    '''
    return jsonify({
        "message": "ok",
        "data": project.find_project_users(project_id)
    })


# @app.route("/project/<int:project_id>/user", methods=['PUT'])
@fresh_jwt_required
def project_user_update(project_id):
    '''更新项目成员
    
    PUT /api/project/<int:project_id>/user
    '''
    if not request.json or\
    not 'memberIdArr' in request.json['data']:
        abort(400)
    session['project_id'] = project_id    
    try:
        return jsonify(
            project.update_project_users(project_id, request.json['data']))
    except PermissionDenied:
        return jsonify({'msg': 'PermissionDenied'})

@fresh_jwt_required
def fuzzy_query_member():
    '''模糊查询用户'''
    return {
        "message": "ok",
        "data": project.fuzzy_query(request.args.to_dict())
    }

@fresh_jwt_required
def project_member_add():
    '''添加项目成员'''
    return {
        "message": "ok",
        "data": project.member_add(request.json)
    }
@fresh_jwt_required
def project_member_delete():
    '''删除项目成员'''
    return {
        "message": "ok",
        "data": project.member_delete(request.args.to_dict())
    }