import streamlit as st
import json
import pandas as pd
from io import BytesIO

# Data Storage
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = []
if 'progress' not in st.session_state:
    st.session_state['progress'] = {}
if 'streak' not in st.session_state:
    st.session_state['streak'] = 0
if 'points' not in st.session_state:
    st.session_state['points'] = 0
if 'challenges' not in st.session_state:
    st.session_state['challenges'] = {}
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
if 'challenge_responses' not in st.session_state:
    st.session_state['challenge_responses'] = {}

# Home Page
st.title("🚀 Learning Growth Management System")
st.subheader("Track your learning progress, complete challenges, and manage tasks effectively!")

# Sidebar - User Information
st.sidebar.header("📌 User Information")
name = st.sidebar.text_input("Enter your Name")
email = st.sidebar.text_input("Enter your Email")
fields = ["Web Development", "AI", "Data Science", "Cybersecurity"]
field = st.sidebar.selectbox("Select Your Field", fields)

# Saving User Data
if st.sidebar.button("Save Info"):
    user_entry = {"name": name, "email": email, "field": field}
    st.session_state['user_data'].append(user_entry)
    st.sidebar.success("User Info Saved!")

syllabus = {
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "AI": ["Python", "TensorFlow", "PyTorch", "Deep Learning"],
    "Data Science": ["Python", "Pandas", "NumPy", "Scikit-learn"],
    "Cybersecurity": ["Network Security", "Ethical Hacking", "Cryptography"]
}

selected_languages = syllabus.get(field, [])
language = st.sidebar.radio("Select Language", selected_languages)

# Roadmap Display
st.subheader(f"🎯 Learning Path for {field} ({language})")

roadmaps = {
        "HTML": ["Introduction", "Basic Tags", "Forms & Tables", "SEO Optimization"],
    "CSS": ["Selectors", "Flexbox", "Grid", "Animations"],
    "JavaScript": ["Syntax", "ES6", "DOM Manipulation", "Frameworks"],
    "React": ["JSX & Components", "State & Props", "Hooks", "Routing"],
    "Node.js": ["Modules", "Express.js", "Middleware", "Database Connectivity"],
    "Python": ["Basics", "Data Structures", "OOP", "Advanced Concepts"],
    "TensorFlow": ["Tensors", "Neural Networks", "CNNs", "RNNs"],
    "PyTorch": ["Tensors", "Autograd", "Neural Networks", "Training Models"],
    "Deep Learning": ["Neurons & Perceptrons", "Activation Functions", "Backpropagation", "Optimization"],
    "Pandas": ["DataFrames", "Series", "Data Cleaning", "Visualization"],
    "NumPy": ["Arrays", "Indexing", "Broadcasting", "Linear Algebra"],
    "Scikit-learn": ["Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Hyperparameter Tuning"],
    "Network Security": ["Firewalls", "Encryption", "Pentesting", "Incident Response"],
    "Ethical Hacking": ["Reconnaissance", "Exploitation", "Post-Exploitation", "Security Hardening"],
    "Cryptography": ["Symmetric Encryption", "Asymmetric Encryption", "Hashing", "Digital Signatures"]
}

progress = 0
if language in roadmaps:
    for index, step in enumerate(roadmaps[language]):
        completed = st.checkbox(f"{step}", key=f"{language}_{index}")
        if completed:
            progress += 1
    
    st.progress(progress / len(roadmaps[language]))
    if progress == len(roadmaps[language]):
        st.success("🌟 Congratulations! You have completed this roadmap!")
        st.session_state['points'] += 50
    else:
        st.info("Keep going! Every step counts.")

# Streak & Points System
if progress > 0:
    st.session_state['points'] += 10

st.sidebar.metric("🏆 Total Points", f"{st.session_state['points']}")

# Challenges Section
st.subheader("💡 Challenges")
questions = {
        "HTML": [
        {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "Hyperlink Text Model Language"], "answer": "Hyper Text Markup Language"},
        {"question": "Which tag is used for a hyperlink?", "options": ["<a>", "<link>", "<href>", "<url>"], "answer": "<a>"}
    ],
    "CSS": [
        {"question": "Which property is used to change text color?", "options": ["color", "font-color", "text-color"], "answer": "color"},
        {"question": "Which display property creates a flex container?", "options": ["block", "inline", "flex", "grid"], "answer": "flex"}
    ],
    "JavaScript": [
        {"question": "What is 'typeof null' in JavaScript?", "options": ["object", "null", "undefined", "number"], "answer": "object"},
        {"question": "Which keyword is used to declare variables?", "options": ["var", "let", "const", "All of the above"], "answer": "All of the above"}
    ],
    "React": [
        {"question": "What is JSX?", "options": ["A syntax extension", "A CSS preprocessor", "A database query language"], "answer": "A syntax extension"},
        {"question": "Which hook is used for state management?", "options": ["useState", "useEffect", "useContext"], "answer": "useState"}
    ],
    "Node.js": [
        {"question": "Which module is used for creating a server?", "options": ["http", "fs", "express"], "answer": "http"},
        {"question": "Which command installs Express.js?", "options": ["npm install express", "node install express", "express create"], "answer": "npm install express"}
    ],
    "Python": [
        {"question": "What is the output of print(2**3)?", "options": [6, 8, 9, 12], "answer": 8},
        {"question": "Which library is used for DataFrames in Python?", "options": ["NumPy", "Pandas", "Matplotlib", "TensorFlow"], "answer": "Pandas"},
    ],
    "TensorFlow": [
        {"question": "What is a Tensor in TensorFlow?", "options": ["A type of variable", "A multi-dimensional array", "A deep learning model"], "answer": "A multi-dimensional array"},
        {"question": "Which function is used to define a sequential model?", "options": ["tf.model()", "tf.keras.Sequential()", "tf.create_model()"], "answer": "tf.keras.Sequential()"}
    ],
    "PyTorch": [
        {"question": "Which module in PyTorch is used for automatic differentiation?", "options": ["torch.tensor", "torch.autograd", "torch.nn"], "answer": "torch.autograd"},
        {"question": "Which function is used to move a tensor to GPU?", "options": [".cuda()", ".gpu()", ".to_device()"], "answer": ".cuda()"}
    ],
    "Deep Learning": [
        {"question": "What is the purpose of an activation function?", "options": ["To initialize weights", "To introduce non-linearity", "To store training data"], "answer": "To introduce non-linearity"},
        {"question": "Which type of neural network is best for image processing?", "options": ["RNN", "CNN", "GAN"], "answer": "CNN"}
    ],
    "Pandas": [
        {"question": "Which data structure does Pandas use for tabular data?", "options": ["DataFrame", "Series", "Array"], "answer": "DataFrame"},
        {"question": "Which function is used to read a CSV file?", "options": ["pd.read_csv()", "pd.load_csv()", "pd.open_csv()"], "answer": "pd.read_csv()"}
    ],
    "NumPy": [
        {"question": "Which function creates a NumPy array?", "options": ["np.array()", "np.create()", "np.make_array()"], "answer": "np.array()"},
        {"question": "Which function is used for matrix multiplication?", "options": ["np.multiply()", "np.dot()", "np.matmul()"], "answer": "np.matmul()"}
    ],
    "Scikit-learn": [
        {"question": "Which module is used for classification algorithms?", "options": ["sklearn.linear_model", "sklearn.tree", "sklearn.svm"], "answer": "sklearn.svm"},
        {"question": "Which function is used to split data into training and testing sets?", "options": ["train_test_split()", "split_data()", "data_partition()"], "answer": "train_test_split()"}
    ],
    "Network Security": [
        {"question": "What is a firewall used for?", "options": ["Blocking unauthorized access", "Encrypting data", "Detecting viruses"], "answer": "Blocking unauthorized access"},
        {"question": "Which protocol is used for secure web browsing?", "options": ["HTTP", "FTP", "HTTPS", "SSH"], "answer": "HTTPS"}
    ],
    "Ethical Hacking": [
        {"question": "What is the first phase of hacking?", "options": ["Scanning", "Reconnaissance", "Exploitation"], "answer": "Reconnaissance"},
        {"question": "Which tool is used for penetration testing?", "options": ["Metasploit", "Wireshark", "Nmap"], "answer": "Metasploit"}
    ],
    "Cryptography": [
        {"question": "Which algorithm is used in symmetric encryption?", "options": ["AES", "RSA", "SHA-256"], "answer": "AES"},
        {"question": "What is the purpose of hashing?", "options": ["Encrypt data", "Generate unique fingerprint", "Secure a network"], "answer": "Generate unique fingerprint"}
    ]
}

if language in questions:
    total_questions = len(questions[language])
    correct = 0
    
    for i, q in enumerate(questions[language]):
        st.write(f"**Q{i+1}: {q['question']}**")
        answer = st.radio("Options", q["options"], key=f"q_{i}_{language}")
        submit = st.button(f"Submit Answer {i+1}", key=f"sub_{i}_{language}")
        
        if submit:
            if language not in st.session_state['challenge_responses']:
                st.session_state['challenge_responses'][language] = [{}]*total_questions
            
            is_correct = answer == q["answer"]
            response = {
                "question": q["question"],
                "user_answer": answer,
                "correct_answer": q["answer"],
                "is_correct": is_correct
            }
            st.session_state['challenge_responses'][language][i] = response
            
            if is_correct and not st.session_state['challenge_responses'][language][i].get('points_awarded'):
                st.session_state['points'] += 20
                st.session_state['challenge_responses'][language][i]['points_awarded'] = True
        
        response = st.session_state['challenge_responses'][language][i] if language in st.session_state['challenge_responses'] and i < len(st.session_state['challenge_responses'][language]) else {}
        if response:
            if response['is_correct']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Correct answer: {response['correct_answer']}")

    # Calculate status
    responses = st.session_state['challenge_responses'].get(language, [])
    correct = sum(1 for r in responses if isinstance(r, dict) and r.get('is_correct'))
    
    if correct == total_questions:
        status = "Pro"
    elif correct > 0:
        status = "In Progress"
    else:
        status = "Need Progress"

# Task Management System
st.subheader("🏆 Task Management")
task_name = st.text_input("Enter Task Name")
if st.button("Save Task"):
    if name and email:
        st.session_state['tasks'].append({
            "name": name,
            "email": email,
            "task": task_name,
            "status": status
        })
        st.success("Task Saved Successfully!")
    else:
        st.error("Please enter name and email in sidebar")

if st.session_state['tasks']:
    st.write("### User Tasks")
    st.table(pd.DataFrame(st.session_state['tasks']))

# Leaderboard
st.subheader("📌 Data Management")
leaderboard = sorted(st.session_state['user_data'], key=lambda x: x.get('score', 0), reverse=True)
st.table(leaderboard)

# Download Functionality
st.subheader("📥 Download Data")

def convert_df(df, format):
    if format == "csv":
        return df.to_csv(index=False).encode('utf-8')
    elif format == "json":
        return json.dumps(df.to_dict(orient='records')).encode('utf-8')
    elif format == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

# Combined Data Download
if 'task_responses' in st.session_state or 'challenge_responses' in st.session_state:
    combined_data = []
    
    # Process Task Management Data
    if 'task_responses' in st.session_state:
        for lang, responses in st.session_state['task_responses'].items():
            for resp in responses:
                if isinstance(resp, dict):
                    combined_data.append({
                        "Category": "Task Management",
                        "Name": name,
                        "Email": email,
                        "Language": lang,
                        "Question": resp.get('question', ''),
                        "User Answer": resp.get('user_answer', ''),
                        "Correct Answer": resp.get('correct_answer', ''),
                        "Is Correct": resp.get('is_correct', False)
                    })
    
    # Process Data Management (Challenge) Data
    if 'challenge_responses' in st.session_state:
        for lang, responses in st.session_state['challenge_responses'].items():
            for resp in responses:
                if isinstance(resp, dict):
                    combined_data.append({
                        "Category": "Data Management",
                        "Name": name,
                        "Email": email,
                        "Language": lang,
                        "Question": resp.get('question', ''),
                        "User Answer": resp.get('user_answer', ''),
                        "Correct Answer": resp.get('correct_answer', ''),
                        "Is Correct": resp.get('is_correct', False)
                    })

    if combined_data:
        combined_df = pd.DataFrame(combined_data)
        
        # Format selection
        export_format = st.radio("Select Download Format:", 
                               ("CSV", "Excel", "JSON"),
                               horizontal=True)
        
        # Convert data based on selected format
        converted_data = convert_df(combined_df, export_format.lower())
        
        # Set MIME types and file extension
        mime_type = {
            "CSV": "text/csv",
            "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "JSON": "application/json"
        }[export_format]
        
        file_extension = export_format.lower()
        
        # Single download button
        st.download_button(
            label=f"Download Combined Data ({export_format})",
            data=converted_data,
            file_name=f"combined_data.{file_extension}",
            mime=mime_type
        )