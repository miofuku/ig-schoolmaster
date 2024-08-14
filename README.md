# The Ignorant Schoolmaster

The Ignorant Schoolmaster is an AI-powered virtual teaching assistant inspired by [Jacques Rancière](https://en.wikipedia.org/wiki/Jacques_Ranci%C3%A8re)'s book of the same name. This project aims to create a personalized learning experience by combining the power of large language models with knowledge graphs and adaptive learning techniques.

## Features

- GPT-Neo-based language model for natural conversations
- Knowledge graph integration for concept relationships
- Personalized tutoring based on individual learning pace and style
- Continuous learning and adaptation through user feedback
- Additional information and learning path suggestions

## Getting Started

### Prerequisites

- Python 3.7+
- PyTorch
- Transformers
- NetworkX

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ig-schoolmaster.git
   cd ig-schoolmaster
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Prepare your data:
   - Add your course content to `data/course_content.txt`
   - Create a Q&A dataset in `data/course_qa.json`
   - Prepare your knowledge graph in `data/knowledge_graph.json`

4. Train the model with provided data:
   ```
   python train.py
   ```

4. Run the application with trained model:
   ```
   python app.py
   ```

## Usage

After starting the application, you can interact with the virtual teacher by typing your questions or comments. The system will provide personalized responses and additional information based on your learning progress and style.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
