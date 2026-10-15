from fastapi import FastAPI, Request
#from fastapi.responses import HTMLResponse
#above import is for returning HTML responses on the webpage instead of JSON responses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#declare all the routes
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates =Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Anuska Sinha",
        "title": "Learning FastAPI",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
     {
        "id": 2,
        "author": "Sagar Kashyap",
        "title": "Python is great for web development",
        "content": "Python is a great language for development and FastAPI makes it even better!",
        "date_posted": "September 11, 2025",
    },
]

#@app.get("/", response_class=HTMLResponse, include_in_schema=False) #these are called decorators
#include_in_schema is an in-built function that helps to keep the swagger UI clean and precise by hiding the endpoint you don't want to display for example the HTML routes.
#@app.get("/posts", response_class=HTMLResponse)
#FastAPI allows stacking of decorators when we want the same content for multiple routes/urls
 #return f"<h1>{posts[0]['title']}</h1>"
#FastAPI will automatically convert the above command into JSON

#below is the function we are decorating
#FastAPI supports both async and sync functions

@app.get("/", include_in_schema=False)
@app.get("/posts",include_in_schema=False)
def home(request: Request):
#Jinja2 requires you to have an argument inside the function
   return templates.TemplateResponse(request, "home.html", {"posts":posts, "title": "Home"})
@app.get("/api/posts")
def get_posts():
    return posts