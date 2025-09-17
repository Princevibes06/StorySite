StoryCraft is a simple, minimalist web application for writing, editing, and managing your stories. Built with Flask and SQLite, it provides a clean and distraction-free environment for creative writing, allowing users to sign up, log in, and manage their personal collection of stories.

### Key Features ✨

  * **User Authentication:** Secure user sign-up, login, and logout functionality.
  * **Story Management:** Create, edit, and delete your stories from a personalized dashboard.
  * **Minimalist Editor:** A clean and simple writing interface to help you focus on your content.
  * **Word Count:** The app automatically counts the words in your stories.
  * **Dashboard View:** A dashboard displays all of a user's stories in a clean, card-based layout.
  * **Database Integration:** Uses SQLite for a lightweight, file-based database.

### Technologies Used 🛠️

  * **Backend:**
      * **Python:** The core programming language.
      * **Flask:** A lightweight and flexible web framework for Python.
      * **SQLite3:** The default database for data storage.
      * **Werkzeug:** For secure password hashing.
  * **Frontend:**
      * **HTML:** For the page structure.
      * **CSS:** For styling.
      * **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

### Setup and Installation 🚀

Follow these steps to get a copy of the project up and running on your local machine.

#### Prerequisites

  * **Python 3.x:** Make sure you have Python installed. You can download it from the official [Python website](https://www.python.org/).

#### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/storycraft.git
    cd storycraft
    ```

2.  **Create a virtual environment** (recommended):

    ```sh
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

      * **On Windows:**
        ```sh
        venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```sh
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**

    ```sh
    pip install Flask
    pip install Werkzeug
    ```

5.  **Run the application:**

    ```sh
    python app.py
    ```

The application will start, and you can access it by opening your web browser and navigating to `http://127.0.0.1:5000`.


### File Structure 📁

  * `app.py`: The main Flask application file. Contains all the routes, database logic, and application setup.
  * `database.db`: The SQLite database file (created automatically on first run).
  * `templates/`: Directory for HTML template files.
      * `base.html`: The base template containing the navigation bar and footer.
      * `index.html`: The welcome page.
      * `login.html`: The user login form.
      * `signup.html`: The user registration form.
      * `dashboard.html`: The user dashboard, displaying their stories.
      * `new_story.html`: The form for creating and editing stories.

### Contribution Guidelines 🤝

Contributions are welcome\! If you find a bug or have an idea for a new feature, feel free to open an issue or submit a pull request.

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name`
3.  **Make your changes.**
4.  **Commit your changes:** `git commit -m 'feat: Add new feature'`
5.  **Push to the branch:** `git push origin feature/your-feature-name`
6.  **Open a Pull Request.**

### License 📄

This project is open-source and available under the MIT License.
