from langchain.chains import RetrievalQA
#For faster inference on CPU
from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager

class GenerativeModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.llm = OllamaLLM(model=model_name, num_predict=256)

    def generate_response(self, query, retriever):
        prompt_template = """You are an assistant for question-answering tasks.The context \nUse the given information as context to answer the question.The context provided you are the details of a person named Vamsi taken from his Resume. If you don't know the answer, just say that you don't know.Use three sentences maximum and keep the answer concise and to the point.\nQuestion: {question}\nContext: {context}\nAnswer:
        """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # Define a RetrievalQA chain that is responsible for retrieving related pieces of text,
        # and using a LLM to formulate the final answer.
        retrievalQA = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )        
        response = retrievalQA.invoke(query)
        return response["result"]
