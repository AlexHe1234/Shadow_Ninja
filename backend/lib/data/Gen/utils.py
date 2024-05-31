import os
import json
import csv


def read_json(file_path):
    with open(file_path, 'r') as f:
        json_read = json.load(f)
    return json_read


def save_json(obj, file_path):
    with open(file_path, 'w') as f:
        json.dump(obj, f, indent=4)   
        

def read_txt(file_path):
    with open(file_path, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    return lines    


def read_csv(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data


def extract_data(data_dir):
    student = read_json(os.path.join(data_dir, 'student.json'))
    for i in range(len(student)):
        student[i]['id'] = int(i)
        
    course = read_json(os.path.join(data_dir, 'course.json'))   
    comment = read_json(os.path.join(data_dir, 'comment.json'))
    for i in range(len(course)):
        course[i]['id'] = int(i)   
        assert course[i]['name'] == comment[i]['name']
        comment_list = [list(it.values())[0] for it in comment[i]['comments']]
        course[i]['comment'] = comment_list
        
    return student, course 


if __name__ == '__main__':
    extract_data('./')
