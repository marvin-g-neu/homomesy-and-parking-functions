from animate import simulate_classical_parking, plot_parking_state
import streamlit as st
import matplotlib.pyplot as plt
import time

# SETUP

# hide sidebar and set tab config
st.set_page_config(
    page_title="Classical PF", 
    page_icon="🚗",    
    initial_sidebar_state="collapsed"
)

# center title
col1, col2, col3 = st.columns([3, 6, 1])

with col2:
    st.title(r"Classical $PF_n$")

# preface and example
st.markdown(r"""
We have $n$ cars, each with a preferred spot. They arrive in order $c_1, c_2, \dots, c_n$:
- If a car, $c_i$ has its preferred spot available, they will park there.
- Otherwise, $c_i$ will try every spot in linear order after their preferred parking spot until they find an open spot. If no open spot is found when a $c_i$ reaches the end of the list, we conclude that specfic $n$-tuple is NOT a Classical Parking Function.
""")

st.markdown("Here's another example image from our mentor's video linked on our the home page for a better idea: ")

st.image("imgs/classical_case.png", caption="")

# adj styling
st.markdown("""
    <style>
        [data-testid="stImage"] {
            border-radius: 10px;
            border: 2px solid #ddd;
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ANIMATE

st.write("---")

# center title
col1, col2, col3 = st.columns([4.5, 6, 1])

with col2:
    # title
    st.title("Animate")

n = st.selectbox(fr"Select the number of cars ($n$)", list(range(2, 11)), index=1)

st.markdown("### Enter the preferences as a tuple:")
st.markdown(f"Example format for n = {3}: (1, 2, 3)")

# single text input
pref_input = st.text_input(
    label="Enter preferences",
    value=f"({', '.join(str(i+1) for i in range(n))})"
)

# parse and validate input and run animation
if st.button("Generate"):
    try:
        # convert to tuple of ints
        cleaned_input = pref_input.replace(" ", "").strip("()").split(",")
        preferences = tuple(int(x) for x in cleaned_input)
        
        # validate length
        if len(preferences) != n:
            st.error(f"Please enter exactly {n} numbers.")
        # validate range
        elif not all(1 <= x <= n for x in preferences):
            st.error(f"All numbers must be between 1 and {n}.")
        else:
            # run animation if valid
            parking_func = preferences
            frames = simulate_classical_parking(parking_func)
            
            placeholder = st.empty()
            
            for step in range(len(frames)):
                fig = plot_parking_state(parking_func, frames[step], step)
                placeholder.pyplot(fig)
                plt.close(fig)  
                time.sleep(1.0)
            
            if all((s is not None) for s in frames[-1]):
                st.success(f"All cars parked. This **is** a valid Classical Parking Function of length {n}!")
            else:
                st.error("A car reached the end of the street. Therefore, this is **not** a valid Classical Parking Function!")
    
    except ValueError:
        st.error("Invalid input format. Please enter numbers separated by commas.")
