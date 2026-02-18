"""
Simple social media demo built with Streamlit
- Left column: list of friends (click a name to select)
- Middle column: search bar + options, shows search results
- Right column: selected friend's full profile (only one shown at a time)

Run: pip install -r requirements.txt && streamlit run streamlit_app.py
"""

import streamlit as st
from typing import List, Dict

st.set_page_config(page_title="Simple Social — Streamlit", layout="wide")

FRIENDS: List[Dict] = [
    {
        "name": "Ava Martinez",
        "birthday": "1994-03-12",
        "hometown": "San Diego, CA",
        "hobbies": ["Photography", "Hiking", "Cooking"],
        "bio": "Landscape photographer who loves weekend hikes and trying new recipes."
    },
    {
        "name": "Liam O'Connor",
        "birthday": "1989-11-02",
        "hometown": "Dublin, Ireland",
        "hobbies": ["Guitar", "Cycling", "Chess"],
        "bio": "Coffee-loving guitarist and amateur cyclist; enjoys strategy games and storytelling."
    },
    {
        "name": "Sofia Patel",
        "birthday": "1997-06-25",
        "hometown": "Dallas, TX",
        "hobbies": ["Painting", "Yoga", "Travel"],
        "bio": "Painter who practices yoga daily and collects travel postcards."
    },
    {
        "name": "Noah Kim",
        "birthday": "1992-01-09",
        "hometown": "Seattle, WA",
        "hobbies": ["Coding", "Gaming", "Bouldering"],
        "bio": "Full-stack developer into indie games and weekend bouldering sessions."
    },
    {
        "name": "Maya Rossi",
        "birthday": "1995-08-30",
        "hometown": "Florence, Italy",
        "hobbies": ["Cooking", "Singing", "Cycling"],
        "bio": "Chef-in-training who sings at open mics and explores local cycling routes."
    },
    {
        "name": "Ethan Zhang",
        "birthday": "1990-12-14",
        "hometown": "Toronto, Canada",
        "hobbies": ["Basketball", "Birdwatching", "Gardening"],
        "bio": "Data analyst by day; weekend gardener and birdwatching enthusiast."
    },
    {
        "name": "Olivia Brown",
        "birthday": "2000-05-18",
        "hometown": "Austin, TX",
        "hobbies": ["Blogging", "Photography", "Skateboarding"],
        "bio": "Lifestyle blogger capturing city life and urban skate spots."
    },
    {
        "name": "Lucas Fernández",
        "birthday": "1987-09-03",
        "hometown": "Barcelona, Spain",
        "hobbies": ["Soccer", "Cooking", "Travel"],
        "bio": "Amateur chef and soccer fan who loves short city-break adventures."
    },
]

# --- helpers ---

def search_friends(query: str, fields: List[str], hometown: str, hobby_filters: List[str]) -> List[Dict]:
    q = query.strip().lower()
    results: List[Dict] = []
    for f in FRIENDS:
        # hometown filter
        if hometown != "All" and f["hometown"] != hometown:
            continue
        # hobby filters: if provided, require at least one match
        if hobby_filters:
            lowered = [h.lower() for h in f["hobbies"]]
            if not any(h.lower() in lowered for h in hobby_filters):
                continue
        # empty query -> include (after filters above)
        if not q:
            results.append(f)
            continue
        matched = False
        if "Name" in fields and q in f["name"].lower():
            matched = True
        if "Hometown" in fields and q in f["hometown"].lower():
            matched = True
        if "Hobbies" in fields and any(q in h.lower() for h in f["hobbies"]):
            matched = True
        if "Bio" in fields and q in f["bio"].lower():
            matched = True
        if matched:
            results.append(f)
    return results

# --- session state ---
if "selected_friend" not in st.session_state:
    st.session_state.selected_friend = None

# --- layout: three columns ---
left_col, mid_col, right_col = st.columns([1, 2, 2])

# LEFT: friend names (each in its own clickable box)
with left_col:
    st.header("Friends")
    for i, fr in enumerate(FRIENDS):
        if st.button(fr["name"], key=f"left_{i}"):
            st.session_state.selected_friend = fr["name"]

# MIDDLE: search bar + options + results
with mid_col:
    st.header("Search")
    query = st.text_input("Search text", value="", key="query_input")
    search_fields = st.multiselect("Search in", ["Name", "Hometown", "Hobbies", "Bio"], default=["Name", "Hometown"])

    hometown_options = ["All"] + sorted({f["hometown"] for f in FRIENDS})
    hometown_filter = st.selectbox("Hometown filter", hometown_options)

    all_hobbies = sorted({h for f in FRIENDS for h in f["hobbies"]})
    hobby_filter = st.multiselect("Filter by hobby (optional)", all_hobbies, default=[])

    results = search_friends(query, search_fields, hometown_filter, hobby_filter)

    st.markdown(f"**Results — {len(results)}**")
    for idx, r in enumerate(results):
        card = st.container()
        c1, c2 = card.columns([3, 1])
        c1.markdown(f"**{r['name']}**  \n{r['birthday']} · {r['hometown']}")
        if c2.button("View", key=f"view_{idx}"):
            st.session_state.selected_friend = r['name']

# RIGHT: full profile (only one friend shown at a time)
with right_col:
    st.header("Profile")
    if st.session_state.selected_friend:
        friend = next((f for f in FRIENDS if f["name"] == st.session_state.selected_friend), None)
        if friend:
            st.subheader(friend["name"])
            st.write(f"**Birthday:** {friend['birthday']}")
            st.write(f"**Hometown:** {friend['hometown']}")
            st.write("**Hobbies:**")
            for h in friend["hobbies"]:
                st.write(f"- {h}")
            st.write("**Biography:**")
            st.write(friend["bio"])
        else:
            st.info("Selected friend not found.")
    else:
        st.info("Click a name on the left or press 'View' on a search result to show full profile here.")
