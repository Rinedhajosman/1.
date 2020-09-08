from flask import Flask
import psycopg2
import numpy as np
from flask import request
np.random.seed(0)
connection = psycopg2.connect(user='postgres', password='12345', host='127.0.0.1', port='5432', database='test')
cursor = connection.cursor()
print("connected to database..")
app = Flask(__name__)

@app.route('/get_data_count', methods=['GET'])
def get_data_count():
    label = str(request.args.get("label"))
    count = request.args.get("count")
    try:
       if label=='positive':
            cursor.execute("SELECT text_id,label_id FROM data_labeling WHERE label_id=1 LIMIT "+str(count))
            re = cursor.fetchall()
            print(len(re))
       elif label=='negative':
            cursor.execute("SELECT text_id,label_id FROM data_labeling WHERE label_id=0 LIMIT "+str(count))
            re = cursor.fetchall()
            print(len(re))
       elif label=='all text':
            cursor.execute("SELECT text_id,label_id FROM data_labeling WHERE label_id=0 AND label_id=1 LIMIT "+str(count))
            re = cursor.fetchall()
            print(len(re))
       return {'len': len(re)}, 200
    except:
       return "Try again"

@app.route('/get_data', methods=['GET'])
def get_data():
    i = request.args.get("i")
    sort = str(request.args.get("sort"))
    try:
       if sort=='desc':
          cursor.execute("SELECT text, label_id FROM data_input INNER JOIN data_labeling ON id = text_id ORDER BY text_date DESC LIMIT "+str(i))
          a = cursor.fetchall()
          print(a)
       elif sort=='asc':
          cursor.execute("SELECT text, label_id FROM data_input INNER JOIN data_labeling ON id = text_id ORDER BY text_date ASC LIMIT "+str(i))
          a = cursor.fetchall()
          print(a)
       return {'data': a}, 200
    except:
       return "Try again"

if __name__ == "__main__":
   app.run(port=3000)

connection.commit()
