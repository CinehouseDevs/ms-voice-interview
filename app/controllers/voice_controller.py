from fastapi import APIRouter, WebSocket
from services.voice_service import VoiceService
import os

router = APIRouter(
    prefix="/v1/voice",
    tags=["voice"],
)
service = VoiceService()

@router.websocket("/stream_ai")
async def stream_ai(ws: WebSocket):
    """Exemplo de stream de áudio + texto + resposta AI (usando Eleven Labs)."""
    await ws.accept()
    try:
        while True:
            data = await ws.receive_bytes()
            if data == b'END':
                break

            temp_file = "temp/audio_in.wav"
            with open(temp_file, "wb") as f:
                f.write(data)

            # Etapa 1: Transcrição
            user_text = service.transcribe(temp_file)

            if user_text:
                # Etapa 2: Geração de resposta
                reply = service.generate_ai_answer(user_text)

                # Etapa 3: Geração de áudio com Eleven Labs
                reply_audio = service.synthesize(reply)

                # Etapa 4: Enviar texto e áudio para o cliente
                await ws.send_text(f"STT: {user_text}")
                await ws.send_bytes(reply_audio)

            os.remove(temp_file)

    except Exception as e:
        print(f"Erro no stream_ai: {e}")

    finally:
        await ws.close()