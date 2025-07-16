from langchain.prompts.prompt import PromptTemplate

few_shots = [
    {
        'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
        'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        'SQLResult': "[(91,)]",
        'Answer': "91"
    },
    {
        'Question': "How much is the total price of the inventory for all S-size t-shirts?",
        'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        'SQLResult': "[(22292,)]",
        'Answer': "22292"
    },
    {
        'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
        'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue FROM
        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
        group by t_shirt_id) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "[(Decimal('16725.4'),)]",
        'Answer': "16725.4"
    },
    {
        'Question': "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
        'SQLResult': "[(17462,)]",
        'Answer': "17462"
    },
    {
        'Question': "How many white color Levi's shirt I have?",
        'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        'SQLResult': "[(290,)]",
        'Answer': "290"
    },
    {
        'Question': "How much sales amount will be generated if we sell all large size t-shirts today in Nike brand after discounts?",
        'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue FROM
        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
        group by t_shirt_id) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "[(Decimal('290'),)]",
        'Answer': "290"
    }
]

example_prompt= PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
)

CUSTOM_suffix= """
    Only use the following tables:

    {table_info}

    Question: {input}
"""


CUSTOM_prefix2= """
    Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

    Never query for all the columns from a specific table, only ask for a few relevant columns given the question.

    Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

    Use the following format:

    Question: Question here
    Answer: generated answer here
"""


CUSTOM_prefix3= """
    Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.

    Unless the user specifies a specific number of results, limit your query to at most {top_k} rows using the LIMIT clause.

    Never SELECT all columns. Only query the columns needed to answer the question.

    Only use the column names and tables shown in the schema. Do not guess or invent columns or table names.

    Use CURDATE() if the question refers to "today".

    Use this exact format:

    Here’s how to format your answer:

    Question: How many white Nike t-shirts are in stock?
    Answer: your final answer here

"""

CUSTOM_prefix4= """
    You are an expert retail data analyst working with a MySQL database for a clothing store.
    Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Your job is to answer natural language questions about the store’s t-shirt inventory and pricing. You must:
    - Generate a correct MySQL query that uses only the tables and columns shown below.
    - If relevant, calculate total value by multiplying `price` × `stock_quantity`.
    - Apply discounts from the `discounts` table using `pct_discount`, if the question mentions discounts.
    - Use filters like brand, color, or size only if mentioned in the question.
    - Use `LIMIT {top_k}` if the question involves multiple results but no specific count.
    - Wrap all column names in backticks (e.g., `brand`) for MySQL syntax.
    - Use `CURDATE()` if the question includes the word “today.”

    - Always follow this format:

    - Question: the user’s original question
    - Answer: clear, simple final answer — no extra explanation, no repeating the question
"""

CUSTOM_prefix= """
    You are an expert retail data analyst working with a {dialect} database for a clothing store.

    Your job is to answer natural language questions about the store’s t-shirt inventory and pricing.

    Follow these rules:
    - Always use only the tables and columns provided in the schema.
    - If the question asks "how many t-shirts", return the total based on the `stock_quantity` column.
    - If the question mentions discounts, apply the `pct_discount` from the `discounts` table.
    - To calculate value, use `price * stock_quantity`, and adjust with discounts if needed.
    - Use filters like brand, color, or size **only if** mentioned in the question.
    - Use `LIMIT {top_k}` when the question doesn’t specify how many results to return.
    - Use `CURDATE()` if the question includes "today".
    - Never select all columns — only select the columns needed for the answer.
    - Wrap column names in backticks (e.g., `brand`, `stock_quantity`).

    Respond in the following format:

    Question: the user’s input
    Answer: a short, clear sentence with the final result, no SQL query.
"""