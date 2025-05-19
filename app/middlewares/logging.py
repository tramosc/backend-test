# app/middlewares/logging.py
import logging
import time
import uuid
from contextvars import ContextVar
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Crear variable de contexto para almacenar el ID de la solicitud
request_id_var = ContextVar("request_id", default=None)

def get_request_id():
    """Obtiene el ID de la solicitud actual desde la variable de contexto"""
    return request_id_var.get()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para registrar solicitudes HTTP y establecer un ID único"""
    
    async def dispatch(self, request: Request, call_next):
        # Generar ID único para esta solicitud
        request_id = str(uuid.uuid4())
        # Guardar en la variable de contexto
        request_id_var.set(request_id)
        
        # Configurar logger
        logger = logging.getLogger(__name__)
        
        # Registrar inicio de solicitud
        start_time = time.time()
        logger.info(f"Solicitud iniciada: {request.method} {request.url.path} [request_id={request_id}]")
        
        try:
            # Procesar la solicitud
            response = await call_next(request)
            
            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time
            
            # Registrar finalización de solicitud
            logger.info(
                f"Solicitud completada: {request.method} {request.url.path} "
                f"status={response.status_code} tiempo={process_time:.3f}s "
                f"[request_id={request_id}]"
            )
            
            # Agregar ID de solicitud a las cabeceras de respuesta
            response.headers["X-Request-ID"] = request_id
            
            return response
        except Exception as e:
            # Registrar errores
            process_time = time.time() - start_time
            logger.error(
                f"Error en solicitud: {request.method} {request.url.path} "
                f"error={str(e)} tiempo={process_time:.3f}s "
                f"[request_id={request_id}]",
                exc_info=True
            )
            raise