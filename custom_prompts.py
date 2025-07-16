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


CUSTOM_prefix= """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Question: Question here
Answer: generated answer here
"""



