from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date

from app import db
from app.models.member import Member
from app.models.membership import Membership
from app.models.membership_type import MembershipType

auth_bp = Blueprint('auth', __name__)  # ✅ 一定要先定义这个！

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields = ['title', 'name', 'gender', 'dob', 'phone', 'email', 'password', 'member_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        if Member.query.filter_by(MEMBER_Email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # 先创建用户
        new_member = Member(
            MEMBER_Title=data['title'],
            MEMBER_Name=data['name'],
            MEMBER_Gender=data['gender'],
            MEMBER_DOB=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            MEMBER_Phone=data['phone'],
            MEMBER_Email=data['email'],
            MEMBER_PwdHash=generate_password_hash(data['password']),
            MEMBER_Type=data['member_type'],
            MEMBER_JCID=data.get('jc_id'),
            MEMBER_JCCompUsrnme=data.get('jc_username')
        )
        db.session.add(new_member)
        db.session.commit()

        # 根据传入的 member_type 查找会员类型ID
        mem_type_obj = MembershipType.query.filter_by(MEM_TYPE_Name=data['member_type']).first()
        if not mem_type_obj:
            return jsonify({'error': 'Invalid member type'}), 400

        # 创建 membership 记录
        new_membership = Membership(
            MEMBER_ID=new_member.MEMBER_ID,
            MEM_TYPE_ID=mem_type_obj.MEM_TYPE_ID,
            MEMBERSHIP_StartDate=date.today(),
            MEMBERSHIP_ExpDate=date.today() + timedelta(days=180),
            MEMBERSHIP_Declared=False
        )
        db.session.add(new_membership)
        db.session.commit()

        return jsonify({
            'message': 'Member registered successfully',
            'member_id': new_member.MEMBER_ID,
            'membership_id': new_membership.MEMBERSHIP_ID
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
