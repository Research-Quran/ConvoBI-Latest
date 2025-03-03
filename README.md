# TD Bank Conversational Chatbot (GenAI PoC)

This project is a **Conversational Chatbot** leveraging **Generative AI (GenAI)** as a **Proof of Concept (PoC)** for **TD Bank**. The chatbot is designed to interact naturally with users and provide intelligent responses based on available data.

## Prerequisites
Before running the chatbot, ensure you have the following set up:

1. **PostgreSQL Database & Neo4j Database**: Ensure that your local PostgreSQL instance is running and properly configured with the required dataset.
2. **Python Virtual Environment**: Create a virtual environment to manage dependencies.
3. **Required Dependencies**: Install all necessary Python packages.

## Installation & Setup

Follow these steps to set up and run the chatbot:

### 1. Clone the Repository
```sh
git clone https://github.com/Research-Quran/Convobi.git
cd tdbank_poc-dev
```

### 2. Set Up a Virtual Environment
Create and activate a Python virtual environment:
```sh
python -m venv venv
```
On Windows:
```sh
venv\Scripts\activate
```
On macOS/Linux:
```sh
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages from `requirements.txt`:
```sh
pip install -r requirements.txt
```

### 4. Run the Application
Make sure you are in the correct project directory, then start the chatbot using **Streamlit**:
```sh
streamlit run app.py
```

## Usage
- The chatbot will launch in your web browser.
- Interact with the bot through the chat interface.
- Ensure the PostgreSQL database and Neo4j is correctly configured for optimal performance.

## Troubleshooting
- If you encounter missing dependencies, try re-running:
  ```sh
  pip install -r requirements.txt
  ```
- If `streamlit` is not found, ensure your virtual environment is activated.
- Verify that your PostgreSQL instance is running and accessible.


