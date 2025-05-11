import requests

# Step 1: Send POST request to generate webhook
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

payload = {
    "name": "Sanket",
    "regNo": "REG12347",
    "email": "youremail@example.com"
}

response = requests.post(generate_url, json=payload)

if response.status_code == 200:
    data = response.json()
    webhook_url = data.get("webhook")
    access_token = data.get("accessToken")

    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)

    # Step 2: Final SQL query for Question 1 (odd regNo)
    final_sql_query = """
    SELECT 
        p.AMOUNT AS SALARY,
        CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
        FLOOR(DATEDIFF(CURRENT_DATE, e.DOB) / 365) AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE DAY(p.PAYMENT_TIME) != 1
    ORDER BY p.AMOUNT DESC
    LIMIT 1;
    """

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    answer_payload = {
        "finalQuery": final_sql_query.strip()
    }

    # Step 3: Send final answer to webhook
    answer_response = requests.post(webhook_url, headers=headers, json=answer_payload)

    if answer_response.status_code == 200:
        print("Query submitted successfully!")
    else:
        print("Error submitting query:", answer_response.text)
else:
    print("Error generating webhook:", response.text)