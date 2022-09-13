from datetime import datetime
from app.domains.source_order_request.source_order_request_repository import SourceOrderRequestRepository


class SourceOrderRequestService:

    def __init__(self, source_order_request_repository: SourceOrderRequestRepository):
        self.source_order_req_repo = source_order_request_repository

    def create(self, data):
        return self.source_order_req_repo.create(data)

    def list(self, hospital_id: int):
        return self.source_order_req_repo.list(hospital_id)

    def get(self, id: int):
        return self.source_order_req_repo.get(id)

    def update(self, data, source_id, user_id):
        return self.source_order_req_repo.update(data, source_id, user_id)

    def _is_created_by_user(self, user_id):
        return self.source_order_req_repo.check_user_id(user_id)

    def delete(self, id: int):
        """
        If user has the same id as created_by id -> delete
        If not -> check if user is in the same id
        """
        try:
            return self.source_order_req_repo.delete(id)
        except:
            raise PermissionError
