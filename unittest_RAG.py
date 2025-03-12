import unittest
from pdfread_retrieval import ReadPdf, GetDocuments, VectorDB
from langchain.chains import RetrievalQA
from genmodel import GenerativeModel
import os
import shutil

# Database tests not running in Github CI. Please use local host and make GITHUBCI is False
GITHUBCI = True

if not GITHUBCI:
    print("Cleaning up previous DB")
    if os.path.exists("./pdf_collection"):
        shutil.rmtree("./pdf_collection")
    #Initializing the Database and LLM model
    database = VectorDB("sentence-transformers/all-mpnet-base-v2","./pdf_collection","pdf_collection")
    llm = GenerativeModel(r"llama3.2:1b")

def CheckKeyWords(text):
    """
    Check if the text contains the keywords
    """
    keywords = ["Python", "C++"]
    for keyword in keywords:
        if keyword not in text:
            return False
    return True

class TestRAGPipeline(unittest.TestCase):
    
    def testRAG(self):
        # Sample Data
        if not GITHUBCI:
            file_path = r"Resume_VamsikrishnaChemudupati.pdf"
            query = "Can you give the skillsets which Vamsi has worked with?"
            
            self.assertEqual(database.CheckDuplicates(file_path), False)
            # Execute functions
            pdf_text = ReadPdf(file_path)
            self.assertIsInstance(pdf_text, str, "PDF text should be a string")
            
            documents = GetDocuments(pdf_text)
            self.assertIsInstance(documents, list, "Documents should be a list")
            self.assertGreater(len(documents), 0, "Documents list should not be empty")
            db_status = database.AddFilesChromaDB(documents)
            self.assertEqual(db_status, "success", "Database status should be success")
            db = database.GetDatabaseObj()
            retriever = db.as_retriever(search_kwargs={"k": 2})
            
            llm = GenerativeModel(r"llama3.2:1b")
            response = llm.generate_response(query, retriever)
            print(response)
        
            self.assertIsInstance(response, str, "Response should be a string")
            self.assertGreater(len(response), 0, "Response should not be empty")
            self.assertEqual(CheckKeyWords(response), True, "Response should contain the keywords")

    def testDocumentRead(self):
        file_path = r"Resume_VamsikrishnaChemudupati.pdf"
        # Execute functions
        pdf_text = ReadPdf(file_path)
        self.assertEqual(len(pdf_text), 9069, "PDF text length should be same")

if __name__ == '__main__':
    unittest.main()
