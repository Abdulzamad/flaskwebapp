from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return "OPPs Its 404 | Page Not Found" , 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "OPPs Its 500 code | Something  went wrong", 500