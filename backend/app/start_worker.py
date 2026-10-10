from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.tasks import process_new_order

app = FastAPI(title="E-Commerce API")

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://your-frontend.onrender.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "API is online and CORS is enabled"}

@app.post("/orders/process")
def create_order(order_id: int, email: str):
    # Offload work asynchronously to your Celery worker via Redis
    task = process_new_order.delay(order_id, email)
    return {"message": "Order queued successfully", "task_id": task.id}