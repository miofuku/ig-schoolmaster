from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from universal_book.repository import UniversalBookRepository
from question_generator.generator import QuestionGenerator
from peer_platform.collaboration import PeerCollaborationPlatform
from progress_tracker.tracker import ProgressTracker
from ai_facilitator.facilitator import AIFacilitator
from knowledge_map.mapper import KnowledgeMapper
from datetime import datetime

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
        user_id = session.get('user_id', 'anonymous')
        peer_platform.add_discussion_post(book_id, user_id, content)
        progress_tracker.log_activity(user_id, 'discussion_post', f"Posted in discussion for book {book_id}")

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
    return render_template('study_groups.html', groups=groups, books=book_repo.books)


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
    return render_template('progress.html', goals=goals, activities=activities, summary=summary)


@app.route('/log_activity', methods=['POST'])
def log_activity():
    user_id = session.get('user_id', 'anonymous')
    activity_type = request.form.get('type')
    details = request.form.get('details')
    progress_tracker.log_activity(user_id, activity_type, details)
    return jsonify({'success': True})


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
