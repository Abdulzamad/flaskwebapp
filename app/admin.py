from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_login import current_user

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        
        return current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('home', next=request.url))