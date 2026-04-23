from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('record', __name__, url_prefix='/records')

@bp.route('/')
def index():
    """
    讀取所有歷史收支紀錄並呈現於列表頁面。
    """
    pass

@bp.route('', methods=['POST'])
def create():
    """
    接收首頁的新增收支表單資料。
    驗證通過後存入資料庫，並導向回首頁。
    """
    pass

@bp.route('/<int:id>/edit')
def edit(id):
    """
    顯示特定收支紀錄的修改表單。
    """
    pass

@bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    接收修改表單送出的新資料，更新制資料庫中。
    完成後重導向至歷史紀錄清單。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    接收刪除某筆收支的請求，從資料庫中移除。
    完成後重導向至歷史紀錄清單。
    """
    pass
