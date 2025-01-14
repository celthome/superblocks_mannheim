# How to use OpenRouteService (ORS)

Follow the steps below to get started with using the OpenRouteService API with the provided [isochrones script](isochrones.py).

---

## Prerequisites

Before using the script, make sure you have the following:
1. **Environment installed**: Ensure you have installed the provided requirements on your system.
```python
pip install -r requirements.txt
```
2. **API Key**: Obtain an API key from OpenRouteService by following the instructions below.

---

## How to Get an API Key

1. **Sign Up**:
   - Visit the [OpenRouteService website](https://openrouteservice.org/dev/#/signup).
   - Create a free account by clicking "Sign Up" and filling in the required details.

2. **Access Your API Key**:
   - Once logged in, go to your dashboard by clicking your username in the top-right corner and selecting **"API Keys"**.
   - Click **"Create API Key"** to generate a new key.

3. **Copy the Key**:
   - Copy the generated API key. Keep it safe, as you'll need it to configure the script.

---

## Request Limitations

OpenRouteService applies rate limits based on your account type, look them up [here](https://openrouteservice.org/plans/):
The Standard plan includes for isochrones 500 requests per day, 20 per minute. If this is not enough, you might be able to apply for the Collaborative plan, which provides 2.500 isochrones per day and 40/min.
>If your application is in a humanitarian, academic, governmental, or non-for-profit organisation, you may be eligible for the collaborative plan.

---

## Steps to Use the Python Script

### Locate the Placeholder in the script
After locating the placeholder in the [isochrones script](isochrones.py) (line 61 "API-KEY") replace with your actual API Key.
