import requests

BASE_URL = "http://localhost:8000"


def upload_pdf(file_path):
    """Uploads a PDF file to the API."""
    url = f"{BASE_URL}/upload/"
    
    response = requests.post(url, json={"file_path": file_path})
    print("Upload Response:", response.json())


def query_knowledge_base(query_text):
    """Sends a query to the knowledge base and retrieves an answer."""
    url = f"{BASE_URL}/query/"
    payload = {"query": query_text, "debug": True}
    response = requests.post(url, json=payload)
    print("Query Response:", response.json())


def check_api_status():
    """Checks if the API is running."""
    url = f"{BASE_URL}/"
    
    response = requests.get(url)
    print("API Status:", response.json())


if __name__ == "__main__":
    check_api_status()
    # Step 1: Upload a PDF file
    pdf_path = r"C:\Users\chemu\Downloads\Resume_VamsikrishnaChemudupati.pdf"  # Replace with your actual file path
    upload_pdf(pdf_path)
    print("\n**********************************\n")
    # Step 2: Query the Knowledge Base
    query_text = "Can you give the skillsets which Vamsi has worked with?"
    query_knowledge_base(query_text)
    print("\n**********************************\n")

    # Step 3: Check API Status
    