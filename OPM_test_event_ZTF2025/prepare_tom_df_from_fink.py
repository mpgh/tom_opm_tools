import requests
import pandas as pd
from io import BytesIO

def generate_pdf(object_id, output_csv=False):
    """
    Generate a CSV file from Fink Portal API data.

    Parameters:
        object_id (str): The ID of the object to retrieve.

    Returns:
        new_pdf (pandas.DataFrame): The TOM photometry format
        max_microlensing (float): The maximum fink microlensing probability
    """

    # Set up API request parameters

    try:
        r = requests.post(
            "https://api.fink-portal.org/api/v1/objects",
            json={"objectId": object_id, "output-format": "json"},
        )
        
        if not r.status_code == 200:
            print(f"Failed to retrieve data. Status code: {r.status_code}")
            return None

        # Parse JSON response
        pdf = pd.read_json(BytesIO(r.content))

        # Maximum microlensing probability
        max_microlensing = pdf.loc[pdf['i:jd'].idxmax(),"d:mulens"]

        # Rename columns for easier access
        namedic = {1: "ZTF_g", 2: "ZTF_r"}
        pdf["filter"] = pdf["i:fid"].map(namedic)

        new_pdf = pdf[["i:jd", "filter", "i:magpsf", "i:sigmapsf"]].copy()
        
        # Rename columns for better understanding
        new_pdf = new_pdf.rename(
            {"i:jd": "time", "i:magpsf": "magnitude", "i:sigmapsf": "error"}
        )
        
        # Save to CSV file
        if output_csv:
            filename = f"{object_id}.csv"
            new_pdf.to_csv(filename, index=False)

        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    return new_pdf, max_microlensing

# Example usage:
new_pdf, max_micro = generate_pdf("ZTF25abcwzci", output_csv=False)
print(max_micro)
