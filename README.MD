# **Shopify Developer Internship Challenge**

## *Introduction*
---
The Shopify Developer Internship Challenge is as follows:

>Build an inventory tracking web application for a logistics company. We are looking for a web application that meets the requirements listed below, along with one additional feature, with the options also listed below. You can tackle this challenge using any technology you want. This is an open-ended task, but we want to focus on high quality back-end code.

The requirements are basic CRUD (create, read, update, delete) functions as follows:
- Create inventory items
- Edit Them
- Delete Them
- View a list of them

After completing the requirements, the challenge calls for one additional feature from the following list:
- When deleting, allow deletion comments and undeletion
- Ability to create warehouses/locations and assign inventory to specific locations
- Ability to create “shipments” and assign inventory to the shipment, and adjust inventory appropriately

I selected and implemented the "create shipments" functionality. This project was completed in as a Python Flask web application using Python 3 and the Flask web framework.


## *Getting Started*
---
The API is written in Python 3 and uses the following dependencies:
- flask
- pymongo
- python-dotenv

If you would like to run the API locally, you can clone this repository to your local machine and then do the following:
1. Ensure you have a download of Python 3.x.x. This can be checked by running the following command in the command: 
    ```python --version```

2. Next you will need to download dependencies using pipenv. Pipenv can be installed using `pip install --user pipenv`. After pipenv is installed, change directories to the local project directory and run `pipenv install`.

3. To run the API simply run the following command: `pipenv run server.py`. Following the command completion, navigate to http://127.0.0.1:5000 in a web browser and you should see "Shopify Developer Internship Challenge API V1" as plain text in the browser.

## *Making Requests*
---
### *Request Headers*
The API only accepts JSON data. As a result, API requests will require the `Content-Type` header to be set to `application/json`. The following is an example curl request:
```
curl -X POST http://127.0.0.1:5000/api/v1/inventory 
    -H Content-Type: application/json 
    -d {"name": "Toilet Paper", "quantity": "194", "cost": 14.65, "price": 20.00}
```
### *Routes*
| Endpoint | GET | POST | PUT | DELETE |
| :---: | :--- | :--- | :--- | :--- |
| /api/v1/inventory | Get all inventory items from the database | Add a new inventory item to the database. Data should be  in the following format: `{"name": "Toilet Paper", "quantity": "194", "cost": 14.65, "price": 20.00}` | N/A | N/A |
| /api/v1/inventory/<itemID\> | Get information for item with an ID of <itemID\> | N/A | Edit item information. Data must be passed in as JSON. All attributes or any subset of them can be edited in one request | Delete the item with an ID of <itemID\> from the inventory entirely |
| /api/v1/shipment | Get all shipments from inventory | Add a new shipment to the database. Only the recipient will be added at this time and the data should be structured as follows: `{"recipient": "Danny Cordoba"}` | N/A | N/A |
| /api/v1/shipment/<shipmentID\> | Get information for shipment with an ID of <shipmentID\> | N/A | Edits the shipment receipient only. Data should be structured identically shipment creation request | Delete the shipment with an ID of <shipmentD\> |
| /api/v1/shipment/<shipmentID\>/items | N/A | Add an item to the shipment. Data should be structured as follows: `{"itemID": "<itemID>", "quantity": 12}` | Edit the quantity of an item in the shipment. Data should be formatted identically to the post request where quantity is the new quantity. | N/A |
| /api/v1/shipment/<shipmentID\>/items/<itemID\> | N/A | N/A | N/A | Delete the item with an ID of <itemID\> from the shipment |

## *Request Examples* 

---

### **Get inventory items**
```
curl http://127.0.0.1:5000/api/v1/inventory
```
**Response:**
```
{
    "count": 7,
    "items": [
        {
            "_id": {
                "$oid": "6279489115c9541d2b160efd"
            },
            "cost": 0.87,
            "name": "Masking Tape (roll)",
            "price": 1.37,
            "quantity": 450
        },
        {
            "_id": {
                "$oid": "62794fddffccfef57733ed6c"
            },
            "cost": 0.22,
            "name": "Box (small)",
            "price": 0.33,
            "quantity": 149
        },
        {
            "_id": {
                "$oid": "627a86d6669fad9c39422b33"
            },
            "cost": 0.35,
            "name": "Box (medium)",
            "price": 0.42,
            "quantity": 647
        },
        {
            "_id": {
                "$oid": "627a86e8669fad9c39422b34"
            },
            "cost": 0.45,
            "name": "Box (large)",
            "price": 0.55,
            "quantity": 342
        },
        {
            "_id": {
                "$oid": "627a9e5f669fad9c39422b35"
            },
            "cost": 1.29,
            "name": "Box Cutter",
            "price": 2.0,
            "quantity": 97
        },
        {
            "_id": {
                "$oid": "627a9ec4669fad9c39422b37"
            },
            "cost": 0.95,
            "name": "Packing Tape (roll)",
            "price": 1.5,
            "quantity": 234
        }    
    ]
}
```

---

### **Add inventory item**
```
curl -X POST http://127.0.0.1:5000/api/v1/inventory 
    -H Content-Type: application/json 
    -d {"name": "Toilet Paper", "quantity": 194, "cost": 14.65, "price": 20.00}
```
**Response:**
```
{
    "insertedItemID": {
        "$oid": "627abfd658d7c8efe48b90ea"
    },
    "status": "Success"
}
```
**Note:** All fields are required.

---

### **Get inventory item**
```
curl http://127.0.0.1:5000/api/v1/inventory/627abfd658d7c8efe48b90ea
```
**Response:**
```
{
    "item": {
        "_id": {
            "$oid": "627abfd658d7c8efe48b90ea"
        },
        "cost": 14.65,
        "name": "Toilet Paper",
        "price": 20.0,
        "quantity": 194
    }
}
```

---

### **Edit inventory item**
```
curl -X PUT http://127.0.0.1:5000/api/v1/inventory/627abfd658d7c8efe48b90ea
    -H Content-Type: application/json 
    -d {"name": "Toilet Paper (12 pack)", "quantity": 200}
```
**Response:**
```
{
    "status": "Success"
}
```
**Note:** You can change all of the item attributes or any subset of the item attributes. The attributes are `name`, `cost`, `price`, and `quantity`.

---

### **Delete inventory item**
```
curl -X DELETE http://127.0.0.1:5000/api/v1/inventory/627abfd658d7c8efe48b90ea
```
**Response:**
```
{
    "status": "Success"
}
```

---

### **Get all shipments**
```
curl http://127.0.0.1:5000/api/v1/shipment
```
**Response:**
```
{
    "count": 1,
    "shipments": [
        {
            "_id": {
                "$oid": "627ac2ac05312ffd980d7ea5"
            },
            "items": [
                {
                    "itemID": "6279489115c9541d2b160efd",
                    "quantity": 50
                }
            ],
            "modifiedDate": {
                "$date": "2022-05-10T15:54:14.103Z"
            },
            "orderDate": {
                "$date": "2022-05-10T15:53:16.438Z"
            },
            "recipient": "Joe Schmoe"
        }
    ]
}
```

---

### **Add shipment**
```
curl -X POST http://127.0.0.1:5000/api/v1/shipment 
    -H Content-Type: application/json 
    -d {"recipient": "Whoever is reviewing this"}
```
**Response:**
```
{
    "insertedShipmentID": {
        "$oid": "627ac49092d0028a9056466b"
    },
    "status": "Success"
}
```
**Note:** Recipient is required.

---

### **Get shipment**
```
curl http://127.0.0.1:5000/api/v1/shipment/627ac49092d0028a9056466b
```
**Response:**
```
{
    "shipment": {
        "_id": {
            "$oid": "627ac49092d0028a9056466b"
        },
        "items": [],
        "modifiedDate": null,
        "orderDate": {
            "$date": "2022-05-10T16:01:20.813Z"
        },
        "recipient": "Whoever is reviewing this"
    }
}
```

---

### **Edit shipment recipient**
```
curl -X PUT http://127.0.0.1:5000/api/v1/shipment/627ac49092d0028a9056466b
    -H Content-Type: application/json 
    -d {"recipient": "You having fun?"}
```
**Response:**
```
{
    "status": "Success"
}
```

---

### **Delete shipment**
```
curl -X DELETE http://127.0.0.1:5000/api/v1/shipment/627ac49092d0028a9056466b
```
**Response:**
```
{
    "status": "Success"
}
```
**Note:** This will automatically add the quantities back into stock for each item in the shipment.

---

### **Add inventory item to a shipment**
```
curl -X POST http://127.0.0.1:5000/api/v1/shipment/627ac2ac05312ffd980d7ea5/items
    -H Content-Type: application/json
    -d {"itemID": "627a86d6669fad9c39422b33", "quantity": 147}
```
**Response:**
```
{
    "status": "Success"
}
```
**Note:** This will automatically adjust stock.

---

### **Edit inventory item quantity in a shipment**
```
curl -X PUT http://127.0.0.1:5000/api/v1/shipment/627ac2ac05312ffd980d7ea5/items
    -H Content-Type: application/json
    -d {"itemID": "627a86d6669fad9c39422b33", "quantity": 135}
```
**Response:**
```
{
    "status": "Success"
}
```
**Note:** This will automatically adjust stock to account for the item quantity changing in the shipment.

---

### **Delete inventory item from shipment**
```
curl -X DELETE http://127.0.0.1:5000/api/v1/shipment/627ac2ac05312ffd980d7ea5/items/627a86d6669fad9c39422b33
```
**Response:**
```
{
    "status": "Success"
}
```
**Note:** This will automatically add the quantity back into stock for each item in the shipment.

---

## *Error Codes*

| Error Code | Description | Possible solution |
| :---: | :--- | :--- |
| 10 | General server error regarding a faulty database connection | N/A |
| 20 | The requested _id does not belong to an existing resource | Verify the object id of the resource in question |
| 21 | The request is missing required data fields. A list of the required data fields will be included in the response.| Include the required data fields |
| 22 | The request does not include applicable data fields. A list of possible data fields will be included in the response | Include one or more of the applicable data fields |
| 23 | The requested shipment does not exist or the item being edited is not in the shipment | Verify the shipment exists and that it contains the specified item |
| 24 | Quantity values must be greater than 0 when passed in to a request | Verify quantity is greater than 0 |
| 25 | Assigning quantity to shipment exceeds stock or the item is not in the shipment | Verify the shipment exists and that the requested quantity is in inventory |