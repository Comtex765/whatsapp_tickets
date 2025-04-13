from database import guardar_comprobante
from fastapi import APIRouter, HTTPException
from models import TransferenciaSch

router = APIRouter()


@router.post("/transferencia")
async def registrar_transferencia(transferencia: TransferenciaSch):
    try:
        # Verificar que los datos de la transferencia sean válidos (opcional, si es necesario)
        if not transferencia.comprobante:
            raise HTTPException(status_code=400, detail="Comprobante es obligatorio")

        # Guardar el comprobante en la base de datos
        guardar_comprobante(
            transferencia.model_dump()
        )  # Pasar los datos como diccionario

        # Respuesta exitosa
        return {"message": "Transferencia guardada exitosamente"}

    except ValueError as ve:
        # Excepción más específica para errores de valor
        raise HTTPException(
            status_code=400, detail=f"Error en los datos proporcionados: {ve}"
        )

    except Exception as e:
        # Error genérico para otros tipos de excepciones
        raise HTTPException(
            status_code=500, detail=f"Error al guardar la transferencia: {e}"
        )
