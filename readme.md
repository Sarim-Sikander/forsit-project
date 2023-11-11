# Forsit FastAPI Project with MongoDB

* Author: Sarim Sikander
* Email: sarimsikander24@gmail.com
* Date: 2023-11-11

## Make Enviroment

1. Install environment
```bash
pip install virtualenv
```
2. Make enviroment
```bash
python -m venv venv
```
3. Activate environment
```bash
venv\Scripts\activate
```

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2.  Install dependencies:
```bash 
pip install -r requirements.txt
```

3. Create a .env file in the project root and set the following environment variables:
```bash
MONGODB_URL=<your-mongodb-url>
```

4. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

The FastAPI application should be running at http://127.0.0.1:8000.

# API Endpoints
## Sales Endpoints
1. GET /sales: Get a list of all sales.
2. GET /sales/analyze: Analyze sales data, providing total quantity and average unit price.
3. GET /sales/total_revenue_by_category: Get total revenue grouped by product categories.
4. GET /sales/categories: Get a list of sales categories.
5. GET /sales/total_sales: Get the total sales amount.
6. GET /sales/total_revenue: Get the total revenue amount.
7. GET /sales/{product_line}: Get sales data for a specific product line.

## Inventory Endpoints
1. GET /inventory: Get a list of all inventory items.
2. GET /inventory/stats: Get statistics for the inventory, including total items and total quantity.
3. GET /inventory/{item_id}: Get details of a specific inventory item.
4. POST /inventory: Add a new inventory item.
5. PUT /inventory/{item_id}: Update an existing inventory item.
6. DELETE /inventory/{item_id}: Delete an inventory item.

# Database Documentation
## Inventory Collection
1. _id: The unique identifier for each inventory item.
2. ProductName: The name of the product.
3. Quantity: The quantity available in the inventory.

## Sales Collection
1. _id: The unique identifier for each sale.
2. invoice_id: The ID of the invoice.
3. branch: The branch where the sale occurred.
4. city: The city where the sale occurred.
5. ... (other fields as per your schema)