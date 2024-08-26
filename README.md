# Lifting Log
Lifting Log is a web application designed to help users track and analyze their workout routines by utalizing Flask, HTML/CSS, Bootstrap and Python. Users can create an account, log in and create custom workouts where they will be able to log each workout and analyze their progress over time.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Lifting Log application allows users to log their workouts, analyze their progress over time, and maintain a detailed history of their exercise routines. With a user-friendly interface and dynamic features, this application is perfect for fitness enthusiasts looking to keep track of their lifting regimen.

## Features
+ **User Authentication:** Secure user registration and login functionality.
+ **Workout Logging:** Users can log their workouts with specific exercises, sets, reps, and weights.
+ **Dynamic Workout Creation:** Create new workout routines and add multiple exercises on the go.
+ **Progress Analysis:** View workout progress over time with interactive charts.
+ **Responsive Design:** Mobile-friendly interface built with Bootstrap.


## Installation

### Prerequisites

Ensure you have the following installed on your local development environment:

- Python 3.x
- Flask
- Virtualenv (optional but recommended)

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/jtnicastro/lifting-log.git
    cd lifting-log
    ```

2. **Create a Virtual Environment (optional):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```bash
    python app.py
    ```
5. **Open your Web Browser:**
    
    Navigate to http://127.0.0.1:5000 to start using the Lifting Log.

## Usage
### Register an Account

* Navigate to the "Register" page to create a new account.
* Fill in your details and click "Submit".

### Log In

* Use your credentials to log in to the application.

### Add a Workout

* Go to "Add Workout" to create a new workout routine.
* Add exercises to your workout by entering exercise names and details.
* Submit your workout to save it.

### View and Analyze Workouts

* Access the "Entries" page to view your workout logs.
* Use the "Analyze" page to visualize your progress over different time ranges using interactive charts.

## Screenshots

## Project Structure
```bash
    lifting-log/
    │
    ├── app.py            # Main application file
    ├── forms.py          # Form classes for Flask-WTF
    ├── models.py         # Database models
    ├── views.py          # View functions
    ├── templates/        # HTML templates
    │   ├── base.html
    |   ├── alt_base.html
    │   ├── home.html
    │   ├── addExercise.html
    │   ├── entries.html
    │   ├── analyze.html
    │   └── register.html
    ├── static/           # Static files (CSS, JS, Images)
    │   └── theme.css
    └── README.md         # This README file 
```
## Technologies Used
+ **Python:** Backend logic using Flask.
+ **Flask:** Web framework for routing and templating.
+ **Bootstrap:** Frontend framework for responsive design.
+ **HTML/CSS:** Structure and styling of the web pages.
+ **JavaScript:** For rendering dynamic charts on the Analyze page.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.tldrlegal.com/license/mit-license) file for details.


