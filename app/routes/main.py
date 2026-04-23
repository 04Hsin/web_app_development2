from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    獲取最新收支列表與餘額總數，並渲染首頁儀表板。
    同時需傳入 categories 給新增表單的下拉選單使用。
    """
    pass
