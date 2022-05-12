from inventorytracker.api import errors
from bson import ObjectId, json_util, errors as bsonErrors
from inventorytracker import mongodb
from traceback import print_exc

inventoryCollection = mongodb["Shopify"]["inventory"]

ERROR = errors.generalServerError("inventoryController")

def _finalQtyGreaterThanZero(itemID, qtyAdjustment):
    """
    Helper function that verifies inventory quantities
    """
    try:
        item = json_util.loads(getItemByID(itemID)[0])["item"]
        currentItemQty = item.get("quantity")
        if currentItemQty and currentItemQty + qtyAdjustment > 0:
            return True
    except:
        return errors.invalidID(itemID)

def getAllItems():
    """
    Gets all inventory items
    """
    try:
        cursor = inventoryCollection.find()
        itemList = [item for item in cursor]
        return json_util.dumps({
            "items": itemList,
            "count": len(itemList)
        }), 200
    except:
        return ERROR

def addItem(itemData):
    """
    Adds an inventory item
    """
    try:
        name = itemData.get("name")
        quantity = itemData.get("quantity")
        cost = itemData.get("cost")
        price = itemData.get("price")
        
        if name and quantity and cost and price:
            if quantity <= 0:
                return errors.quantityError()
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
                return ERROR
        else:
            return errors.missingRequiredDataFields(
                "name", "quantity", "cost", "price"
            )
    except:
        return ERROR

def getItemByID(id):
    """
    Get a specific item
    """
    try:
        item = inventoryCollection.find_one({"_id": ObjectId(id)})
        if item:
            return json_util.dumps({
                "item": item
            }), 200
        else:
            return errors.invalidID(id)
    except bsonErrors.InvalidId:
        return errors.invalidID(id)
    except:
        return ERROR

def editItemByID(id, itemData):
    """
    Edits item details
    """
    try:
        jsonData = {}

        name = itemData.get("name")
        if name:
            jsonData["name"] = name
        quantity = itemData.get("quantity")
        if quantity:
            if quantity > 0:
                jsonData["quantity"] = quantity
            else:
                return errors.quantityError()
        cost = itemData.get("cost")
        if cost:
            jsonData["cost"] = cost
        price = itemData.get("price")
        if price:
            jsonData["price"] = price

        if jsonData:
            response = inventoryCollection.update_one(
                {"_id": ObjectId(id)},
                {"$set": jsonData}
            )
            if response.matched_count == 1:
                return json_util.dumps({
                    "status": "Success"
                }), 200
            else:
                return errors.invalidID(id)
        else:
            return errors.missingSubsetDataFields(
                "name", "quantity", "cost", "price"
            )
    except:
        return ERROR

def editItemQuantityByID(id, qtyToAdjust):
    """
    Edits an items quantity
    """
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
                return errors.invalidID(id)
        else:
            return errors.quantityError()
    except:
        return ERROR

def deleteItemByID(id):
    """
    Deletes a specific item
    """
    try:
        response = inventoryCollection.delete_one({"_id": ObjectId(id)})
        if response.deleted_count == 1:
            return json_util.dumps({
                "status": "Success"
            }), 200
        else:
            return ERROR
    except:
        return ERROR