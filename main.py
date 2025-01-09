import streamlit as st

# hide sidebar and set tab config
st.set_page_config(
    page_title="PF Visualizer", 
    page_icon="🚗",    
    initial_sidebar_state="collapsed"
)

# adj styling
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none;}
        footer {visibility: hidden;}
        .block-container {padding-top: 2rem; max-width: 800px;}
        
        /* Style the image */
        .stImage img {
            border-radius: 10px;
            border: 2px solid #ddd;
            padding: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# center title
col1, col2, col3 = st.columns([3, 6, 1])

with col2:
    # title
    st.title(r"$PF_n$ Visualizer")

# preface
st.markdown("""
<div style='text-align: left;'>
This site was created to help present the research conducted by <u><i>Marvin Gandhi</i></u> and <u><i>Cyrus Young</i></u> on <b>Homomesy and Parking Functions</b>. A link to our final draft on <a href="https://arxiv.org/" style="color: #FF4B4B; text-decoration: none;">arXiv</a> will be available <a href="about:blank" style="color: #FF4B4B; text-decoration: none;">here</a> once we have submitted for publication.

This research took place at the University of Puerto Rico, Ponce, under the mentorship of <i>Dr. Jennifer Elder</i> 
and <i>Dr. Pamela E. Harris</i> as part of an REU program in the summer of 2024.

Some of our work has been documented, such as a contribution on <a href="https://www.findstat.org" style="color: #FF4B4B; text-decoration: none;">FindStat</a>, which can be seen <a href="https://findstat.org/Contributors/" style="color: #FF4B4B; text-decoration: none;">here</a>.

We also presented our work at two conferences: the <b>Young Mathematicians Conference (YMC 2024)</b> and 
the <b>Joint Math Meetings (JMM 2025)</b>. A link to our slides from YMC August 2024 is available <a href="https://drive.google.com/file/d/1rRz4d6YIA8XE3GmuhkepW-vBuP-6IWK8/view?usp=sharing" style="color: #FF4B4B; text-decoration: none;">here</a>.
In addtion, here is the abstract book from our year, <a href="https://ymc.osu.edu/sites/default/files/2024-08/YMC_2024-2.pdf" style="color: #FF4B4B; text-decoration: none;">here</a>.
            
Now, feel free to explore classical parking functions, subsets, and more with live animations!
</div>
""", unsafe_allow_html=True)

# page options
col1, col2 = st.columns(2)

with col1:
    if st.button(r"Classical Parking Functions", use_container_width=True):
        st.switch_page("pages/classical.py")
    
    if st.button(r"$k$-Naples Parking Functions", use_container_width=True):
        st.switch_page("pages/k_naples.py")

with col2:
    if st.button(r"$l$-Interval Parking Functions", use_container_width=True):
        st.switch_page("pages/l_interval.py")
    
    if st.button(r"Unit-Interval Parking Functions", use_container_width=True):
        st.switch_page("pages/unit_interval.py")

st.markdown("""
---
""")

# what are they section
col1, col2, col3 = st.columns([3, 6, 1])
with col2:
    st.title(r"What is a $PF_n$?")

st.markdown("""
Parking functions are mathematical objects that model parking scenarios where cars have preferred parking spots. Different variants explore various constraints and rules for these parking arrangements.
            
The notation $PF_n$ repsresnts the set of all parking functions of order, or length $n$. An $n$-tuple represents the preferences (spots) where each car wishes to park, consider this possible $PF_3$, which ends up following the rules for classical parking functions in the example below.
            
To learn more about parking functions, check out this <a href="https://www.youtube.com/watch?v=WRHQRVXljR8" style="color: #FF4B4B; text-decoration: none;">excellent introduction</a> by our mentor <i>Dr. Pamela E. Harris</i> who also provided this image.
""", unsafe_allow_html=True)

# image
st.image("imgs/example.png", caption="")
