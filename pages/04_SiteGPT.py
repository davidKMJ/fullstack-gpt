import streamlit as st
from langchain.document_loaders import AsyncChromiumLoader, SitemapLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from bs4 import BeautifulSoup

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-4o",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

answers_prompt = ChatPromptTemplate.from_template(
"""
Using ONLY the following context answer the user's question.
If you can't just say you don't know, don't make anything up.

Then, give a score to the answer between 0 and 5.
The score should be high if the answer is related to the user's question, and low otherwise.
If there is no relevant content, the score is 0.
Always provide scores with your answers
Context: {context}

Examples:

Question: How far away is the moon?
Answer: The moon is 384,400 km away.
Score: 5

Question: How far away is the sun?
Answer: I don't know
Score: 0

Your turn!
Question: {question}
"""
)

def get_answers(inputs):
    print(inputs)
    docs = inputs["docs"]
    question = inputs["question"]
    answers_chain = answers_prompt | llm
    return {"question": question, "answers": [
        {
           "answer": answers_chain.invoke({"context": doc, "question": question}).content,
           "source": doc.metadata["source"],
           "date": doc.metadata["lastmod"],
        } 
        for doc in docs
    ]}

choose_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
"""
Use ONLY the following pre-existing answers to answer the user's question.

Use the answers that have the highest score (more helpful) and favor the most recent ones.
Cite sources. Do not modify the source. Give the link to the source if possible.
Answers: {answers}

Example output(just care about the format not the content):
The moon is 384,400 km away.
Source: https://example.com/moon
""",
        ),
        ("human", "{question}"),
    ]
)

def choose_answer(inputs):
    answers = inputs["answers"]
    question = inputs["question"]
    choose_chain = choose_prompt | llm
    condensed = "\n\n".join(f"Answer: {answer['answer']}\nSource: {answer['source']}\nDate: {answer['date']}\n\n" for answer in answers)
    return choose_chain.invoke({
        "answers": condensed,
        "question": question,
    })

def parse_page(soup: BeautifulSoup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return str(soup.get_text()).replace("\n","")

@st.cache_resource(show_spinner="Loading website...")
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 1000,
        chunk_overlap = 200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            r"^(?!.*\/blogs\/).*",
        ],
        parsing_function=parse_page,
    )
    docs = loader.load_and_split(text_splitter=splitter)
    vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
    return vector_store.as_retriever()


st.set_page_config(
    page_title="Site GPT",
    page_icon="🌐",
)

html2text_transformer = Html2TextTransformer()

st.title("Site GPT")

st.markdown("""
Ask questions about the content of a website.
            
Start by writing the URL of the website on the sidebar.
""")

with st.sidebar:
    url = st.text_input("Write down a URL", placeholder="https://example.com")

# if url:
#     loader = AsyncChromiumLoader([url])
#     docs = loader.load()
#     transformed = html2text_transformer.transform_documents(docs)
#     st.write(transformed)

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please provide a sitemap URL.")
    else:
        retriever = load_website(url)
        query = st.text_input("Ask a question about the website.")
        if query:
            chain = {
                "docs": retriever, 
                "question": RunnablePassthrough()
            } | RunnableLambda(get_answers) | RunnableLambda(choose_answer)
            result = chain.invoke(query)
            st.write(result.content.replace("$", "\$"))