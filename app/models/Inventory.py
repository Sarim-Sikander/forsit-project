from typing import Optional

from pydantic import BaseModel

"""
A data model for creating an inventory.

Attributes:
    Products (str): The name of the products in the inventory.
    Quantity (int): The quantity of the products in the inventory.
"""


class InventoryCreate(BaseModel):
    Products: str
    Quantity: int


"""
A data model representing an inventory in the database.

This class inherits from `InventoryCreate` and includes additional attributes `_id`, `Products`, and `Quantity`.

Attributes:
    _id (str): The ID of the inventory in the database.
    Products (str): The name of the products in the inventory.
    Quantity (int): The quantity of the products in the inventory.
"""


class InventoryUpdate(BaseModel):
    Products: Optional[str] = None
    Quantity: Optional[int] = None


class InventoryInDB(InventoryCreate):
    _id: str
    Products: str
    Quantity: int


"""
A data model representing an inventory.

This class inherits from `InventoryInDB` and includes a nested `Config` class with the `orm_mode` attribute set to True.

Attributes:
    None
"""


class Inventory(InventoryInDB):
    pass

    class Config:
        orm_mode = True
