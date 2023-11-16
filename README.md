# ATR Social

**ATR Social** is a Django web application designed for social media interactions. It follows an agile development approach, providing users with features like posting images, following other users, and receiving suggestions for new connections. The application also includes user profiles, post management, and suggestions based on user interactions.

## Features

- **User Profile**: Users can create profiles with details such as bio, location, and profile images.
- **Post Feed**: View a feed of posts from followed users, including the user's own posts.
- **User Suggestions**: Receive suggestions for new connections based on current following relationships.
- **Post Interaction**: Like and comment on posts from other users.
- **Randomized Suggestions**: Suggestions for new connections are presented in a randomized order.
- **Post Management**: Users can delete and edit their own posts.
- **Responsive Design**: The application utilizes Bootstrap for a responsive and visually appealing UI.

## Technologies Used

- **Django**: Python web framework for backend development.
- **HTML/CSS**: Frontend development for user interface.
- **JavaScript**: Client-side interactions for dynamic features.
- **Bootstrap**: Front-end framework for responsive design.

## Installation

1. **Clone the Repository**:

    ```shell
    git clone https://github.com/your-username/atr-social.git
    ```

2. **Create a Virtual Environment**:

    ```shell
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

   - **Windows**:

    ```shell
    venv\Scripts\activate
    ```

   - **Linux/macOS**:

    ```shell
    source venv/bin/activate
    ```

4. **Install Dependencies**:

    ```shell
    pip install -r requirements.txt
    ```

5. **Apply Database Migrations**:

    ```shell
    python manage.py migrate
    ```

6. **Run the Development Server**:

    ```shell
    python manage.py runserver
    ```

## Usage

1. **Create a User Account and Log In**:

    - Register a new account and log in.

2. **Explore and Interact**:

    - Explore the platform, view the feed, and interact with posts.

3. **Manage Posts and Profile**:

    - Delete or edit your own posts, update your profile details.

4. **Connect with Others**:

    - Follow other users and receive suggestions for new connections.

## Directory Structure

- `atr_social/`: Main Django application directory.
- `templates/`: HTML templates.
- `core/`: Application-specific files, including models, views, and forms.
- `static/`: Static files such as CSS, JavaScript, and images.
- `media/`: User-uploaded media files.

## Dependencies

- **Django**: High-level Python web framework.
- **Bootstrap**: Front-end framework for UI styling.
- **SQLite**: Default database for data storage.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.


