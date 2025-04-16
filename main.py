import os
import matplotlib.pyplot as plt

# Data file paths
STUDENTS_FILE = 'data/students.txt'
ASSIGNMENTS_FILE = 'data/assignments.txt'
SUBMISSIONS_FILE = 'data/submissions.txt'

def load_students():
    students = {}
    with open(STUDENTS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                student_id = line[:3]
                student_name = line[3:].strip()
                students[student_name] = student_id
    return students

def load_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as file:
        for line in file:
            name, points, aid = line.strip().rsplit(',', 2)
            assignments[name.strip()] = (aid.strip(), int(points.strip()))
    return assignments

def load_submissions(filepath):
    submissions = {}
    with open(filepath, 'r') as file:
        for line in file:
            sid, aid, percentage = line.strip().split(',')
            key = (sid.strip(), aid.strip())
            submissions[key] = float(percentage.strip())
    return submissions

def option_student_grade(students, assignments, submissions):
    name = input("What is the student's name: ").strip()
    if name not in students:
        print("Student not found")
        return

    sid = students[name]
    total_score = 0

    for assignment_name, (aid, points) in assignments.items():
        key = (sid, aid)
        if key in submissions:
            total_score += submissions[key] * points

    grade_percent = round((total_score / 1000) * 100)
    print(f"{grade_percent}%")

def option_assignment_statistics(assignments, submissions):
    name = input("What is the assignment name: ").strip()
    if name not in assignments:
        print("Assignment not found")
        return

    aid, points = assignments[name]
    scores = []
    for (sid, sub_aid), percent in submissions.items():
        if sub_aid == aid:
            scores.append(percent * 100)

    if scores:
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")
        print(f"Max: {int(max(scores))}%")

def option_assignment_graph(assignments, submissions):
    name = input("What is the assignment name: ").strip()
    if name not in assignments:
        print("Assignment not found")
        return

    aid, points = assignments[name]
    scores = []
    for (sid, sub_aid), percent in submissions.items():
        if sub_aid == aid:
            scores.append(percent * 100)

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Score Distribution for {name}")
    plt.xlabel("Score (%)")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments("data/assignments.txt")
    submissions = load_submissions("data/submissions.txt")

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")

    choice = input("Enter your selection: ").strip()

    if choice == "1":
        option_student_grade(students, assignments, submissions)
    elif choice == "2":
        option_assignment_statistics(assignments, submissions)
    elif choice == "3":
        option_assignment_graph(assignments, submissions)

if __name__ == "__main__":
    main()
