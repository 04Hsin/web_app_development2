from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('category', __name__, url_prefix='/categories')

@bp.route('/')
def index():
    """
    列出所有可用的自訂分類，同時呈現新增分類的表單介面。
    """
    pass

@bp.route('', methods=['POST'])
def create():
    """
    接收新增分類請求，寫入 DB 後重導向至 /categories 本身。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除特定分類。
    若該分類下尚有收支紀錄，將會被阻擋並以 Flash 提示使用者。
    """
    pass
