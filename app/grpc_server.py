import grpc
from concurrent import futures

from sqlalchemy.orm import Session

from .db import SessionLocal
from . import models
from .grpc_generated import partner_pb2, partner_pb2_grpc


class PartnerServiceServicer(partner_pb2_grpc.PartnerServiceServicer):
    def GetPartner(self, request, context):
        db: Session = SessionLocal()
        try:
            partner = (
                db.query(models.Partner)
                .filter(models.Partner.id == request.id)
                .first()
            )
            if not partner:
                context.set_details("Partner not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return partner_pb2.GetPartnerResponse()

            return partner_pb2.GetPartnerResponse(
                id=partner.id,
                name=partner.name,
                active=partner.active,
                tenant_id=partner.tenant_id or "",
            )
        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    partner_pb2_grpc.add_PartnerServiceServicer_to_server(
        PartnerServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")  # gRPC port
    server.start()
    print("gRPC PartnerService running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
