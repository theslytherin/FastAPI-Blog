from fastapi import FastAPI, Request, HTTPException, status
#from fastapi.responses import HTMLResponse
#above import is for returning HTML responses on the webpage instead of JSON responses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


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

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
#the int type setting is important as it automatically validates the user inputs in the url and gives appropriate error. Also helps in maintaining Swagger UI docs with correct type for debugging, testing and documentation.
    for post in posts:
        if(post.get("id")== post_id):
            title = post["title"][:50]
            return templates.TemplateResponse(request,"post.html", {"post": post, "title": title})

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail= "Post not found",
        )




@app.get("/api/posts")
def get_posts():
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
#the int type setting is important as it automatically validates the user inputs in the url and gives appropriate error. Also helps in maintaining Swagger UI docs with correct type for debugging, testing and documentation.
    for post in posts:
        if(post.get("id")== post_id):
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
#return {"error": "Post not found"} is incorrect reponse as it will give a 200 return code instead of 400 even though the post doesn't exists. Not the best practice.
#important to return the correct status code for debugging purpose.


@app.exception_handler(StarletteHTTPException) #@app.exception_handler  is called the decorator which tells to catch the Starlette exceptions
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

#Above one handles not found kind of exceptions and below one handles validation exceptions
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )