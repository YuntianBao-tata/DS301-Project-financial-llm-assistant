# src/tools/rag_manager.py
import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

class FinancialKnowledgeBase:
    def __init__(self, persist_directory="./financial_db"):
        self.persist_directory = persist_directory
        # Using a lightweight model for embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Initialize Vector DB
        self.db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=self.embeddings
        )

    def add_document(self, file_path: str, source_name: str) -> str:
        """Ingests a document into the knowledge base."""
        try:
            # 1. Handle Paths: Look inside 'data/' folder by default
            full_path = Path(file_path)
            
            # If user just says "news.txt", prepend "data/"
            if not full_path.exists():
                suggested_path = Path("data") / file_path
                if suggested_path.exists():
                    full_path = suggested_path
                else:
                    return f"Error: File '{file_path}' not found."
            
            # 2. Load Document
            if str(full_path).endswith(".pdf"):
                loader = PyPDFLoader(str(full_path))
            else:
                # Assumes text/csv/md/etc.
                loader = TextLoader(str(full_path), encoding='utf-8')
            
            documents = loader.load()
            
            # Add metadata so the AI knows the source
            for doc in documents:
                doc.metadata["source"] = source_name

            # 3. Split Text (Chunking)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200 
            )
            chunks = text_splitter.split_documents(documents)

            # 4. Embed and Store
            self.db.add_documents(chunks)
            
            return f"Successfully ingested {len(chunks)} chunks from {source_name} into memory."
        
        except Exception as e:
            return f"Error ingesting document: {str(e)}"

    def search_news(self, query: str, k: int = 3) -> str:
        """Searches the knowledge base for relevant info."""
        # Check if DB has data
        try:
            count = self.db._collection.count()
            if count == 0:
                return "The knowledge base is empty. Please ingest a file first."
        except:
             return "The knowledge base is not initialized."

        # Perform similarity search
        docs = self.db.similarity_search(query, k=k)
        
        if not docs:
            return "No relevant news found."
        
        # Format results
        context = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content.replace("\n", " ") # Clean newlines
            context.append(f"[Source: {source}]: {content}")
            
        return "\n\n".join(context)

# Singleton instance
kb_manager = FinancialKnowledgeBase()