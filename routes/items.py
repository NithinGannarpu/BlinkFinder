from fastapi import APIRouter

router = APIRouter()

items = set()

@router.get("/")
def root():
    return {"message": "Hello, World!"}


@router.get("/items")
def get_items():
    return {"items" : list(items)} #FastAPI/JSON cannot directly serialize a Python set

@router.post("/additem")
def add_item(itm: str):
    items.add(itm.lower())
    return {"message": f"Added {itm}"}


# Not routerlicable since this is a set now
# @router.get("/item/{item_id}")
# def get_item(item_id:int):
#     try:
#         item = items[item_id]
#     except IndexError:
#         return {"error": "Index out of range"}
#     else : 
#         return {"message": f"Item at index {item_id} is {item}"}
    
@router.delete("/item/{item}")    
def delete_item(item):

    item = item.lower()
    if(item in items):
        items.remove(item)
        return {"message" : f"{item} removed successfully!"}
    return {"error" : f"{item} not present"}


@router.get("/exists/{thing}")
def dummy(thing):
    exists = False
    for i in items:
        lowercase_i = str(i).lower()
        lowercase_thing = str(thing).lower()
        if(lowercase_i ==lowercase_thing):
            exists = True
            break
    return {"message" : exists}

@router.get("/exists1/{thing}")
def exists(thing: str):
    return {"message": thing.lower() in items}

