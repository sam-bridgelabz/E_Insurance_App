import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Plan, Scheme


def plan_popularity_by_scheme_count(db: Session):
    """
    Count how many schemes are attached to each plan.
    """
    result = (
        db.query(
            Plan.name.label("plan_name"), func.count(Scheme.id).label("scheme_count")
        )
        .join(Scheme, Scheme.plan_id == Plan.id)
        .group_by(Plan.name)
        .order_by(desc("scheme_count"))
        .all()
    )
    return result


def top_5_plans_by_scheme_count(db: Session):
    """
    Return the top 5 plans based on number of attached schemes.
    """
    return plan_popularity_by_scheme_count(db)[:5]


def plot_plan_popularity(data, title="Plans by Scheme Count"):
    """
    Create a bar chart of scheme counts per plan.
    """
    df = pd.DataFrame(data, columns=["Plan", "Number of Schemes"])
    df.plot(kind="bar", x="Plan", y="Number of Schemes", legend=False)
    plt.ylabel("Number of Schemes")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def main():
    db = SessionLocal()
    try:
        print("📊 Scheme Count per Plan:")
        data = plan_popularity_by_scheme_count(db)
        for name, count in data:
            print(f"{name}: {count} schemes")

        print("\n🏆 Top 5 Plans by Scheme Count:")
        for name, count in top_5_plans_by_scheme_count(db):
            print(f"{name}: {count} schemes")

        plot_plan_popularity(data)
    finally:
        db.close()


if __name__ == "__main__":
    main()
