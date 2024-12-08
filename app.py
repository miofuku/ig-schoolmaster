from flask import Flask, render_template, request, jsonify, session
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents.verification_agent import LearningVerificationAgent
from chains.knowledge_assessment_chain import KnowledgeAssessmentChain
from chains.misconception_chain import MisconceptionDetectionChain
from chains.depth_analysis_chain import KnowledgeDepthChain

# Load environment variables
load_dotenv()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_material(file):
    """Process uploaded file and extract text content."""
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        reader = PdfReader(file)
        return ' '.join(page.extract_text() for page in reader.pages)
    return ""

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

    # Initialize LLM and chains
    llm = ChatOpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    verification_chains = {
        "misconception_detection": MisconceptionDetectionChain(llm),
        "depth_analysis": KnowledgeDepthChain(llm),
        "knowledge_assessment": KnowledgeAssessmentChain(llm)
    }
    
    # Initialize verification agent
    app.verification_agent = LearningVerificationAgent(llm, verification_chains)
    app.knowledge_assessment_chain = verification_chains["knowledge_assessment"]

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

@app.route('/api/analyze-trends', methods=['POST'])
async def analyze_trends():
    try:
        data = request.json
        if not data or 'subject' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        subject_context = app.context_manager.get_subject_context(data['subject'])
        trend_analysis = await app.verification_agent.analyze_learning_trends(subject_context)
        
        return jsonify({
            'success': True,
            'trends': trend_analysis
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

@app.route('/trends')
def trends_dashboard():
    return render_template('trends.html')

if __name__ == '__main__':
    app.run(debug=True)
