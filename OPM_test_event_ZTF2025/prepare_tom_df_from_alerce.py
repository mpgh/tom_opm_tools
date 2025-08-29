import pandas as pd
from alerce.core import Alerce


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
        alerce = Alerce()
        #More options are available, see https://alerce.readthedocs.io/en/latest/tutorials/ztf_api.html#
        lightcurve = alerce.query_lightcurve(object_id,format="json")
        pdf = pd.DataFrame.from_dict(lightcurve["detections"])
        probabilities = alerce.query_probabilities(object_id)
        prob_pd = pd.DataFrame.from_dict(probabilities)
        stochastic_bhrf_rank = prob_pd.loc[prob_pd["classifier_name"] \
            == "lc_classifier_BHRF_forced_phot_stochastic"]
        
        # Rename columns for easier access
        namedic = {1: "ZTF_g", 2: "ZTF_r", 3: "ZTF_i"}
        pdf["filter"] = pdf["fid"].map(namedic)
        
        #convert to JD
        new_pdf = pdf[["mjd", "filter", "magpsf", "sigmapsf"]].copy()
        new_pdf["mjd"] = new_pdf["mjd"] + 2400000.5
        
        # Rename columns for better understanding
        new_pdf = new_pdf.rename(
            {"mjd": "time", "magpsf": "magnitude", "i:sigmapsf": "error"}
        )
        print(new_pdf)
        # Save to CSV file
        if output_csv:
            filename = f"lc_{object_id}.csv"
            new_pdf.to_csv(filename, index=False)

        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return new_pdf,stochastic_bhrf_rank[stochastic_bhrf_rank["class_name"] == "Microlensing"].iloc[0]

# Example usage:
new_pdf, last_probability = generate_pdf("ZTF25abcwzci", output_csv=False)
print(last_probability["probability"])
