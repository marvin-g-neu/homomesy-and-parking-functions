from animate import simulate_interval_parking, plot_parking_state
import streamlit as st
import matplotlib.pyplot as plt
import time

# SETUP

# hide sidebar and set tab config
st.set_page_config(
    page_title="Interval PF", 
    page_icon="🚗",    
    initial_sidebar_state="collapsed"
)

# center title
col1, col2, col3 = st.columns([3, 6, 1])

with col2:
    # title
    st.title("$l$-Interval $PF_n$")

# preface
st.markdown(r"""
An interval parking function consists of two vectors $\alpha = (a_1, a_2, \ldots, a_n)$ and $\beta = (b_1, b_2, \ldots, b_n)$ where:
- $b_i \geq a_i$ for all $1 \leq i \leq n$.
- Each car $c_i$ must park in some spot between positions $a_i$ and $b_i$ (inclusive).
- Cars park in order, taking the first available spot in their allowed interval.
""")

# img
st.markdown("---")
st.markdown(r"A more formal definition of $l$-Interval $PF_n$:")
st.markdown("""
<style>
    [data-testid="stImage"] img {
        border-radius: 10px;
        border: 2px solid #ddd;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)
st.image("imgs/l_interval.png")

# input section
st.write("---")

# center title
col1, col2, col3 = st.columns([4.5, 6, 1])

with col2:
    # title
    st.title("Animate")

n = st.number_input("Number of cars (n)", min_value=1, max_value=10, value=3)

# get alpha preferences
st.markdown(f"Enter {n} comma-separated numbers for α (starting positions) as a tuple:")
alpha_input = st.text_input("α preferences", value="(1, 1, 1)")

# get beta preferences
st.markdown(f"Enter {n} comma-separated numbers for β (ending positions) as a tuple:")
beta_input = st.text_input("β preferences", value="(3, 3, 3)")

if st.button("Generate"):
    try:
        # clean and validate input
        alpha = tuple(int(x.strip()) for x in alpha_input.strip('()').split(","))
        beta = tuple(int(x.strip()) for x in beta_input.strip('()').split(","))
        
        # validate inputs
        if len(alpha) != n or len(beta) != n:
            st.error(f"Please enter exactly {n} numbers for both α and β.")
        elif not all(1 <= x <= n for x in alpha + beta):
            st.error(f"All numbers must be between 1 and {n}.")
        elif not all(b >= a for a, b in zip(alpha, beta)):
            st.error("Each number in β must be greater than or equal to the corresponding number in α.")
        else:
            frames = simulate_interval_parking(alpha, beta)
            
            placeholder = st.empty()
            
            for step in range(len(frames)):
                fig = plot_parking_state(alpha, frames[step], step)
                placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(1.0)
            
            if all(s is not None for s in frames[-1]):
                st.success(f"All cars parked successfully! This **is** a valid $l$-Interval Parking Function!")
            else:
                st.error(f"A car couldn't park in its allowed interval. This is **not** a valid $l$-Interval Parking Function!")
    
    except ValueError:
        st.error("Invalid input format. Please enter numbers separated by commas in parentheses.")
