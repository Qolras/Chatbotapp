# Chatbot Application with Tkinter

This project is a simple Tkinter application that interacts with OpenAI's API to create a chatbot. The application features a graphical user interface for chatting with AI, browsing folders, and opening files.

## Author

Sultan Ali Sultan  Fakhroo

[LinkedIn Profile](https://www.linkedin.com/in/sultan-fakhroo-01412630b)

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Setup Instructions for VS Code

1. **Clone the repository** (if you are using version control):
    ```sh
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - **Windows**:
        ```sh
        venv\Scripts\activate
        ```
    - **macOS and Linux**:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Set your OpenAI API key**:
    - Create a `.env` file in the root directory of your project and add your OpenAI API key:
        ```env
        OPENAI_API_KEY=your_openai_api_key
        ```

6. **Run the Tkinter application**:
    ```sh
    python app.py
    ```

## Project Structure

├── app.py
├── requirements.txt
├── README.md


- `app.py`: The main Tkinter application script.
- `requirements.txt`: The list of required Python packages.
- `README.md`: This file with setup instructions.

## Usage

- Run the application.
- Interact with the chatbot by typing a message and clicking "Send".
- Use the "Browse Folder" button to select a folder and navigate its contents.
- Open files directly from the interface.

## License

This project is licensed under the MIT License.

## Google Colab

For a more in-depth step-by-step process and to run this script locally, follow the instructions provided in this Google Colab notebook:

[Google Colab Notebook](https://colab.research.google.com/drive/1DZOArKdX9Vaz6wL7ZFBDHPa2q-TQhh4W#scrollTo=zb2_UBbi-qNm)


## requirements.txt
 tkinter
requests==2.26.0

## Google Colab Notebook

To run the provided Tkinter application and understand the step-by-step process, you can refer to the detailed Google Colab notebook:

(https://colab.research.google.com/drive/1DZOArKdX9Vaz6wL7ZFBDHPa2q-TQhh4W#scrollTo=zb2_UBbi-qNm)

This setup includes clear instructions for setting up and running the Tkinter application both locally and via Google Colab.