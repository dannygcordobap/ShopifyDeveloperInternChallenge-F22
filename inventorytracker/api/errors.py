from bson import json_util 

def generalServerError(moduleName):
    return json_util.dumps({
        "errorDescription": f"Server error, cannot connect to database in {moduleName}",
        "errorCode": 10
    }), 500

def invalidID(id):
    return json_util.dumps({
        "errorDescription": "Invalid request, _id does not exist",
        "errorCode": 20,
        "requestedID": id
    }), 400

def missingRequiredDataFields(*args):
    return json_util.dumps({
        "errorDescription": f"Invalid request, missing the following required data fields: {', '.join([arg for arg in args])}",
        "errorCode": 21
    }), 400

def missingSubsetDataFields(*args):
    return json_util.dumps({
        "errorDescription": f"Invalid request, at least one of the following data fields must be included: {', '.join([arg for arg in args])}",
        "errorCode": 22
    }), 400

def editShipmentItemIDError(shipmentID, itemID):
    return json_util.dumps({
        "errorDescription": "Invalid request, shipmentID or itemID does not exist",
        "errorCode": 23,
        "requestedShipmentID": shipmentID,
        "requestedItemID": itemID
    }), 400

def quantityError():
    return json_util.dumps({
        "errorDescription": "Invalid request, quantity must be greater than zero",
        "errorCode": 24
    }), 400

def cycleItemQuantityError(id):
    return json_util.dumps({
        "errorDescription": "Invalid request, quantity exceeds stock or id does not exist",
        "errorCode": 25
    }), 400