import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher


hashed_password = Hasher(['password123'])
print(hashed_password.hash('password123'))