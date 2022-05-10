from inventorytracker import server
from inventorytracker.api import inventoryRoutes, shipmentRoutes

@server.route("/")
def home(): 
    return "Shopify Developer Internship Challenge API V1"