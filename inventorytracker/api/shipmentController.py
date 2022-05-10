from datetime import datetime as dt
from bson import ObjectId, json_util
from inventorytracker import mongodb
from inventorytracker.api import inventoryController

shipmentCollection = mongodb["Shopify"]["shipment"]

ERROR = json_util.dumps({
            "error": "Error connecting to database in shipmentController"
        }), 500

def _cycleItemQuantity(itemID, qty):
    response, status = inventoryController.editItemQuantityByID(itemID, qty)
    if status == 200:
        return True

def _getShipmentItemQty(shipmentID, itemID):
    qty = 0
    shipment = json_util.loads(getShipmentByID(shipmentID)[0])["shipment"]
    shipmentItems = shipment["items"]
    for item in shipmentItems:
        if item["itemID"] == itemID:
            qty += item["quantity"]
    return qty

def getAllShipments():
    try:
        shipments = [shipment for shipment in shipmentCollection.find()]
        return json_util.dumps({
            "shipments": shipments,
            "count": len(shipments)
        }), 200
    except:
        return ERROR

def addShipment(data):
    try:
        recipient = data.get("recipient")
        if recipient:
            response = shipmentCollection.insert_one({
                "recipient": recipient,
                "items": [],
                "orderDate": dt.now(),
                "modifiedDate": None
            })
            if response.inserted_id:
                return json_util.dumps({
                    "status": "Success",
                    "insertedShipmentID": response.inserted_id
                }), 200
            else:
                raise Exception()
        else:
            return json_util.dumps({"error": "Invalid request, recipient required"
            }), 400 
    except:
        return ERROR

def addItemToShipment(id, data):
    try:
        itemID = data["itemID"]
        qty = data["quantity"]
    except:
        return json_util.dumps({"error": "Invalid request, itemID and quantity required"
        }), 400
    try:
        if _cycleItemQuantity(itemID, -1 * qty):
            response = shipmentCollection.update_one(
                {"_id": ObjectId(id)},
                {   "$set": {"modifiedDate": dt.now()},
                    "$push": {
                        "items": {
                            "itemID": itemID,
                            "quantity": qty
                        }
                    }
                }
            )
        if response.matched_count == 1:
            return json_util.dumps({
                "status": "Success",
            }), 200
        else:
            return json_util.dumps({"error": "Invalid request, no \
                matching ObjectID"
            }), 400
    except:
        return ERROR

def editShipmentItem(id, data):
    try:
        itemID = data.get("itemID")
        newQty = data.get("quantity")
        if itemID and newQty:
            response, status = deleteItemFromShipment(id, itemID)
            if status == 200:
                response, status = addItemToShipment(
                    id, {
                        "itemID": itemID,
                        "quantity": newQty
                    }
                )
            else:
                return json_util.dumps({
                    "error": "Invalid request, itemID not in shipment or shipment ID incorrect"
                }), 400
            if status == 200:
                return json_util.dumps({
                    "status": "Success",
                }), 200  
            else:
                return json_util.dumps({
                    "error": "Error connecting to database"
                }), 500
        else:
            return json_util.dumps({
                "error": "Invalid request, itemID and new quantity required"
            }), 400
    except:
        return ERROR

def deleteItemFromShipment(id, itemID):
    try:
        qty = _getShipmentItemQty(id, itemID)
        if _cycleItemQuantity(itemID, qty):
            response = shipmentCollection.update_one(
                {"_id": ObjectId(id)},
                {
                    "$pull": {
                        "items": {
                            "itemID": {
                                "$eq": itemID
                            }
                        }
                    }
                }
            )
        if response.matched_count == 1:
            return json_util.dumps({
                "status": "Success",
            }), 200 
        else:
            return json_util.dumps({
                "error": "Invalid request, itemID not in shipment or shipment ID incorrect"
            }), 400
    except:
        return ERROR

def getShipmentByID(id):
    try:
        shipment = shipmentCollection.find_one({"_id": ObjectId(id)})
        if shipment:
            return json_util.dumps({
                "shipment": shipment
            }), 200 
        else: 
            return json_util.dumps({"error": "Invalid request, no \
                matching ObjectID"
            }), 400
    except:
        return ERROR

def deleteShipmentByID(id):
    try:
        shipment, status = getShipmentByID(id)
        items = None
        if status == 200:
            items = json_util.loads(shipment)["shipment"]["items"]
        if items:
            for item in items:
                deleteItemFromShipment(id, item["itemID"])
        if status == 200:
            response = shipmentCollection.delete_one({"_id": ObjectId(id)})
            if response.deleted_count == 1:
                return json_util.dumps({
                    "status": "Success"
                }), 200
            else:
                return json_util.dumps({"error": "Deletion error"
                }), 500
    except:
        return ERROR

def editShipmentRecipient(id, shipmentData):
    try:
        recipient = shipmentData["recipient"]
    except:
        return json_util.dumps({"error": "Invalid request, recipient required"
        }), 400
    shipmentData["modifiedDate"] = dt.now()
    response = shipmentCollection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": {"recipient": recipient, "modifiedDate": dt.now()}}
    )
    if response.matched_count == 1:
        return json_util.dumps({"status": "Success"}), 200
    else:
        return json_util.dumps({"error": "Invalid request, no \
            matching ObjectID"
        }), 400