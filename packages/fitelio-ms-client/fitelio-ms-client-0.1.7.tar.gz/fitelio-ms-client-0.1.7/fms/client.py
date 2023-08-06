import grpc
import structlog
from fms import settings
from fms.pb import fms_pb2 as pb, fms_pb2_grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

logger = structlog.getLogger("client")


def health_check():
    channel = grpc.insecure_channel(settings.MS_SERVER_URL)
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(health_pb2.HealthCheckRequest(service="ms-server"), timeout=10)
    logger.info(f"response: {response}")


class FMSError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class FMSClient:
    def __init__(self, raise_exception=False):
        self.client = fms_pb2_grpc.MessagingServiceAPIStub(grpc.insecure_channel(settings.MS_SERVER_URL))
        self.raise_exception = raise_exception

    @classmethod
    def _build_message(
        cls,
        recipient,
        text,
        uid="",
        tag="",
        method=None,
        provider=None,
        alpha_name="",
        topic=None,
        title="",
        action=None,
        data=None,
        image=None,
        start_time=None,
        ttl=30,
    ):

        if method:
            method = pb.SendMethod.Value(method)
        if provider:
            provider = pb.Provider.Value(provider)
        return pb.Message(
            recipient=recipient,
            text=text,
            uid=uid,
            tag=tag,
            method=method,
            provider=provider,
            alpha_name=alpha_name,
            topic=topic,
            title=title,
            action=action,
            data=data,
            image=image,
            start_time=start_time,
            ttl=ttl,
        )

    def _handle_error(self, message, code=""):
        logger.error(message)
        if self.raise_exception:
            raise FMSError(code, message)
        return None

    def send_message(
        self,
        recipient,
        text,
        uid="",
        tag="",
        method=None,
        provider=None,
        alpha_name="",
        topic="",
        title="",
        action="",
        data=None,
        image=None,
        start_time=None,
        ttl=30,
    ):
        message = self._build_message(
            recipient,
            text,
            uid=uid,
            tag=tag,
            method=method,
            provider=provider,
            alpha_name=alpha_name,
            topic=topic,
            title=title,
            action=action,
            data=data,
            image=image,
            start_time=start_time,
            ttl=ttl,
        )
        try:
            response = self.client.Send(pb.MessageRequest(message=message))
        except grpc.RpcError as e:
            return self._handle_error(f"RPC call failed: {e}")
        except Exception as e:
            return self._handle_error(f"RPC call failed: {e}")
        if response.error.code:
            return self._handle_error(message=response.error.message, code=response.error.code)
        return response.message_id


__all__ = ["FMSError", "FMSClient", "health_check"]
