# Assignment-2

---

# Olist E-Commerce Data Visualization

This project generates **six different charts** based on the Olist e-commerce dataset using **Python**, **Pandas**, **Matplotlib**, and **PostgreSQL**. The visualizations provide insights into orders, product prices, delivery delays, and more.

---


## Features

The project produces the following visualizations:

1. **Horizontal Bar Chart** – Average delivery delay by state.
2. **Vertical Bar Chart** – Top 10 product categories by canceled orders.
3. **Pie Chart** – Order status distribution.
4. **Line Chart** – Average shipping cost by month.
5. **Histogram** – Product price distribution.
6. **Scatter Plot** – Product count vs total order value per order.

All charts are saved to the `charts/` folder.

---

## Requirements

* Python 3.10+
* PostgreSQL with Olist dataset imported
* Python packages:

```bash
pip install pandas psycopg2-binary matplotlib python-dotenv
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

The charts will be saved in the `charts/` folder.

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


Хочешь, чтобы я так сделал?
