# Habit Tracker

Habit Tracker is a simple application for tracking habits. It uses a SQLite database to store habit data and PyQt for the user interface.

## Features

- Add, edit, and remove habits
- Track progress for each habit
- View all habits in a table
- Simple and intuitive UI

## Requirements

- Python 3.13 or higher
- PyQt6
- SQLite3

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python main.py
   ```

## Project Structure

- [main.py](http://_vscodecontentref_/1): Entry point of the application.
- [db_setup.py](http://_vscodecontentref_/2): Script to initialize the database.
- [db_operations.py](http://_vscodecontentref_/3): Contains functions to interact with the database.
- [db_test.py](http://_vscodecontentref_/4): Contains test functions to insert and query data.
- [ui.py](http://_vscodecontentref_/5): Contains the PyQt UI code.
