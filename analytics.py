import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import StrMethodFormatter

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '0000'),
        port=os.getenv('DB_PORT', '5432')
    )

def main():
    os.makedirs("charts", exist_ok=True)

    queries = {
        "horizontal_bar_avg_delay": """
            SELECT c.customer_state,
                   ROUND(AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date))/86400), 2) AS avg_delay_days
            FROM olist_orders o
            JOIN olist_customers c ON o.customer_id = c.customer_id
            WHERE o.order_delivered_customer_date IS NOT NULL
            GROUP BY c.customer_state
            HAVING COUNT(o.order_id) >= 50
            ORDER BY avg_delay_days DESC;
        """,
        "vertical_bar_canceled_orders": """
            SELECT pt.product_category_name_english, COUNT(o.order_id) AS canceled_orders
            FROM olist_orders o
            JOIN olist_order_items oi ON o.order_id = oi.order_id
            JOIN olist_products p ON oi.product_id = p.product_id
            JOIN product_category_name_translation pt ON p.product_category_name = pt.product_category_name
            WHERE o.order_status = 'canceled'
            GROUP BY pt.product_category_name_english
            ORDER BY canceled_orders DESC
            LIMIT 10;
        """,
        "pie_order_status_distribution": """
            SELECT order_status, COUNT(*) AS status_count
            FROM olist_orders
            GROUP BY order_status
            ORDER BY status_count DESC;
        """,
        "line_avg_shipping_cost": """
            SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
                   ROUND(AVG(i.freight_value), 2) AS avg_shipping_cost
            FROM olist_orders o
            JOIN olist_order_items i ON o.order_id = i.order_id
            JOIN olist_sellers s ON i.seller_id = s.seller_id
            WHERE o.order_status = 'delivered'
            GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
            ORDER BY month;
        """,
        "histogram_product_prices": """
            SELECT i.price
            FROM olist_orders o
            JOIN olist_order_items i ON o.order_id = i.order_id
            JOIN olist_products p ON i.product_id = p.product_id
            WHERE o.order_status = 'delivered';
        """,
        "scatter_product_count_vs_total_value": """
            SELECT COUNT(i.product_id) AS product_count,
                   SUM(i.price) AS total_order_value
            FROM olist_orders o
            JOIN olist_order_items i ON o.order_id = i.order_id
            JOIN olist_products p ON i.product_id = p.product_id
            WHERE o.order_status = 'delivered'
            GROUP BY o.order_id;
        """
    }

    with get_db_connection() as conn:
        dfs = {name: pd.read_sql_query(query, conn) for name, query in queries.items()}

    dfs["horizontal_bar_avg_delay"].plot.barh(
        x='customer_state', y='avg_delay_days', figsize=(10,8), color='skyblue'
    )
    plt.xlabel("Average Delay (days)")
    plt.ylabel("State")
    plt.title("Average Delivery Delay by State", fontsize=14, fontweight="bold")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("charts/horizontal_bar.png", dpi=100)
    plt.close()

    dfs["vertical_bar_canceled_orders"].plot.bar(
        x='product_category_name_english', y='canceled_orders', figsize=(10,6), color='salmon'
    )
    plt.xlabel("Product Category")
    plt.ylabel("Canceled Orders")
    plt.title("Top 10 Categories by Canceled Orders", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("charts/vertical_bar_.png", dpi=100)
    plt.close()

    df_pie = dfs["pie_order_status_distribution"]
    total = df_pie['status_count'].sum()
    df_pie['percent'] = df_pie['status_count'] / total * 100
    major = df_pie[df_pie['percent'] >= 3]
    other = df_pie[df_pie['percent'] < 3]

    labels, values = [], []
    for row in major.itertuples():
        labels.append(f"{row.order_status}\n{row.status_count} ({row.percent:.1f}%)")
        values.append(row.status_count)

    if not other.empty:
        other_sum = other['status_count'].sum()
        other_percent = other_sum / total * 100
        values.append(other_sum)
        other_details = "\n".join([f"{row.order_status}: {row.status_count} ({row.percent:.1f}%)" for row in other.itertuples()])
        labels.append(f"Other\n{other_sum} ({other_percent:.1f}%)\n---\n{other_details}")

    plt.figure(figsize=(10,10))
    plt.pie(values, labels=labels, startangle=140, explode=[0.05]*len(values), wedgeprops=dict(width=0.45))
    plt.title("Order Status Distribution", fontsize=14, fontweight="bold")
    plt.savefig("charts/pie.png", dpi=120)
    plt.close()

    df_line = dfs["line_avg_shipping_cost"]
    df_line['month'] = pd.to_datetime(df_line['month'])
    df_line.plot(
        x='month', y='avg_shipping_cost', marker='o', linestyle='-', color='steelblue', figsize=(12,6)
    )
    plt.title("Average Shipping Cost by Month", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Average Shipping Cost")
    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.2f}"))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("charts/line.png", dpi=120)
    plt.close()

    dfs["histogram_product_prices"].plot.hist(
        y='price', bins=50, color='skyblue', edgecolor='black', figsize=(10,6)
    )
    plt.title("Product Price Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Price ($)")
    plt.ylabel("Number of Products")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0,500)
    plt.tight_layout()
    plt.savefig("charts/histogram.png", dpi=120)
    plt.close()

    dfs["scatter_product_count_vs_total_value"].plot.scatter(
        x='product_count', y='total_order_value', alpha=0.6, color='teal', edgecolor='black', figsize=(10,6)
    )
    plt.title("Product Count vs Total Order Value", fontsize=14, fontweight="bold")
    plt.xlabel("Product Count")
    plt.ylabel("Total Order Value ($)")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.2f}'))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("charts/scatter.png", dpi=120)
    plt.close()

if __name__ == "__main__":
    main()
