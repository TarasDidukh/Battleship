import random
import string
import time

WIN_STOOTS = 60

class ShootType:
    WIN_GAME = "ти виграв"
    HIT = "ранив"
    KILL = "вбив корабель"
    MISS = "мимо"


class GameManager:
    __shoots = 0
    
    def shoot(self, location):
        self.__shoots += 1
        return ShootType.WIN_GAME if self.__shoots > WIN_STOOTS else random.choice([ShootType.HIT, ShootType.MISS, ShootType.KILL])

    def opponent_shoot(self):
        print("...Почекай, я подумаю...")
        time.sleep(1.5)
        print("??? Зараз стріляю...")
        time.sleep(1)

        return random.choice(string.ascii_uppercase[0:10]) + str(random.randint(0, 10))
