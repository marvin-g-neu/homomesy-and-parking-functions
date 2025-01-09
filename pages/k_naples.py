from animate import simulate_k_naples_parking, plot_parking_state
import streamlit as st
import matplotlib.pyplot as plt
import time

# SETUP

# hide sidebar and set tab config
st.set_page_config(
    page_title="k-Naples PF", 
    page_icon="🚗",    
    initial_sidebar_state="collapsed"
)

# center title
col1, col2, col3 = st.columns([3, 6, 1])

with col2:
    # title
    st.title(r"$k$-Naples $PF_n$")

# preface
st.markdown(r"""
We have $n$ cars, each with a preferred spot. They arrive in order $c_1, c_2, \dots, c_n$:
- If a car, $c_i$ has its preferred spot available, they will park there.
- If the spot is occupied, $c_i$ will first look backwards up to $k$ spots for an available spot.
- If no spot is found going backwards, $c_i$ will try every spot in linear order after their preferred parking spot until they find an open spot.
- If no open spot is found when $c_i$ reaches the end of the list, we conclude that specific $n$-tuple is NOT a $k$-Naples Parking Function.
""")

# img
st.markdown("---")
st.markdown(r"More to know about $k$-Naples $PF_n$:")
st.markdown("""
<style>
    [data-testid="stImage"] img {
        border-radius: 10px;
        border: 2px solid #ddd;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)
st.image("imgs/naples.png")

# ANIMATE

st.write("---")

# center title
col1, col2, col3 = st.columns([4.5, 6, 1])

with col2:
    # title
    st.title("Animate")

n = st.selectbox(fr"Select the number of cars ($n$)", list(range(2, 11)), index=1)
k = st.selectbox(fr"Select your steps back ($k$)", list(range(1, n)), index=1)

st.markdown("### Enter the preferences as a tuple:")
st.markdown(f"Example format for n = 3 and k = 2: (1, 2, 3)")

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
            frames = simulate_k_naples_parking(parking_func, k)
            
            placeholder = st.empty()
            
            for step in range(len(frames)):
                fig = plot_parking_state(parking_func, frames[step], step)
                placeholder.pyplot(fig)
                plt.close(fig)  
                time.sleep(1.0)
            
            if all((s is not None) for s in frames[-1]):
                st.success(f"All cars parked. This **is** a valid {k}-Naples Parking Function of length {n}!")
            else:
                st.error(f"A car reached the end of the street without parking. This is **not** a valid {k}-Naples Parking Function!")
    
    except ValueError:
        st.error("Invalid input format. Please enter numbers separated by commas.")
