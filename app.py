# Prompts
from prompt import question_prompt_template, refine_prompt_template

# Application Config
from configuration import llm, fetch_entries

# Streamlit
import validators, streamlit as st

# RSS Feedoarser
import feedparser

# Vertex AI
import vertexai
from google.cloud import aiplatform

# Langchain
from langchain import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain


## GLOBAL VARS ##

# Create an empty dictionary
entries_list = []

# Create empty list
summaries_list = []

# Set entry counter
entry_counter = 1

# Set summary counter
summary_counter=0

# Define streamlit columns
col1, col2 = st.columns(2)


# StreamLit app
st.subheader('RSS Feed Summarizer')
"Summarize articles into a few lines."

url = st.text_input("URL", label_visibility="collapsed")
"e.g. https://www.bleepingcomputer.com/feed/ "


# Propmt Design
question_prompt = PromptTemplate(
    template=question_prompt_template, input_variables=["text"]
)

# Refine Prompt
refine_prompt = PromptTemplate(
    template=refine_prompt_template, input_variables=["text"]
)


# Function to parse RSS feed from URL
def parse_feed(source_url, num_entries):
    feed = feedparser.parse(url)

    for entry in feed.entries[:fetch_entries]:
        entry_dict = {'title': entry.title, 'url': entry.link}
        entries_list.append(entry_dict)

    return entries_list


# Function to summarize text from supplied article
def summarize_article(article):
    refine_chain = load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
    )

    # Document loader - summarize article
    loader = WebBaseLoader(article['url'])
    data = loader.load()

    article_summarization = refine_chain({"input_documents": data})

    return article_summarization


# Function to dsiplay the results to a Streamlit app
def display_results(summaries, counter):
    for summary in summaries:
        if (counter % 2 == 0):
            with col1:
                st.header(summaries[counter]['title'])
                st.write(summaries[counter]['summary'])
        else:
            with col2:
                st.header(summaries[counter]['title'])
                st.write(summaries[counter]['summary'])

        counter+=1


def main(entry_counter):

    # If 'Summarize Feed' button is clicked
    if st.button("Summarize"):

        #validate inputs
        if not validators.url(url):
            st.error("Please enter a valid URL.")

        else:

            try:

                with st.spinner("Please wait..."):
                    feed_result = parse_feed(url, fetch_entries)

                    # Summarize RSS Articles
                    for article in feed_result:

                        result = summarize_article(article)

                        summaries_dict = {'entry': entry_counter, 'title': article['title'], 'url': article['url'], 'summary': result['output_text']}

                        summaries_list.append(summaries_dict)

                        entry_counter+=1

                    st.success(display_results(summaries_list, summary_counter))

            except Exception as e:
                st.exception(f"Exception: {e}")


if __name__ == "__main__":
    main(entry_counter)
