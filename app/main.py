import py_eureka_client.eureka_client as eureka_client

from fastapi import FastAPI
from controllers import voice_controller

EUREKA_SERVER_URL = "http://localhost:8761/eureka"
INSTANCE_PORT = 8000

app = FastAPI(
    title="MS Voice Interview API",
    description="API for Process user inputs (Speech-to-Text/Text-to-Speech) and response using AI models.",
    version="0.0.1",
    root_path="/api/voices",
)

app.include_router(voice_controller.router)


@app.on_event("startup")
async def register_with_eureka():
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER_URL,
        app_name="ms-voice-interview",
        instance_port=INSTANCE_PORT,
    )


@app.on_event("shutdown")
async def shutdown_eureka():
    await eureka_client.stop_async()
