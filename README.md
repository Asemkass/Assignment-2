# Assignment-2


---

# Olist E-Commerce Data Visualization

This project generates **six different charts** based on the Olist e-commerce dataset using **Python**, **Pandas**, **Matplotlib**, and **PostgreSQL**. The visualizations provide insights into orders, product prices, delivery delays, and more.

Additionally, the project supports **exporting data to Excel with formatting** and **interactive time slider functionality** for temporal analysis.

---


## Features

The project produces the following visualizations:

1. **Horizontal Bar Chart** – Average delivery delay by state.
2. **Vertical Bar Chart** – Top 10 product categories by canceled orders.
3. **Pie Chart** – Order status distribution.
4. **Line Chart** – Average shipping cost by month.
5. **Histogram** – Product price distribution.
6. **Scatter Plot** – Product count vs total order value per order.

**Additional Features:**

* **Excel Export** – Export all datasets used for visualizations to `.xlsx` files with formatted headers, number formats, and filters.
* **Interactive Time Slider** – Filter charts (e.g., line chart of shipping costs) by specific time ranges dynamically.

All charts and exported Excel files are saved to the `charts/` and `exports/` folders respectively.

---

## Requirements

* Python 3.10+
* PostgreSQL with Olist dataset imported
* Python packages:

```bash
pip install pandas psycopg2-binary matplotlib openpyxl python-dotenv plotly dash
```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/olist-data-viz.git
cd olist-data-viz
```

2. Create a `.env` file with your PostgreSQL connection details:

```env
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

3. Ensure the Olist dataset tables are available in your database:

* `olist_orders`
* `olist_order_items`
* `olist_products`
* `olist_customers`
* `olist_sellers`
* `product_category_name_translation`

---

## Usage

Run the main Python script:

```bash
python main.py
```

The charts will be saved in the `charts/` folder, and datasets will be exported to `exports/`.

---

## Generated Charts

| Chart Type     | Description                          |
| -------------- | ------------------------------------ |
| Horizontal Bar | Average Delivery Delay by State      |
| Vertical Bar   | Top 10 Categories by Canceled Orders |
| Pie Chart      | Order Status Distribution            |
| Line Chart     | Average Shipping Cost by Month       |
| Histogram      | Product Price Distribution           |
| Scatter Plot   | Product Count vs Total Order Value   |

---

## Excel Export

* All query results are saved to **Excel files** in the `exports/` folder.
* Features include:

  * Formatted headers
  * Number formatting (currency, dates, percentages)
  * Auto-filters for easy sorting and searching
* Example export files:

  * `exports/avg_delivery_delay_by_state.xlsx`
  * `exports/canceled_orders_by_category.xlsx`
  * `exports/order_status_distribution.xlsx`

---

## Interactive Time Slider

* Line charts with time-series data (e.g., monthly shipping costs) can include a **time slider** using **Plotly/Dash** for dynamic exploration.
* Users can select a specific range of months, and the chart updates interactively to show trends within that period.
* Enhances temporal analysis without regenerating static charts.
