import turtle 

import time 

import random 



delay = 0.1 



import mysql.connector 

mydb=mysql.connector.connect(host="localhost",user="root",passwd="pavan4404",database="Python_Game",charset="utf8") 

mycursor=mydb.cursor()

mycursor.execute("create table if not exists hs(high int)")
mydb.commit()

mycursor.execute("insert into hs values(0)")
mydb.commit()

mycursor.execute("select * from hs") 

myres=mycursor.fetchall() 

         

# Score 

score = 0 
if(myres[-1][0]==0):
    high_score = myres[-2][0]
else:
    high_score = myres[-1][0]

 

# Set up the screen 

wn = turtle.Screen() 

wn.title("Snake Game by Pavan") 

wn.bgcolor("lightgreen") 

wn.setup(width=650, height=630) 

wn.tracer(0) # Turns off the screen updates 

 

# Snake head 

head = turtle.Turtle() 

head.speed(0) 

head.shape("square") 

head.color("black") 

head.penup() 

head.goto(0,0) 

head.direction = "stop" 

 

# Snake food 

food = turtle.Turtle() 

food.speed(0) 

food.shape("circle") 

food.color("red") 

food.penup() 

food.goto(0,280) 

 

segments = [] 

 

# Pen 

pen = turtle.Turtle() 

pen.speed(0) 

pen.shape("circle") 

pen.color("black") 

pen.penup() 

pen.hideturtle() 

pen.goto(0,250) 

pen.write("Score: {}  High Score: {}".format(score,high_score), align="center", font=("Courier", 24, "normal")) 

 

pen1 = turtle.Turtle() 

pen1.shape("circle") 

pen1.color("black") 

pen1.penup() 

pen1.hideturtle() 

pen1.goto(0,200) 

 

# Functions 

def go_up(): 

    if head.direction != "down": 

        head.direction = "up" 

 

def go_down(): 

    if head.direction != "up": 

        head.direction = "down" 

 

def go_left(): 

    if head.direction != "right": 

        head.direction = "left" 

 

def go_right(): 

    if head.direction != "left": 

        head.direction = "right" 

 

def move(): 

    if head.direction == "up": 

        y = head.ycor() 

        head.sety(y+20) 

 

    if head.direction == "down": 

        y = head.ycor() 

        head.sety(y-20) 

 

    if head.direction == "left": 

        x = head.xcor() 

        head.setx(x-20) 

 

    if head.direction == "right": 

        x = head.xcor() 

        head.setx(x+20) 

 

# Keyboard bindings 

wn.listen() 

wn.onkeypress(go_up,"Up") 

wn.onkeypress(go_down,"Down") 

wn.onkeypress(go_left,"Left") 

wn.onkeypress(go_right,"Right") 

 

# Main game loop 

while True: 

    wn.update() 

 

    # Check for a collision with the border 

    if head.xcor()>300 or head.xcor()<-300 or head.ycor()>300 or head.ycor()<-300:


        pen.clear() 

        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))  

        pen1.write("You Lost!!! Start Again", align="center", font=("Courier", 30, "bold"))
        
        if(score > high_score):
                
            sql="insert into hs(high) values (%s)" 

            mycursor.execute(sql,[high_score]) 

            mydb.commit() 
        

        time.sleep(2) 

        head.goto(0,0) 

        head.direction = "stop" 

                   

        # Hide the segments 

        for segment in segments: 

            segment.goto(1000, 1000) 

         

        # Clear the segments list 

        segments.clear() 

         

        # Reset the score 

        score = 0 

 

        # Reset the delay 

        delay = 0.1 
 

    # Check for a collision with the food 

    if head.distance(food) < 20: 

        # Move the food to a random spot 

        x = random.randint(-300,300) 

        y = random.randint(-300,300) 

        food.goto(x,y) 

 

        # Add a segment 

        new_segment = turtle.Turtle() 

        new_segment.speed(0) 

        new_segment.shape("circle") 

        new_segment.color("brown") 

        new_segment.penup() 

        segments.append(new_segment) 

 

        # Shorten the delay 

        delay -= 0.001 

 

        # Increase the score 

        score += 10 

 

        if score > high_score: 

            high_score = score 

         

        pen.clear() 

        pen1.clear() 

        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))  

 

    # Move the end segments first in reverse order 

    for index in range(len(segments)-1, 0, -1): 

        x = segments[index-1].xcor() 

        y = segments[index-1].ycor() 

        segments[index].goto(x, y) 

 

    # Move segment 0 to where the head is 

    if len(segments) > 0: 

        x = head.xcor() 

        y = head.ycor() 

        segments[0].goto(x,y) 

    move()     

 

    # Check for head collision with the body segments 

    for segment in segments: 

        if segment.distance(head) < 20:
            

            # Update the score display 


            pen.clear()

            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

            pen1.write("You Lost!!! Start Again", align="center", font=("Courier", 30, "bold"))

            if(score>high_score):

                sql="insert into hs(high) values (%s)" 

                mycursor.execute(sql,[high_score]) 

                mydb.commit() 



            time.sleep(2) 

            head.goto(0,0) 

            head.direction = "stop" 

            # Hide the segments 

            for segment in segments: 

                segment.goto(1000, 1000)  

            # Clear the segments list 

            segments.clear() 

            # Reset the score 

            score = 0 

            # Reset the delay 

            delay = 0.1             
 

    time.sleep(delay) 

 

wn.mainloop() 

sql="Delete from hs where high=0" 

mycursor.execute(sql) 

sql="insert into hs(high) values (%s)" 

mycursor.execute(sql,[high_score]) 

mydb.commit()
