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



custom_prefix= """
    Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.

    Unless the user specifies a specific number of results, limit your query to at most {top_k} rows using the LIMIT clause.

    Never SELECT all columns. Only query the columns needed to answer the question.

    Only use the column names and tables shown in the schema. Do not guess or invent columns or table names.

    Use CURDATE() if the question refers to "today".

    Use this exact format:

    Here’s how to format your answer:

    Question: How many white Nike t-shirts are in stock?
    SQLQuery: SELECT sum(`stock_quantity`) FROM `t_shirts` WHERE `brand` = 'Nike' AND `color` = 'White'
    SQLResult: [(Decimal('208'),)]
    Answer: 208

"""

CUSTOM_suffix= """
    Only use the following tables:

    {table_info}

    Question: {input}
    Answer:
"""


