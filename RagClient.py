import requests
import time
BASE_URL = "http://localhost:8000"


def upload_pdf(file_path):
    """Uploads a PDF file to the API."""
    url = f"{BASE_URL}/upload/"
    
    response = requests.post(url, json={"file_path": file_path})
    print("Upload Response:", response.json()['message'])


def query_knowledge_base(query_text):
    """Sends a query to the knowledge base and retrieves an answer."""
    url = f"{BASE_URL}/query/"
    payload = {"query": query_text, "debug": True}
    response = requests.post(url, json=payload)
    return response.json()

def check_api_status():
    """Checks if the API is running."""
    url = f"{BASE_URL}/"
    
    response = requests.get(url)
    print("API Status:", response.json())


if __name__ == "__main__":
    check_api_status()
    # Step 1: Upload a PDF file or directory containing PDF files
    pdf_path = r"Resume_VamsikrishnaChemudupati.pdf"  # Replace with your actual file path

    start_time = time.time()
    upload_pdf(pdf_path)
    print("Time taken to upload PDF:", time.time() - start_time)
    print("\n**********************************\n")
    # Step 2: Query the Knowledge Base
    start_time = time.time()
    query_text = "Can you give the skillsets which Vamsi has worked with?"
    print("Query: ", query_text)
    response = query_knowledge_base(query_text)
    print("Response: ", response["response"])

    print("Time taken to Query and Generate response:", time.time() - start_time)
    print("\n**********************************\n")

    