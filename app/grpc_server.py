import grpc
from concurrent import futures

from sqlalchemy.orm import Session

from .db import SessionLocal, get_db_session
from . import models
from .grpc_generated import partner_pb2, partner_pb2_grpc


class PartnerServiceServicer(partner_pb2_grpc.PartnerServiceServicer):
    def GetPartner(self, request, context):
        # 1. Extract tenant from metadata (similar to your get_tenant_id header logic)
        metadata = dict(context.invocation_metadata())
        tenant_id = metadata.get('x-tenant-id', 'public')

        # 2. Use 'with' to drive the generator and get the actual session
        # This handles the try/finally/close automatically
        with get_db_session(schema=tenant_id) as db:
            partner = (
                db.query(models.Partner)
                .filter(models.Partner.id == request.id)
                .first()
            )

            if not partner:
                context.abort(grpc.StatusCode.NOT_FOUND, "Partner not found")

            return partner_pb2.GetPartnerResponse(
                id=partner.id,
                name=partner.name,
                active=partner.active,
                tenant_id=partner.tenant_id or "",
            )


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
