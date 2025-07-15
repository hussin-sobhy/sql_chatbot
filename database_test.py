from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

from custom_prompts import few_shots, custumo_suffix, custom_prefix
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
        model="gemini-2.5-pro",
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

    db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=3)

    return db


def get_example_selector() -> SemanticSimilarityExampleSelector:
    """Get the example selector for few-shot learning."""

    # Create a vector store from the few-shot examples
    # This will be used to select the most relevant examples based on semantic similarity
    embrddings= HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore= Chroma.from_texts(
        texts=to_vectorize,
        embedding=embrddings,
        metadatas=few_shots,
        )
    
    example_selector= SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    return example_selector


def get_sql_database_chain() -> SQLDatabaseChain:
    """Get the SQL database chain with few-shot learning."""

    # Define the example prompt template
    example_prompt= PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )


    # Create the FewShotPromptTemplate with the example selector and example prompt
    # The prefix and suffix are used to format the input for the LLM
    few_shot_prompt = FewShotPromptTemplate(
        example_selector= get_example_selector(), # `get_example_selector()` returns the SemanticSimilarityExampleSelector instance
        example_prompt= example_prompt,
        prefix= custom_prefix,
        suffix= custumo_suffix,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )

    # Create the SQLDatabaseChain with the LLM, database, and prompt
    chain= SQLDatabaseChain.from_llm(
        get_llm(), # `get_llm()` returns the ChatGoogleGenerativeAI instance
        get_database(), # `get_database()` returns the SQLDatabase instance
        prompt=few_shot_prompt,
        verbose=True,
        use_query_checker=True,
    )

    return chain


if __name__ == "__main__":
    """Main function to run the SQL database chain."""
    
    chain = get_sql_database_chain()

    # Example query
    question = "What is the total number of nike's t-shirts?"
    
    # Invoke the chain with the query
    response = chain.invoke({"query": question})
    
    print(response)
    #print(chain.input_keys)


   