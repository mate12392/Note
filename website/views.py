from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Library
from . import db
import json

views = Blueprint('views', __name__)

def DeleteLib(lib):
    todel = db.session.query(Library).filter_by(name = lib, user_id = current_user.id)
    lib_id = todel.first().__dict__['id']
    todel2 = db.session.query(Note).filter_by(lib_id = lib_id)
    todel.delete(synchronize_session=False)
    todel2.delete(synchronize_session=False)
    
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    dest = "home.html"
    if request.method == 'POST':
        req_cat = request.form.get('category')
        if req_cat:
            req_cat = req_cat.replace(" ", "_")
            lib_query = Library.query.filter_by(name = req_cat, user_id = current_user.id).all()
            if len(lib_query) == 0:
                new_lib = Library(user_id=current_user.id, name=req_cat)
                db.session.add(new_lib)
                db.session.commit()
            else:
                flash('This category already exists!', category='error')
            dest = "home.html"
        elif request.form.get('del'):
            dest = "home.html"
        elif request.form.getlist('delete'):
            delete = request.form.getlist('delete')
            [DeleteLib(i) for i in delete if i != ""]
            db.session.commit()
            dest = "home.html"
        else:
            req_select = request.form.get('select')
            if req_select:
                dest = str(req_select)+".html"
                return redirect(url_for('views.note', name = req_select))

    return render_template(dest, user=current_user)

@views.route('/note/<name>', methods=['GET', 'POST'])
@login_required
def note(name):
    lib_id = Library.query.filter_by(name = name, user_id = current_user.id).all()[0].__dict__['id']
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, lib_id=lib_id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')

    return render_template('note.html', user=current_user, val=name)

@views.route('/search', methods=['GET', 'POST'])
def search():
    search = request.form.get('search')
    lib_id_list, name_delete_list = [], []
    if search:
        search_q = Note.query.filter_by(user_id = current_user.id).filter(Note.data.contains(search)).all()
        [lib_id_list.append(i.__dict__["lib_id"]) for i in search_q]
        [name_delete_list.append(Library.query.filter_by(id = i).all()[0].__dict__["name"]) for i in lib_id_list]
        name_delete_list = list(dict.fromkeys(name_delete_list))

    return render_template('search.html', user=current_user, val=name_delete_list)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})