from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import sys
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class LawDocumentProcessor:
    def __init__(self, document_directory="data", index_directory="faiss_index"):
        # Obtener la ruta absoluta del directorio actual
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construir rutas absolutas
        self.document_directory = os.path.join(current_dir, document_directory)
        self.index_directory = os.path.join(current_dir, index_directory)
        
        print(f"Directorio de documentos: {self.document_directory}")
        print(f"Directorio de índices: {self.index_directory}")
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Crear directorios si no existen
        os.makedirs(self.document_directory, exist_ok=True)
        os.makedirs(self.index_directory, exist_ok=True)

    def load_vector_store(self):
        index_faiss_path = os.path.join(self.index_directory, "index.faiss")
        try:
            if os.path.exists(index_faiss_path):
                print(f"Cargando índice FAISS desde: {index_faiss_path}")
                vector_store = FAISS.load_local(
                    self.index_directory,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                return vector_store
            else:
                print(f"No se encontró el índice FAISS en: {index_faiss_path}")
                return self.process_documents()
        except Exception as e:
            print(f"Error cargando el índice FAISS: {e}")
            return self.process_documents()

    def process_documents(self):
        try:
            print(f"Procesando documentos desde: {self.document_directory}")
            files = os.listdir(self.document_directory)
            documents = []

            for file_name in files:
                file_path = os.path.join(self.document_directory, file_name)
                print(f"Procesando archivo: {file_path}")
                
                if file_name.lower().endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                elif file_name.lower().endswith(".txt"):
                    loader = TextLoader(file_path)
                else:
                    continue  # Por ahora solo soportamos PDF y TXT

                docs = loader.load()
                documents.extend(docs)

            if not documents:
                print("No se encontraron documentos válidos para procesar.")
                return None

            print(f"Documentos cargados: {len(documents)}")
            texts = self.text_splitter.split_documents(documents)
            print(f"Fragmentos generados: {len(texts)}")
            
            vectorstore = FAISS.from_documents(texts, self.embeddings)
            vectorstore.save_local(self.index_directory)

            print(f"✅ Vector store creado con {len(texts)} fragmentos.")
            print(f"Guardado en: {self.index_directory}")
            return vectorstore
        except Exception as e:
            print(f"Error procesando documentos: {e}")
            import traceback
            traceback.print_exc()
            return None
