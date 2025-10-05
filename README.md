# FastChat

FastChat is a full-stack real-time chat application project, developed in Python with the FastAPI framework. The application demonstrates a robust authentication system and bidirectional communication using WebSockets.

## Features

- **Complete Authentication System**:
  - **Registration and Login**
  - **Password Hashing**
- **Real-Time Chat**:
  - **Communication via WebSockets**
  - **Status Notifications**
  - **Message Broadcasting**

## Technologies Used

- **Backend:** Python, FastAPI
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** SQLite with SQLAlchemy

## Installation and Setup

Follow the steps below to set up and run the project locally:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ArthurDOli/FastChat.git
    cd FastChat
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the project root and add the following variables. These keys are essential for the security of JWT tokens. Use different keys for SECRET_KEY and REFRESH_SECRET_KEY.

    ```
    SECRET_KEY="your_key1"
    REFRESH_SECRET_KEY="your_key2"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_MINUTES=10080
    ```

5.  **Create the database:**
    Run the `database.py` script once to create the `database.db` file and the tables.

    ```bash
    python database.py
    ```

6.  **Run the application:**
    The project is configured to use Uvicorn, a high-performance ASGI server.
    ```bash
    uvicorn main:app --reload
    ```

## Project Structure

```bash
/FastChat
|-- /static/
|   |-- logo.png
|-- /templates/
|   |-- chat.html
|   |-- register.html
|-- .env
|-- .gitignore
|-- auth.py
|-- chat.py
|-- database.py
|-- main.py
|-- models.py
|-- schemas.py
`-- ws_manager.py
```
