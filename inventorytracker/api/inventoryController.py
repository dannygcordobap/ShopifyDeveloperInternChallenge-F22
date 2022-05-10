from bson import ObjectId, json_util
from inventorytracker import mongodb

inventoryCollection = mongodb["Shopify"]["inventory"]

ERROR = json_util.dumps({
            "error": "Error connecting to database in inventoryController"
        }), 500

def _finalQtyGreaterThanZero(itemID, qtyAdjustment):
    try:
        item = json_util.loads(getItemByID(itemID)[0])["item"]
        currentItemQty = item["quantity"]
        if currentItemQty + qtyAdjustment > 0:
            return True
    except:
        return json_util.dumps({
            "error": "Invalid request, itemID does not exist"
        }), 400

def getAllItems():
    try:
        itemList = [item for item in inventoryCollection.find()]
        return json_util.dumps({
            "items": itemList,
            "count": len(itemList)
        }), 200
    except:
        return ERROR

def addItem(itemData):
    try:
        name = itemData["name"]
        quantity = itemData["quantity"]
        cost = itemData["cost"]
        price = itemData["price"]
    except:
        return json_util.dumps({
            "error": "Invalid request, all data fields are required"
        }), 400
    try:
        response = inventoryCollection.insert_one({
            "name": name,
            "quantity": quantity,
            "cost": cost,
            "price": price
        })
        if response.inserted_id:
            return json_util.dumps({
                "status": "Success",
                "insertedItemID": response.inserted_id
            }), 200
        else:
            return json_util.dumps({
                "error": "Insertion error"
            }), 500
    except:
        return ERROR

def getItemByID(id):
    try:
        item = inventoryCollection.find_one({"_id": ObjectId(id)})
        if item:
            return json_util.dumps({
                "item": item
            }), 200
        else:
            return json_util.dumps({"error": "Invalid request, no \
                matching ObjectID"
            }), 400
    except:
        return ERROR

def editItemByID(id, itemData):
    try:
        if set(itemData.keys()).issubset(["name", "quantity", "cost", "price"]):
            editedQty = itemData.get("quantity")
            if editedQty and editedQty < 0:
                return json_util.dumps({
                    "error": "Invalid request, quantity must be greater than \
                        or equal to zero"
                }), 400
            inventoryCollection.update_one(
                {"_id": ObjectId(id)},
                {"$set": itemData}
            )
            return json_util.dumps({
                "status": "Success"
            }), 200
        else:
            return json_util.dumps({"error": "Invalid request, \
                only name, quantity, cost, and price allowed"
            }), 400
    except:
        return ERROR

def editItemQuantityByID(id, qtyToAdjust):
    try:
        if _finalQtyGreaterThanZero(id, qtyToAdjust):
            response = inventoryCollection.update_one(
                {"_id": ObjectId(id)},
                {"$inc": {"quantity": qtyToAdjust}}
            )
            if response.matched_count == 1:
                return json_util.dumps({
                    "status": "Success"
                }), 200
            else:
                return json_util.dumps({"error": "Invalid request, no \
                    matching ObjectID"
                }), 400
        else:
            return json_util.dumps({
                "error": "Invalid request, quantity must be greater than \
                    or equal to zero"
            }), 400
    except:
        return ERROR

def deleteItemByID(id):
    try:
        response = inventoryCollection.delete_one({"_id": ObjectId(id)})
        if response.deleted_count == 1:
            return json_util.dumps({
                "status": "Success"
            }), 200
        else:
            return json_util.dumps({"error": "Deletion error"
            }), 500
    except:
        return ERROR