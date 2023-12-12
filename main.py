import turtle
import sys
import math
import heapq
from collections import defaultdict

#I convert the map to a graph, 0:{1:5, ...}} which mean that island 0 connect island 1 with a bridge have score is 5
graph = {
  0: {1: 5, 2: 7, 3: 1},
  1: {0: 5, 2: 9, 4: 2},
  2: {0: 7, 1: 9, 4: 7, 5: 4, 6: 3, 3: 6},
  3: {0: 1, 2: 6, 6: 5},
  4: {1: 2, 2: 7, 5: 4, 7: 5, 8: 5},
  5: {2: 4, 4: 4, 6: 1, 8: 3},
  6: {2: 3, 3: 5, 5: 1, 8: 5, 9: 8},
  7: {4: 5, 8: 5, 10: 1},
  8: {4: 5, 7: 5, 10: 2, 9: 4, 6: 5, 5: 3},
  9: {6: 8, 8: 4, 10: 3},
  10: {7: 1, 8: 2, 9: 8}
}

#set up for Djiktra Algorithm for the shortest path
def Djiktra(graph, start):
    distance = {vertex: float('infinity') for vertex in graph}
    distance[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance > distance[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            new_distance = current_distance + weight
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))
    return distance

start_vertex = 0
shortest_distance = Djiktra(graph, start_vertex)
list_of_shortest_distances =  []
for distance in shortest_distance.items():
    list_of_shortest_distances.append(distance)
shortest_path = list_of_shortest_distances[10][1]

#set up for DFS Algorithm for the Longest path
def dfs(graph, node, visited, current_length):
    visited[node] = True
    max_length = current_length
    for neighbor, weight in graph[node].items():
        if not visited[neighbor]:
            new_length = current_length + weight
            max_length = max(max_length, dfs(graph, neighbor, visited, new_length))
    visited[node] = False
    return max_length

def longest_path(graph):
    max_length = 0
    visited = {node: False for node in graph}
    for start_node in graph:
        max_length = max(max_length, dfs(graph, start_node, visited, 0))
    return max_length

longest_path_value = longest_path(graph)


# Set up the turtle screen

screen = turtle.Screen()
s = turtle.getscreen()
size = 70
w = 9 * size
h = 16 * size
s.screensize(h, w)
s.setup(h + 10, w + 10)

my_turtle = turtle.Turtle()
def build_background():
    screen.bgpic("bg.png")

# set up turtle island
turtle.addshape("island.gif")

#set up initial and final point
xi = -screen.window_width() / 2 + 60
yi = -screen.window_height() / 2 + 60
xf = screen.window_width() / 2 - 60
yf = screen.window_height() / 2 - 60
lenX = abs(xf - xi) / 4
lenY = abs(yf - yi) / 4

#set up island
dic_islands = {}
list_island = []
cnt = 0
list_island.append(((xi, (yi + yf) / 2))) # I map the island, The island's serial number corresponds to its coordinates
dic_islands[((xi, (yi + yf) / 2))] = cnt #I map the island, The island's coordinates corresponds to its serial number
i = xi + lenX
while(i <= xf - lenX):
    cnt += 1
    list_island.append((i,yi + lenY))
    dic_islands[(i,yi + lenY)] = cnt
    cnt += 1
    list_island.append((i,yi + 2 * lenY))
    dic_islands[(i,yi + 2 * lenY)] = cnt
    cnt += 1
    list_island.append((i,yi + 3 * lenY))
    dic_islands[(i,yi + 3 * lenY)] = cnt
    i += lenX
cnt += 1
list_island.append(((xf, (yi + yf) / 2)))
dic_islands[(xf, (yi + yf) / 2)] = cnt 
def build_island():
    for _ in range (len(list_island)):
        island = turtle.Turtle()
        island.shape("island.gif")
        island.penup()
        island.speed("fastest")
        island.goto(list_island[_][0], list_island[_][1])

#set up bridge
turtle.addshape("wood_parallel.gif")
turtle.addshape("wood_perpendicular.gif")
def setup_bridge(xI, yI, xF, yF):
  if(yI == yF and xI != xF):
    x = xI + 25
    y = yI - 10
    while(True):
      wood = turtle.Turtle()
      wood.shape("wood_perpendicular.gif")
      wood.penup()
      wood.speed("fastest")
      wood.goto(x + 10, y)
      x += 10
      if x > xF - 40:
        break
  elif(xI == xF and yI != yF):
    x = xI
    y = yI + 16
    while(True):
      wood = turtle.Turtle()
      wood.shape("wood_parallel.gif")
      wood.penup()
      wood.speed("fastest")
      wood.goto(x, y + 12)
      y += 12
      if y > yF - 40:
        break
  else:
    a = (yI - yF)/(xI - xF)
    b = yI - a * xI
    x = xI + 20
    y = a * x + b
    while(True):
      wood = turtle.Turtle()
      wood.shape("wood_perpendicular.gif")
      wood.penup()
      wood.speed("fastest")
      x += 10
      y =  a * x + b
      wood.goto(x, y)
      if y > yF - 40  and x > xF - 40:
        break
turtle.pendown()
#this is the way that I connect 2 island with each other by bridge
def build_Bridge():
    setup_bridge(list_island[0][0], list_island[0][1], list_island[1][0], list_island[1][1])
    setup_bridge(list_island[2][0], list_island[2][1], list_island[4][0], list_island[4][1])
    setup_bridge(list_island[4][0], list_island[4][1], list_island[8][0], list_island[8][1])
    setup_bridge(list_island[7][0], list_island[7][1], list_island[10][0], list_island[10][1])
    setup_bridge(list_island[0][0], list_island[0][1], list_island[3][0], list_island[3][1])
    setup_bridge(list_island[2][0], list_island[2][1], list_island[6][0], list_island[6][1])
    setup_bridge(list_island[6][0], list_island[6][1], list_island[8][0], list_island[8][1])
    setup_bridge(list_island[9][0], list_island[9][1], list_island[10][0], list_island[10][1])
    setup_bridge(list_island[0][0], list_island[0][1], list_island[2][0], list_island[2][1])
    for _ in range(1, 7):
        setup_bridge(list_island[_][0], list_island[_][1], list_island[_ + 3][0], list_island[_ + 3][1])
    setup_bridge(list_island[8][0], list_island[8][1], list_island[10][0], list_island[10][1])
    setup_bridge(list_island[1][0], list_island[1][1], list_island[2][0], list_island[2][1])
    setup_bridge(list_island[2][0], list_island[2][1], list_island[3][0], list_island[3][1])
    setup_bridge(list_island[4][0], list_island[4][1], list_island[5][0], list_island[5][1])
    setup_bridge(list_island[5][0], list_island[5][1], list_island[6][0], list_island[6][1])
    setup_bridge(list_island[7][0], list_island[7][1], list_island[8][0], list_island[8][1])
    setup_bridge(list_island[8][0], list_island[8][1], list_island[9][0], list_island[9][1])



#set up the connected island
#islands.append([1, 2, 3]) means island 0 connect to island 1, 2 , 3
#...
#islands.append([4, 7, 10, 9, 6, 5]) means island 8 connect to island 4, 7, 10, 9. 6, 5
islands = []
islands.append([1, 2, 3])
islands.append([0, 2, 4])
islands.append([0, 1, 4, 5, 6, 3])
islands.append([0, 2, 6])
islands.append([1, 2, 5, 7, 8])
islands.append([2, 4, 6, 8])
islands.append([2, 3, 5, 8, 9])
islands.append([4, 8, 10])
islands.append([4, 7, 10, 9, 6, 5])
islands.append([6, 8, 10])
islands.append([7, 8, 9])

#set up Viet Cong
viet_cong = turtle.Turtle()
turtle.addshape("viet_cong.gif")
viet_cong.shape("viet_cong.gif")
viet_cong.penup()
viet_cong.hideturtle()
viet_cong.speed("slowest")


results_ques=[2]
results_ans = [2]
ques0 = turtle.Turtle()
clickmouse = turtle.Turtle() 
wrong_answer = turtle.Turtle()
correct_answer = turtle.Turtle()

#if the ansewer is wrong, it will call wrongAnswer Function
def wrongAnswer():
    turtle.addshape("wrong_answer.gif")
    wrong_answer.shape("wrong_answer.gif")
    wrong_answer.penup()
    wrong_answer.hideturtle()
    wrong_answer.goto((xi + xf)/2, yi)
    wrong_answer.speed("slow")
    wrong_answer.showturtle()
    wrong_answer.goto(0, 0)
    wrong_answer.goto((xi + xf)/2, yi)
    wrong_answer.hideturtle()

#this is the way that when the question was show, player can choose the option
def click_handler_question(x, y):
    clickmouse.showturtle()
    clickmouse.goto(x, y)
    if y <= -70 and y >= -160:
        if x >= -160 and x < 0:
            results_ques.append(1)
        if x <= 160 and x > 0:
            results_ques.append(0) 

#the function that will show the question
def showQuestion(x, y):
    ques0.showturtle()

#when player click the mouse of the question
def answerQues(x, y):
    raw_file = "ques_" + str(x) + "_" + str(y) + ".gif"
    turtle.addshape(raw_file)
    ques0.shape(raw_file)
    ques0.penup()
    ques0.goto(0, 0)
    turtle.addshape("clickmouse.gif")
    clickmouse.shape("clickmouse.gif")
    clickmouse.penup()
    clickmouse.speed("slow")
    s.onclick(click_handler_question)
    return results_ques[-1]

#open the file that include answer of each question
dic_answer = {}
file_path = "dic_answer.txt"
with open(file_path, 'r') as file:
    for line in file:
        #splits line into words
        words = line.split()
        key = words[0]
        value = int(words[-1])
        dic_answer[key] = value

#open the file that include point of each bridge
dic_point = {}
file_path = "dic_point.txt"
with open(file_path, 'r') as file:
    for line in file:
        #splits line into words
        word = line.split()
        keys = word[0]
        value = int(word[-1])
        dic_point[keys] = value

#turle that show the score
total_score = 0
count_turtle = turtle.Turtle()
count_turtle.penup()
count_turtle.hideturtle()
count_turtle.goto(450, 250)

#function that update the score for the player
def update_count():
    count_turtle.clear()
    count_turtle.write("Total Score: {}".format(total_score), align="center", font=("Arial", 16, "normal"))

#function that will make the clickmouse go to the nearest island with the range is 50
def exactly_island(x, y):
    for i, island in enumerate(list_island):
        if math.sqrt((x - island[0]) ** 2 + (y - island[1]) ** 2) < 50:
            return island[0], island[1]
    return x, y

#the list that check player has chose the island or not
list_checked_bridge = []

#the function to determine the "click" of player is island or not, for example, the player click to sun or bridge is wrong
def is_that_island(x, y):
    for i, island in enumerate(list_island):
        if math.sqrt((x - island[0]) ** 2 + (y - island[1]) ** 2) < 50:
            return True
    return False

#the function to delete turtle
def remove_turtle_at_position(x, y):
    for t in turtle.turtles():
        if t.xcor() == x and t.ycor() == y:
            t.hideturtle()
            t.clear()
#the function to identify the bridge turtle and then delete
def delete_bridge(xI, yI, xF, yF):
    cnt_bridge = 0
    if(yI == yF and xI != xF):
        x = xI + 25
        y = yI - 10
        while(True):
            x += 10
            remove_turtle_at_position(x, y)
            cnt_bridge += 1
            if x > xF - 40 or cnt_bridge >= 23:
                break
    elif(xI == xF and yI != yF):
        x = xI
        y = yI + 16
        while(True):
            y += 12
            remove_turtle_at_position(x, y)
            cnt_bridge += 1
            if y > yF - 40 or cnt_bridge >= 23:
                break
    else:
        a = (yI - yF)/(xI - xF)
        b = yI - a * xI
        x = xI + 20
        y = a * x + b
        while(True):
            x += 10
            y =  a * x + b
            remove_turtle_at_position(x, y)
            cnt_bridge += 1
            if y > yF - 40  and x > xF - 40 or cnt_bridge >= 23:
                break

#if the bridge was chosen, then the player can not go by that bridge anymore
def check_bridge(xi, yi, xf, yf):
    pairI = (xi, yi)
    pairF = (exactly_island(xf, yf))
    pairOfPair = (pairI, pairF)
    if pairOfPair in list_checked_bridge:
        return True
    pairOfPair = (pairF, pairI)
    if pairOfPair in list_checked_bridge:
        return True
    return False

#function to check that there are any way for player to go, if no, then return false
def checkLoser(x, y):
    for i in islands[dic_islands[(x, y)]]:
        if check_bridge(x, y, list_island[i][0], list_island[i][1]) == False:
            return True
    return False

#function to end the game
def exit_program():
    sys.exit()

#function of click that process all most click 
def click_handler(x, y):
    global shortest_path
    global longest_path_value
    global total_score
    wrong_answer.hideturtle
    results_ques.clear()
    results_ques.append(2)
    results_ans.clear()
    results_ans.append(2)
    if is_that_island(x, y) == False: 
        s.onclick(click_handler)
    else:
        x, y = exactly_island(x, y)
        current_x = character.xcor()
        current_y = character.ycor()
        xI = current_x
        yI = current_y
        if dic_islands[(x, y)] not in islands[dic_islands[(xI, yI)]]:
            s.onclick(click_handler)
        else:
            if check_bridge(current_x, current_y, x, y) == True:
                s.onclick(click_handler)
            else:
                to_x = (current_x + x) / 2
                to_y = (current_y + y) / 2
                character.goto(to_x, to_y)
                ufo.goto(to_x,yi + 4 *lenY)
                current_x = ufo.xcor()
                current_y = ufo.ycor()
                viet_cong.goto(current_x, current_y - 5)
                viet_cong.showturtle()
                viet_cong.goto(to_x, to_y)
                viet_cong.hideturtle()
                showQuestion(to_x, to_y)
                clickmouse.showturtle()
                while(True):
                    result_ques = answerQues(to_x, to_y)
                    if result_ques != 2:
                        break
                ques0.hideturtle()
                turtle.addshape("loading.gif")
                ques0.shape("loading.gif")
                clickmouse.hideturtle()
                clickmouse.goto(0, 0)
                tmp = "ques_" + str(to_x) + "_" + str(to_y)
                if result_ques == dic_answer[tmp]:
                    correct_answer.showturtle()
                    tmp = "point_" + str(to_x) + "_" + str(to_y)
                    total_score += dic_point[tmp]
                    update_count()
                    correct_answer.hideturtle()
                    character.goto(x, y)
                    x, y = exactly_island(x, y)
                    character.goto(x, y)
                else:
                    wrongAnswer()
                    character.goto(xI, yI)
                clickmouse.hideturtle()
                clickmouse.goto(0, 0)
                pairI = (xI, yI)
                pairF = (exactly_island(x, y))
                pairOfPair = (pairI, pairF)
                list_checked_bridge.append(pairOfPair)
                pairOfPair = (pairF, pairI)
                list_checked_bridge.append(pairOfPair)
                delete_bridge(xI, yI, x, y)
                delete_bridge(x, y, xI, yI)
                current_x = character.xcor()
                current_y = character.ycor()
                if checkLoser(current_x, current_y) == False:
                        turtle.addshape("you_lose.gif")
                        you_lose = turtle.Turtle()
                        you_lose.shape("you_lose.gif")
                        you_lose.penup
                        you_lose.goto(0, 0)
                        screen.ontimer(you_lose.showturtle(), 2000)
                        s.onclick(exit_program())
                if current_x == list_island[10][0] and current_y == list_island[10][1]:
                    turtle.addshape("you_win.gif")
                    you_win = turtle.Turtle()
                    you_win.shape("you_win.gif")
                    you_win.penup
                    you_win.goto(0, 0)
                    offset = 20
                    font_letter = 20
                    shortest_turtle = turtle.Turtle()
                    shortest_turtle.penup()
                    shortest_turtle.hideturtle()
                    shortest_turtle.goto(0, 30 - offset)
                    str_shortest_path = "BEST SCORE: " + str(shortest_path)
                    shortest_turtle.write(str_shortest_path, align="center", font=("Times New Roman", font_letter, "normal"))

                    longest_turtle = turtle.Turtle()
                    longest_turtle.penup()
                    longest_turtle.hideturtle()
                    longest_turtle.goto(0, -40 - offset)
                    str_longest_path = "WORST SCORE: " + str(longest_path_value)
                    longest_turtle.write(str(str_longest_path), align="center", font=("Times New Roman", font_letter, "normal"))

                    yours_turtle = turtle.Turtle()
                    yours_turtle.penup()
                    yours_turtle.hideturtle()
                    yours_turtle.goto(0, -116 - offset)
                    str_total_score = "YOUR SCORE: " + str(total_score)
                    yours_turtle.write(str_total_score, align="center", font=("Times New Roman", font_letter, "normal"))

                    percen_turtle = turtle.Turtle()
                    percen_turtle.penup()
                    percen_turtle.hideturtle()
                    percen_turtle.goto(0, -186 - offset)
                    percen = (total_score - longest_path_value) / (shortest_path - longest_path_value) * 100
                    percentage = "{:.2f}".format(percen)
                    str_percen = "YOU WIN " + str(percentage) + "% OF THE GAME!"
                    percen_turtle.write(str_percen, align="center", font=("Times New Roman", font_letter, "normal"))
                    screen.ontimer(you_win.showturtle(), 10000)
                    # s.onclick(exit_program())
                s.onclick(click_handler)

results_menu = [2]
result_tutorial = [2]

#function to click and choose option of the menu
def click_handler_menu(x, y):
    clickmouse.showturtle()
    clickmouse.goto(x, y)
    if y <= 74 and y >= 20:
        if x >= -100 and x <= 100:
            results_menu.append(1)
    if y <= -50 and y >= -92:
        if x >= -136 and x <= 136:
            results_menu.append(0)
#function answer the menu
def answerMenu():
    turtle.addshape("clickmouse.gif")
    clickmouse.shape("clickmouse.gif")
    clickmouse.penup()
    clickmouse.speed("slow")
    s.onclick(click_handler_menu)
    return results_menu[-1]
#the function that if player choose tutorial of the menu of clicking
def click_handler_tutorial(x, y):
    clickmouse.showturtle()
    clickmouse.goto(x, y)
    if y <= 200 and y >= -234:
        if x >= -150 and x <= 150:
            result_tutorial.append(1)

#the function that if player chooser tutorial of the menu
def answerTutorial():
    turtle.addshape("clickmouse.gif")
    clickmouse.shape("clickmouse.gif")
    clickmouse.penup()
    clickmouse.speed("slow")
    s.onclick(click_handler_tutorial)
    return result_tutorial[-1]
#the function that will start the game
def start_game():
    s.onclick(click_handler)

#main function
if __name__ == "__main__":
    result_menu = [2]
    menu_game = turtle.Turtle()
    #show the menu
    turtle.addshape("menu_game.gif")
    menu_game.shape("menu_game.gif")
    menu_game.penup()
    result_for_menu = 2
    while(True):
        result_for_menu = answerMenu()
        if result_for_menu != 2:
            break
    clickmouse.hideturtle()
    #if player choose tutorial
    if result_for_menu == 0:
        tutorial = turtle.Turtle()
        turtle.addshape("tutorial.gif")
        tutorial.shape("tutorial.gif")
        tutorial.penup()
        result_for_tutorial = 2
        while(True):
            result_for_tutorial = answerTutorial()
            if result_for_tutorial == 1:
                break
        clickmouse.hideturtle()
        if result_for_tutorial == 1:
            menu_game.hideturtle()
            tutorial.hideturtle()
            build_background()
            build_island()
            build_Bridge()
            character = turtle.Turtle()
            turtle.addshape("character.gif")
            character.shape("character.gif")
            character.penup()
            character.goto(list_island[0][0], list_island[0][1])
            character.speed("fast")
            ufo = turtle.Turtle()
            turtle.addshape("ufo.gif")
            ufo.shape("ufo.gif")
            ufo.penup()
            ufo.speed("fast")
            ufo.goto(xf, yf)
            start_game()
                
    #if player choose start right now
    clickmouse.hideturtle()
    if result_for_menu == 1:
        menu_game.hideturtle()
        build_background()
        build_island()
        build_Bridge()
        character = turtle.Turtle()
        turtle.addshape("character.gif")
        character.shape("character.gif")
        character.penup()
        character.goto(list_island[0][0], list_island[0][1])
        character.speed("fast")
        ufo = turtle.Turtle()
        turtle.addshape("ufo.gif")
        ufo.shape("ufo.gif")
        ufo.penup()
        ufo.speed("fast")
        ufo.goto(xf, yf)
        start_game()
# Stamp the image
my_turtle.stamp()
turtle.mainloop()
