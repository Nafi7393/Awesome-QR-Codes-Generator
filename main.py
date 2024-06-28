import os
import io
from itertools import cycle
import segno
import streamlit as st
from streamlit.components.v1 import html
from PIL import Image
import requests

# Set Streamlit page configuration
st.set_page_config(page_title="Awesome QR Generator")

# Define basic styling
BASIC_STYLE = """
<style>
#MainMenu { visibility: collapse; }
footer { visibility: collapse; }
h1 { text-align: center; }
img { display: block; margin-left: auto; margin-right: auto; }
.css-1kyxreq, .css-firdtp {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.css-firdtp {
    width: 40%;
    height: 60px;
}
.css-1offfwp p {
    font-size: 25px;
    font-weight: bold; 
}
iframe { height: 48px; font-size: 45px; }
</style>
"""

# Display page title and apply basic styling
st.markdown("# Make Awesome QR Codes!")
st.markdown(BASIC_STYLE, unsafe_allow_html=True)


@st.cache_data(max_entries=20)
def generate_qr_code(input_data, input_image, qr_color, qr_bg_color, size):
    """Generate a QR code with optional background image and custom colors."""
    qrcode = segno.make(input_data, error='h')
    output = io.BytesIO()

    try:
        if input_image:
            file_type = "gif" if input_image.name.endswith("gif") else "png"
            qrcode.to_artistic(background=input_image, target=output, scale=12, kind=file_type)
        else:
            qrcode.save(output, kind='png', scale=12, dark=qr_color, light=qr_bg_color)

        output.seek(0)
        image = Image.open(output)
        image = image.resize(size, Image.ANTIALIAS)

        output = io.BytesIO()
        image.save(output, format='PNG')
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
        return None

    return output


def shorten_url(url):
    """Shorten a URL using the TinyURL API."""
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text
    else:
        # st.error("Error shortening the URL.")
        return url


# User input and customization options
user_data = st.text_input("Input your data here.")
uploaded_image = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
                                  label_visibility="collapsed")

# Display color pickers side by side
col1, col2 = st.columns(2)
with col1:
    qr_color = st.color_picker("Pick a color for the QR code", "#000000")
with col2:
    qr_bg_color = st.color_picker("Pick a background color", "#FFFFFF")

# Set constant size for QR code image
constant_size = (400, 400)  # Width, Height in pixels

# Generate QR code on button click
if st.button("Generate Now", type="primary"):
    if user_data:
        shortened_url = shorten_url(user_data)
        qr_code = generate_qr_code(shortened_url, uploaded_image, qr_color, qr_bg_color, constant_size)
        if qr_code:
            qr_code.seek(0)
            st.image(qr_code)

            file_extension = "gif" if uploaded_image and uploaded_image.name.endswith("gif") else "png"
            st.download_button("Download QR Code", data=qr_code, file_name=f"qr_code.{file_extension}")
    else:
        st.error("Please enter some data to generate a QR code.")

st.markdown("#")
# Display example section
html("<h2 class='example'><u>Example:</u></h2>")

# Showcase examples from 'showcase' directory
size = 7
cols = cycle(st.columns(size))
showcase_directory = "showcase"
showcase_files = [os.path.join(showcase_directory, f) for f in os.listdir(showcase_directory)]

for showcase_file in showcase_files:
    col = next(cols)
    col.image(showcase_file)
