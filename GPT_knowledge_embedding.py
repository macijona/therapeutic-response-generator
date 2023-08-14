import streamlit as st
from langchain.document_loaders import DataFrameLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS # to locally store the vector database
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import pandas as pd
from encode_newline_escape import clean_file_path

load_dotenv()
extension_file_path = "depression.csv"

# 1. Vectorise the patient/therapist csv data
loader = CSVLoader(clean_file_path, encoding="utf8") # DataFrameLoader(df)
documents = loader.load()
documents.extend(CSVLoader(extension_file_path, encoding="utf8").load())

#print(documents[-1].page_content)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search
def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_response]

    return page_contents_array

# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
You are a observant and empathetic therapist. 
I will share a client's message with you and you will give me the best answer that 
I should send to this client based on past best practies, 
and you will follow ALL of the rules below:

1/ Response should be very similar or even identical to the past best practies, 
in terms of length, ton of voice, logical arguments and other details

2/ If the best practice are irrelevant, then try to mimic the style of the best practice to prospect's message

Below is a message I received from the client:
{message}

Here is a list of best practies of how we normally respond to clients in similar scenarios:
{best_practice}

Please write the best response that I should send to this client, and remember that you are the client's therapist:
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# 4. Retrieval augmented generation
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response


# 5. Build an app with streamlit
def main():
    # msg = "I like to drive around my city at night to reflect and listen to my thoughts. Is this healthy?"
    # result = generate_response(msg)
    # print(msg)
    # print()
    # print(result)
    # return
    st.set_page_config(
        page_title="Therapeutic response generator", page_icon=":bird:")

    st.header("Therapeutic client response generator :bird:")
    message = st.text_area("customer message")

    if message:
        st.write("Generating best practice message...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()