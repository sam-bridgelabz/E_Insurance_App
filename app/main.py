
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.app_config import get_host_ip_address_n_port



# App metadata
app = FastAPI(
    title="E-Insurance Management System",
    description="A role-based insurance system built with FastAPI.",
    version="1.0.0",
    contact={
        "name": "Monocept Team",
        "url": "https://github.com/sam-bridgelabz/E_Insurance_App",
        "email": "sam.varghese@bridgelabz.com"
    }
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "running", "payload": "Welcome to E-Insurance API","satus_code": 200}


def run_web_mode():
    try:
        import uvicorn

        host_ip_address, host_port_number_str = get_host_ip_address_n_port()
        host_port_number = int(host_port_number_str)

        uvicorn.run(
            "app.main:app", host=host_ip_address, port=host_port_number
        )
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    run_web_mode()
