# Ignorant Schoolmaster AI

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/miofuku/ig-schoolmaster.git
   cd ig-schoolmaster
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python3 app.py
   ```

5. Open a web browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py`: Main application entry point.
- `universal_book/`: Digital library management, including book retrieval and search functionalities.
- `question_generator/`: AI-powered question generation tools for books.
- `peer_platform/`: Peer collaboration and interaction features, including discussion posts and study groups.
- `progress_tracker/`: Self-assessment and goal-setting tools to track user progress.
- `ai_facilitator/`: Minimal AI guidance implementation for generating prompts and questions.
- `knowledge_map/`: Open-ended concept mapping tools for visualizing knowledge.
- `templates/`: HTML templates for the web interface.
- `static/`: CSS and JavaScript files for styling and interactivity.
- `models.py`: Database models for SQLAlchemy, including the `Book` model.
- `config.py`: Configuration settings, including loading environment variables.

## Future Enhancements
- Implement user authentication and profiles.
- Enhance the AI question generation with more context-aware prompts.
- Add more interactive features for discussions and study groups.
- Improve the UI/UX for better user engagement.

## Dependencies
- Flask
- SQLAlchemy
- LangChain (with community and OpenAI support)
- Other libraries listed in `requirements.txt`

## License
MIT License

Copyright (c) 2024 Bijun Li

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
