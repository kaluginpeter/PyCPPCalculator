# backend/tasks.py
from celery import Celery
import requests

app = Celery('computation_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    result_expires=3600,
)

@app.task
def make_computation(title, operation, a, b):
    """
    Celery task to send a computation request to the C++ backend and return the result.
    """
    # URL of the C++ backend
    cpp_backend_url = "http://localhost:8080/compute"

    # Prepare the payload for the C++ backend
    payload = {
        "title": title,
        "operation": operation,
        "a": a,
        "b": b
    }

    try:
        # Send a POST request to the C++ backend
        response = requests.post(cpp_backend_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        result = response.json().get("result")

        # Return the result to the Celery task
        return result

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        raise Exception(f"Failed to communicate with C++ backend: {e}")