from bson import json_util 

def generalServerError(moduleName):
    return json_util.dumps({
        "error": f"Server error, cannot connect to database in {moduleName}"
    }), 500

def invalidID(id):
    return json_util.dumps({
        "error": "Invalid request, _id does not exist",
        "_id": id
    }), 400

def missingRequiredDataFields(*args):
    return json_util.dumps({
        "error": f"Invalid request, missing the following required data fields: {', '.join([arg for arg in args])}"
    }), 400

def missingSubsetDataFields(*args):
    return json_util.dumps({
        "error": f"Invalid request, at least one of the following data fields must be included: {', '.join([arg for arg in args])}"
    }), 400

def editShipmentItemIDError(shipmentID, itemID):
    return json_util.dumps({
        "error": "Invalid request, shipmentID or itemID does not exist",
        "shipmentID": shipmentID,
        "itemID": itemID
    }), 400

def quantityError():
    return json_util.dumps({
        "error": "Invalid request, quantity must be greater than zero"
    }), 400

def cycleItemQuantityError(id):
    return json_util.dumps({
        "error": "Invalid request, quantity exceeds stock or id does not exist"
    }), 400