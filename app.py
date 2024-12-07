from flask import Flask, render_template, request, jsonify, session
from models import db, Book
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from chains.assessment_chain import ConceptVerificationChain
from chains.gap_analysis_chain import KnowledgeGapChain
from agents.verification_agent import LearningVerificationAgent

# Load environment variables
load_dotenv()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_verification.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

    # Initialize database
    db.init_app(app)

    # Initialize LLM and chains
    llm = ChatOpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gpt-4-turbo-preview",
        temperature=0.7
    )

    verification_chains = {
        "concept_verification": ConceptVerificationChain(llm),
        "knowledge_gap": KnowledgeGapChain(llm)
    }
    
    # Initialize verification agent
    app.verification_agent = LearningVerificationAgent(llm, verification_chains)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

# API Routes
@app.route('/api/verify-understanding', methods=['POST'])
async def verify_understanding():
    try:
        data = request.json
        if not data or 'response' not in data or 'concept' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        result = await app.verification_agent.verify_understanding(
            student_response=data['response'],
            concept=data['concept']
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-progress', methods=['POST'])
async def analyze_progress():
    try:
        data = request.json
        if not data or 'history' not in data or 'competencies' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        result = await app.verification_agent.analyze_progress(
            assessment_history=data['history'],
            target_competencies=data['competencies']
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-assessment', methods=['POST'])
async def generate_assessment():
    try:
        data = request.json
        knowledge_area = data['knowledge_area']
        difficulty = data.get('difficulty', 'intermediate')
        
        # Handle optional material upload
        material_context = ""
        if 'material' in request.files:
            file = request.files['material']
            if file and allowed_file(file.filename):
                # Process uploaded material
                material_context = process_material(file)
        
        assessment = await app.knowledge_assessment_chain.arun({
            "knowledge_area": knowledge_area,
            "difficulty": difficulty,
            "optional_material": material_context,
            "assessment_type": data.get('assessment_type', 'comprehensive')
        })
        
        return jsonify({
            'success': True,
            'assessment': assessment,
            'knowledge_area': knowledge_area,
            'difficulty': difficulty
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Web Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

if __name__ == '__main__':
    app.run(debug=True)
