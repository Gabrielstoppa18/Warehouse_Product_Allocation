import resolvedor
import streamlit as st
import pandas as pd

alg= resolvedor.SA()

st.set_page_config(
    page_title="Product Allocation",
    page_icon="📦",
)

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    st.image("assets/image_3.png", width=244)
    st.header("")

if st.button("Load Files"):
    alg.arm.openFile()
else:
        st.info(
            f"""
                👆 Click On Load Files First
                """
        )

if st.button("Solver"):
    alg.sa()

if st.button("Open CSV File"):
    alg.save_xls()
    file_container = st.expander("Check the Solution")
    shows = pd.read_excel(file_name='Solution.xlsx')
    #uploaded_file.seek(0)
    file_container.write(shows)