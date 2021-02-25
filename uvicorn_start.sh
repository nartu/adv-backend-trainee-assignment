 #!/usr/bin/bash

# dev (port 8000)
# uvicorn src.main:app --host 0.0.0.0 --port 9000 --reload

# deploy
uvicorn src.main:app --host 0.0.0.0 --port 9000
