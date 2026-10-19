"""MedRule Production WSGI Application Entrypoint for Gunicorn/Render."""

import os
from medrule_engine.web.app import create_app

# Create WSGI application instance
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
