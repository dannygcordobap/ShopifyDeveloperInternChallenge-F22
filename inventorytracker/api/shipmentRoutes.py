import json
from flask import request
from inventorytracker import server
from inventorytracker.api import shipmentController

SHIPMENT_ENDPOINT = "/api/v1/shipment"

@server.route(f"{SHIPMENT_ENDPOINT}/<id>", methods = ["GET", "PUT", "DELETE"])
@server.route(f"{SHIPMENT_ENDPOINT}", methods = ["GET", "POST"])
def shipment(id = None):
    """
    Handles the retrieval of all shipments, shipment creation/deletion, and the 
    editing of a shipment's recipient
    """
    try:
        if id:
            if request.method == "GET":
                response, status = shipmentController.getShipmentByID(id)
            
            elif request.method == "PUT":
                data = request.get_json()
                if data:
                    response, status = shipmentController.editShipmentRecipient(
                        id, data
                    )
                else:
                    response, status = json.dumps({
                        "error": "Invalid request, no data passed"
                    }), 400
            elif request.method == "DELETE":
                response, status = shipmentController.deleteShipmentByID(id)
        
        else:
            if request.method == "GET":
                response, status = shipmentController.getAllShipments()
            
            elif request.method == "POST":
                data = request.get_json()
                if data:
                    response, status = shipmentController.addShipment(data)
                else:
                    response, status = json.dumps({
                        "error": "Invalid request, no data passed"
                    }), 400
        return json.loads(response), status
    
    except:
        return json.loads({
            "error": "Server error in shipmentRoutes.shipment"
        }), 500

@server.route(f"{SHIPMENT_ENDPOINT}/<id>/items/<itemID>", methods = ["DELETE"])
@server.route(f"{SHIPMENT_ENDPOINT}/<id>/items", methods = ["POST", "PUT"])
def shipmentItems(id, itemID = None):
    """
    Handles the addition and removal of items from a shipment as well as
    editing shipment item quantities.
    """
    try:
        data = request.get_json()
        if request.method == "POST" and data:
            response, status = shipmentController.addItemToShipment(id, data)
        elif request.method == "PUT" and data:
            response, status = shipmentController.editShipmentItem(id, data)
        elif request.method == "DELETE" and itemID:
            response, status = shipmentController.deleteItemFromShipment(id, itemID)
        else:
            response, status = json.dumps({
                "error": "Invalid request, no data passed or missing itemID"
            }), 400
        return json.loads(response), status 
    except:
        return json.loads({
            "error": "Server error in shipmentRoutes.shipmentItems"
        }), 500