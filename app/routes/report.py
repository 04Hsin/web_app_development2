from flask import Blueprint, render_template, jsonify

bp = Blueprint('report', __name__)

@bp.route('/reports')
def index():
    """
    渲染統計圖表分析的報表頁面。
    圖表繪製主要依靠前端讀取下方的 api 進行渲染。
    """
    pass

@bp.route('/api/reports')
def api_reports():
    """
    回傳各分類支出或收入的加總統計 JSON 資料。
    """
    pass
