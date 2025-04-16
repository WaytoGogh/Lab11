import os
import matplotlib.pyplot as plt

# --- File paths ---
DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

# --- Load students ---
students = {}
name_to_id = {}
with open(STUDENTS_FILE, 'r') as f:
    for line in f:
        student_id = line[:3]
        name = line[3:].strip()
        students[student_id] = name
        name_to_id[name] = student_id

# --- Load assignments ---
assignments = {}
name_to_assignment_id = {}
with open(ASSIGNMENTS_FILE, 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = lines[i+1]
        points = int(lines[i+2])
        assignments[aid] = (name, points)
        name_to_assignment_id[name] = aid

# --- Load submissions ---
submissions = {}
for filename in os.listdir(SUBMISSIONS_DIR):
    if filename.endswith('.txt'):
        filepath = os.path.join(SUBMISSIONS_DIR, filename)
        with open(filepath, 'r') as f:
            for line in f:
                student_id, assignment_id, percent = line.strip().split('|')
                percent = float(percent)
                if assignment_id not in submissions:
                    submissions[assignment_id] = {}
                submissions[assignment_id][student_id] = percent

# --- Menu ---
print("1. Student grade")
print("2. Assignment statistics")
print("3. Assignment graph")
choice = input("Enter your selection: ")

# --- Option 1 ---
if choice == "1":
    student_name = input("What is the student's name: ").strip()
    if student_name not in name_to_id:
        print("Student not found")
    else:
        student_id = name_to_id[student_name]
        total_score = 0
        for aid, (aname, points) in assignments.items():
            percent = submissions[aid][student_id]
            total_score += (percent / 100) * points
        grade = round((total_score / 1000) * 100)
        print(f"{grade}%")

# --- Option 2 ---
elif choice == "2":
    assignment_name = input("What is the assignment name: ").strip()
    if assignment_name not in name_to_assignment_id:
        print("Assignment not found")
    else:
        aid = name_to_assignment_id[assignment_name]
        scores = [submissions[aid][sid] for sid in submissions[aid]]
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores)/len(scores))}%")
        print(f"Max: {int(max(scores))}%")

# --- Option 3 ---
elif choice == "3":
    assignment_name = input("What is the assignment name: ").strip()
    if assignment_name not in name_to_assignment_id:
        print("Assignment not found")
    else:
        aid = name_to_assignment_id[assignment_name]
        scores = [submissions[aid][sid] for sid in submissions[aid]]
        plt.hist(scores, bins=10, range=(50, 100), edgecolor='black')
        plt.title(f"Scores for {assignment_name}")
        plt.xlabel("Score (%)")
        plt.ylabel("Number of Students")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()