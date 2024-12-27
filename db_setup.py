import sqlite3

def initialize_database():
  conn = sqlite3.connect('db/habits.db')
  cursor = conn.cursor()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    frequency TEXT NOT NULL,
    goal INTEGER NOT NULL,
    start_date TEXT NOT NULL
  )
  """)
  
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
    """)
  
  conn.commit()
  conn.close()

  print("Database initialized")

if __name__ == "__main__":
  initialize_database()
  
