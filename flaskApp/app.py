from flask import Flask, render_template, request, redirect
import spoonacular as sp
import json
import requests
from bs4 import BeautifulSoup
from recipe import Recipe
from users import *
from methods import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")


def home():
    return render_template("index.html")

@app.route("/id", methods=['GET', 'POST'])
def id():
    if request.method == 'POST':
        
        data_input = str(request.form['data_input'])
        
        url = f"https://api.spoonacular.com/recipes/"+data_input+"/information"
        params = {
                    "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)
        recipe = parseData(data)

        return render_template("id.html", recipe = recipe)
    
@app.route("/random")
def random():

    api = sp.API("b67eb3c9d9f94a94bc7d8d966daa48fc")

    response = api.get_random_recipes()
        
    data = response.json()
    
    random = ""
    recepies = data['recipes'] 
    for recepieTitle in recepies:
        random = str(recepieTitle["id"])
    url = "https://api.spoonacular.com/recipes/" + random + "/information"
    params = {
                "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                
             }
    response = requests.get(url, params)
    data = json.loads(response.text)
    recipe = parseData(data)
    return render_template('random.html', recipe = recipe)

@app.route("/idInfo", methods = ['GET', 'POST'])
def idInfo():
    
        
        value = request.args.get('value')
        
        url = f"https://api.spoonacular.com/recipes/"+value+"/information"
        params = {
                    "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)

        recipe = parseData(data)
        return render_template("idInfo.html", recipe = recipe)

@app.route("/searchResults", methods=['GET', 'POST'])
def search():


    if request.method == 'POST':
        selection = str(request.form['search_criteria'])
        
        search = str(request.form['search_query'])
        if selection == "ingredient":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                        "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                        "query":search
                    }

            response = requests.get(url, params)
            data = json.loads(response.text)
            recipes = data['results']

            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)
        elif selection == "cuisine":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                    "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                    "cuisine":search,
                    "number":10
                      }
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            recipes = data['results'] 
            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)
        elif selection == "diet":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
            "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
            "diet":search,
            "number":10
            }
            response = requests.get(url, params)
            data = json.loads(response.text)
            recipes = data['results'] 
            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    return render_template("login.html" )

@app.route("/userdata", methods=['GET', 'POST'])
def userdata():
    username = str(request.form['user_name'])
    password = str(request.form['password'])

    recipeList = saved(username) 

    return render_template("userdata.html", recipeList=recipeList, username = username)

@app.route("/delete", methods=[ 'GET', 'POST'])
def delete():
    username = str(request.form['username'])
    recipe_id= str(request.form['recipe_id'])
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db['favorites']

    collection.delete_one({'_id': recipe_id})
    recipeList = saved(username)

    return render_template("userdata.html", recipeList=recipeList, username = username)




if __name__ == '__main__':
    app.run(debug=True, port=5001)



