import json

def load_course_data(content_file, qa_file):
    with open(content_file, 'r') as f:
        course_content = f.read()
    with open(qa_file, 'r') as f:
        course_qa = json.load(f)
    return course_content, course_qa