from flask import Flask, jsonify, request
from data_dict import random_users
import sqlite3
import requests #til API


app = Flask(__name__)

# Function to connect to the database
def connect_db():
    return sqlite3.connect('database.db')

#Hent medlemmerne og put dem i et dictionary så de kan arbejdes med
@app.route('/members', methods=['GET'])
def get_members():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    conn.close()

    member_list = []
    for member in members:
        github_username = member[10]
        repos = get_github_repos(github_username)

        member_dict = {
            'id': member[0],
            'first_name': member[1],
            'last_name': member[2],
            'birth_date': member[3],
            'gender': member[4],
            'email': member[5],
            'phonenumber': member[6],
            'address': member[7],
            'nationality': member[8],
            'active': member[9],
            'github_username': github_username,
            'github_repositories': repos
        }
        member_list.append(member_dict)

    return jsonify(member_list), 200 #HTTP korrekt status kode

def get_github_repos(username):
    if username == "NikoJulius1":
        response = requests.get(f'https://api.github.com/user/repos')
    else:
        response = requests.get(f'https://api.github.com/users/{username}/repos')

    if response.status_code == 200:
        repos = response.json()
        print(f"Repos for {username}: {repos}")
        return [repo['name'] for repo in repos]
    else: 
        print(f"Failed to get repos for {username}: {response.text}")
        return []


@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.get_json()  # Hent det nye member data 
    random_users.append(new_member)  # Tilføjer den nye member
    return jsonify(new_member), 201  # Returner med 201 status

#PUT til at opdaterer brugernavn på hver user 
@app.route('/members/<int:member_id>', methods=['PUT'])
def update_github(member_id):
    new_github_username = request.json['github_username'] #skaffer nuværende username

    # connect til databasen
    conn = connect_db()
    c = conn.cursor()

    #Opdater deres brugernavn
    c.execute('UPDATE members SET github_username = ? WHERE id = ?', (new_github_username, member_id))

    #Luk for forbindelsen når SQL queryen er kørt
    conn.commit()
    conn.close()

    #Udskriv resultatet
    return f"GitHub username for member {member_id} updated to {new_github_username}!", 200

if __name__ == '__main__':
    print("Starting Flask app...")  # Tjek om script faktisk starter
    app.run(debug=True)