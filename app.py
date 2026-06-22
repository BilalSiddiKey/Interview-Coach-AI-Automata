st.set_page_config(
page_title="Interview Coach AI",
page_icon="🎯",
layout="wide"
)

st.title("🎯 Automata-Based Interview Coach Assistant")

# =========================

# SESSION STATE

# =========================

if "current_state" not in st.session_state:
    st.session_state.current_state = "START"

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None

if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = None

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

# =========================

# MAIN DESCRIPTION

# =========================

st.write("""
This system demonstrates:

* Regular Expressions (RE)
* NFA
* DFA
* DFA Minimization
* Moore Machine
* CFG
* PDA
* Retrieval-Augmented Generation (RAG)

Domains:

* AI / Machine Learning
* Data Science
* Cybersecurity
  """)

# =========================

# SIDEBAR

# =========================

st.sidebar.title("Automata Dashboard")

st.sidebar.write(
f"Current State: {st.session_state.current_state}"
)

st.sidebar.write(
f"Selected Domain: {st.session_state.selected_domain}"
)

st.sidebar.write(
f"Difficulty: {st.session_state.selected_difficulty}"
)

# =========================

# STATE 1: START

# =========================

if st.session_state.current_state == "START":

    st.info(
        "Welcome to the Interview Coach Assistant"
    )

if st.button("Start Interview"):

    st.session_state.current_state = "DOMAIN_SELECTION"

    st.rerun()

# =========================

# STATE 2: DOMAIN SELECTION

# =========================

elif st.session_state.current_state == "DOMAIN_SELECTION":

    st.subheader("Select Interview Domain")

    domain = st.selectbox(
        "Domain",
        [
            "AI/ML",
            "Data Science",
            "Cybersecurity"
        ]
    )

if st.button("Confirm Domain"):

    st.session_state.selected_domain = domain

    st.session_state.current_state = "DIFFICULTY_SELECTION"

    st.rerun()


# =========================

# STATE 3: DIFFICULTY

# =========================

elif st.session_state.current_state == "DIFFICULTY_SELECTION":


    st.subheader("Select Difficulty")

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

if st.button("Confirm Difficulty"):

    st.session_state.selected_difficulty = difficulty

    st.session_state.current_state = "QUESTION_STATE"

    st.rerun()


# =========================

# STATE 4: QUESTION

# =========================

elif st.session_state.current_state == "QUESTION_STATE":

```
st.success(
    f"""
```

Domain: {st.session_state.selected_domain}

Difficulty: {st.session_state.selected_difficulty}
"""
)

```
question = st.text_input(
    "Enter Interview Question"
)

if st.button("Ask Question"):

    if question.strip() == "":
        st.warning(
            "Please enter a question."
        )

    else:

        st.session_state.user_question = question

        st.session_state.current_state = "EVALUATION_STATE"

        st.rerun()
```

# =========================

# STATE 5: EVALUATION

# =========================

elif st.session_state.current_state == "EVALUATION_STATE":

```
question = st.session_state.user_question

st.subheader("Interview Question")

st.write(question)

chunks = retrieve_chunks(
    question
)

context = "\n".join(
    [
        chunk["content"]
        for chunk in chunks
    ]
)

prompt = f"""
```

You are Interview Coach AI.

Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

```
answer = generate_answer(
    prompt
)

st.write("## Answer")

st.write(answer)

st.write("## Sources")

for chunk in chunks:

    st.write(
        chunk["source"]
    )

    st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button("Next Question"):

        st.session_state.current_state = "QUESTION_STATE"

        st.rerun()

with col2:

    if st.button("End Interview"):

        st.session_state.current_state = "INTERVIEW_COMPLETE"

        st.rerun()
```

# =========================

# STATE 6: COMPLETE

# =========================

elif st.session_state.current_state == "INTERVIEW_COMPLETE":

```
st.success(
    "Interview Completed Successfully"
)

st.write(
    f"Domain: {st.session_state.selected_domain}"
)

st.write(
    f"Difficulty: {st.session_state.selected_difficulty}"
)

if st.button("Start New Interview"):

    st.session_state.current_state = "START"

    st.session_state.selected_domain = None

    st.session_state.selected_difficulty = None

    st.session_state.user_question = ""

    st.rerun()
```
