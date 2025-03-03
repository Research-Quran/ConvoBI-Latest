import streamlit as st
import streamlit_authenticator as stauth
import yaml 
import navigation
from yaml.loader import SafeLoader

  
def Login(k):
    st.session_state.logged_in = True
    st.success("Logged in successfully!")
    st.switch_page("pages/app.py")
    
navigation.make_sidebar()

with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['key'],
    config['cookie']['name'],
    config['cookie']['expiry_days']
)

try:
   t= authenticator.login(callback=Login)
   print(t)
except Exception as e:
    st.error(e)
  