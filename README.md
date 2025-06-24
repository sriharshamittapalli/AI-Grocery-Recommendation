# Smart Grocery Assistant

Simple multi-agent demo built with the Google Cloud Agent Development Kit (ADK) and Streamlit. It finds nearby stores, estimates prices and suggests the best route.

## Features
- Finds nearby stores using Google Maps APIs
- Estimates prices and suggests the cheapest options
- Plans an efficient shopping route
- Runs locally or in the cloud via Streamlit

## Quick Start
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Set `GOOGLE_MAPS_API_KEY` in your environment or `.env` file
3. Launch the app
```bash
streamlit run app.py
```

## Running Tests
```bash
pytest -q
```

## Screenshots
Sample images are available in the `screenshots/` folder.

## License
[MIT](LICENSE)

## Disclaimer
This project is an independent demonstration created for the Google Cloud ADK Hackathon. It is not affiliated with or endorsed by Google. Generative AI outputs may be inaccurate or incomplete.
