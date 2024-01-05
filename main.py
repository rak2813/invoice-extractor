from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 
#API Config
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Load Gemini Model
model = genai.GenerativeModel('gemini-pro-vision')

def get_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text 

#Configure streamlit
st.set_page_config(page_title="Invoice Extractor")
st.header("Invoice Extractor")
input = st.text_input("Input Prompt: ", key='input')
uploaded_file = st.file_uploader("Choose an invoice ", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


submit = st.button("Generate")

input_prompt = """You are an expert in understanding invoices.
I will upload an image of an invoice and you are required to answer any question based on the invoice accurately."""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_response(input_prompt, image_data, input)
    st.write(response)
