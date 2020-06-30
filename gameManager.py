import random
import string
import time

import socketio

# sio = socketio.Client()


# @sio._handle_error(namespace='/battle', data='')
# def on_error(err):
#     print("error")
# @sio.on('connect', namespace='/battle')
# def on_connect():
#     print("I'm connected to the /battle namespace!")
#     sio.emit("message", "players")

# @sio.event
# def disconnect():
#     print("I'm disconnected")

# @sio.event
# def connect_error(err):
#     print("The connection failed!")
    
# @sio.event
# def players(players):
#     print("here")
#     print(players)
#     num = int(input("chose to play: "))
#     if num == -1:
#         return
#     sio.emit("play_with", players[num][0])

# @sio.event
# def ask_play(player):
#     print(player["player"] + " wants to play with you.")
#     input("type anything to start ")
#     sio.emit("accept", player["id"])


# @sio.on("message", namespace='/battle')
# def on_message(message):
#     print("message")



# try:
#     sio.connect('http://localhost:5000?username=Taras', namespaces=['/battle'])
# except socketio.exceptions.ConnectionError:
#     print("error")
# print('my sid is: ', sio.sid)



WIN_STOOTS = 60

class ShootType:
    WIN_GAME = "ти виграв"
    HIT = "ранив"
    KILL = "вбив корабель"
    MISS = "мимо"

sio = socketio.Client()

class GameManager(socketio.ClientNamespace):
    __shoots = 0
    

    def __init__(self, on_shoot, shot_answer_from, namespace):
        socketio.ClientNamespace.__init__(self, namespace)
        
        self.on_shoot = on_shoot
        self.shot_answer_from = shot_answer_from
        
    def on_connect(self):
        print("connected")
        self.emit("message", "players")

    def disconnect(self):
        print("I'm disconnected")
    
    def on_players(self, players):
        print(players)
        num = input("вибери з ким грати: ")
        if num.isnumeric():
            num = int(num)
            if num < len(players):
                print("Почекай з'єднання...")
                self.opponent = players[num][0]
                self.emit("play_with", self.opponent)
                return
        print("Чекайте поки Вас виберуть або перезапустіть.")

    def on_ask_play(self, player):
        print(player["player"] + " хоче грати з тобою")
        input("Напиши щось і починаєм > ")
        self.opponent = player["id"]
        self.emit("accept", self.opponent)

    def on_start(self, player_id):
        self.on_shoot("")
    
    def shoot_to(self, location):
        self.__shoots += 1
        self.emit("shot", {"player": self.opponent, "zone": location})
        #return ShootType.WIN_GAME if self.__shoots > WIN_STOOTS else random.choice([ShootType.HIT, ShootType.MISS, ShootType.KILL])
    def on_shot_answer(self, data):
        self.shot_answer_from(data)
    
    def shot_answer_to(self, answer):
        answer["player"] = self.opponent
        self.emit("shot_answer", answer)

    def on_shot(self, data):
        self.on_shoot(data["zone"])
    


    def opponent_shoot(self):
        print("...Почекай, я подумаю...")
        time.sleep(1.5)
        print("??? Зараз стріляю...")
        time.sleep(1)

        return random.choice(string.ascii_uppercase[0:10]) + str(random.randint(0, 10))
