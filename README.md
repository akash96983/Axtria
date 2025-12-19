# Axtria Chat Bot

A state-of-the-art AI-powered chatbot designed to provide accurate information based on drug documentation and excel data.

## Features

- **Context-Aware Conversations**: Handles follow-up questions by maintaining session context.
- **Intelligent Routing**: Automatically routes queries to document-based or excel-based lookup.
- **Modern UI**: Sleek, responsive interface built with React and Tailwind CSS.
- **Document Lookup**: Retrieves quantitative and qualitative data from Word documents.
- **Excel Analysis**: Powerful data retrieval from structured Excel files.

## Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS, Framer Motion, Lucide React.
- **Backend**: FastAPI (Python), Pandas, Docx, thefuzz (fuzzy matching).

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the root directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Testing

### Backend Tests
Run the provided test scripts to verify logic:
```bash
python backend/test_context.py
python backend/test_excel.py
python backend/test_router.py
```

## Security Note
Ensure that `.env` files and the `venv` directory are never pushed to the repository.
