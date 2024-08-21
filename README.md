# Python Programming Chatbot

This is a simple chatbot built using Google's Generative AI (Gemini API) and Streamlit. The chatbot is designed to assist with Python programming-related questions.

## Features

- Responds to Python programming-related queries.
- Handles basic greetings.
- Displays responses in a user-friendly chat interface.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/reemamemon/python-programming-chatbot.git
    cd python-programming-chatbot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    - Create a `.env` file in the root directory.
    - Add your Gemini API key to the `.env` file:
    ```plaintext
    Gemini_API_Key=your_api_key_here
    ```

5. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage

- Open the app in your browser.
- Enter your Python-related question and get the response from the chatbot.
- If the response contains code, it will be highlighted in a black box with syntax highlighting.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

