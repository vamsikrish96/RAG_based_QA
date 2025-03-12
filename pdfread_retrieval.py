import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def ReadPdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def GetDocuments(pdf_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(pdf_text)
    # Convert the chunks to Document objects so the LangChain framework can process them.
    documents = [Document(page_content=t) for t in chunks]
    return documents

class VectorDB:
    def __init__(self, embedding_model, collection_directory, collection_name):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.db = Chroma(embedding_function=self.embeddings, persist_directory=collection_directory, collection_name=collection_name)
        self.indexed_files = set()

    def AddFilesChromaDB(self, documents):
        #Add the documents to the database
        try:
            self.db.add_documents(documents)
            return "success"

        except Exception as e:
            print(f"Error adding documents to ChromaDB: {str(e)}")
            return "error"
    
    def CheckDuplicates(self, file_path):
        if file_path in self.indexed_files:
            return True
        return False
    
    def GetDatabaseObj(self):
        return self.db