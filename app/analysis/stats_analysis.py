import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.policy_model import Policy

sns.set_theme(style="whitegrid")

# Ensure the plots directory exists
PLOT_DIR = "plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def load_policy_data(db: Session):
    result = (
        db.query(
            Policy.id.label("policy_id"),
            Policy.agent_id,
            Policy.scheme_id,
            Policy.premium_amount,
            Policy.start_date
        ).all()
    )
    df = pd.DataFrame(result, columns=["policy_id", "agent_id", "scheme_id", "premium_amount", "start_date"])
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['month'] = df['start_date'].dt.to_period('M').astype(str)
    return df


def top_5_agents_by_amount(df):
    grouped = (
        df.groupby(["month", "agent_id"])["premium_amount"].sum()
        .reset_index()
        .sort_values(["month", "premium_amount"], ascending=[True, False])
        .groupby("month").head(5)
    )
    return grouped


def top_5_agents_by_count(df):
    grouped = (
        df.groupby(["month", "agent_id"])["policy_id"].count()
        .reset_index(name="policy_count")
        .sort_values(["month", "policy_count"], ascending=[True, False])
        .groupby("month").head(5)
    )
    return grouped


def top_5_policies(df):
    grouped = (
        df.groupby("policy_id")["premium_amount"]
        .sum()
        .reset_index()
        .sort_values("premium_amount", ascending=False)
        .head(5)
    )
    return grouped


def top_5_schemes(df):
    grouped = (
        df.groupby("scheme_id")["policy_id"]
        .count()
        .reset_index(name="policy_count")
        .sort_values("policy_count", ascending=False)
        .head(5)
    )
    return grouped


def monthly_sales_summary(df):
    grouped = (
        df.groupby("month")
        .agg(total_sales=("premium_amount", "sum"), policies_sold=("policy_id", "count"))
        .reset_index()
    )
    return grouped


def plot_top_5_agents_by_amount(data, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="month", y="premium_amount", hue="agent_id", data=data)
    plt.title("Top 5 Agents by Premium Amount Sold (Monthly)")
    plt.ylabel("Total Premium Amount")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_top_5_agents_by_count(data, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="month", y="policy_count", hue="agent_id", data=data)
    plt.title("Top 5 Agents by Number of Policies Sold (Monthly)")
    plt.ylabel("Number of Policies")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_monthly_sales_summary(data, filename):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    sns.barplot(x="month", y="total_sales", data=data, ax=ax1, color="skyblue", label="Total Sales")
    sns.lineplot(x="month", y="policies_sold", data=data, ax=ax2, marker="o", color="orange", label="Policies Sold")
    ax1.set_title("Monthly Sales Summary")
    ax1.set_ylabel("Total Premium Amount")
    ax2.set_ylabel("Number of Policies")
    fig.tight_layout()
    plt.savefig(filename)
    plt.close()


def main():
    db = SessionLocal()
    try:
        df = load_policy_data(db)

        print("\n📊 Top 5 Agents by Premium Amount:")
        print(top_5_agents_by_amount(df))

        print("\n📊 Top 5 Agents by Policy Count:")
        print(top_5_agents_by_count(df))

        print("\n🏆 Top 5 Policies by Premium Amount:")
        print(top_5_policies(df))

        print("\n🏆 Top 5 Schemes by Policy Count:")
        print(top_5_schemes(df))

        summary = monthly_sales_summary(df)

        # Save Plots to Files
        plot_top_5_agents_by_amount(top_5_agents_by_amount(df), f"{PLOT_DIR}/top_agents_by_amount.png")
        plot_top_5_agents_by_count(top_5_agents_by_count(df), f"{PLOT_DIR}/top_agents_by_count.png")
        plot_monthly_sales_summary(summary, f"{PLOT_DIR}/monthly_summary.png")

        print(f"\n✅ Plots saved in '{PLOT_DIR}/'")

    finally:
        db.close()


if __name__ == "__main__":
    main()
