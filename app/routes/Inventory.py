import logging

from bson import ObjectId
from fastapi import APIRouter

from ..models.Inventory import Inventory, InventoryCreate, InventoryUpdate
from ..utils.database import inventory_collection
from ..utils.error_handling import ErrorHandling, InventoryErrorHandler

logger = logging.getLogger(__name__)

router = APIRouter()
error_handler = ErrorHandling()

"""
Get the inventory data.

Returns:
    A list of `Inventory` objects representing the inventory data.

Raises:
    InternalServerError: If an error occurs while retrieving the inventory data.
"""


@router.get("/inventory", response_model=list[Inventory])
async def get_inventory() -> list[Inventory]:
    try:
        inventory_data = await inventory_collection.find().to_list(100)
        for item in inventory_data:
            item["_id"] = str(item["_id"])
        return inventory_data
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Check for low quantity items in the inventory.

Returns:
    A dictionary containing the low quantity items and their corresponding warning messages.

Raises:
    None.
"""


@router.get("/inventory/low_quantity_warning", response_model=dict)
async def check_low_quantity_warning() -> dict:
    low_quantity_items = await inventory_collection.find(
        {"Quantity": {"$lt": 10}}
    ).to_list(length=100)

    # Check and handle quantity warning for each low quantity item
    warning_messages = []
    for item in low_quantity_items:
        warning_messages.append(
            {"product_name": item["Products"], "quantity": item["Quantity"]}
        )
        InventoryErrorHandler.handle_quantity_warning(
            item["Quantity"], item["Products"]
        )

    return {"low_quantity_items": warning_messages}


"""
Get the statistics of the inventory.

Returns:
    A dictionary containing the total number of items and the total quantity of the inventory.

Raises:
    InternalServerError: If an error occurs while retrieving the inventory statistics.
"""


@router.get("/inventory/stats", response_model=dict)
async def get_inventory_stats() -> dict:
    try:
        total_items = await inventory_collection.count_documents({})
        total_quantity = await inventory_collection.aggregate(
            [{"$group": {"_id": None, "total_quantity": {"$sum": "$Quantity"}}}]
        ).to_list(1)

        return {
            "total_items": total_items,
            "total_quantity": total_quantity[0]["total_quantity"]
            if total_quantity
            else 0,
        }
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Get the inventory item with the specified item ID.

Args:
    item_id (str): The ID of the item to retrieve.

Returns:
    An `Inventory` object representing the inventory item.

Raises:
    NotFoundError: If the item with the specified ID is not found.
    InternalServerError: 
"""


@router.get("/inventory/{item_id}", response_model=Inventory)
async def get_item(item_id: str) -> Inventory:
    try:
        item = await inventory_collection.find_one({"_id": item_id})
        if item:
            return item
        else:
            raise error_handler.handle_not_found_error("Item")
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Add an inventory item.

Args:
    item (InventoryCreate): The inventory item to be added.

Returns:
    The added inventory item.

Raises:
    InternalServerError: If an error occurs while adding the inventory item.
"""


@router.post("/inventory", response_model=Inventory)
async def add_inventory(item: InventoryCreate) -> Inventory:
    try:
        result = await inventory_collection.insert_one(item.model_dump())
        if result.inserted_id:
            return Inventory(**item.model_dump(), _id=str(result.inserted_id))
        else:
            raise error_handler.handle_internal_server_error()
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Update an inventory item with the specified item ID.

Args:
    item_id (str): The ID of the item to update.
    updated_item (InventoryUpdate): The updated inventory item.

Returns:
    A dictionary with a message indicating the success of the update.

Raises:
    NotFoundError: If the item with the specified ID is not found.
    InternalServerError: If an error occurs while updating the inventory item.
"""


@router.put("/inventory/{item_id}", response_model=dict)
async def update_inventory(item_id: str, updated_item: InventoryUpdate) -> dict:
    try:
        object_id = ObjectId(item_id)
        result = await inventory_collection.update_one(
            {"_id": object_id}, {"$set": updated_item.dict(exclude_unset=True)}
        )

        if result.modified_count > 0:
            return {"message": "Item updated successfully"}
        else:
            raise error_handler.handle_not_found_error("Item")
    except Exception as e:
        raise error_handler.handle_internal_server_error()


"""
Delete an inventory item with the specified item ID.

Args:
    item_id (str): The ID of the item to delete.

Returns:
    A dictionary with a message indicating the success of the deletion.

Raises:
    NotFoundError: If the item with the specified ID is not found.
    InternalServerError: If an error occurs while deleting the inventory item.
"""


@router.delete("/inventory/{item_id}", response_model=dict)
async def delete_inventory(item_id: str) -> dict:
    try:
        object_id = ObjectId(item_id)
        result = await inventory_collection.delete_one({"_id": object_id})

        if result.deleted_count > 0:
            return {"message": "Item deleted successfully"}
        else:
            raise error_handler.handle_not_found_error("Item")
    except Exception as e:
        raise error_handler.handle_internal_server_error()
