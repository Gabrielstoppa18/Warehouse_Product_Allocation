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



if st.button("Solver"):
    alg.sa()

else:
        st.info(
            f"""
                👆 Click On Solver First
                """
        )

if st.button("View solution"):
    file_container = st.expander("Check the collect order")
    shows1 = pd.read_csv('orders.csv')
    shows2 = pd.read_csv('layout.csv')
    #uploaded_file.seek(0)
    file_container.write(shows1)

    file_container2 = st.expander("Check the warehouse layout")

    file_container.write(shows2)