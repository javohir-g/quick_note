from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Import the routers
from api.note_api.note import router as note_router
from api.budget_api.budget import router as budget_router

app = FastAPI(title="Quick Note App")



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/templates", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers with prefixes
app.include_router(note_router, prefix="/api", tags=["notes"])
app.include_router(budget_router, prefix="/api", tags=["budgets"])

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
