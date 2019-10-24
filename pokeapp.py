from flask import Flask, render_template, request, send_from_directory
import os
import joblib
import pandas as pd 
import numpy as np 
import requests
import matplotlib
import random
matplotlib.use('Agg')
import matplotlib.pyplot as plt 


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('menupokemon.html')

@app.route('/hasil', methods=['GET', 'POST'])
def hasil():
    # os.remove('static/images/pokemon.png')
    body = request.form 
    df = pd.read_csv('Dataset_3/pokemon.csv')
    df = df.set_index('#')

    name1 = body['contender1'].capitalize()
    name2 = body['contender2'].capitalize()

    url = 'http://pokeapi.co/api/v2/pokemon/'
    id1 = requests.get(url + name1.lower())
    id2 = requests.get(url + name2.lower())


    if str(id1) == '<Response [404]>' or str(id2) == '<Response [404]>':
        return render_template('pokerror.html')
    else:
        img1 = requests.get(url + name1.lower()).json()["sprites"]["front_default"]
        img2 = requests.get(url + name2.lower()).json()["sprites"]["front_default"]

        id1 = id1.json()['id']
        id2 = id2.json()['id']

        combat = pd.DataFrame()
        combat = combat.append(df[df['Name'] == name1])
        combat = combat.append(df[df['Name'] == name2])

        columns = combat.drop(columns=['Name', 'Type 1', 'Type 2', 'Generation', 'Legendary']).columns

        plt.figure(figsize=(15, 3))
        for i in range(len(columns)):
            plt.subplot(1, 6, i + 1)
            plt.title(columns[i])
            plt.bar(combat['Name'], combat[columns[i]], color='green')

        r = random.randint(0, 10000000000000000000000)
        plt.savefig('static/images/pokemon{}.png'.format(r), transparent=True)

        index1 = df[df['Name'] == name1].index[0]
        index2 = df[df['Name'] == name2].index[0]

        predict = [[index1, index2]]

        proba = model.predict_proba(predict)
        proba = f'{round(proba.max() * 100, 0)}%'

        battling_pokemon = [name1, name2]

        output = f'{proba} {battling_pokemon[model.predict(predict)[0]]} Wins!'


        return render_template('hasil.html', p1=name1, p2=name2, 
                                            img1=img1, img2=img2,
                                            winner=output,r=r)

if __name__ == '__main__':
    model = joblib.load('poke_rfc')
    app.run(debug = True)