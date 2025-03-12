from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pdfread_retrieval import ReadPdf, GetDocuments, VectorDB
from langchain.chains import RetrievalQA
from genmodel import GenerativeModel
import uvicorn
import os 
import shutil
from langchain.globals import set_verbose, set_debug


app = FastAPI(debug=True)

# Global Variables
llm = GenerativeModel(r"llama3.2:1b")  # LLM Model instance needs to be global to assist in changing the model dynamically.

class QueryRequest(BaseModel):
    query: str
    debug: bool = False

class ModelRequest(BaseModel):
    model_path: str

class PdfRequest(BaseModel):
    file_path: str

#Removing previous pdf_collection database
if os.path.exists("./pdf_collection"):
    shutil.rmtree("./pdf_collection")

#Creating a new database
database = VectorDB("sentence-transformers/all-mpnet-base-v2","./pdf_collection","pdf_collection")

@app.post("/load_model/")
async def load_model(request: ModelRequest):
    """
    Loads the specified GenerativeModel dynamically.
    """
    global llm
    try:
        llm = GenerativeModel(request.model_path)
        return {"message": f"Model '{request.model_path}' loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


@app.post("/upload/")
async def upload_pdf(request: PdfRequest):
    """
    Uploads a PDF file, extracts text, and adds it to ChromaDB.
    """
    print("File uploading started",flush=True)
    try:
        if database.CheckDuplicates(request.file_path):
            return {"message": "File is already indexed."}
        else:
            print("Adding file to database",flush=True)
            database.indexed_files.add(request.file_path)

        pdf_text = ReadPdf(request.file_path)
        documents = GetDocuments(pdf_text)

        # Add to ChromaDB
        db = database.AddFilesChromaDB(documents)
        if db == "success":
            return {"message": "File successfully uploaded."}
        else:
            return {"message": "Error uploading file."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/")
async def query_knowledge_base(request: QueryRequest):
    """
    Queries the indexed documents using ChromaDB and LLM.
    """
    global llm
    if request.debug:
        print("Debug model enabled.", flush=True)
        set_debug(True)
        set_verbose(True)
        
    if not llm:
        raise HTTPException(status_code=400, detail="No model loaded. Please load a model first.")

    if not database.indexed_files:
        raise HTTPException(status_code=400, detail="No files indexed. Please upload a document first.")

    try:
        db = database.GetDatabaseObj()
        retriever = db.as_retriever(search_kwargs={"k": 2})
        response = llm.generate_response(request.query, retriever)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "FastAPI Knowledge Retrieval API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)