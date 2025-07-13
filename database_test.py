from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate

from few_shots import few_shots
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm() -> ChatGoogleGenerativeAI:
    """Get the language model."""
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("You must set GOOGLE_API_KEY in your .env")

    # Instantiate the free Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.1,
    )
    return llm


def get_database() -> SQLDatabase:
    """Get the SQL database connection."""

    db_uri = os.getenv("DATABASE_URL") # mysql+pymysql://root:YourRootPassword@localhost/atliq_tshirts
    if db_uri is None:
        raise ValueError("Missing DATABASE_URL in environment")

    db = SQLDatabase.from_uri(db_uri)

    return db


def get_example_selector() -> SemanticSimilarityExampleSelector:
    """Get the example selector for few-shot learning."""

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

    mysql_prompt = _mysql_prompt

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    example_selector= get_example_selector()
    llm= get_llm()
    db= get_database()

    few_shot_prompt = FewShotPromptTemplate(
        example_selector= example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )

    

    chain= SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        prompt=few_shot_prompt,
        verbose=True,
    )

    return chain


'''if __name__ == "__main__":
    """Main function to run the SQL database chain."""
    
    chain = get_sql_database_chain()

    # Example query
    query = "What is the total number of Adidas t-shirts?"
    
    # Run the chain with the query
    response = chain.run(query)
    
    print(response)'''

   