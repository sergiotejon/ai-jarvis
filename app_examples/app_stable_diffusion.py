# Description: Streamlit app for testing the model
# Dependencies: streamlit, requests
# Installation: pip install streamlit requests watchgod
# Usage: streamlit run app.py IP:PORT

import streamlit as st
import requests
import sys
import base64
from io import BytesIO

# Get for argument the IP:PORT of the model
ARG1 = sys.argv[1]
st.caption(f"Using model at {ARG1}")

prompt = st.text_input(
    'Prompt', 'A cow',
    key="placeholder",
    help="Enter the prompt you want to use"
)

if prompt != "":
    data = requests.post("http://" + ARG1 + "/predictions", json={"input": {"prompt": prompt}}).json()

    if data['output'] == None:
        if data['error'] != None:
            output = data['error']
            st.write(output)
        else:
            output = "Sorry, I don't know what you mean."
            st.write(output)
    else:
        output = data['output']
        # Decode the base64 string
        decoded_bytes = base64.b64decode(output)
        image = BytesIO(decoded_bytes)

        st.image(
            image
        )
