from flask import *
from menousdb import *
from flask_session import Session
from functools import wraps
import json
import os
import sys
from auth import *
import json
from secrets import token_urlsafe
from pathlib import Path
import os
import getpass
import sys

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

API_URL = "http://127.0.0.1:5555/"

if sys.platform == "darwin":
    if not os.path.exists("/Library/Caches/.menousdb"):
        os.mkdir("/Library/Caches/.menousdb")
    if not os.path.exists("/Library/Caches/.menousdb/authdata"):
        os.mkdir("/Library/Caches/.menousdb/authdata")
    path = "/Library/Caches/.menousdb/authdata"

elif sys.platform == "win32":
    if not os.path.exists(os.getenv("APPDATA")+"\\MenoudDb"):
        os.mkdir(os.getenv("APPDATA")+"\\MenoudDb")
    if not os.path.exists(os.getenv("APPDATA")+"\\MenoudDb"+"\\authdata"):
        os.mkdir(os.getenv("APPDATA")+"\\MenoudDb\\authdata")
    path = os.getenv("APPDATA")+"\\MenoudDb"+"\\authdata"


def check_key(key):
    with open(path+'/keys.json') as file:
        data = json.load(file)

    if key in data:
        return True
    else:
        return False

def generate_key():
    with open(path+'/keys.json') as file:
        data = json.load(file)

    key = token_urlsafe(16)

    with open(path+'/keys.json', 'w') as file:
        data.append(key)
        json.dump(data, file, indent=4)

    return key

def login(username, password):
    if not os.path.exists(path + "/login.json"):
        with open(path + "/login.json", 'w') as file:
            file.dump({})
        return 'Sign Up Required! Please contact Administrator'
    with open(path + "/login.json", 'r') as file:
        data = json.load(file)
        for i in data:
            if i == username and data[i][0] == password:
                return True
        return False
    
def getUserKey(username):
    with open(path + "/login.json", 'r') as file:
        data = json.load(file)
        for i in data:
            if i == username:
                return data[i][0]

def signup():
    with open(path + "/login.json", "r") as file:
        data = json.load(file)
    
    while True:
        print("~~~~~~~~~~~~~~~~~~~~~~WELCOME TO MENOUSDB~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        uname = input("ENTER A USERNAME: ")
        pw = getpass.getpass("ENTER PASSWORD: ")
        confirm = getpass.getpass("RE-ENTER PASSWORD: ")
        if pw == confirm:
            data[uname] = [pw, generate_key()]
            with open(path + "/login.json", "w") as file:
                json.dump(data, file, indent=4)
            exit()
        else:
            print("ERROR! PASSWORDS DO NOT MATCH! TRY AGAIN!\n")

def checksignup():
    with open(path + "/login.json", "r") as file:
        data = json.load(file)

    if data == {}:
        signup()

checksignup()

databaseHTML = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <style>
        .container {
            width: 50%;
            background-color: aliceblue;
            text-align: center;
            padding: 50px;
            position: absolute;
            left:50%;
            top:50%;
            transform: translate(-50%, -50%);
        }
        .list-group{
            text-align: left;
            margin-top: 30px;
        }

    </style>
</head>
<body>
    <script>
        var counts = 0
        function addFields(){
            let modal_body=document.getElementsByClassName("modal-body")[0];
            // console.log(document.getElementById("parameter1").value);
            let div1 = document.createElement("div");
            div1.setAttribute("class","mb-3");
            let inp = document.createElement("input");
            inp.setAttribute("type", "text");
            inp.setAttribute("class", "form-control"); 
            inp.setAttribute("name", `param${counts}`);
            div1.appendChild(inp);
            modal_body.appendChild(div1);
            counts++;
        }
    </script>
    <nav class="navbar navbar-dark navbar-expand-lg bg-dark justify-content-center">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Menous DB</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ">
            <li class="nav-item">
              <a class="nav-link" href="/view">My Databases</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Modal title</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post" id = "modal-form-1">
                <div class="modal-body">

                    <div class="mb-3">
                        <label class="form-label">Enter Table Name: </label>
                        <input type="text" class="form-control" id="exampleInputPassword1" name = "table_name">
                      </div>

                      <div class="mb-3">
                        <label class="form-label">Enter Parammeters: </label>
                        <input type="text" class="form-control" id="parameter1" name = "param">
                      </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="addFields()">Add Parameter</button>
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </div>
            </form>
            
          </div>
        </div>
      </div>
      
      <div class="modal fade" id="staticBackdrop4" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Delete</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post">
              <div class="modal-body">
                <h4>Are you sure you want to delete this Database?</h4>
                </div>
                <div class="modal-footer">
                  <button type="submit" name = "deleteDatabase" class="btn btn-danger" onclick="checkForm()">Delete</button>
                </div>
          </form>

          </div>
        </div>
      </div>

    <div class = "container">
        
        <h1>Database: {{database }}</h1>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop4">
          Delete This Database
      </button>
        <button name = "add" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop1">
            Add Table
        </button>
        
        <div class="list-group">
            {% for i in tables %}
                <a href="/view/{{database}}/{{i}}" class="list-group-item list-group-item-action">{{i}}</a>
            {% endfor %}
      </div>
    </div>
    
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js" integrity="sha384-Y4oOpwW3duJdCWv5ly8SCFYWqFDsfob/3GkgExXKV4idmbt98QcxXYs9UoXAB7BZ" crossorigin="anonymous"></script>
</body>
</html>

"""
indexHTML="""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <style>
        .container {
            width: 50%;
            background-color: aliceblue;
            text-align: center;
            padding: 50px;
            position: absolute;
            left:50%;
            top:50%;
            transform: translate(-50%, -50%);
        }
        .list-group{
            text-align: left;
            margin-top: 30px;
        }

    </style>
</head>
<body>
    <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Modal title</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post">
                <div class="modal-body">

                    <div class="mb-3">
                        <label class="form-label">Enter Database Name: </label>
                        <input type="text" class="form-control" id="exampleInputPassword1" name = "database_name">
                      </div>
                  </div>
                  <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </div>
            </form>
            
          </div>
        </div>
      </div>
    <div class = "container">
    
    <h1>Select Database</h1>


        <button name = "add" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop1">
            Add Database
        </button>

        <div class="list-group">
            {% for i in databases %}
                <a href="/view/{{i}}" class="list-group-item list-group-item-action">{{i}}</a>
            {% endfor %}
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js" integrity="sha384-Y4oOpwW3duJdCWv5ly8SCFYWqFDsfob/3GkgExXKV4idmbt98QcxXYs9UoXAB7BZ" crossorigin="anonymous"></script>
</body>
</html>

"""
loginHTML="""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <style>
        .container {
            width: 50%;
            background-color: aliceblue;
            text-align: left;
            padding: 50px;
            position: absolute;
            left:50%;
            top:50%;
            transform: translate(-50%, -50%);
        }
        .list-group{
            text-align: left;
            margin-top: 30px;
        }

    </style>
</head>
<body>
          
    <div class = "container">
        <form method="POST">
            {% if loggFail == True %}
            <div class="alert alert-danger" role="alert">
               Login Failed! Check username and password
              </div>
            {% endif %}
            {% if signup == True %}
            <div class="alert alert-danger" role="alert">
                {{ msg }}
              </div>
            {% endif %}
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Enter Username</label>
              <input placeholder="Enter Username"type="text" class="form-control" name="username" id="username" aria-describedby="emailHelp">
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" name="password"id="password">
            </div>
            
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        
    </div>
    
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js" integrity="sha384-Y4oOpwW3duJdCWv5ly8SCFYWqFDsfob/3GkgExXKV4idmbt98QcxXYs9UoXAB7BZ" crossorigin="anonymous"></script>
</body>
</html>

"""
tableHTML="""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <style>
        #myInput {
            background-image: url('https://www.w3schools.com/css/searchicon.png'); /* Add a search icon to input */
            background-position: 10px 12px; /* position the search icon */
            background-repeat: no-repeat; /* Do not repeat the icon image */
            width: 50%; /* Full-width */
            font-size: 16px; /* Increase font-size */
            padding: 12px 20px 12px 40px; /* Add some padding */
            border: 1px solid #ddd; /* Add a grey border */
            margin: auto;
            align-content: center;
            margin-bottom: 12px; /* Add some space below the input */
            margin-top: 12px;
            border-radius: 5px;
            /*float: none;*/
        }
        #myForm{
          justify-content: center;
          align-items: center;
          text-align: center;
        }
        #myForm button{
          margin-left: 30px;
        }
    </style>

</head>
<body>
  <nav class="navbar navbar-dark navbar-expand-lg bg-dark justify-content-center">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Menous DB</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ">
          <li class="nav-item">
            <a class="nav-link" href="/view">My Databases</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

    <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Enter</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form>
                <div class="modal-body">
                    {% for i in data['attributes'] %}
                    <div class="mb-3">
                        <label class="form-label">{{i}}</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" name = "{{i}}"">
                      </div>
                    {% endfor %}
                  </div>
                  <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </div>
            </form>
            
          </div>
        </div>
      </div>

      <div class="modal fade" id="staticBackdrop2" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Update</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post">
                <div class="modal-body">
                  <p>Where Attributes = values </p>
                  <div id="updateOriginal">
                    <div class="input-group" >
                      <input type="text" class="form-control" placeholder="Attribute" style="margin-bottom:20px;" name="originalAttribute" onkeyup="checkForm()">
                      <input type="text" class="form-control" placeholder="Value" style="margin-bottom:20px;" name = "originalValue" onkeyup="checkForm()">
                    </div>
                  </div>
                  
                  <p>Change to Attributes = new values</p>
                  <div id="updateNew">
                    <div class="input-group">
                      <input type="text" class="form-control" placeholder="Attribute" style="margin-bottom:20px;" name="newAttribute" onkeyup="checkForm()">
                      <input type="text" class="form-control" placeholder="New Value" style="margin-bottom:20px;" name="newValue" onkeyup="checkForm()">
                    </div>
                  </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="addFields1()">Add Condition</button>
                    <button type="button" class="btn btn-secondary" onclick="addFields2()">Add New Value</button>
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </div>
            </form>
            
          </div>
        </div>
      </div>

      <div class="modal fade" id="staticBackdrop3" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Delete</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post">
              <div class="modal-body">
                <p>Where Attributes = values </p>
                <div id="deleteWhere">
                  <div class="input-group" >
                    <input type="text" class="form-control" placeholder="Attribute" style="margin-bottom:20px;" name="deleteAttribute" onkeyup="checkForm()">
                    <input type="text" class="form-control" placeholder="Value" style="margin-bottom:20px;" name = "deleteValue" onkeyup="checkForm()">
                  </div>
                </div>
                
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" onclick="addFields3()">Add Condition</button>
                  <button type="submit" class="btn btn-primary" onclick="checkForm()">Submit</button>
                </div>
          </form>

          </div>
        </div>
      </div>

      <div class="modal fade" id="staticBackdrop4" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="staticBackdropLabel">Delete</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post">
              <div class="modal-body">
                <h4>Are you sure you want to delete this table?</h4>
                </div>
                <div class="modal-footer">
                  <button type="submit" name = "deleteTable" class="btn btn-danger" onclick="checkForm()">Delete</button>
                </div>
          </form>

          </div>
        </div>
      </div>
    <form id="myForm">
        <label for="myInput"></label>
        <input type="text" id="myInput" onkeyup="myFunction()"
               placeholder="Search for entries by and parameters except id">
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop1">
            Add Entry
        </button>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop2">
          Update Entry
      </button>
      <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop3">
        Delete Entry
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop4">
      Delete Table
  </button>
    </form>

    <table id = "myTable" class="table table-hover table-bordered">
        <thead id="tableHead">
          <tr>
            <th scope="col">Id</th>
            {% for i in data['attributes'] %}
                <th scope="col">{{i}}</th>
            {% endfor %}
          </tr>
        </thead>
        <tbody>
          
            {% for i in data %}
            <tr>
                {% if i != "attributes" %}
                    <th scope="row">{{ i }}</th>
                    {% for j in data['attributes'] %}
                        <td>{{ data[i][j] }}</td>
                    {% endfor %}
                {% endif %}
            </tr>
            {% endfor %}
        </tbody>
      </table>
      <script>
        
function myFunction() {
// Declare variables
var input, filter, table, tr, td, i;
input = document.getElementById("myInput");
filter = input.value.toUpperCase();
table = document.getElementById("myTable");
thead = document.getElementsByTagName("thead");
tr = table.getElementsByTagName("tr");

// Loop through all table rows, and hide those who don't match the search query
for (i = 0; i < tr.length; i++) {
  td = tr[i].getElementsByTagName("td");
  var ans = 0;
  for (k=0; k< td.length; k++){
    tdd = td[k]
    if(tdd){
      txtValue = tdd.textContent || tdd.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        ans++;
      }
    }
  }
  if (ans > 0) {
    tr[i].style.display = "";
  } else {
    tr[i].style.display = "none";
  }
}
}
head = document.getElementById("tableHead");
ths = head.getElementsByTagName("th");
let attributes = [];
for (var i = 1; i < ths.length; i++) {
  array.push(ths[i].innerText);
}

var counts = 1;
function addFields1(){
  let updateOriginal = document.getElementById("updateOriginal")
  // let updateNew = document.getElementById("updateNew")
  let div = document.createElement("div");
  div.setAttribute("class", "input-group")

  let inp1 = document.createElement("input");
  inp1.setAttribute("type", "text");
  inp1.setAttribute("class","form-control");
  inp1.setAttribute("placeholder","Attribute");
  inp1.setAttribute("name",`originalAttribute${counts}`);
  inp1.setAttribute("style","margin-bottom:20px;")

  let inp2 = document.createElement("input");
  inp2.setAttribute("type", "text");
  inp2.setAttribute("class","form-control");
  inp2.setAttribute("placeholder","Value");
  inp2.setAttribute("name",`originalValue${counts}`);
  inp2.setAttribute("style","margin-bottom:20px;")

  div.appendChild(inp1);
  div.appendChild(inp2);

  updateOriginal.appendChild(div);
  counts++;
}

counts = 1;

function addFields2(){
  let updateOriginal = document.getElementById("updateNew")
  // let updateNew = document.getElementById("updateNew")
  let div = document.createElement("div");
  div.setAttribute("class", "input-group")

  let inp1 = document.createElement("input");
  inp1.setAttribute("type", "text");
  inp1.setAttribute("class","form-control");
  inp1.setAttribute("placeholder","Attribute");
  inp1.setAttribute("name",`newAttribute${counts}`);
  inp1.setAttribute("style","margin-bottom:20px;")

  let inp2 = document.createElement("input");
  inp2.setAttribute("type", "text");
  inp2.setAttribute("class","form-control");
  inp2.setAttribute("placeholder","New Value");
  inp2.setAttribute("name",`newValue${counts}`);
  inp2.setAttribute("style","margin-bottom:20px;")

  div.appendChild(inp1);
  div.appendChild(inp2);

  updateOriginal.appendChild(div);
  counts++;
}

function addFields3(){
  let updateOriginal = document.getElementById("deleteWhere")
  // let updateNew = document.getElementById("updateNew")
  let div = document.createElement("div");
  div.setAttribute("class", "input-group")

  let inp1 = document.createElement("input");
  inp1.setAttribute("type", "text");
  inp1.setAttribute("class","form-control");
  inp1.setAttribute("placeholder","Attribute");
  inp1.setAttribute("name",`deleteAttribute${counts}`);
  inp1.setAttribute("style","margin-bottom:20px;")

  let inp2 = document.createElement("input");
  inp2.setAttribute("type", "text");
  inp2.setAttribute("class","form-control");
  inp2.setAttribute("placeholder","New Value");
  inp2.setAttribute("name",`deleteValue${counts}`);
  inp2.setAttribute("style","margin-bottom:20px;")

  div.appendChild(inp1);
  div.appendChild(inp2);

  updateOriginal.appendChild(div);
  counts++;
}
function checkAttibutes(attribute){
  yes = false;
  for (i = 0; i < attributes.length; i++) 
  {
    if (i == attribute)
    {
      yes = true;
      break;
    }
  }
  if (yes == false){
    alert("Attributes Do Not Match. Kindly Check the Attributes!")
  }
}
function checkForm(){
  originalForm = document.getElementById("updateOriginal");
  inpGroups = originalForm.getElementsByClassName("input-group");
  inps = [];
  for (i = 0; i < inpGroups.length; i++)
  {
    inps.push(inpGroups[i][0].value);
  }
  for (i=0; i<inps.length; i++)
  {
    checkAttibutes(inps[i]);
  }
}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js" integrity="sha384-Y4oOpwW3duJdCWv5ly8SCFYWqFDsfob/3GkgExXKV4idmbt98QcxXYs9UoXAB7BZ" crossorigin="anonymous"></script>
</body>
</html>
"""

filePath = Path(__file__).parent
if not os.path.exists(os.path.join(filePath, "templates")):
    os.mkdir(os.path.join(filePath, "templates"))

templatePath = os.path.join(filePath, "templates")

if not os.path.exists(os.path.join(templatePath,"index.html")):
    with open(os.path.join(templatePath,"index.html"), "w") as file:
        file.write(indexHTML)
if not os.path.exists(os.path.join(templatePath,"table.html")):
    with open(os.path.join(templatePath,"table.html"), "w") as file:
        file.write(tableHTML)
if not os.path.exists(os.path.join(templatePath,"database.html")):
    with open(os.path.join(templatePath,"database.html"), "w") as file:
        file.write(databaseHTML)
if not os.path.exists(os.path.join(templatePath,"login.html")):
    with open(os.path.join(templatePath,"login.html"), "w") as file:
        file.write(loginHTML)
        
# Author : Snehashish Laskar
# Date Stated : 1st November 2022
# Version : 0.1.0
# Copyright (C) Snehashish Laskar 2023
# LICENSE: MIT OPen Source Software License

# This is a python module for interacting with the
# MenousDb database. To actually use the database,
# You must download it from github link given below:
# Link :

# Import the only necessary module
import requests as req

"""
methods included:

1: readDB (key, database)
2: create-db (key, database)
3: check-db-exists (key, database)
4: del-database (key database)
5: check-table-exists (key, database, table)
6: create-table (key, database, table, attributes)
7: insert-into-table (key, database, table, values)
8: select-where (key, database, table, conditions)
9: select-columns (key, database, table, columns)
10: select-columns-where (key, database, table, columns, conditions)
11: delete-where (table, conditions)
12: delete-table (table)
13: update-table (table, conditions, values)

"""

class MenousDB:

    """
    To interact with the database, we need to create a
    and instance of the MenoudDb class. This class helps
    """

    def __init__(self, url, key, database):
        self.url = url
        self.key = key
        self.database = database

    def readDB(self):

        if self.database == None:
            raise Exception('No database')

        Headers = {
            'key': self.key,
            'database': self.database
        }
        ans = req.get(self.url + 'read-db', headers=Headers)
        try:
            return ans.json()
        except:
            return ans.text


    def createDb(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.post(self.url + 'create-db', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def deleteDatabase(self):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.delete(self.url + 'del-database', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def checkDbExists(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.get(self.url + 'check-db-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def createTable(self, table:str, attributes:list):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'attributes': attributes
            }

            ans = req.post(self.url + 'create-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def __str__(self) -> str:
        return self.database

    def checkTableExists(self, table):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            ans = req.get(self.url + 'check-table-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def insertIntoTable(self, table, values):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'values': values,
            }

            ans = req.post(self.url + 'insert-into-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def selectWhere(self, table, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'conditions': conditions
            }

            ans = req.get(self.url + 'select-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumns(self, table, columns):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns
            }

            ans = req.get(self.url + 'select-columns', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumnsWhere(self, table, columns, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns,
                'conditions': conditions,
            }

            ans = req.get(self.url + 'select-columns-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def delete_where(self, table, conditions):
        if self.database == None:
            raise Exception('No Database')
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions
            }

            ans = req.delete(self.url+"delete-where", headers = Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            return ex

    def delete_table(self, table):
            if self.database == None:
                raise Exception('No Database')
            try:
                Headers = {
                    'key': self.key,
                    'database': self.database,
                    'table': table,
                }
                ans = req.delete(self.url + "delete-table", headers=Headers)
                try:
                    return ans.json()
                except:
                    return ans.text
            except Exception as ex:
                return ex


    def update_table(self, table, conditions, values):
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions,
                'values':values
            }
            ans = req.post(self.url+'update-table', headers=Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            return ex
        

    def get_databases(self):
        try:
            Headers = {
                'key': self.key,
            }
            ans = req.get(self.url+'get-databases', headers=Headers)
            try:
                return ans.json()
            except:
                return ans.text()
        except Exception as ex:
            return ex


def Login(username, password):
    Path = "/Library/Caches/.menousdb/authdata"
    if not os.path.exists(Path):
        os.mkdir(Path)
    if not os.path.exists(Path + "/keys.json"):
        with open(Path + "/login.json", 'w') as file:
            json.dump([],file)
    if not os.path.exists(Path + "/login.json"):
        with open(Path + "/login.json", 'w') as file:
            json.dump({},file)
        return 'Sign Up Required! Please contact Administrator'
    with open(Path + "/login.json", 'r') as file:
        data = json.load(file)
        for i in data:
            if i == username and data[i][0] == password:
                return True
        return False
    

def getUserKey(username):
    Path = "/Library/Caches/.menousdb/authdata"
    with open(Path + "/login.json", 'r') as file:
        data = json.load(file)
        for i in data:
            if i == username:
                return data[i][1]
            
def login_required(f):
   
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logStatus"):
            session["logStatus"] = False

        if session["logStatus"] == False:
            return redirect('/login')
        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)
       
   
    return wrap
@app.route('/session',methods=['GET'])
def sess():
    return jsonify(session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        if Login(username, password) == True:
            session['logStatus'] = True
            session['key'] = getUserKey(username)
            return redirect('/')
        elif Login(username, password) == False:
            return render_template('login.html', loggFail=True)
        else:
            return render_template('login.html', signup=True, msg=Login(username, password))
    return render_template('login.html')
        

@app.route('/', methods=['GET'])
def indexmain():
    return redirect('/view')

@app.route('/view', methods=['GET','POST'])
@login_required
def homePage():
    if request.method == 'GET':
        db = MenousDB(
        API_URL,
        session["key"],
        'test'
    )
        return render_template('index.html',databases=db.get_databases())
    elif request.method == "POST":
        database = request.form.get("database_name").replace(" ", "_")
        db = MenousDB(
        API_URL,
        session["key"],
        database
        )
        db.createDb()
        return redirect(f'/view/{database}')
    

@app.route('/view/<database>/<table>', methods=["GET", "POST"])
@login_required
def index(database, table):
    db = MenousDB(
            API_URL,
            session["key"],
            database
        )
    if request.method == "GET":
        data = db.readDB()
        if not request.args == {}:
            values = {}
            for i in data[table]['attributes']:
                values[i] = request.args.get(i)
            db.insertIntoTable(
                table,values
            )
            return redirect(f'/view/{database}/{table}')
        return render_template('table.html', data = data[table])
    
    if request.method == "POST":
        conditions = {}
        values = {}
        deleteConditions = {}
        for i in request.form:
            if "originalAttribute" in i:
                conditions[request.form.get(i)] = request.form.get(i.replace("Attribute","Value"))
            elif "newAttribute" in i:
                values[request.form.get(i)] = request.form.get(i.replace("Attribute","Value"))
            elif "deleteAttribute" in i:
                deleteConditions[request.form.get(i)] = request.form.get(i.replace("Attribute","Value"))
            
        if conditions != {} and values != {}:
            db.update_table(table,conditions,values)
            return redirect(f"/view/{database}/{table}")
        
        if deleteConditions != {}:
            db.delete_where(table, deleteConditions)
            return redirect(f"/view/{database}/{table}")
    
        if "deleteTable" in request.form:
            db.delete_table(table)
            return redirect(f"/view/{database}")
        return jsonify(request.form)
        

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    session.pop('logStatus')
    session.pop('key')
    return redirect('/')

@app.route('/view/<database>', methods = ['GET', 'POST'])
@login_required
def db(database):
    if request.method == 'POST':
        table = request.form.get("table_name")
        params = []
        for i in request.form:
            if 'param' in i:
                params.append(request.form[i])
        db=MenousDB(
            API_URL,
            session["key"],
            database
        )
        if "deleteDatabase" in request.form:
            db.deleteDatabase()
            return redirect('/view')
        try:
            db.createTable(table, params)
            return redirect(f'/view/{database}')
        except:
            return "Table already Exists"
        
    else:
        db = MenousDB(
            API_URL,
            session["key"],
            database
        )
        tables = []
        for i in db.readDB():
            tables.append(i)
        return render_template('database.html', tables=tables, database=database)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--signup":
        signup()
    app.run(debug=True,host="0.0.0.0", port=5096)
