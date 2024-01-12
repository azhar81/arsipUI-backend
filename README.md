# Django REST Framework App with MySQL Database

This is a Django REST Framework (DRF) app configured to use a MySQL database as its backend. The app provides a foundation for building RESTful APIs using the powerful Django framework.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/azhar81/arsipUI-backend.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd arsipUI-backend
    ```

3. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

6. **Configure the system settings:**

    Create a `.env` file for the system configuration in `project/.env`:

    ```
    SECRET_KEY=django secret key
    FRONTEND_URL=URL to the frontend
    DB_NAME=name of mysql database
    DB_HOST=host of mysql database
    DB_PORT=port of mysql database
    DB_USERNAME=username
    DB_PASSWORD=password
    ```

7. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

8. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The app should now be accessible at [http://localhost:8000/](http://localhost:8000/).
