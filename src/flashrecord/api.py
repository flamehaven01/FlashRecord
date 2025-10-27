"""
FastAPI Server - Expose CLI functionality as REST API
Auto-generated Swagger documentation at /docs
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .cli import FlashRecordCLI
from .config import Config

# Initialize FastAPI app
app = FastAPI(
    title="FlashRecord API", description="Screen recording and GIF generation API", version="0.1.0"
)

# Global CLI instance
cli = FlashRecordCLI()


# Response Models
class CommandResponse(BaseModel):
    """Response from command execution"""

    success: bool
    action: str
    message: str
    result: Optional[dict] = None


class ConfigResponse(BaseModel):
    """Configuration info"""

    command_style: str
    auto_delete_hours: int
    save_dir: str
    screenshot_dir: str
    video_dir: str
    gif_dir: str


class StatusResponse(BaseModel):
    """System status"""

    is_recording: bool
    recording_file: Optional[str] = None
    config: ConfigResponse


# Endpoints
@app.get("/", tags=["Info"])
async def root():
    """API Information"""
    return {
        "name": "FlashRecord API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "config": "/config",
            "status": "/status",
            "screenshot": "/screenshot",
            "recording": "/recording",
        },
    }


@app.get("/config", response_model=ConfigResponse, tags=["Configuration"])
async def get_config():
    """Get current configuration"""
    return ConfigResponse(
        command_style=cli.config.command_style,
        auto_delete_hours=cli.config.auto_delete_hours,
        save_dir=cli.config.save_dir,
        screenshot_dir=cli.config.screenshot_dir,
        video_dir=cli.config.video_dir,
        gif_dir=cli.config.gif_dir,
    )


@app.get("/status", response_model=StatusResponse, tags=["Status"])
async def get_status():
    """Get current system status"""
    config = await get_config()
    return StatusResponse(
        is_recording=cli.recording, recording_file=cli.recording_file, config=config
    )


@app.post("/screenshot", response_model=CommandResponse, tags=["Actions"])
async def take_screenshot():
    """Take a screenshot"""
    try:
        cli.handle_command("screenshot", None)
        if cli.recording_file:
            return CommandResponse(
                success=True,
                action="screenshot",
                message="Screenshot taken successfully",
                result={"path": cli.recording_file},
            )
        else:
            raise HTTPException(status_code=400, detail="Screenshot failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/recording/start", response_model=CommandResponse, tags=["Recording"])
async def start_recording():
    """Start video recording"""
    try:
        cli.handle_command("start", None)
        return CommandResponse(
            success=True,
            action="start_recording",
            message="Recording started",
            result={"path": cli.recording_file},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/recording/stop", response_model=CommandResponse, tags=["Recording"])
async def stop_recording():
    """Stop video recording"""
    try:
        if not cli.recording:
            raise HTTPException(status_code=400, detail="No recording in progress")
        cli.handle_command("stop", None)
        return CommandResponse(
            success=True,
            action="stop_recording",
            message="Recording stopped",
            result={"path": cli.recording_file},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/recording/gif", response_model=CommandResponse, tags=["Recording"])
async def convert_to_gif():
    """Convert recording to GIF"""
    try:
        if not cli.recording_file:
            raise HTTPException(status_code=400, detail="No recording to convert")
        cli.handle_command("gif", None)
        return CommandResponse(
            success=True, action="convert_to_gif", message="GIF conversion completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/save/{ai_model}", response_model=CommandResponse, tags=["Save"])
async def save_session(ai_model: str):
    """Save session to AI model file"""
    try:
        cli.handle_command("save", ai_model)  # type: ignore[attr-defined]
        return CommandResponse(
            success=True,
            action="save_session",
            message=f"Session saved to {ai_model}.md",
            result={"model": ai_model},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/config/schema", tags=["Configuration"])
async def get_config_schema():
    """Get configuration JSON schema"""
    config = Config()
    return config.schema_json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
