from flask import Flask, render_template, request, redirect, url_for

from webscraping import Webscraping

app = Flask(__name__)

webscraper = Webscraping()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['player_entry']
        return redirect(url_for('results', query=query))
    return render_template('home.html')

@app.route('/results/<query>')
def results(query):
    results = webscraper.show_results(player_name=query)
    if not results:
        return render_template('stats.html', player_info=None)
    elif len(results) == 1:
        return redirect(url_for('show_player_stats', id=results[0]["id"]))
    else:
        return render_template('results.html', players=results)

@app.route('/player/<id>', methods=['GET', 'POST'])
def show_player_stats(id):
    if request.method == 'POST':
        player = request.form["player"]
    else:
        try:
            player = webscraper.show_results(player_name=id)[0]
        except IndexError:
            return render_template('stats.html', player_info=None)
        player = str(player)
    player = webscraper.webscrape(player)
    return render_template('stats.html', player_info=player)

if __name__ == '__main__':
    app.run(debug=True)
