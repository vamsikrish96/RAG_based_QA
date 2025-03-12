
# RAG_based_QA
A Question Answering API using Retrieval Augmented Generation.

## Libraries Used
- **LangChain**
- **ChromaDB**
- **FastAPI**

## Steps to Run

1. **Install the required dependencies** in a virtual environment (Conda or venv):

   ```bash
   pip install -r requirements.txt
   ```

2. **Activate the virtual environment**.

3. **Start the RAG Server** in one terminal:

   ```bash
   python RagServer.py
   ```

4. **Run the RAG Client** in another terminal to see the question answering bot in action:

   ```bash
   python RagClient.py
   ```

## Running Unit Tests

If making any changes, please ensure the unit tests pass before committing:

1. Run the unit tests:

   ```bash
   python unittest_RAG.py
   ```
