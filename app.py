import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load environment variables securely from a hidden local file
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 1. Page Configuration & Custom CSS Injection for High-End Branding
st.set_page_config(page_title="Aura Style AI Live Support", page_icon="🛍️", layout="wide")

# Inject structural overrides to mirror a real mobile WhatsApp thread layout
st.markdown("""
    <style>
    /* Clean, modern background styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* System Health Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #4A00E0 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
    }
    
    /* Suggestion Pills / Quick-Click Buttons */
    .stButton>button {
        border-radius: 12px !important;
        border: 2px solid #8E2DE2 !important;
        background: #FFFFFF !important;
        color: #4A00E0 !important; 
        font-weight: 700 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        color: #FFFFFF !important; 
        background: linear-gradient(to right, #8E2DE2, #4A00E0) !important;
        box-shadow: 0 6px 12px rgba(74, 0, 224, 0.2) !important;
    }
    
    /* FORCE chat text to maintain explicit high-contrast readability rules */
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span {
        color: #1A1A2E !important; 
        font-weight: 500 !important;
        margin: 0 !important;
    }

    /* Base row alignment overrides to separate left and right message lines */
    div[data-testid="stChatMessageContainer"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
    }

    /* ── USER BUBBLE: WHATSAPP OUTGOING STYLE (RIGHT) ── */
    div[data-testid="stChatMessageUser"] {
        background-color: #E3F2FD !important; /* Soft messaging blue */
        border: 1px solid #B39DDB !important;
        border-radius: 16px 16px 0px 16px !important; /* WhatsApp curved edge cornering */
        padding: 12px 18px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        
        /* Force alignment to wrap to content length and anchor to the right */
        align-self: flex-end !important;
        max-width: 65% !important;
        width: auto !important;
        
        /* Flips the structure so content loads cleanly toward the right boundary */
        flex-direction: row-reverse !important;
    }

    /* ── ASSISTANT BUBBLE: WHATSAPP INCOMING STYLE (LEFT) ── */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #FFFFFF !important; /* Clean bubble white */
        border: 1px solid #E0E4EC !important;
        border-radius: 16px 16px 16px 0px !important; /* WhatsApp curved edge cornering */
        padding: 12px 18px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
        
        /* Force layout to stick left */
        align-self: flex-start !important;
        max-width: 65% !important;
        width: auto !important;
        
        flex-direction: row !important;
    }
    
    /* Force user writing bar text to be crisp and clear */
    div[data-testid="stChatInput"] textarea {
        color: #1A1A2E !important;
        background-color: #FFFFFF !important;
    }
    
    /* Main branding gradient dashboard block banner */
    .main-banner {
        background: linear-gradient(to right, #8E2DE2, #4A00E0);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(74, 0, 224, 0.15);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Administration Panel
with st.sidebar:
    st.markdown("<h2 style='color: #4A00E0; font-weight:700;'>🏬 Aura Control</h2>", unsafe_allow_html=True)
    st.caption("Enterprise AI Agent Management Matrix")
    st.divider()
    
    # Colorful Simulated Performance Metrics
    st.markdown("#### 📊 System Health")
    col_metrics1, col_metrics2 = st.columns(2)
    with col_metrics1:
        st.metric(label="RAG Latency", value="142ms", delta="-12ms")
    with col_metrics2:
        st.metric(label="System Accuracy", value="99.4%", delta="0.2%")
        
    st.divider()
    st.markdown("#### 📄 Connected Knowledge Bases")
    st.success("✅ `store_policies.txt` (Active Index)")
    
    st.divider()
    # Reset Conversation Button Execution
    if st.button("🔄 Clear Active Session"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your Aura Style support assistant. How can I assist you with your shipping, tracking, or refund inquiry today?"}
        ]
        st.rerun()

# 3. Main Data Infrastructure Initializer
@st.cache_resource
def initialize_knowledge_base():
    try:
        loader = TextLoader("store_policies.txt")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        final_documents = text_splitter.split_documents(docs)
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        vector_store = FAISS.from_documents(final_documents, embeddings)
        return vector_store.as_retriever(search_kwargs={"k": 2})
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return None

retriever = initialize_knowledge_base()

if retriever:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    system_prompt = (
        "You are a professional, helpful customer service AI assistant for the Aura Style e-commerce store.\n"
        "Answer the user's questions utilizing exclusively the provided context below. "
        "If you do not know the answer based on the context, politely state that you do not know and advise "
        "them to email support@aurastyle.com.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Colorful Main Center View Header UI Layout
    st.markdown("""
        <div class='main-banner'>
            <h1 style='color: white; margin: 0; font-weight: 800;'>🛍️ Aura Style Interactive Support Engine</h1>
            <p style='color: #E0D5FF; margin: 5px 0 0 0; font-size: 1.1rem;'>Next-Gen Conversational RAG Engine Prototype for Retail Brands</p>
        </div>
    """, unsafe_allow_html=True)

    # Conversation Session State Matrix Initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your Aura Style support assistant. How can I assist you with your shipping, tracking, or refund inquiry today?"}
        ]

    # 4. Interactive Quick-Click Suggestion Tokens Area
    st.markdown("<p style='font-weight: 600; color: #4A00E0; margin-bottom: 5px;'>⚡ Quick-Click Inquiries:</p>", unsafe_allow_html=True)
    suggest_col1, suggest_col2, suggest_col3 = st.columns(3)
    
    click_query = None
    with suggest_col1:
        if st.button("✈️ International Delivery Times"):
            click_query = "What are the rules and timelines for international shipping?"
    with suggest_col2:
        if st.button("📦 How to Track Orders"):
            click_query = "How can I track my package?"
    with suggest_col3:
        if st.button("💰 Return and Sale Policy"):
            click_query = "Can I return an item bought on final sale?"

    st.divider()

    # Wrap messages inside a strict flex layout tag block
    st.markdown("<div data-testid='stChatMessageContainer'>", unsafe_allow_html=True)

    # Render Active Messaging Stream UI
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    st.markdown("</div>", unsafe_allow_html=True)

    # Collect Input via regular text bar or suggestion tokens
    user_query = st.chat_input("Type your store policy query here...")
    if click_query:
        user_query = click_query

    # 5. Process and Display Runtime Query Operations
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
        if {"role": "user", "content": user_query} not in st.session_state.chat_history:
            st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            with st.spinner("Querying vector neural index..."):
                try:
                    response = rag_chain.invoke({"input": user_query})
                    answer = response["answer"]
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    if click_query:
                        st.rerun()
                except Exception as e:
                    st.error(f"Execution API latency anomaly: {e}")