from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import FewShotPromptTemplate

from prompts import few_shots, CUSTOM_suffix, example_prompt, CUSTOM_prefix
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm() -> ChatGoogleGenerativeAI:
    """Get the language model."""

    # Check if the Google API key is set in the environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("You must set GOOGLE_API_KEY in your .env")

    # Create a ChatGoogleGenerativeAI instance with the specified model and temperature
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
    )
    return llm


def get_database() -> SQLDatabase:
    """Get the SQL database connection."""

    # Load the database URI from environment variables
    # Example: DATABASE_URL=mysql+pymysql://root:YourRootPassword@localhost/database_name
    db_uri = os.getenv("DATABASE_URL")

    # Check if the database URI is set
    if db_uri is None:
        raise ValueError("Missing DATABASE_URL in environment")

    db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=0)

    return db


def get_example_selector() -> SemanticSimilarityExampleSelector:
    """Load or create a persistent vector store for few-shot example selection."""

    persist_directory = os.path.join(os.path.dirname(__file__), "chroma_fewshots_db")
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Check if vector store already exists
    if os.path.exists(persist_directory):
        # Load existing Chroma vectorstore from disk
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model
        )
    else:
        # Build new vector store from examples
        to_vectorize = [" ".join(example.values()) for example in few_shots]
        vectorstore = Chroma.from_texts(
            texts=to_vectorize,
            embedding=embedding_model,
            metadatas=few_shots,
            persist_directory=persist_directory,
        )
        # Check if the vector store was created successfully
        print("Example selector initialized with vector store.")

    # Create semantic selector from vectorstore
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )



    return example_selector


def get_sql_database_chain() -> SQLDatabaseChain:
    """Get the SQL database chain with few-shot learning."""

    # Create the FewShotPromptTemplate with the example selector and example prompt
    # The prefix and suffix are used to format the input for the LLM
    few_shot_prompt = FewShotPromptTemplate(
        example_selector= get_example_selector(), # `get_example_selector()` returns the SemanticSimilarityExampleSelector instance
        example_prompt= example_prompt,
        prefix= CUSTOM_prefix,
        suffix= CUSTOM_suffix,
        input_variables=["input", "table_info", "top_k", "dialect"], #These variables are used in the prefix and suffix
    )

    # Create the SQLDatabaseChain with the LLM, database, and prompt
    chain= SQLDatabaseChain.from_llm(
        get_llm(), # `get_llm()` returns the ChatGoogleGenerativeAI instance
        get_database(), # `get_database()` returns the SQLDatabase instance
        prompt=few_shot_prompt,
        verbose=True,
    )

    return chain