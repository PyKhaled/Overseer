import os

if __package__:
    from . import app
else:
    # ``python overseer`` executes this file without package context. Add the
    # repository root so the package can still be imported normally.
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from overseer import app


if __name__ == "__main__":
    app.run(
        debug=os.getenv("OVERSEER_DEBUG") == "1",
        host=os.getenv("OVERSEER_HOST", "127.0.0.1"),
        port=int(os.getenv("OVERSEER_PORT", "8000")),
    )
