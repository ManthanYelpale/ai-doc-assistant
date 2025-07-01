import streamlit as st
import requests

#  Page config 
st.set_page_config(page_title="Doc AI Q&A", layout="centered")

#  CSS Styling
#  CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #f7faff;
    }

    .main {
        font-family: 'Segoe UI', sans-serif;
    }

    .title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #222;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .subtext {
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-size: 1rem;
    }

    .box {
        background-color: #fff;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        margin-top: 1rem;
        transition: all 0.3s ease;
    }

    .box:hover {
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        transform: scale(1.01);
        border: 1px solid #e0e0e0;
    }

    .answer {
        font-size: 1.05rem;
        color: #222;
        line-height: 1.6;
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stFileUploader"] button {
        background-color: #4F8EF7 !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #3a75d2 !important;
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        cursor: pointer;
    }

    div.stButton > button {
        background-color: #4F8EF7 !important;
        color: white !important;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    div.stButton > button:hover {
        background-color: #3a75d2;
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
        cursor: pointer;
    }

    section[data-testid="stFileUploader"] {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: #f0f4f8;
        border: 2px dashed #ccc;
        margin-bottom: 1.5rem;
    }

    section[data-testid="stFileUploader"] > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stTextInput"] > div > input {
        padding: 0.7rem 1rem;
        border: 2px solid #ccc !important;
        border-radius: 10px !important;
        font-size: 1rem;
        background-color: #fff !important;
        color: #222 !important;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stTextInput"] > div > input:hover {
        border-color: #4F8EF7 !important;
        box-shadow: 0 0 0 3px rgba(79, 142, 247, 0.1) !important;
    }

    div[data-testid="stTextInput"] > div > input:focus {
        border-color: #4F8EF7 !important;
        box-shadow: 0 0 0 3px rgba(79, 142, 247, 0.3) !important;
        outline: none !important;
    }

    div[data-testid="stTextInput"] > div > input:invalid {
        border: 2px solid #ccc !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .glow-loader {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin-top: 20px;
    }

    .glow-loader div {
        width: 10px;
        height: 10px;
        background: #4F8EF7;
        border-radius: 50%;
        box-shadow: 0 0 10px #4F8EF7;
        animation: glow 1s infinite ease-in-out alternate;
    }

    .glow-loader div:nth-child(2) {
        animation-delay: 0.2s;
    }
    .glow-loader div:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes glow {
        0% {
            transform: scale(1);
            opacity: 0.5;
            box-shadow: 0 0 5px #4F8EF7;
        }
        100% {
            transform: scale(1.6);
            opacity: 1;
            box-shadow: 0 0 20px #4F8EF7;
        }
    }
    </style>
""", unsafe_allow_html=True)



# Title 
st.markdown('<div class="title"> Talk with document using AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Upload a file and ask any question about it!</div>', unsafe_allow_html=True)

# Upload Section 
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv", "xlsx", "pptx"])

# Upload to backend
if uploaded_file is not None:
    with st.spinner("Uploading..."):
        try:
            res = requests.post(
            "https://ai-doc-assistant-34ml.onrender.com/upload/",
            files={"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)},
            timeout=60
    )
            if res.status_code == 200:
                st.success("Document uploaded successfully!")
            else:
                st.error(f"❌ Upload failed: {res.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Upload failed due to connection issue: {e}")


        
        if res.status_code == 200:
            st.success(" Document uploaded successfully!")
        else:
            st.error(f" Upload failed: {res.text}")

#  Question Form 
st.markdown("---")
question = st.text_input(" Ask AI anything about your document")

if st.button("Ask AI"):
    if not uploaded_file:
        st.warning("Please upload a document first.")
    elif question.strip() == "":
        st.warning("Type a question to get started.")
    else:
        with st.spinner("Generating answer..."):
            try:
                res = requests.post("https://ai-doc-assistant-34ml.onrender.com/ask/", data={"question": question}, timeout=60)
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(f'<div class="box answer">{answer}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {res.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to connect to backend: {e}")

