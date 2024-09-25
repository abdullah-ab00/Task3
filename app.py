from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow frontend and other origins to access this API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Likelihood probabilities (example values)
likelihood_probabilities = {
    'outlook': {('Sunny', 'Yes'): 0.5, ('Overcast', 'Yes'): 0.7, ('Rain', 'Yes'): 0.6, ('Sunny', 'No'): 0.3, ('Overcast', 'No'): 0.2, ('Rain', 'No'): 0.4},
    'temp': {('Hot', 'Yes'): 0.6, ('Mild', 'Yes'): 0.4, ('Cool', 'Yes'): 0.7, ('Hot', 'No'): 0.3, ('Mild', 'No'): 0.5, ('Cool', 'No'): 0.6},
    'humidity': {('High', 'Yes'): 0.7, ('Normal', 'Yes'): 0.6, ('High', 'No'): 0.4, ('Normal', 'No'): 0.5},
    'wind': {('Weak', 'Yes'): 0.8, ('Strong', 'Yes'): 0.4, ('Weak', 'No'): 0.3, ('Strong', 'No'): 0.7}
}

# Prior probabilities
p_yes = 9/14
p_no = 5/14

@app.post("/predict/")
async def predict(outlook: str = Form(...), temp: str = Form(...), humidity: str = Form(...), wind: str = Form(...)):
    # Compute the probabilities for 'Yes' and 'No'
    prob_yes = p_yes * likelihood_probabilities['outlook'][(outlook, 'Yes')] * \
                      likelihood_probabilities['temp'][(temp, 'Yes')] * \
                      likelihood_probabilities['humidity'][(humidity, 'Yes')] * \
                      likelihood_probabilities['wind'][(wind, 'Yes')]

    prob_no = p_no * likelihood_probabilities['outlook'][(outlook, 'No')] * \
                     likelihood_probabilities['temp'][(temp, 'No')] * \
                     likelihood_probabilities['humidity'][(humidity, 'No')] * \
                     likelihood_probabilities['wind'][(wind, 'No')]

    if prob_yes > prob_no:
        result = "Yes"
    else:
        result = "No"
    
    return {"prediction": result, "prob_yes": prob_yes, "prob_no": prob_no}
