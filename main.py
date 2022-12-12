from itertools import cycle
import os
import io
import segno
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Awesome QR Generator")
basic_style = """
<style>
#MainMenu {
    visibility: collapse;
}
footer {
    visibility: collapse;
    }
h1 {
    text-align: center;
}
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.css-1kyxreq{
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.css-firdtp{
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 40%;
    height: 60px;
}
.css-1offfwp p{
    font-size: 25px;
    font-weight: bold; 
}
iframe{
    height: 48px;
    font-size: 45px;
}
</style>"""

st.markdown("""# Make Awesome QR Codes!""")
st.markdown(basic_style, unsafe_allow_html=True)


@st.cache(suppress_st_warning=True, max_entries=20, allow_output_mutation=True)
def making_qr_code(data, img):

    if img:
        if img.name[-3:] == "gif":
            kind = "gif"
        else:
            kind = "png"

        qrcode = segno.make(data, error='h')
        out = io.BytesIO()
        qrcode.to_artistic(background=img, target=out, scale=12, kind=kind)

        return out
    else:
        qrcode = segno.make(data, error='h')
        img = qrcode.to_pil(scale=12)
        return img


url_data = st.text_input("Input your data here.")
image_file = st.file_uploader("Upload your image", type=['png', 'jpg', "jpeg", "gif", "webp"], label_visibility="collapsed")

if st.button("Generate Now", type="primary"):
    file = making_qr_code(url_data, image_file)
    st.image(file)


html("""<h2 class='ex'><u> </u></h2>""")
html("""<h2 class='example'><u>Example:</u></h2>""")

size = 7
cols = cycle(st.columns([size, size, size, size, size, size, size]))
showcase = [f"showcase/{i}" for i in os.listdir("showcase")]
for i in range(len(showcase)):
    this_col = next(cols)
    this_col.image(showcase[i])













