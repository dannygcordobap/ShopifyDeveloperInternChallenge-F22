from inventorytracker import server

# Importing the API routes
from inventorytracker.api import inventoryRoutes, shipmentRoutes

# Placeholder for the home page
@server.route("/")
def home(): 
    return "Shopify Developer Internship Challenge API V1"