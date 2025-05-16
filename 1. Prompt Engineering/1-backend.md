Act as an expert Google Cloud backend developer.
Generate a Python 3.9 Cloud Function (Gen 2) that is triggered by messages published to a Pub/Sub topic named 'my-data-topic'.
The function should:


1. Decode the incoming message data (assuming it's a UTF-8 encoded string).
2. Log the decoded message content using the standard Python logging library.
3. If the message contains the keyword 'ERROR', it should write the entire message to a BigQuery table named 'project-id.my_dataset.error_logs'. The table has two columns: 'timestamp' (TIMESTAMP) and 'message_payload' (STRING).
4. Ensure the function handles potential errors gracefully during BigQuery insertion and logs them. Provide only the Python code for the main.py file and a requirements.txt file.

