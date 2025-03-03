import streamlit as st
from llm import ollama_use
from SQLUtility import execute
import lineagequeries
import Configs
from langchain_community.llms import Ollama


def main():
    st.set_page_config(layout="wide")

    st.title("LLM connectivity Test")
    with st.sidebar:
        "[Graph Database]("+Configs.Graph_URL+")"
    input_text = st.chat_input("enter your prompt")
    print('Prompt entered :'+str(input_text))

    if input_text is not None:
        llm1 = Ollama(model="openhermes:latest", base_url=Configs.llm_URL,temperature=0)
        llmresponse=llm1.invoke(input_text)
    
        st.markdown(llmresponse)
        #df=execution(llm_output)
        #st.write(df)

    


if __name__ == "__main__":
    main()