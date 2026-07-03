# Next-Gen E-Commerce Storefront with Integrated RAG AI Assistant 🛍️

A production-ready, highly responsive e-commerce web application prototype optimized with automated lifestyle photo carousels, dynamic horizontal text marquees, a Single Page Application (SPA) multi-page view switcher, and an embedded WhatsApp-style custom AI support chatbot.

This project demonstrates a fully decoupled, data-driven full-stack architecture where store product data and conversational knowledge bases are managed independently of the front-end layout elements.

---

## 🚀 Key Technical Features
- **Dynamic SPA Navigation Framework:** Built a seamless view-switching matrix that transitionally swaps the main grid catalog view for an in-depth product information layout on the fly, entirely client-side.
- **Hardware-Accelerated Layout Systems:** Engineered a CSS keyframe-driven header carousel banner and an infinite horizontal announcer marquee top bar, running completely free of execution lag.
- **Context-Grounded Customer Support Chatbot (RAG):** Implemented a Retrieval-Augmented Generation conversational interface trained dynamically on unstructured store policies. It strictly enforces boundary constraints to completely eliminate hallucinations.
- **Free-Tier Neural Infrastructure Routing:** Scaled the vector search pipeline to use the `gemini-embedding-001` model for parsing local `FAISS` vector stores and deployed the generation tasks over the fast `gemini-2.5-flash` engine via Google AI Studio.
- **Sleek Custom Chat Styling (WhatsApp-Inspired):** Applied custom CSS overrides to construct a responsive mobile message bubble design layout, featuring right-aligned content-length matched customer text blocks and left-anchored assistant cards.

---

## 🛠️ The Technical Stack
- **Frontend Core:** HTML5, CSS3 (Flexbox & Keyframe Animations), Vanilla JavaScript (ES6+ Layout Switchers)
- **AI Core Framework:** Python 3.10+, LangChain Orchestration Core, LangChain-Google-GenAI Integration
- **Vector Storage Platform:** FAISS (Facebook AI Similarity Search)
- **LLM Base Architecture:** Google Gemini Studio Pro API (`gemini-2.5-flash` & `gemini-embedding-001`)
- **Dashboard Interface UI:** Streamlit Web Server Layout Matrix

---

## ⚙️ Project Folder Tree Map
```text
├── .venv/                     # Local Python binary dependencies (Ignored by Git)
├── js/
│   └── app.bundle.js          # Main decoupled JavaScript bundle orchestrator
├── app.py                     # Python RAG pipeline vector retrieval backend script
├── index.html                 # Main frontend storefront application interface canvas
├── .env                       # Local private API authorization tokens (Securely Ignored)
├── .gitignore                 # Safe system architecture ignore configurations
├── store_policies.txt         # Unstructured raw document data text knowledge base
└── README.md                  # Comprehensive technical overview markdown file
