from flask import Flask, render_template, request, jsonify, session
from universal_book.repository import UniversalBookRepository
from question_generator.generator import QuestionGenerator
from peer_platform.collaboration import PeerCollaborationPlatform
from progress_tracker.tracker import ProgressTracker
from ai_facilitator.facilitator import AIFacilitator
from knowledge_map.mapper import KnowledgeMapper

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

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
        questions = question_gen.generate_multiple_questions(book, n=3)
        return jsonify({'questions': questions})
    except Exception as e:
        app.logger.error(f"Error generating questions: {str(e)}")
        return jsonify({'error': 'An error occurred while generating questions'}), 500


@app.route('/discuss/<int:book_id>', methods=['GET', 'POST'])
def discuss_book(book_id):
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = session.get('user_id', 'anonymous')  # In a real app, you'd use proper user authentication
        peer_platform.add_discussion_post(book_id, user_id, content)

    book = book_repo.get_book_by_id(book_id)
    posts = peer_platform.get_discussion_posts(book_id)
    return render_template('discuss.html', book=book, posts=posts)


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
    return render_template('study_groups.html', groups=groups)


@app.route('/track_progress', methods=['POST'])
def track_progress():
    goal = request.json['goal']
    progress = progress_tracker.update_progress(goal)
    return jsonify({'progress': progress})


@app.route('/facilitate', methods=['POST'])
def facilitate():
    context = request.json['context']
    prompt = ai_facilitator.generate_prompt(context)
    return jsonify({'prompt': prompt})


@app.route('/map_knowledge', methods=['POST'])
def map_knowledge():
    concepts = request.json['concepts']
    knowledge_map = knowledge_mapper.create_map(concepts)
    return jsonify({'map': knowledge_map})


if __name__ == '__main__':
    app.run(debug=True)
