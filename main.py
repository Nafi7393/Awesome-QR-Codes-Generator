import random
import string
from itertools import cycle
from PIL import Image
from amzqr import amzqr
import os
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


def remove_files(max_limit):
    l_files = os.listdir("logo")
    if len(l_files) >= max_limit:
        for f in l_files:
            os.remove(f"logo/{f}")

        o_files = os.listdir("output")
        for i in o_files:
            os.remove(f"output/{i}")


def convert_img(pic_src):
    base_width = 400
    base_img = Image.open(pic_src).convert("RGB")
    ratio = (base_width / float(base_img.size[0]))
    height_size = int((float(base_img.size[1]) * float(ratio)))
    img = base_img.resize((base_width, height_size), Image.Resampling.LANCZOS)
    os.remove(pic_src)
    img.save(f"{pic_src.split('.')[0]}.png", quality=95)


def save_uploaded_file(uploadedfile):
    with open(os.path.join("logo", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())


@st.cache(suppress_st_warning=True, max_entries=20)
def making_qr_code(qr_ink, img):
    if img:
        save_uploaded_file(img)
        name = img.name
        src_pic_name = f"logo\\{img.name}"
        if src_pic_name.split('.')[-1] == "png" or src_pic_name.split('.')[-1] == "gif":
            pass
        else:
            convert_img(src_pic_name)
            src_pic_name = f"{src_pic_name.split('.')[0]}.png"
            name = src_pic_name.split('\\')[1]
    else:
        name = ''.join(random.choice(string.ascii_letters + "0123456789") for i in range(8)) + ".png"
        src_pic_name = None

    version, level, qr_name = amzqr.run(
        words=qr_ink,
        version=1,
        level='H',
        picture=src_pic_name,
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=f"output\\{name}",
        save_dir=os.getcwd())

    return f'output/{name}'


url_data = st.text_input("Input your data here.")
image_file = st.file_uploader("Upload your image", type=['png', 'jpg', "jpeg", "gif", "webp"], label_visibility="collapsed")

if st.button("Generate Now", type="primary"):
    file= making_qr_code(url_data, image_file)
    st.image(file, width=400)

remove_files(max_limit=10)


html("""<h2 class='ex'><u> </u></h2>""")
html("""<h2 class='example'><u>Example:</u></h2>""")

size = 7
cols = cycle(st.columns([size, size, size, size, size, size, size]))
showcase = [f"showcase/{i}" for i in os.listdir("showcase")]
for i in range(len(showcase)):
    this_col = next(cols)
    this_col.image(showcase[i])













