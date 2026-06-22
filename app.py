import streamlit as st
import os
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_models():

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(
        model_name
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name
    )

    return embedding_model, tokenizer, model


embedding_model, tokenizer, model = load_models()

@st.cache_resource
def load_documents():

    documents = []

    data_folder = "data"

    for filename in os.listdir(data_folder):

        if filename.endswith(".pdf"):

            pdf_path = os.path.join(
                data_folder,
                filename
            )

            reader = PdfReader(pdf_path)

            pdf_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    pdf_text += text + "\n"

            documents.append({
                "source": filename,
                "content": pdf_text
            })

    return documents


documents = load_documents()

st.success(
    f"Knowledge Base Loaded: {len(documents)} PDFs"
)

def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks

@st.cache_resource
def create_chunks():

    all_chunks = []

    for doc in documents:

        chunks = chunk_text(
            doc["content"]
        )

        for chunk in chunks:

            all_chunks.append({
                "source": doc["source"],
                "content": chunk
            })

    return all_chunks


all_chunks = create_chunks()

st.info(
    f"Created {len(all_chunks)} chunks"
)

@st.cache_resource
def create_embeddings():

    texts = [
        chunk["content"]
        for chunk in all_chunks
    ]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=False
    )

    return embeddings


embeddings = create_embeddings()



st.success(
    f"Generated {len(embeddings)} embeddings"
)

def retrieve_chunks(question, top_k=3):

    query_embedding = embedding_model.encode(
        [question]
    )[0]

    similarities = np.dot(
        embeddings,
        query_embedding
    )

    top_indices = np.argsort(
        similarities
    )[-top_k:][::-1]

    retrieved_chunks = []

    for idx in top_indices:

        retrieved_chunks.append(
            all_chunks[idx]
        )

    return retrieved_chunks

def generate_answer(prompt):

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=200
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

st.set_page_config(
    page_title="Interview Coach AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Interview Coach AI")

if "current_state" not in st.session_state:
    st.session_state.current_state = "START"

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None

if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = None

if "user_question" not in st.session_state:
    st.session_state.user_question = ""


st.write("""
Ask interview questions across:

- Software Engineering
- Databases
- AI / Machine Learning
- Data Science
- Cyber Security
- Cloud & DevOps
""")

st.sidebar.title("Automata Dashboard")

st.sidebar.write(
    f"Current State: {st.session_state.current_state}"
)

st.sidebar.write(
    f"Domain: {st.session_state.selected_domain}"
)

st.sidebar.write(
    f"Difficulty: {st.session_state.selected_difficulty}"
)


if st.session_state.current_state == "START":

    if st.button("Start Interview"):

        st.session_state.current_state = "DOMAIN_SELECTION"

        st.rerun()

if st.session_state.current_state == "DOMAIN_SELECTION":

    domain = st.selectbox(
        "Select Domain",
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


if st.session_state.current_state == "DIFFICULTY_SELECTION":

    difficulty = st.selectbox(
        "Select Difficulty",
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

if st.session_state.current_state == "QUESTION_STATE":

    st.success(
        f"""
Domain:
{st.session_state.selected_domain}

Difficulty:
{st.session_state.selected_difficulty}
"""
    )

    question = st.text_input(
        "Enter Interview Question"
    )

    if st.button("Ask"):

        st.session_state.current_state = "EVALUATION_STATE"

        st.session_state.user_question = question

        st.rerun()

if st.session_state.current_state == "EVALUATION_STATE":

    question = st.session_state.user_question

    chunks = retrieve_chunks(question)

    context = "\n".join(
        [
            chunk["content"]
            for chunk in chunks
        ]
    )

    prompt = f"""
You are Interview Coach AI.

Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate_answer(prompt)

    st.write("## Answer")

    st.write(answer)

    st.write("## Sources")

    for chunk in chunks:

        st.write(chunk["source"])

        st.divider()

    if st.button("Next Question"):

        st.session_state.current_state = "QUESTION_STATE"

        st.rerun()

    if st.button("End Interview"):

        st.session_state.current_state = "INTERVIEW_COMPLETE"

        st.rerun()


if st.session_state.current_state == "INTERVIEW_COMPLETE":

    st.success(
        "Interview Completed Successfully"
    )

    st.write(
        f"Domain: {st.session_state.selected_domain}"
    )

    st.write(
        f"Difficulty: {st.session_state.selected_difficulty}"
    )
