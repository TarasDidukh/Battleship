import random
import uuid
import os
from gameManager import *

class Zone :
  x=0
  y=0
  def __init__(self, x , y , type):
    self.x=x
    self.y=y
    self.type=type
class ZoneType :
  SPACE=" "
  MISS="*"
  SHIP="#"
  HIT="x"
    

field = []
opponent_field = []
size = 10



# field = [
#         [Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP)],
#         [Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP)],
#         [Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP),Zone(0 , 0 , ZoneType.SHIP)]
#     ]
def init(f):
    for i in range(0, size):
        f.append([])
        for j in range(0, size):
            f[i].append( Zone(j , i , ZoneType.SPACE))

init(field)
init(opponent_field)

def fillShip(x, y, length, isVertical):
    # TODO заповнити корабель чи 1, 2, 3, 4
    
    # тут я перевіряю чи достатньо місця щоб построїти корабель
    if (isVertical and y + length > size) or (not isVertical and x + length > size):
        # print("Помилка, недостатньо місця для корабля")
        return False
    
    # Початок: перевірка чи по сторонах нема інших кораблів
    offsetX = length + 1
    offsetY = length + 1
    if isVertical:
        offsetX = 2
    else:
        offsetY = 2
  
    for i in range(y - 1, y + offsetY):
        for j in range(x - 1, x + offsetX):
            if i < 0 or j < 0:
                continue
            if i >= len(field) or j >= len(field[y]):
                continue
            if field[i][j].type != ZoneType.SPACE:
                # print("Помилка, корабель уже висталений")
                return False
    # Кінець перевірки чи по сторонах нема інших кораблів
    
    # Якщо дійшло до цього коду, то можна ставити корабель, що і роблю
    start = y if isVertical else x 
    for i in range(start, start + length):
        x = x if isVertical else i
        y = y if not isVertical else i
        field[y][x] = Zone(x, y, ZoneType.SHIP)
    return True


# fillShip(7, 7, 3, True)
# field[0][0] = Zone(0, 0, ZoneType.SHIP)

# fillShip(0, 1, 4, True)

# fillShip(2, 4, 1, False)

# fillShip(4, 3, 2, False)

# fillShip(9, 9, 1, False)

# fillShip(7, 0, 3, False)

# fillShip(2, 0, 3, True)

# fillShip(2, 9, 1, True)

# fillShip(0, 9, 1, True)

# fillShip(8, 6, 2, True)

# fillShip(5, 0, 2, True)


def fill_random():
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    
    for ship in ships:
        while not fillShip( random.randint(0, 9), random.randint(0, 9), ship, not random.randint(0,1) ):
            pass


def printField(f):
    def convert(z): 
        return  z.type #str(z.x) + "-" + str(z.y)
    
    alphabet = "   A B C D E F G H J K\n"

    resultShip = alphabet
    for i in range(0, size):
        resultShip = resultShip + "{:02d}".format(i + 1) + " " + "|".join(map(convert,f[i])) + "\n"
    print(resultShip)
    
    return resultShip
    


print("Result:")
fill_random()

# тут я генерую унікальний ід на 8 символів
dirName = str(uuid.uuid4())[:8]
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

# тут я створюю папку і записую свій та противника полі
path_original_field = os.path.join(os.path.dirname(__file__), dirName)
game_file = open(os.path.join(path_original_field, "my.txt"), "wt")
game_file_current = open(os.path.join(path_original_field, "my_current.txt"), "wt")
game_file_opponent = open(os.path.join(path_original_field, "opponent.txt"), "wt")
game_file.write( printField(field) )
game_file_opponent.write( printField(opponent_field) )
game_file.close()
game_file_opponent.close()

manager = GameManager()
alphabet = "ABCDEFGHJK"

def save_current_state():
    game_file_current = open(os.path.join(path_original_field, "my_current.txt"), "wt")
    game_file_current.write(printField(field))
    game_file_current.close()

def move():
    save_current_state()
    printField(field)
    location = input("Стріляю: ")
    if location == ".":
        print("Кінець")
        return True
    result = manager.shoot(location)
    
    if result == ShootType.MISS:
        print("Я промахнувся")
        opponent()
    elif result == ShootType.WIN_GAME:
        print("Ура, я Виграв!")
    else:
        print("Єс, попав.")
        move()
    
def is_destroyed():
    for i in range(0, size):
        for j in range(0, size):
            if field[i][j].type == ZoneType.SHIP:
                return False  
    return True 

def opponent():
    save_current_state()
    location = manager.opponent_shoot()
    print("location: " + location[0] + str(int(location[1]) + 1) )
    zone = field[int(location[1])][alphabet.find(location[0])]
    if zone.type == ZoneType.SHIP:
        zone.type = ZoneType.HIT
        print("Нас підстрелили!")
        if is_destroyed():
            print("Я програв!")
            return
        opponent()
    elif zone.type in [ZoneType.SPACE, ZoneType.MISS]:
        print("Противник промахнувся!")
        zone.type = ZoneType.MISS
        move()
    else:
        print("Противник вже стріляв!")
        move()
#printField()
move()





        


