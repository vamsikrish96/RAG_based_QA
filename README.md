
# RAG_based_QA
A Question Answering API using Retrieval Augmented Generation.

## Libraries Used
- **LangChain**
- **ChromaDB**
- **FastAPI**


## Sample Run Output

Query:  Can you give the skillsets which Vamsi has worked with?

Response:  Vamsi has worked with various programming languages and tools in the field of software systems, including:

- Programming languages: Python, C, C++, SQL, Shell, Matlab, Simulink, Jenkins, Ansible.
- Machine Learning frameworks: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, Flask, HuggingFace, LlamaIndex, LangChain, Cython.
- Time series analysis tools: Git, Slurm, Azure, Apache Airflow, Docker, REST API, CI/CD.

He is also proficient in deployment strategies using software products.

**Time taken to Query and Generate response: 6.04859471321106**



# Time Analysis of Complete Pipeline (seconds)

| Task | Time Taken (seconds) |
|------|----------------------|
| Load LLM model | 0.34 |
| Create database and initialize embedding model | 5.05 |
| Upload PDF | 3.47 |
| Generate response | 3.99 |
| Query and generate response | 6.04 |



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
