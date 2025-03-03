import streamlit as st
from llm import ollama_use
from SQLUtility import execute
import lineagequeries
import Configs
import requests

import streamlit as st
import streamlit_authenticator as stauth
import yaml 
from streamlit_option_menu import option_menu
from pathlib import Path


from navigation import make_sidebar

from yaml.loader import SafeLoader

def main():
    # st.set_page_config(layout="wide")
    # st.sidebar.image('td_logo.png')
    # st.title("Apexon AML Quest")
    

    # selected2 = option_menu(None, ["Home", "Import", 'Settings'], 
    # icons=['house', 'cloud-upload',  'gear'], 
    # menu_icon="cast", default_index=0, orientation="horizontal")
    
     
    # if(selected2=='Home'):
    make_sidebar()
    
    st.markdown("Current Database: "+st.session_state.get('selected_db',Configs.db_name))
    st.markdown("Model : " + Configs.llm_model)
    print(st.session_state)

    input_text = st.chat_input("enter your prompt")
    print('Prompt entered :'+str(input_text))
    st.empty()

    if input_text is not None:
        Counter=1
        st.markdown('**Prompt** :'+input_text)
        llm_object=ollama_use()
        llm_output=llm_object.call_llm(input_text)
    
        st.markdown(llm_output)
        
        #df=execution(llm_output)
    #st.write(df)

        
    # with st.sidebar:
    #     "[Graph Database]("+Configs.Graph_URL+")"
    #     llm_responsecode=CheckNetworkConnectivity(Configs.llm_URL)
    #     if(llm_responsecode is not None and llm_responsecode.status_code==200):
    #         "LLM is Online"
    #     else:
    #         "LLM is Offline"
            
    #     graphurl_responsecode=CheckNetworkConnectivity(Configs.Graph_URL)
    #     if(graphurl_responsecode is not None and graphurl_responsecode.status_code==200):
    #         "GRAPHDB is Online"
    #     else:
    #         "GRAPHDB is Offline"
    
   

    
def CheckNetworkConnectivity(URL):

    try:
        print('Checking URL - '+URL)
        response = requests.get(URL)
        if response.status_code==200:
            print("URL is Online.")
        else:
            print(f"Response code : {response.status_code}")
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"Failure - Unable to establish connection: {e}.")
        response=None
    except Exception as e:
        print(f"Failure - Unknown error occurred: {e}.")
        response=None
    return response


def import_mapping_data():
    return False
    
    
if __name__ == "__main__":
    main()