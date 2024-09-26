import sqlite3
from data_dict import random_users  # Assuming this imports your random_users list

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop the members table if it exists (optional, for a clean start)
print("Dropping existing members table if it exists...")
c.execute('''
    DROP TABLE IF EXISTS members
''')

# Create the members table with the required columns
print("Creating the members table...")
c.execute('''
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        birth_date TEXT,
        gender TEXT,
        email TEXT,
        phonenumber TEXT,
        address TEXT,
        nationality TEXT,
        active BOOLEAN,
        github_username TEXT
    )
''')

# Insert the random_users into the members table
print("Inserting data into the members table...")
c.executemany('''
    INSERT INTO members (
        first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [(member['first_name'], member['last_name'], member['birth_date'], member['gender'], member['email'], member['phonenumber'], member['address'], member['nationality'], member['active'], member['github_username']) for member in random_users])

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup completed, and data inserted.")
