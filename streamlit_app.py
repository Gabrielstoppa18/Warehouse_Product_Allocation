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

st.title("Product Allocation")
with c30:
    st.image("assets/image_3.png", width=244)
    st.header("")

st.markdown('''Organizing products on shelves in order to facilitate collection during the consolidation of the most varied orders, as well as organizing these collection orders, are problems that distribution centers face on a daily basis.
 These issues are known as product allocation issues in distribution centers. The tool considers two heuristics based on simulated annealing, one to generate the allocation of products and the other to determine how to carry out the collection orders. 
 The developed tool seeks to optimally generate a disposition to allocate products and a sequence to collect products from orders in a way that the operational cost of collection is as low as possible.''')

st.markdown('''**Instructions** 

1- Select your test order.

2- Click on Solver Button .

3- Wait for the total cost of solution.

4- Click on View Solution Button.

5- Check the collect order and the warehouse layout.''')

order=st.selectbox('Chose order',
    ["instances_d5_ord5.txt","instances_d5_ord6.txt","instances_d5_ord7.txt",
        "instances_d10_ord5.txt","instances_d10_ord6.txt","iinstances_d10_ord7.txt",
        "instances_d20_ord5.txt","instances_d20_ord6.txt","instances_d20_ord7.txt"
    ],
    index=0,
)

if st.button("Solver"):
    alg.sa(order)

else:
        pass

if st.button("View solution"):
    file_container = st.expander("Check the collect order")
    shows1 = pd.read_csv('orders.csv')
    shows2 = pd.read_csv('layout.csv')
    #uploaded_file.seek(0)
    file_container.write(shows1)

    file_container2 = st.expander("Check the warehouse layout")

    file_container2.write(shows2)