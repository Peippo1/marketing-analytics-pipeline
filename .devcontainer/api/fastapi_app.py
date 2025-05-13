from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from scripts.mysql_utils import get_customers_data

# ----------------------------------------
# 🌐 Initialize FastAPI app
# ----------------------------------------
app = FastAPI(
    title="Marketing Analytics API",
    description="Expose MySQL data through a RESTful endpoint",
    version="1.0.0"
)

# ----------------------------------------
# 🔓 Enable CORS (Cross-Origin Resource Sharing)
# This allows frontend apps like Streamlit or React to access this API
# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# 📊 Endpoint: /customers
# Returns customer data from MySQL in JSON format
# ----------------------------------------
@app.get("/customers", summary="Get cleaned customer data from MySQL")
def read_customers():
    try:
        # Load customer data from MySQL using shared utility function
        df = get_customers_data()

        # Convert DataFrame to list of JSON records and return
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        # If anything goes wrong, return a 500 error with details
        return JSONResponse(status_code=500, content={"error": str(e)})
