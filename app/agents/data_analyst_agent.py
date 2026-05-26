from app.database.db import db
from app.services.langchain_service import run_langchain_agent
from app.mcp.context import shared_context

def data_analyst_agent(message):

    sales_data = list(db.sales.find({}, {"_id": 0}))

    if not sales_data:
        context = "No sales data found."
    else:
        total_sales = sum(
            item.get("sales", 0)
            for item in sales_data
        )

        context = f"""
Total Records: {len(sales_data)}
Total Sales: {total_sales}
Sales Data: {sales_data[:5]}
"""

    response = run_langchain_agent(
        system_role="Data Analyst Agent",
        user_query=message.query,
        context=context
    )

    shared_context["latest_sales_summary"] = context

    return response