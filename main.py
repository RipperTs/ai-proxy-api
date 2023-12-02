import uvicorn

from application.common import config


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "application.app:get_app",
        workers=config.server_workers,
        host=config.server_name,
        port=config.server_port,
        reload=config.reload,
        factory=True,
    )


if __name__ == "__main__":
    main()
