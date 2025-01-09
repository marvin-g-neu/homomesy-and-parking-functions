from animate import simulate_unit_interval_parking, plot_parking_state
import streamlit as st
import matplotlib.pyplot as plt
import time

# SETUP

# hide sidebar and set tab config
st.set_page_config(
    page_title="Unit Interval PF", 
    page_icon="🚗",    
    initial_sidebar_state="collapsed"
)

# center title
col1, col2, col3 = st.columns([2, 6, 1])

with col2:
    # title
    st.title("Unit-Interval $PF_n$")

# preface
st.markdown(r"""
A unit interval parking function is like a classical parking function, but each car $c_i$ can park in either:
- Their preferred spot $p_i$
- The next spot $p_i + 1$ (except for the last car)

Cars park in order, taking the first available spot in their allowed interval.
""")

# img
st.markdown("---")
st.markdown(r"A more formal definition of Unit-Interval $PF_n$:")
st.markdown("""
<style>
    [data-testid="stImage"] img {
        border-radius: 10px;
        border: 2px solid #ddd;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)
st.image("imgs/unit.png")

# input section
st.write("---")

# center title
col1, col2, col3 = st.columns([4.5, 6, 1])

with col2:
    # title
    st.title("Animate")

n = st.number_input("Number of cars (n)", min_value=1, max_value=10, value=3)

# get preferences
st.markdown(f"Enter {n} comma-separated numbers for preferred spots:")
pref_input = st.text_input("Preferences", value="(2, 1, 1)")

if st.button("Generate"):
    try:
        # clean and validate input
        preferences = tuple(int(x.strip()) for x in pref_input.strip('()').split(","))
        
        # create alpha (preferences) and beta (preferences + 1, except last car)
        alpha = preferences
        beta = tuple(p if i == len(preferences)-1 else p+1 
                    for i, p in enumerate(preferences))
        
        # validate inputs
        if len(preferences) != n:
            st.error(f"Please enter exactly {n} numbers.")
        elif not all(1 <= x <= n for x in preferences):
            st.error(f"All numbers must be between 1 and {n}.")
        else:
            frames = simulate_unit_interval_parking(alpha, beta)
            
            placeholder = st.empty()
            
            for step in range(len(frames)):
                fig = plot_parking_state(alpha, frames[step], step)
                placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(1.0)
            
            if all(s is not None for s in frames[-1]):
                st.success(f"All cars parked successfully! This **is** a valid Unit Interval Parking Function!")
            else:
                st.error(f"A car couldn't park in its allowed interval. This is **not** a valid Unit Interval Parking Function!")
    
    except ValueError:
        st.error("Invalid input format. Please enter numbers separated by commas in parentheses.")
