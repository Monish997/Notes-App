from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from notes import db
from notes.models import Note
from notes.notes.forms import NoteForm

notes = Blueprint("notes", __name__)


@notes.route("/notes")
@login_required
def user_notes():
    page = request.args.get("page", 1, type=int)
    notes = (
        Note.query.filter_by(author=current_user)
        .order_by(Note.updated_at.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_notes.html", notes=notes, user=current_user)


@notes.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash("Your note has been created!", "success")
        return redirect(url_for("notes.user_notes"))
    return render_template("new_note.html", title="New note", form=form, legend="New note")


@notes.route("/notes/<int:note_id>")
@login_required
def note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    return render_template("note.html", title=note.title, note=note)


@notes.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.updated_at = datetime.utcnow()
        db.session.commit()
        flash("Your note has been edited!", "success")
        return redirect(url_for("notes.note", note_id=note.id))
    elif request.method == "GET":
        form.title.data = note.title
        form.content.data = note.content
    return render_template("new_note.html", title="Edit note", form=form, legend="Edit note")


@notes.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash("Your note has been deleted!", "success")
    return redirect(url_for("notes.user_notes"))
