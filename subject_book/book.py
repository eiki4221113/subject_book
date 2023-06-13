from flask import Blueprint, render_template

book_bp = Blueprint('book', __name__, url_prefix='/book')