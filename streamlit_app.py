from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.mysql_utils import get_customers_data
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Marketing Analytics API",
    description="Exposes customer data from MySQL as a REST endpoint",
    version="1.0.0"
)

# Optional: Enable CORS if accessing from Streamlit or another frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/customers", summary="Get all cleaned customer data")
def read_customers():
    try:
        df = get_customers_data()
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
