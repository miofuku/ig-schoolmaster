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

4. Run the application:
   ```
   python app.py
   ```

## Usage

After starting the application, you can interact with the virtual teacher by typing your questions or comments. The system will provide personalized responses and additional information based on your learning progress and style.

Example interaction:

```
Student: Can you explain the concept of recursion in programming?

Virtual Teacher: Certainly! Recursion in programming is a technique where a function calls itself to solve a problem by breaking it down into smaller, similar sub-problems. It's like a Russian nesting doll, where each doll contains a smaller version of itself.

Let's look at a simple example:

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

In this factorial function, we're using recursion to calculate the factorial of a number. The function calls itself with a smaller number until it reaches the base case (0 or 1).

Additional Information:
Related concepts you might want to explore:
- Base case
- Call stack
- Recursive data structures
  Prerequisites: Functions, Conditional statements

Was this response helpful? (y/n): 
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License