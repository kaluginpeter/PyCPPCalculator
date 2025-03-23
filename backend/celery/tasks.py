import requests

from backend.celery.celery_init import app
from backend.core.config import settings


@app.task
def make_computation(title, operation, operand_a, operand_b):
    """
    Celery task to send a computation request to the C++ backend and return the result.
    """
    # URL of the C++ backend
    cpp_backend_url = settings.CPP_BACKEND_COMPUTATION

    # Prepare the payload for the C++ backend
    payload = {
        "title": title,
        "operation": operation,
        "operand_a": operand_a,
        "operand_b": operand_b
    }

    try:
        # Send a POST request to the C++ backend
        response = requests.post(cpp_backend_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.json().get('error'):
            return {'Error': response.json().get('error')}

        # Parse the JSON response
        result = response.json().get("result")

        # Return the result to the Celery task
        return result

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        raise Exception(f"Failed to communicate with C++ backend: {e}")