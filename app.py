from flask import Flask, render_template, request, jsonify, session
from universal_book.repository import UniversalBookRepository, Book
from question_generator.generator import QuestionGenerator
from peer_platform.collaboration import PeerCollaborationPlatform
from progress_tracker.tracker import ProgressTracker
from ai_facilitator.facilitator import AIFacilitator
from knowledge_map.mapper import KnowledgeMapper
from models import db
from models import Book
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions

    db.init_app(app)

    with app.app_context():
        db.create_all()
        init_db()

    return app


def init_db():
    # Check if the database is empty and add some sample books if it is
    if Book.query.count() == 0:
        sample_books = [
            Book(title="To Kill a Mockingbird", author="Harper Lee",
                 summary="A novel about racial injustice and the loss of innocence.",
                 tags="classic,fiction,racism"),
            Book(title="1984", author="George Orwell",
                 summary="A dystopian novel set in a totalitarian society.",
                 tags="dystopia,fiction,politics"),
            # Add more sample books as needed
        ]
        db.session.add_all(sample_books)
        db.session.commit()


app = create_app()
book_repo = UniversalBookRepository()
question_gen = QuestionGenerator()
peer_platform = PeerCollaborationPlatform()
progress_tracker = ProgressTracker()
ai_facilitator = AIFacilitator()
knowledge_mapper = KnowledgeMapper()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    books = book_repo.get_random_books(5)
    return render_template('explore.html', books=books)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    books = book_repo.search_books(query)
    return render_template('search.html', books=books, query=query)


@app.route('/question', methods=['POST'])
def get_question():
    data = request.json
    book = None
    if 'book_id' in data:
        book = book_repo.get_book_by_id(data['book_id'])
    elif 'topic' in data:
        book = book_repo.get_book_by_title(data['topic'])

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    try:
        if isinstance(book, dict) and 'title' in book and 'author' in book:
            question = ai_facilitator.generate_explore_questions(book)
            return jsonify({'question': question})
        else:
            raise ValueError("Invalid book data")
    except Exception as e:
        app.logger.error(f"Error generating question: {str(e)}")
        return jsonify({'error': 'An error occurred while generating the question'}), 500


@app.route('/discuss/<int:book_id>', methods=['GET', 'POST'])
def discuss_book(book_id):
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = session.get('user_id', 'anonymous')
        peer_platform.add_discussion_post(book_id, user_id, content)
        progress_tracker.log_activity(user_id, 'discussion_post', f"Posted in discussion for book {book_id}")

    book = book_repo.get_book_by_id(book_id)
    posts = peer_platform.get_discussion_posts(book_id)
    discussion_prompt = ai_facilitator.generate_prompt('discussion')
    return render_template('discuss.html', book=book, posts=posts, discussion_prompt=discussion_prompt)


@app.route('/reply/<int:book_id>/<int:post_index>', methods=['POST'])
def reply_to_post(book_id, post_index):
    content = request.form.get('content')
    user_id = session.get('user_id', 'anonymous')
    reply = peer_platform.add_reply(book_id, post_index, user_id, content)
    return jsonify(reply)


@app.route('/study_groups', methods=['GET', 'POST'])
def study_groups():
    if request.method == 'POST':
        name = request.form.get('name')
        book_ids = request.form.getlist('book_ids')
        user_id = session.get('user_id', 'anonymous')
        group_id = peer_platform.create_study_group(name, user_id, book_ids)
        return jsonify({'group_id': group_id})

    user_id = session.get('user_id', 'anonymous')
    groups = peer_platform.get_user_study_groups(user_id)
    books = book_repo.get_random_books(10)  # Get some books to display in the form
    return render_template('study_groups.html', groups=groups, books=books)


@app.route('/set_goal', methods=['POST'])
def set_goal():
    user_id = session.get('user_id', 'anonymous')
    goal_description = request.form.get('description')
    target_date = request.form.get('target_date')
    goal_index = progress_tracker.set_goal(user_id, goal_description, target_date)
    return jsonify({'success': True, 'goal_index': goal_index})


@app.route('/complete_goal/<int:goal_index>', methods=['POST'])
def complete_goal(goal_index):
    user_id = session.get('user_id', 'anonymous')
    success = progress_tracker.complete_goal(user_id, goal_index)
    return jsonify({'success': success})


@app.route('/progress')
def view_progress():
    user_id = session.get('user_id', 'anonymous')
    goals = progress_tracker.get_goals(user_id)
    activities = progress_tracker.get_activities(user_id)
    summary = progress_tracker.get_progress_summary(user_id)
    reflection_prompt = ai_facilitator.generate_reflection_prompt("your learning journey")
    return render_template('progress.html', goals=goals, activities=activities, summary=summary,
                           reflection_prompt=reflection_prompt)


@app.route('/log_activity', methods=['POST'])
def log_activity():
    user_id = session.get('user_id', 'anonymous')
    activity_type = request.form.get('type')
    details = request.form.get('details')
    progress_tracker.log_activity(user_id, activity_type, details)
    return jsonify({'success': True})


@app.route('/get_prompt', methods=['POST'])
def get_prompt():
    context = request.json['context']
    user_id = session.get('user_id', 'anonymous')
    user_data = {
        'recent_activities': progress_tracker.get_activities(user_id, limit=1)
    }
    prompt = ai_facilitator.generate_prompt(context, user_data)
    return jsonify({'prompt': prompt})


@app.route('/reflect_on_goal/<int:goal_index>')
def reflect_on_goal(goal_index):
    user_id = session.get('user_id', 'anonymous')
    goals = progress_tracker.get_goals(user_id)
    if goal_index < len(goals):
        goal = goals[goal_index]['description']
        reflection_prompt = ai_facilitator.generate_reflection_prompt(goal)
        return jsonify({'prompt': reflection_prompt})
    else:
        return jsonify({'error': 'Goal not found'}), 404


@app.route('/knowledge_maps')
def knowledge_maps():
    user_id = session.get('user_id', 'anonymous')
    maps = knowledge_mapper.get_user_maps(user_id)
    return render_template('knowledge_maps.html', maps=maps)


@app.route('/create_map', methods=['POST'])
def create_map():
    user_id = session.get('user_id', 'anonymous')
    title = request.json['title']
    map_id = knowledge_mapper.create_map(user_id, title)
    return jsonify({'map_id': map_id})


@app.route('/get_map/<int:map_id>')
def get_map(map_id):
    user_id = session.get('user_id', 'anonymous')
    map_data = knowledge_mapper.get_map(user_id, map_id)
    if map_data:
        return jsonify(map_data)
    return jsonify({'error': 'Map not found'}), 404


@app.route('/add_node', methods=['POST'])
def add_node():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    label = request.json['label']
    x = request.json['x']
    y = request.json['y']
    node_id = knowledge_mapper.add_node(user_id, map_id, label, x, y)
    return jsonify({'node_id': node_id})


@app.route('/add_edge', methods=['POST'])
def add_edge():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    source_id = request.json['source_id']
    target_id = request.json['target_id']
    label = request.json.get('label', '')
    edge_id = knowledge_mapper.add_edge(user_id, map_id, source_id, target_id, label)
    return jsonify({'edge_id': edge_id})


@app.route('/update_node', methods=['POST'])
def update_node():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    node_id = request.json['node_id']
    label = request.json.get('label')
    x = request.json.get('x')
    y = request.json.get('y')
    success = knowledge_mapper.update_node(user_id, map_id, node_id, label, x, y)
    return jsonify({'success': success})


@app.route('/update_edge', methods=['POST'])
def update_edge():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    edge_id = request.json['edge_id']
    label = request.json['label']
    success = knowledge_mapper.update_edge(user_id, map_id, edge_id, label)
    return jsonify({'success': success})


@app.route('/delete_node', methods=['POST'])
def delete_node():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    node_id = request.json['node_id']
    success = knowledge_mapper.delete_node(user_id, map_id, node_id)
    return jsonify({'success': success})


@app.route('/delete_edge', methods=['POST'])
def delete_edge():
    user_id = session.get('user_id', 'anonymous')
    map_id = request.json['map_id']
    edge_id = request.json['edge_id']
    success = knowledge_mapper.delete_edge(user_id, map_id, edge_id)
    return jsonify({'success': success})


@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Process the document and extract text for knowledge base
        process_document(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True}), 200
    return jsonify({'error': 'File type not allowed'}), 400


def process_document(file_path):
    # Implement logic to extract text from PDF or TXT files
    # Store the extracted text in a knowledge base (e.g., database or in-memory)
    pass


if __name__ == '__main__':
    app.run(debug=True)
