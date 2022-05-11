from inventorytracker.api import errors
from datetime import datetime as dt
from bson import ObjectId, json_util
from inventorytracker import mongodb
from inventorytracker.api import inventoryController

shipmentCollection = mongodb["Shopify"]["shipment"]

ERROR = errors.generalServerError("shipmentController")

def _cycleItemQuantity(itemID, qty):
    """
    Helper function to cycle inventory on item inventory changes
    """
    response, status = inventoryController.editItemQuantityByID(itemID, qty)
    if status == 200:
        return True, status
    else:
        return False, status

def _getShipmentItemQty(shipmentID, itemID):
    """
    Helper function the returns current item quantity in a shipment
    """
    qty = 0
    shipment = json_util.loads(getShipmentByID(shipmentID)[0])["shipment"]
    shipmentItems = shipment.get("items")
    if shipmentItems:
        for item in shipmentItems:
            if item["itemID"] == itemID:
                qty += item["quantity"]
        return qty

def getAllShipments():
    """
    Returns all shipment data
    """
    try:
        shipments = [shipment for shipment in shipmentCollection.find()]
        return json_util.dumps({
            "shipments": shipments,
            "count": len(shipments)
        }), 200
    except:
        return ERROR

def addShipment(data):
    """
    Adds a shipment to the database
    """
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
                return ERROR
        else:
            return errors.missingRequiredDataFields("recipient")
    except:
        return ERROR

def addItemToShipment(id, data):
    """
    Adds an item to an exeisting shipment
    """
    try:
        itemID = data.get("itemID")
        qty = data.get("quantity")
        if itemID and qty:
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
                    return errors.invalidID(id)
            else:
                return ERROR
        else:
            return errors.missingRequiredDataFields("itemID", "quantity")
    except:
        return ERROR

def editShipmentItem(id, data):
    """
    Edits a shipment item's quantity
    """
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
                if status == 200:
                    return json_util.dumps({
                        "status": "Success",
                    }), 200
                elif status == 500:
                    return ERROR
                elif status == 400:
                    return errors.editShipmentItemIDError(id, itemID)
            elif status == 500:
                return ERROR
            elif status == 400:
                return errors.editShipmentItemIDError(id, itemID)
        else:
            return errors.missingRequiredDataFields("itemID", "quantity")
    except:
        return ERROR

def deleteItemFromShipment(id, itemID):
    """
    Deletes an item from a shipment
    """
    try:
        qty = _getShipmentItemQty(id, itemID)
        cycleItemSuccess, status = _cycleItemQuantity(itemID, qty)
        if cycleItemSuccess:
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
                return errors.invalidID(id)
        else:
            if status == 500:
                return ERROR
            elif status == 400:
                return errors.cycleItemQuantityError(id)
    except:
        return ERROR

def getShipmentByID(id):
    """
    Gets a specific shipment
    """
    try:
        shipment = shipmentCollection.find_one({"_id": ObjectId(id)})
        if shipment:
            return json_util.dumps({
                "shipment": shipment
            }), 200 
        else: 
            return errors.invalidID(id)
    except:
        return ERROR

def deleteShipmentByID(id):
    """
    Deletes the specific shipment
    """
    try:
        shipment, status = getShipmentByID(id)
        items = None
        if status == 200:
            items = json_util.loads(shipment)["shipment"]["items"]
        if items:
            for item in items:
                response, status = deleteItemFromShipment(id, item["itemID"])
                if status == 500:
                    return ERROR
        if status == 200:
            response = shipmentCollection.delete_one({"_id": ObjectId(id)})
            if response.deleted_count == 1:
                return json_util.dumps({
                    "status": "Success"
                }), 200
            else:
                ERROR
    except:
        return ERROR

def editShipmentRecipient(id, shipmentData):
    """
    Edits the shipment recipient
    """
    try:
        recipient = shipmentData.get("recipient")
        if recipient:
            response = shipmentCollection.update_one(
                {"_id": ObjectId(id)}, 
                {"$set": {"recipient": recipient, "modifiedDate": dt.now()}}
            )
            if response.matched_count == 1:
                return json_util.dumps({"status": "Success"}), 200
            else:
                errors.invalidID(id)
        else:
            return errors.missingRequiredDataFields("recipient")
    except:
        return ERROR