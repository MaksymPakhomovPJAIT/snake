from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient, DESCENDING
from game_logic import SnakeGame

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
game = SnakeGame()

client = MongoClient(
    'mongodb+srv://max-admin:ewShhhLVkhdrXNyk@cluster0.uz9xvxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['snake_game']
scores_collection = db['scores']


# # Routes
# @app.route('/')
# def auth():
#     return render_template('register.html')


@app.route('/')
def index():
    try:
        users_data = list(scores_collection.find().sort("points", DESCENDING))
        return render_template('index.html', users=users_data)
    except Exception as e:
        app.logger.error(f"Exception on /users [GET]: {e}")
        return {"error": "Internal Server Error"}, 500

#
# @app.route('/users')
# def users():
#     try:
#         users_data = list(scores_collection.find().sort("points", DESCENDING))
#         return render_template('leaderboard.html', users=users_data)
#     except Exception as e:
#         app.logger.error(f"Exception on /users [GET]: {e}")
#         return {"error": "Internal Server Error"}, 500


# Sockets
@socketio.on('change_direction')
def handle_change_direction(direction):
    game.change_direction(direction)


@socketio.on('update')
def handle_update():
    state = game.update()
    emit('game_state', state)


@socketio.on('restart_game')
def handle_restart_game():
    game.reset()
    state = game.get_state()
    emit('game_state', state)


@socketio.on('game_over')
def handle_game_over(data):
    if data["points"] > 0:
        record = {
            "username": data["username"],
            "map_size": data["map_size"],
            "points": data["points"]
        }
        scores_collection.insert_one(record)

    emit('game_saved', {"status": "success"})


if __name__ == '__main__':
    socketio.run(app)
