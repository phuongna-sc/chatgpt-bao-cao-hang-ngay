import os
from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)

# Hàm kết nối BigQuery và trả dữ liệu báo cáo
def get_daily_report():
    client = bigquery.Client()
    query = """
        SELECT 
          COUNT(*) AS total_tasks,
          ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)/COUNT(*)*100, 2) AS completed_percent,
          SUM(CASE WHEN due_date < CURRENT_DATE() AND status != 'completed' THEN 1 ELSE 0 END) AS overdue_tasks
        FROM `your_project.your_dataset.tasks`
    """
    results = client.query(query).result()
    row = list(results)[0]
    return {
        "total_tasks": row["total_tasks"],
        "completed_percent": row["completed_percent"],
        "overdue_tasks": row["overdue_tasks"]
    }

@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "BigQuery Proxy API is running 🚀"})

@app.route("/getDailyReport", methods=["GET"])
def daily_report():
    try:
        report = get_daily_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lệnh khởi chạy ứng dụng Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
