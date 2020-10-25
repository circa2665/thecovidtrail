# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_render_template]
import datetime

from flask import Flask, render_template, request, session

from random import randrange, uniform

app = Flask(__name__)

app.secret_key = b'\xbeH\xd9\x14=\x91\x86\x8c\x0b\x859\x0eI\x80\xc5\xf4Z*\xf6\x15\x96\x812@[Q\xb2\x07\t~\xd0\xf2'

scenarios = [['You need to pick up some groceries today. Will you put on your mask?',[['Yes', .1], ['Naw', .7]]],
             ['Are you stupid?', [['Yes', .5], ['Yes', .5]]],
             ['You saw someone cough on the doorknob. Do you lick it?', [['Yes', .9], ['No', .1]]]]


@app.route('/')
def root():
 

    return render_template('index.html')

@app.route('/scenario_one', methods = ['GET', 'POST', 'DELETE'])
def scenario_one():
    session['name'] = request.form['username']
    session['scenarios_left'] = scenarios[:]
    current_scenario_number = randrange(len(session['scenarios_left']))
    session['current_scenario'] = session['scenarios_left'][current_scenario_number]
    del session['scenarios_left'][current_scenario_number]
    
    return render_template('scenario_one.html', username = session['name'], current_scenario = session['current_scenario'], scenarios_left = session['scenarios_left'])

@app.route('/scenario_two', methods = ['GET', 'POST', 'DELETE'])
def scenario_two():
    covid_chance = float(request.form.get('scenario-one-select'))
    covid_value = uniform(0, 1)
    if covid_value < covid_chance:
        return render_template('loser.html', username = session['name'])
    else:
        current_scenario_number = randrange(len(session['scenarios_left']))
        session['current_scenario'] = session['scenarios_left'][current_scenario_number]
        del session['scenarios_left'][current_scenario_number]
        return render_template('scenario_two.html', username = session['name'], current_scenario = session['current_scenario'], scenarios_left = session['scenarios_left'])
        
        
    

@app.route('/scenario_three', methods = ['GET', 'POST', 'DELETE'])
def scenario_three():
    covid_chance = float(request.form.get('scenario-two-select'))
    covid_value = uniform(0, 1)
    if covid_value < covid_chance:
        return render_template('loser.html', username = session['name'])
    else:
        current_scenario_number = randrange(len(session['scenarios_left']))
        session['current_scenario'] = session['scenarios_left'][current_scenario_number]
        del session['scenarios_left'][current_scenario_number]
        return render_template('scenario_three.html', username = session['name'], current_scenario = session['current_scenario'], scenarios_left = session['scenarios_left'])

@app.route('/finalday', methods = ['GET', 'POST', 'DELETE'])
def finalday():
    covid_chance = float(request.form.get('scenario-three-select'))
    covid_value = uniform(0, 1)
    if covid_value < covid_chance:
        return render_template('loser.html', username = session['name'])
    else:
        return render_template('winner.html', username = session['name'])

@app.route('/redirecthome', methods = ['GET', 'POST', 'DELETE'])
def redirecthome():
    return render_template('index.html')
    
    
    
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_render_template]
