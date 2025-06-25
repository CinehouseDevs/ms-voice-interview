import re
from faster_whisper import WhisperModel
from ollama import chat
from elevenlabs.client import ElevenLabs

class VoiceService:
    def __init__(self, model_name="medium"):
        """Inicializa o modelo Faster Whisper"""
        self.client = ElevenLabs(api_key="sk_b21062798686364d2a6f8d8ad8aa295ae102398cd681e936")  # Sua chave de API
        self.model = WhisperModel(model_name, device="cpu")  # Altere para "cuda" se estiver com GPU
        self.ollama_model = "deepseek-r1:8b"

    def transcribe(self, audio_file: str) -> str:
        """Transcreve o arquivo de áudio para texto"""
        segments, _ = self.model.transcribe(audio_file, language="pt")
        return " ".join([seg.text for seg in segments])

    def generate_ai_answer(self, user_text: str) -> str:
        """Usa Ollama para gerar uma resposta inteligente para o texto do usuário"""
        response = chat(model=self.ollama_model, messages=[
            {"role": "system", "content": "Você é um assistente útil e direto."},
            {"role": "user", "content": user_text}
        ])
        return self.clean_response(response["message"]["content"])

    def clean_response(self, response: str) -> str:
        """Limpa tags desnecessárias da resposta"""
        return re.sub(r"<think>.*?</think>\n?", "", response, flags=re.DOTALL).strip()

    def synthesize(self, text: str) -> bytes:
        """Usa Eleven Labs para transformar texto em áudio"""
        return self.client.generate(text="Exemplo de fala", voice="Rachel", model="eleven_multilingual_v2")
