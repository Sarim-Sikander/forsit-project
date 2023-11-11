from datetime import datetime

from pydantic import BaseModel

"""
A data model representing a sale.

Attributes:
    invoice_id (str): The ID of the invoice.
    branch (str): The branch where the sale occurred.
    city (str): The city where the sale occurred.
    customer_type (str): The type of customer.
    gender (str): The gender of the customer.
    product_line (str): The product line.
    unit_price (float): The unit price of the product.
    quantity (int): The quantity of the product sold.
    tax_5_percent (float): The tax amount (5% of the total).
    total (float): The total amount of the sale.
    date (str): The date of the sale.
    time (str): The time of the sale.
    payment (str): The payment method.
    cogs (float): The cost of goods sold.
    gross_margin_percentage (float): The gross margin percentage.
    gross_income (float): The gross income.
    rating (float): The rating of the sale.
"""


class Sale(BaseModel):
    invoice_id: str
    branch: str
    city: str
    customer_type: str
    gender: str
    product_line: str
    unit_price: float
    quantity: int
    tax_5_percent: float
    total: float
    date: str
    time: str
    payment: str
    cogs: float
    gross_margin_percentage: float
    gross_income: float
    rating: float


class SalesResponseModel(Sale):
    pass


class DateRangeInput(BaseModel):
    start_date: datetime
    end_date: datetime


class MonthYearInput(BaseModel):
    month: int
    year: int
