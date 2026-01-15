from typing import Any
import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


def get_db():
    return sqlite3.connect(os.path.join(BASE_DIR, "movies.db"))


# ============================
# FRONTEND ROUTES
# ============================

@app.get("/", response_class=FileResponse)
def serve_index():
    return os.path.join(BASE_DIR, "frontend", "index.html")


@app.get("/index.html", response_class=FileResponse)
def serve_index_html():
    return os.path.join(BASE_DIR, "frontend", "index.html")


@app.get("/add.html", response_class=FileResponse)
def serve_add_html():
    return os.path.join(BASE_DIR, "frontend", "add.html")


# ============================
# API: MOVIES
# ============================

@app.get("/movies")
def get_movies():
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute("SELECT id, title, year, actors FROM movies").fetchall()
    db.close()

    return [
        {"id": row[0], "title": row[1], "year": row[2], "actors": row[3]}
        for row in rows
    ]


@app.post("/movies")
def add_movie(params: dict[str, Any]):
    title = params.get("title")
    year = params.get("year")
    actors = params.get("actors")

    if not title or not year or not actors:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
        (title, year, actors)
    )

    db.commit()
    new_id = cursor.lastrowid
    db.close()

    return {"message": f"Movie added successfully", "id": new_id}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    db.commit()
    db.close()

    return {"message": "Movie deleted successfully"}


# 🔥 NOWY ENDPOINT: UPDATE FILMU
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    title = params.get("title")
    year = params.get("year")
    actors = params.get("actors")

    if not title or not year or not actors:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE movies SET title = ?, year = ?, actors = ? WHERE id = ?",
        (title, year, actors, movie_id)
    )

    db.commit()
    db.close()

    return {"message": f"Movie updated successfully", "id": movie_id}


# 🔥 NOWY ENDPOINT: USUNIĘCIE WSZYSTKICH FILMÓW
@app.delete("/movies")
def delete_all_movies():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movies")
    db.commit()
    db.close()

    return {"message": "All movies deleted successfully"}


# ============================
# RUN SERVER
# ============================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
