from datetime import datetime

from flask import Flask, redirect, url_for, render_template, request
from DB import Connection
import requests

app = Flask(__name__)

labels = [
    'Mar 02', 'Mar 05', 'Mar 08', 'Mar 11',
    'Mar 14', 'Mar 17', 'Mar 20', 'Mar 23',
    'Mar 26', 'Mar 29', 'Apr 01', 'Apr 04',
    'Apr 07', 'Apr 10', 'Apr 13', 'Apr 16',
    'Apr 19', 'Apr 22', 'Apr 25', 'Apr 28',
    'May 01', 'May 04', 'May 07', 'May 10',
    'May 13', 'May 16', 'May 19', 'May 22',
    'May 25', 'May 28', 'May 31', 'Jun 03',
    'Jun 06', 'Jun 09'
]

dates = [
    "02-03-2020", "05-03-2020", "08-03-2020",
    "11-03-2020", "14-03-2020", "17-03-2020",
    "20-03-2020", "23-03-2020", "26-03-2020",
    "29-03-2020", "01-04-2020", "04-04-2020",
    "11-04-2020", "07-04-2020", "10-04-2020",
    "13-04-2020", "16-04-2020", "19-04-2020",
    "22-04-2020", "25-04-2020", "28-05-2020",
    "01-05-2020", "04-05-2020", "07-05-2020",
    "10-05-2020", "13-05-2020", "16-05-2020",
    "19-05-2020", "22-05-2020", "25-05-2020",
    "28-05-2020", "31-05-2020", "03-06-2020",
    "06-06-2020",
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.before_first_request
def load_huge_file():
    value = 2;
    big_data = []
    for date in dates:
        response3 = requests.get("https://covid19-api.vost.pt/Requests/get_entry/" + date)
        try:
            value += 3
            big_data.append(response3.json()["confirmados"])
        except:
            print(date)
    print("Huge data set loaded!")
    global shared_data
    shared_data = big_data

@app.route("/")
def home():
    response = requests.get("https://coronavirus-19-api.herokuapp.com/all")
    response2 = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
    return render_template('index.html', globalData=response.json(), countriesData=response2.json(), values=shared_data, labels=labels)

@app.route("/share")
def share():
    Conn = Connection.getConnection()
    cursor = Conn.cursor()
    query = ("SELECT * FROM posts ORDER BY exact DESC")
    cursor.execute(query)
    return render_template('share.html', posts=cursor)

# HANDLERS
@app.route('/handle_data', methods=['POST'])
def handle_data():
    Conn = Connection.getConnection()
    cursor = Conn.cursor()
    if request.form.get('type') == 'anon':
        comment = request.form.get('comment')
        author = "Anonymous"
        query = ("INSERT INTO posts (author, comment, date, time) VALUES (%(author)s, %(comment)s, %(date)s, %(time)s)")
        today = datetime.now().date()
        if len(str(datetime.now().minute)) == 1:
           time = str(datetime.now().hour) + ":" + "0" + str(datetime.now().minute) + ":" + str(datetime.now().second)
        else:
            time = str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)
        data = {
            'author': author,
            'comment': comment,
            'date': today,
            'time': time
        }
        cursor.execute(query, data)
        cursor.close()
        Conn.close()
    else:
        user = request.form.get('user')
        comment = request.form.get('comment')
        query = ("INSERT INTO posts (author, comment, date, time) VALUES (%(author)s, %(comment)s, %(date)s, %(time)s)")
        today = datetime.now().date()
        if len(str(datetime.now().minute)) == 1:
            time = str(datetime.now().hour) + ":" + "0" + str(datetime.now().minute) + ":" + str(datetime.now().second)
        else:
            time = str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)
        data = {
            'author': user,
            'comment': comment,
            'date': today,
            'time': time
        }
        cursor.execute(query, data)
        cursor.close()
        Conn.close()


    return redirect(url_for('share'))

def main(_self):
    username, password, comment = ""
if __name__ == "__main__":
    app.run()