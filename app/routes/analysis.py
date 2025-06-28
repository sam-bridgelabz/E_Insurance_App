import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.analysis.stats_analysis import (
    load_policy_data,
    monthly_sales_summary,
    plot_monthly_sales_summary,
    plot_top_5_agents_by_amount,
    plot_top_5_agents_by_count,
    top_5_agents_by_amount,
    top_5_agents_by_count,
    top_5_policies,
    top_5_schemes,
)
from app.db.session import get_db

router = APIRouter(prefix="/analysis", tags=["Analysis"])
PLOT_DIR = "app/analysis/Plots"
os.makedirs(PLOT_DIR, exist_ok=True)


# JSON Endpoints
@router.get("/top-agents-by-amount")
def get_top_agents_by_amount(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    return top_5_agents_by_amount(df).to_dict(orient="records")


@router.get("/top-agents-by-count")
def get_top_agents_by_count(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    return top_5_agents_by_count(df).to_dict(orient="records")


@router.get("/top-policies")
def get_top_policies(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    return top_5_policies(df).to_dict(orient="records")


@router.get("/top-schemes")
def get_top_schemes(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    return top_5_schemes(df).to_dict(orient="records")


@router.get("/monthly-summary")
def get_monthly_summary(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    return monthly_sales_summary(df).to_dict(orient="records")


# Plot Endpoints
media_type = "image/png"


@router.get("/plot/top-agents-by-amount")
def plot_top_agents_amount(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    path = os.path.join(PLOT_DIR, "top_agents_by_amount.png")
    plot_top_5_agents_by_amount(top_5_agents_by_amount(df), filename=path)
    return FileResponse(path, media_type=media_type)


@router.get("/plot/top-agents-by-count")
def plot_top_agents_count(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    path = os.path.join(PLOT_DIR, "top_agents_by_count.png")
    plot_top_5_agents_by_count(top_5_agents_by_count(df), filename=path)
    return FileResponse(path, media_type=media_type)


@router.get("/plot/monthly-summary")
def plot_summary(db: Session = Depends(get_db)):
    df = load_policy_data(db)
    path = os.path.join(PLOT_DIR, "monthly_summary.png")
    plot_monthly_sales_summary(monthly_sales_summary(df), filename=path)
    return FileResponse(path, media_type=media_type)
