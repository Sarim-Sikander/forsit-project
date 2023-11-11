from fastapi import HTTPException, status


class ErrorHandling:
    @staticmethod
    def handle_internal_server_error():
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    @staticmethod
    def handle_not_found_error(resource_name: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource_name} not found"
        )


class InventoryErrorHandler:
    @staticmethod
    def handle_quantity_warning(quantity: int, product: str) -> None:
        if quantity < 10:
            raise HTTPException(
                status_code=200,
                detail=f"Warning: Product ({product}) quantity is low. Current quantity: {quantity}",
            )
