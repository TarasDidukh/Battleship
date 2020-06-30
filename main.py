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
  MISS="•"
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


def printField(f, retrieve = False):
    def convert(z): 
        return  z.type #str(z.x) + "-" + str(z.y)
    
    alphabet = "   A B C D E F G H J K\n"

    resultShip = alphabet
    for i in range(0, size):
        resultShip = resultShip + "{:02d}".format(i + 1) + " " + "|".join(map(convert,f[i])) + "\n"
    if not retrieve:
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

manager = None 
alphabet = "ABCDEFGHJK"

def save_current_state():
    game_file_current = open(os.path.join(path_original_field, "my_current.txt"), "wt")
    game_file_current.write(printField(field, True))
    game_file_current.close()

def save_opponent_state():
    game_file_opponent = open(os.path.join(path_original_field, "opponent.txt"), "wt")
    game_file_opponent.write(printField(opponent_field, True))
    game_file_opponent.close()

def shot_answer_from(data):
    location = data["zone"]
    result = data["answer"]
    parsed = parse(location)
    zone = opponent_field[parsed["y"]][parsed["x"]]
    
    
    if result == ShootType.MISS:
        zone.type = ZoneType.MISS
        save_opponent_state()
        print("Я промахнувся")
    elif result == ShootType.WIN_GAME:
        zone.type = ZoneType.HIT
        save_opponent_state()
        print("Ура, я Виграв!")
    elif result == ShootType.KILL:
        zone.type = ZoneType.HIT
        save_opponent_state()
        print("Кул, я потопив корабель!")
        move()
    else:
        zone.type = ZoneType.HIT
        save_opponent_state()
        print("Єс, попав.")
        move()

def move():
    printField(opponent_field)
    location = input("Стріляю: ")
    if location == ".":
        print("Кінець")
        return True
    manager.shoot_to(location)
    
def is_destroyed():
    for i in range(0, size):
        for j in range(0, size):
            if field[i][j].type == ZoneType.SHIP:
                return False  
    return True 

def check(x, y):
    if field[y][x].type in [ZoneType.MISS, ZoneType.SPACE]:
        return 0
    if field[y][x].type == ZoneType.SHIP:
        return 1
    return -1

def is_ship_destroyed(zone):
    for i in range(zone.x, -1, -1):
        res = check(i, zone.y)
        if res == 0:
            break
        elif res == 1:
            return False

    for i in range(zone.x, len(field)):
        res = check(i, zone.y)
        if res == 0:
            break
        elif res == 1:
            return False
            
    for i in range(zone.y, len(field[0])):
        res = check(zone.x, i)
        if res == 0:
            break
        elif res == 1:
            return False

    for i in range(zone.y, -1, -1):
        res = check(zone.x, i)
        if res == 0:
            break
        elif res == 1:
            return False
    
    return True

def parse(location):
    x = None
    y = None
    if location[0:2].isnumeric():
        y = int(location[0:2])
        x = alphabet.find(location[2])
    elif location[0].isnumeric():
        y = int(location[0])
        x = alphabet.find(location[1])
    elif location[1:3].isnumeric():
        y = int(location[1:3])
        x = alphabet.find(location[0])
    elif location[1].isnumeric():
        y = int(location[1])
        x = alphabet.find(location[0])

    if x == None or y == None:
        raise IndexError()
    return {"x": x, "y": y - 1}



def opponent(location):
    if location == "":
        move()
        return
    # location = manager.opponent_shoot()
    zone = None
    try:
        print("Мені стріляли: " + location)
        parsed = parse(location)
        zone = field[parsed["y"]][parsed["x"]]
    except:
        print("Противник написав: " + location)
        move()
        return
    
    if zone.type == ZoneType.SHIP:
        zone.type = ZoneType.HIT
        save_current_state()
        printField(field)
        if is_destroyed():
            print("Я програв!")
            manager.shot_answer_to({"zone": location, "answer": ShootType.WIN_GAME})
            return
        if is_ship_destroyed(zone):
            print("Мій корабель знищений!")
            manager.shot_answer_to({"zone": location, "answer": ShootType.KILL})
            return
        print("Нас підстрелили!")
        manager.shot_answer_to({"zone": location, "answer": ShootType.HIT})
    elif zone.type in [ZoneType.SPACE, ZoneType.MISS]:
        zone.type = ZoneType.MISS
        save_current_state()
        printField(field)
        print("Противник промахнувся!")
        manager.shot_answer_to({"zone": location, "answer": ShootType.MISS})
        move()
    else:
        print("Противник вже стріляв!")
        move()

manager = GameManager(opponent,shot_answer_from, "/battle")
sio.register_namespace(manager)
my_name = input("Напишіть своє ім'я: ")
try:
    
    server = "https://battle-ship-cc.herokuapp.com/"
    #server = "http://0.0.0.0:5000" # "http://localhost:5000"
    sio.connect(server + "?username=" + my_name, namespaces=['/battle'])
except:
    print("error")


# sio.sleep(5000)
# sio.sleep(100)
#printField()

print ("привіт від Лілеї")







print("Hello World")

sio.wait()
