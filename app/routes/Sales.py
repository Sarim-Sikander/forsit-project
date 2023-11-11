import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Path

from ..models.Sales import *
from ..utils.database import sales_collection, inventory_collection
from ..utils.error_handling import ErrorHandling

logger = logging.getLogger(__name__)

router = APIRouter()
error_handler = ErrorHandling()

"""
Get the sales data.

Returns:
    A list of `Sale` objects representing the sales data.

Raises:
    InternalServerError: If an error occurs while retrieving the sales data.
"""


@router.get("/sales", response_model=List[Sale])
async def get_sales() -> List[Sale]:
    try:
        return await sales_collection.find().to_list(length=100)
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Analyze the sales data.

Returns:
    A dictionary containing the total quantity of sales and the average unit price.

Raises:
    InternalServerError: If an error occurs while analyzing the sales data.
"""


@router.get("/sales/analyze", response_model=dict)
async def analyze_sales() -> dict:
    try:
        total_quantity = await sales_collection.aggregate(
            [{"$group": {"_id": None, "total_quantity": {"$sum": "$quantity"}}}]
        ).to_list(1)

        average_unit_price = await sales_collection.aggregate(
            [{"$group": {"_id": None, "average_unit_price": {"$avg": "$unit_price"}}}]
        ).to_list(1)

        return {
            "total_quantity": total_quantity[0]["total_quantity"]
            if total_quantity
            else 0,
            "average_unit_price": average_unit_price[0]["average_unit_price"]
            if average_unit_price
            else 0,
        }
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the total revenue by category.

Returns:
    A dictionary containing the total revenue for each category.

Raises:
    InternalServerError: If an error occurs while retrieving the total revenue by category.
"""


@router.get("/sales/total_revenue_by_category", response_model=dict)
async def total_revenue_by_category() -> dict:
    try:
        # Group by product_line and calculate total revenue for each category
        pipeline = [
            {"$group": {"_id": "$product_line", "total_revenue": {"$sum": "$total"}}}
        ]

        total_revenue_cursor = sales_collection.aggregate(pipeline)

        total_revenue_by_category = await total_revenue_cursor.to_list(None)

        return {"total_revenue_by_category": total_revenue_by_category}
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the categories of sales.

Returns:
    A dictionary containing the list of categories.

Raises:
    InternalServerError: If an error occurs while retrieving the categories.
"""


@router.get("/sales/categories", response_model=dict)
async def get_categories() -> dict:
    try:
        categories = await sales_collection.distinct("product_line")
        return {"categories": categories}
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the total sales.

Returns:
    A dictionary containing the total sales amount.

Raises:
    InternalServerError: If an error occurs while retrieving the total sales.
"""


@router.get("/sales/total_sales", response_model=dict)
async def total_sales() -> dict:
    try:
        total_sales_cursor = sales_collection.aggregate(
            [{"$group": {"_id": None, "total_sales": {"$sum": "$total"}}}]
        )

        total_sales_result = await total_sales_cursor.to_list(1)

        return {
            "total_sales": total_sales_result[0]["total_sales"]
            if total_sales_result
            else 0
        }
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the total revenue.

Returns:
    A dictionary containing the total revenue amount.

Raises:
    InternalServerError: If an error occurs while retrieving the total revenue.
"""


@router.get("/sales/total_revenue", response_model=dict)
async def total_revenue() -> dict:
    try:
        total_revenue_cursor = sales_collection.aggregate(
            [{"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}]
        )

        total_revenue_result = await total_revenue_cursor.to_list(1)

        return {
            "total_revenue": total_revenue_result[0]["total_revenue"]
            if total_revenue_result
            else 0
        }
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the sales data for a specific product line.

Args:
    product_line (str): The product line to filter the sales data.

Returns:
    A list of `SalesResponseModel` objects representing the sales data for the specified product line.

Raises:
    InternalServerError: If an error occurs while retrieving the sales data.
"""


@router.get("/sales/{product_line}", response_model=List[SalesResponseModel])
async def get_sales_for_product(
    product_line: str = Path(..., title="Product Line")
) -> List[SalesResponseModel]:
    try:
        sales_for_product = await sales_collection.find(
            {"product_line": product_line}
        ).to_list(length=100)
        return sales_for_product
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Add a new sale.

Args:
    sale (Sale): The sale object to be added.

Returns:
    The added sale object.

Raises:
    NotFoundError: If the product line is not found in the inventory.
    HTTPException: If there is insufficient quantity in the inventory.
    HTTPException: If the sale fails to be added to the database.
"""


@router.post("/sales/new_sale", response_model=Sale)
async def add_new_sale(sale: Sale) -> Sale:
    # Add current time and date
    sale.date = datetime.now().strftime("%m/%d/%Y")
    sale.time = datetime.now().strftime("%H:%M:%S")

    product_in_inventory = await inventory_collection.find_one(
        {"Products": sale.product_line}
    )

    if not product_in_inventory:
        raise error_handler.handle_not_found_error("Product")

    # Check if quantity is available in inventory
    if product_in_inventory["Quantity"] < sale.quantity:
        raise HTTPException(
            status_code=404, detail="Insufficient quantity in inventory"
        )

    # Calculate total and tax_5_percent
    sale.total = sale.unit_price * sale.quantity * 0.95
    sale.tax_5_percent = sale.unit_price * sale.quantity * 0.05

    # Update inventory quantity
    updated_quantity = product_in_inventory["Quantity"] - sale.quantity
    await inventory_collection.update_one(
        {"Products": sale.product_line},
        {"$set": {"Quantity": updated_quantity}},
    )

    # Insert the new sale into the database
    result = await sales_collection.insert_one(sale.dict())

    if result.inserted_id:
        return Sale(**sale.dict())
    else:
        raise HTTPException(status_code=500, detail="Failed to add sale")
