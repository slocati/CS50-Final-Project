import os
import math
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Characters info used for the result
char_list = (
    {"name":"Luke Skywalker",
    "description":"Luke Skywalker always wanted to leave home, but he didn't expect that it would be as part of a quest to rescue a princess and save the galaxy",
    "file":"LUKE.jpg",
    "o":9,
    "c":4,
    "e":7,
    "a":9,
    "n":7},
    {"name":"Leia Organa",
    "description":"Princess-turned-General Leia Organa is a sharp, fearless royal who gets herself into trouble and fights her way out of it",
    "file":"LEIA.jpg",
    "o":8,
    "c":6,
    "e":8,
    "a":6,
    "n":6},
    {"name":"Han Solo",
    "description":"There's no one cooler than this intergalactic smuggler who hangs out in dens of iniquity all over the galaxy. And Han Solo knows it!",
    "file":"HAN.jpg",
    "o":7,
    "c":3,
    "e":9,
    "a":2,
    "n":4},
    {"name":"Obi Wan Kenobi",
    "description":"Obi-Wan Kenobi is a sage Jedi who doesn't need to say much to teach you a galaxy's worth of wisdom",
    "file":"OBI.jpg",
    "o":5,
    "c":8,
    "e":3,
    "a":5,
    "n":3}, 
    {"name":"Yoda",
    "description":"Yoda is wise, patient, and capable of kicking ass. He's done his best to mentor young Jedi and protect the balance of Light and Dark",
    "file":"YODA.jpg",
    "o":4,
    "c":7,
    "e":2,
    "a":4,
    "n":2},
    {"name":"C3PO",
    "description":"Sarcastic and always complaining, C3PO is a droid that despite his quirks you always want by your side",
    "file":"C3PO.jpg",
    "o":2,
    "c":9,
    "e":4,
    "a":3,
    "n":9},
    {"name":"R2D2",
    "description":"A reliable and versatile astromech droid, R2-D2 has shown great bravery in rescuing his masters and their friends from many perils. A skilled starship mechanic and fighter pilot's assistant",
    "file":"R2D2.jpg",
    "o":6,
    "c":5,
    "e":6,
    "a":7,
    "n":5},
    {"name": "Chewbacca",
    "description":"Chewbacca is a loyal co-pilot who won't hesitate to rip your arm off",
    "file":"CHEWBACCA.jpg",
    "o":3,
    "c":2,
    "e":5,
    "a":8,
    "n":8}
    )

#attributes used for questions
attribute_list= {
    "o":("curious", "creative", "aventurer", "open-minded"),
    "c":("selfcontroled", "organized", "meticulous", "dedicated"),
    "e":("sociable", "entusiast", "selfconfident", "expresive"),
    "a":("reliable", "altruist", "empathetic", "colaborative"),
    "n":("depresive", "anxious", "irritable", "sensitive")
    }

#answer values used for comparisson, starts at 5 (neutral)
answers_reg= {
    "o": 5,
    "c": 5,
    "e": 5,
    "a": 5,
    "n": 5
    }

#options list for answers and their value
options_list= {"Strongly agree": 2, "Agree": 1, "Neutral": 0, "Disagree": -1, "Strongly disagree": -2}

#least squares method result
sq_res= {}

#Variables for results for easy access
winner= ""
winner_res= 0
winner_desc= ""
winner_pic= ""

#Configure application
app = Flask(__name__)

#Ensure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def quiz():
    #builds quiz and registers answers
    if request.method == "POST":
        #resets answer registry to initial values
        answers_reg= {
            "o": 5,
            "c": 5,
            "e": 5,
            "a": 5,
            "n": 5
            }

        #calculates user attributes level based on his/her answers
        for k,v in attribute_list.items():
            for attribute in attribute_list[k]:
                answers_reg[k]= answers_reg[k] + int(request.form.get(attribute))

        #limits values to 1-10    
        for kk,vv in answers_reg.items():
            if answers_reg[kk] > 10:
                answers_reg[kk]= 10
            elif answers_reg[kk]< 1:
                answers_reg[kk]= 1

        #compares user attributes to each character attributes, through least squares method
        for char in char_list:
            sq_res[char["name"]]= 0
            for kkk,vvv in answers_reg.items():
                sq_res[char["name"]]= sq_res[char["name"]] + pow(answers_reg[kkk] - char[kkk], 2)
            #converts results to a % of coincidence
            sq_res[char["name"]]= float(1-math.sqrt(sq_res[char["name"]])/50)

        #reset variables
        winner_res= 0
        
        #Finds character with higher coincidence
        for kkkk,vvvv in sq_res.items():
            if sq_res[kkkk] > winner_res:
                winner= kkkk
                winner_res= sq_res[kkkk]

        #converts coincidence coefficient to %
        winner_res= int(winner_res*100)
        
        #populate description and file
        for e in char_list:
            if e["name"] == winner:
                winner_desc= e["description"]
                winner_pic= e["file"]


        return render_template("output.html", winner= winner, winner_res= winner_res, winner_desc= winner_desc, winner_pic= winner_pic)


    else:
        return render_template("quiz.html", attribute_list = attribute_list, options_list = options_list)