# #!/bin/bash

# echo "Starting FastAPI server..."
# uvicorn app.main:app --reload

#!/bin/bash

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

