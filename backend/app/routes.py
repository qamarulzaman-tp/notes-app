from flask import Blueprint, request, jsonify
from app import db
from app.models import Note
from app.schemas import NoteSchema

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()
        
        # Validate request data
        is_valid, error_message = NoteSchema.validate_create(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Create new note
        note = Note(content=data['content'].strip())
        db.session.add(note)
        db.session.commit()
        
        # Return created note
        return jsonify(NoteSchema.to_dict(note)), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create note', 'message': str(e)}), 500

@bp.route('/notes', methods=['GET'])
def get_all_notes():
    """Get all notes"""
    try:
        notes = Note.query.all()
        return jsonify(NoteSchema.to_dict_list(notes)), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve notes', 'message': str(e)}), 500

@bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a single note by ID"""
    try:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        return jsonify(NoteSchema.to_dict(note)), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve note', 'message': str(e)}), 500

@bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note by ID"""
    try:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        
        # Validate request data
        is_valid, error_message = NoteSchema.validate_update(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Update note
        note.content = data['content'].strip()
        db.session.commit()
        
        # Return updated note
        return jsonify(NoteSchema.to_dict(note)), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update note', 'message': str(e)}), 500

@bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note by ID"""
    try:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': 'Note deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete note', 'message': str(e)}), 500

