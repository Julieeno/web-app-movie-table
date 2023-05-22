from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, constr
from typing import Optional, Literal
import psycopg2

conn = psycopg2.connect("dbname=test user=test password=test host=localhost port=5432", cursor_factory=RealDictCursor)

cursor = conn.cursor()


class Item(BaseModel):
    name: str
    director: str
    year: int
    company: str
    rating: float


class UpdateItemModel(BaseModel):
    name: Optional[str]
    director: Optional[str]
    year: Optional[int]
    company: Optional[str]
    rating: Optional[float]


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000/items"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items/")
async def create_item(item: Item):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO movies (name, director, year, company, rating) VALUES (%s, %s, %s, %s, %s)",
                           (item.name, item.director, item.year, item.company, item.rating))
    return {
        "message": "Item created"
    }


@app.put("/items/{item_id}")
async def update_item_field(item_id: int, item: UpdateItemModel):
    fields = ""
    new_values = []
    for k, v in item.dict().items():
        if v is not None:
            if fields == "":
                fields += f"{k}=%s"
            else:
                fields += f", {k}=%s"
            new_values.append(v)

    new_values.append(item_id)
    if fields == "":
        return {
            "message": "required body"
        }
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE movies SET {fields} WHERE id=%s", tuple(new_values))
    return {
        "message": f"The following fields of the item with ID={item_id} were updated: {fields.replace('=%s', '')}"
    }


@app.get("/items/")
async def get_items(sort: Optional[Literal["id", "name", "director", "year", "company", "rating"]] = None,
                    order: Optional[Literal["asc", "desc"]] = None,
                    offset: int = None,
                    limit: int = None,
                    search: Optional[str] = None
                    ):
  limitf: Literal[int] = limit
  offsetf: Literal[int] = offset


  with conn:
    with conn.cursor() as cursor:
      query = ""
      countQuery = ""

      if search is not None:
          query = query + "WHERE name LIKE %s OR director LIKE %s OR year::TEXT LIKE %s OR company LIKE %s OR rating::TEXT LIKE %s "
          countQuery = query
      if sort is not None:
          query = query + "ORDER BY " + sort
      if order == "desc" and sort is not None:
            query = query + " DESC "
      query = query + " LIMIT " + str(limitf) + " OFFSET " + str(offsetf)

      cursor.execute(f"SELECT * FROM movies " + query, (search, search, search, search, search))

      items = cursor.fetchall()

      cursor.execute(f"SELECT COUNT(*) FROM movies " + countQuery, (search, search, search, search, search))
      total = cursor.fetchone()["count"]

      return {
        "items": items,
        "total": total,
      }


@app.get("/items/filters")
async def get_filtered(
        yearMin: Optional[int] = 0,
        yearMax: Optional[int] = 9000,
        ratingMin: Optional[float] = 0,
        ratingMax: Optional[float] = 5,
):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM movies WHERE year >= %s AND year <= %s "
                           f"AND rating >= %s AND rating <= %s", (yearMin, yearMax, ratingMin, ratingMax))

            filteredItems = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(*) FROM movies WHERE year >= %(yMin)s AND year <= %(yMax)s "
                           f"AND rating >= %(rMin)s AND rating <= %(rMax)s",
                           {"yMin": yearMin, "yMax": yearMax, "rMin": ratingMin, "rMax": ratingMax})

            totalFiltered = cursor.fetchone()["count"]

            return {
                "items": filteredItems,
                "total": totalFiltered,
            }


@app.delete("/items/{item_id}/")
async def delete_item(item_id: str):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM movies WHERE name LIKE %s", (item_id,))
            if cursor.rowcount == 0:
                return {
                    "message": f"Item {item_id} not found"
                }
            return {
                "message": f"Item {item_id} deleted"
            }
