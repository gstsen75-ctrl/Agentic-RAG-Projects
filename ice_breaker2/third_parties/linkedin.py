import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url : str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from LinkedIn profiles."""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/gstsen75-ctrl/e6e851720963c104526f543b1ebe45ef/raw/c953b4b875550cd87faac41f8f76b8c8b61bc1b2/agastya-sen-scrapin.json"
        response= requests.get(linkedin_profile_url, timeout=10)

    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
                }
        response = requests.get(api_endpoint, params=params, timeout = 10)
    data = response.json().get("person")
    data = {
        k : v
        for k, v in data.items()
        if v not in ([], "", " ", None)
        and k not in ["certifications"]
    }
    return data



if __name__ == '__main__':
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/agastya-sen-7b8268230/",
            mock=True,
        )
    )

