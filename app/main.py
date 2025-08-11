from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .cgol_logic import run_game_of_life
from .gpt_wrapper import handle_prompt

app = FastAPI(
    title="Conway's Game of Life - AI Tool",
    description="Single app serving API + AI tool + UI",
    version="1.0.0"
)

# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve HTML templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/conway")
def conway_api(word: str):
    generations, score = run_game_of_life(word)
    return {"word": word, "generations": generations, "score": score}

@app.post("/prompt")
def prompt_api(prompt: str = Form(...)):
    response = handle_prompt(prompt)
    return {"response": response}
