from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from getPrediction import stockfishPrediction

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

USERNAME = "abcd"
PASSWORD = "pass"

# Store moves
last_input = ""  # Opponent's move
best_move = ""  # Stockfish's move

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": None})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("index.html", {"error": "Invalid Username or Password"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    global best_move

    # Reset the board if the game is over
    if best_move == "Game Over!":
        board.reset()

    return templates.TemplateResponse("dashboard.html", {"request": request, "MOVE": best_move})

@app.post("/process-input")
async def process_input(user_input: str = Form(...)):
    global last_input, best_move
    last_input = user_input
    best_move = stockfishPrediction(user_input)

    return RedirectResponse(url="/dashboard", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
