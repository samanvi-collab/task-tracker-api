from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# 1. Initialize Flask app and SQLite Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. Define our Database Model (Table structure)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database tables
with app.app_context():
    db.create_all()

# -------------------------------------------------------------
# 3. BACKEND ROUTES (APIs)
# -------------------------------------------------------------

# ROUTE 1: Get all tasks (READ)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = [{'id': t.id, 'title': t.title, 'completed': t.completed} for t in tasks]
    return jsonify(output), 200

# ROUTE 2: Add a new task (CREATE)
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required!'}), 400
    
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({'message': 'Task created!', 'task': {'id': new_task.id, 'title': new_task.title}}), 201

# ROUTE 3: Update a task's completion status (UPDATE)
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found!'}), 404
        
    data = request.get_json()
    # Update title or completed status if provided in the request
    if 'title' in data:
        task.title = data['title']
    if 'completed' in data:
        task.completed = data['completed']
        
    db.session.commit()
    return jsonify({'message': f'Task {id} updated successfully!', 'task': {'id': task.id, 'title': task.title, 'completed': task.completed}}), 200

# ROUTE 4: Delete a task (DELETE)
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found!'}), 404
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {id} deleted successfully!'}), 200

# 4. Start the Backend Server
if __name__ == '__main__':
    app.run(debug=True, port=5000)