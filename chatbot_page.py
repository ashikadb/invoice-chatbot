import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import tempfile
import random

def show_chatbot_page():
    st.set_page_config(page_title="BillBanter 💸", page_icon="🧾", layout="wide")

    # 🎨 Styling: background color + wider file uploader
    st.markdown(
        """
        <style>
        body, .main {
            background-color: #fff8f0 !important; /* soft peachy tone */
        }

        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #5e548e;
            margin-bottom: 0px;
        }

        .subtitle {
            text-align: center;
            font-size: 1.3em;
            color: #6c757d;
            margin-top: 0px;
            padding-bottom: 15px;
        }

        .custom-uploader .stFileUploader {
            width: 100% !important;
            border: 2px dashed #a594f9;
            background-color: #f0e7ff;
            border-radius: 10px;
            padding: 15px;
        }

        .stTextInput > div > div > input {
            border: 2px solid #c0bcdc;
            border-radius: 10px;
        }

        .stButton>button {
            border-radius: 10px;
            background-color: #9d4edd;
            color: white;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
        }

        .stButton>button:hover {
            background-color: #7b2cbf;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 💬 Header
    st.markdown('<div class="title">💬 BillBanter</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Bring the bill — we’ll roast it together 😎🔥</div>', unsafe_allow_html=True)
    st.write("")

    # 🧾 Upload section — now full width!
    st.markdown('<div class="custom-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Your financial trauma goes here 😭🧾", type="pdf")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        with st.spinner("Invoice is slower than the Gandhipuram signal on a Friday evening 😭📃Grab some sundal and chill while we decode it... 😅"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # 📄 Load and split PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load_and_split()

            # 🔍 Create embeddings and FAISS index
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            db = FAISS.from_documents(documents, embeddings)

        st.success("This file couldn't keep its mouth shut 😂📢")

        # 🔎 Ask something
        user_query = st.text_input("We opened the file... now it's your move. Ask anything! 🎲🧾")

        if user_query:
            with st.spinner("Hold on... this bill has more secrets than a hostel WhatsApp group 👀📱"):
                llm = ChatOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["OPENROUTER_API_KEY"],
                    model="mistralai/mistral-7b-instruct"
                )

                chain = load_qa_chain(llm, chain_type="stuff")
                relevant_docs = db.similarity_search(user_query)
                response = chain.run(input_documents=relevant_docs, question=user_query)

                st.markdown("### 🤖 BillBanter says:")
                st.success(response)

                # 🎉 Funny comment
                funny_comments = [
                    "Wow, that's a spicy total 🌶️💸",
                    "Ohh fancy seller name, sounds expensive! 💼",
                    "Better not miss that date or your wallet will cry 😭📆",
                    "A July baby invoice, how cute 🎂🧾",
                    "Taxed and attacked 💀💰",
                    "Looks like someone’s been shopping 🛍️",
                    "Those numbers aren’t messing around! 🔢😮",
                    "Hope your bank account's ready 😬🏦",
                    "File this one under ‘financial pain’ 📁😅",
                    "Invoice got jokes too 🤡📑"
                ]
                st.markdown(f"**💡 {random.choice(funny_comments)}**")
                st.markdown("_(Going through it like it owes me money 🧐💵)_")

    # ✅ Done Button at the bottom
    st.write("---")
    if st.button("All done ?! Just Click here"):
        st.success(" Hey You!! I hope everything ran smoothly... now be honest — how were my stand-up skills? 😄🎤🔥")
