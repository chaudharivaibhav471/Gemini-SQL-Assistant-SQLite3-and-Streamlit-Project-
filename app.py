import sqlite3
import pandas as pd 
import streamlit as st 
import google.generativeai as genai
import os 
from dotenv import load_dotenv
load_dotenv()

# LOAD THE GEMINI API KEY 
API_KEY =  os.getenv("GEMINI_API_KEY")

# CONFIGURE OF GEMINI API 
genai.configure(api_key=API_KEY)

# function for prompt to gemini to generate sql
def get_gemini_sql(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    sql_query = response.text.strip()
    sql_query = sql_query.replace("'''sql", "").replace("'''", "")
    return sql_query

# we create a function for  sql Explanation 
def explain_sql_query(query):
    explain_prompt = f"Explain this SQL query step-by-step in simple term:\n{query}"
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(explain_prompt)
    return response.text.strip()

# we create a function for the run sql on sqllite and show the rows and column name
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        col_name = [desc[0] for desc in cur.description]  # use for dynamic clumn name \
        conn.close()
        return rows, col_name
    
    except sqlite3.Error as e:
        return [("SQL Error", str(e))], ["Error"]
    
    # we provide the professional propt for gemini 

prompt = [""" 
# 1. Context:
You are helping to user interact with a SQLite database using natural language.

# 2. Role:
You are an expert SQl assistant who converts English question into SQLite Queries.

# 3. Constraints:
- Use only SQLite syntax.
- Target database: Software_Employee.
- Table: Employee.
- Columns: employee_name (text), employee_role (text), employee_salary (float).
- Do not use backticks (`), triple quotes (```), or semicolons.
- Keep SQL readable and correct.

# 4. Instructions:
- Translate the user's question into a valid SQL query.
- Be precise in filtering, grouping, or sorting.
- Make sure the column names and logic match the schema.
              
# 5. Few-shot Examples:

Q: How many employees are there?
A: SELECT COUNT(*) FROM Naresh_it_employee1

Q: Show all Data Engineers
A: SELECT * FROM Naresh_it_employee1 WHERE employee_role = 'Data Engineer'

Q: Who earns more than 60000?
A: SELECT * FROM Naresh_it_employee1 WHERE employee_salary > 60000

Q: Who earns the highest salary?
A: SELECT * FROM Naresh_it_employee1 ORDER BY employee_salary DESC LIMIT 1

# 6. Chain of Thought:
First, understand the user’s question and identify relevant filters or conditions.  
Then map to the appropriate SQL clause (e.g., SELECT, WHERE, GROUP BY, ORDER BY).  
Finally, return the correct and clean SQL query.

Now generate the SQL query for this question:
"""]
    


# we create the streamlit UI 
st.set_page_config(page_title="LLM SQL Assistent")
st.title("Gemini SQL Assistent (Software Employee DB)")
st.write("Ask questions in English. Get SQl queries and result instantly!")


# we take the user input 
question = st.text_input("Enter Your Question: ")


# we just give the sample suggestions 
with st.expander("Try These Example"):
    st.markdown("""
    - List all employees.
    - Show only Data Scientists.
    - Who earns more than 60,000?
    - Count of Data Engineers?
    - Highest salary employee?
    - Provide the average salary based on job role.
    """)


# for submit 
if st.button("RUN"):
    if question.strip() == "":
        st.warning("please enter a question:")

    # else we generate the SQl
    else:
        sql_query = get_gemini_sql(question, prompt)
        st.subheader("Generate SQl Query: ")
        st.code(sql_query, language="sql")

        # for run the sql query 
        result, columns = read_sql_query(sql_query, "Software_Employee.db")

        # for showing the result 
        if result and "SQL Error" in result[0]:
            st.error(f"Error: {result[0][1]}")

        else:
            st.subheader("Query Result: ")
            df = pd.DataFrame(result, columns=columns)
            st.dataframe(df, use_container_width=True)


            # we also need explanation 
            with st.expander("Gemini Explain the SQl"):
                explanation = explain_sql_query(sql_query)
                st.write(explanation)

