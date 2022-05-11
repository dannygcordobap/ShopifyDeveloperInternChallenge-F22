import json
from flask import request
from inventorytracker import server
from inventorytracker.api import inventoryController
from inventorytracker.api import errors

INVENTORY_ENDPOINT = "/api/v1/inventory"

@server.route(f"{INVENTORY_ENDPOINT}", methods = ["GET", "POST"])
def inventory():
    """
    Handles getting the inventory as a list and adding inventory items
    """
    try:
        if request.method == "GET":
            response, status = inventoryController.getAllItems()
        elif request.method == "POST":
            data = request.get_json()
            if data:
                response, status = inventoryController.addItem(data)
            else:
                response, status = errors.missingRequiredDataFields(
                    "name", "quantity", "cost", "price"
                )
        return json.loads(response), status
    except:
        return json.loads({
            "error": "Server error in inventoryRoutes.inventory"
        }), 500

@server.route(f"{INVENTORY_ENDPOINT}/<id>", methods = ["GET", "PUT", "DELETE"])
def inventoryItem(id):
    """
    Handles getting specific invetory item details, editing item details, 
    and deleting inventory items.
    """
    try:
        if request.method == "GET":
            response, status = inventoryController.getItemByID(id)
        elif request.method == "PUT":
            data = request.get_json()
            if data:
                response, status = inventoryController.editItemByID(id, data)
            else:
                response, status = errors.missingRequiredDataFields(
                    "itemID", "quantity"
                )
        elif request.method == "DELETE":
            response, status = inventoryController.deleteItemByID(id)
        return json.loads(response), status
    except:
        return json.loads({
            "error": "Server error in inventoryRoutes.inventoryItem"
        }), 500