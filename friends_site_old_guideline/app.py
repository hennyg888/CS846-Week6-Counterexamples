import streamlit as st

st.set_page_config(page_title="Friends — Social Demo", layout="wide")

# ----- Example friends data (name, birthday, hometown, 3 hobbies, short bio <= 30 words) -----
FRIENDS = [
    {
        "name": "Maya Patel",
        "birthday": "1992-05-14",
        "hometown": "Ahmedabad, India",
        "hobbies": ["Hiking", "Photography", "Cooking"],
        "bio": "Outdoor photographer who loves sunrise hikes and spicy food."
    },
    {
        "name": "David Kim",
        "birthday": "1988-11-03",
        "hometown": "Busan, South Korea",
        "hobbies": ["Chess", "Piano", "Coding"],
        "bio": "Software engineer, amateur pianist, and competitive chess player."
    },
    {
        "name": "Aisha Thompson",
        "birthday": "1995-07-22",
        "hometown": "Atlanta, USA",
        "hobbies": ["Running", "Painting", "Blogging"],
        "bio": "Painter and marathon runner documenting city life in color."
    },
    {
        "name": "Luca Rossi",
        "birthday": "1990-01-09",
        "hometown": "Florence, Italy",
        "hobbies": ["Cycling", "Cooking", "Wine tasting"],
        "bio": "Chef-in-training who cycles hills and collects vintage recipes."
    },
    {
        "name": "Chen Wei",
        "birthday": "1993-09-30",
        "hometown": "Taipei, Taiwan",
        "hobbies": ["Drone flying", "Gardening", "Tea ceremonies"],
        "bio": "Gardener and drone hobbyist exploring urban rooftops."
    },
    {
        "name": "Sofia García",
        "birthday": "1997-03-18",
        "hometown": "Seville, Spain",
        "hobbies": ["Flamenco", "Photography", "Hiking"],
        "bio": "Flamenco enthusiast capturing moments on mountain trails."
    }
]

# initialize selection
if "selected" not in st.session_state:
    st.session_state.selected = 0
if "show_right" not in st.session_state:
    st.session_state.show_right = False

st.title("Simple Friends — Social Demo")
st.caption("A minimal Streamlit social-style layout — 3 columns")

# layout: left (friends list), center (details), right (meta / actions)
col1, col2, col3 = st.columns([1, 2, 1])

# LEFT: show each friend as just their name in its own box (clickable)
with col1:
    st.header("Friends")
    for idx, friend in enumerate(FRIENDS):
        # each name shown in its own button (box-like UI)
        if st.button(friend["name"], key=f"friend_{idx}"):
            st.session_state.selected = idx
            st.session_state.show_right = True

# CENTER: search + selected friend's full details
with col2:
    st.header("Profile & Search")

    # --- Search bar and options (top of middle column)
    query = st.text_input("Search friends", key="search_query",
                          placeholder="type name, hometown, hobby, or keyword from bio")
    search_fields = st.multiselect("Search in", ["Name", "Hometown", "Hobbies", "Bio"],
                                   default=["Name", "Hometown"], help="Choose fields to include in the search.")

    # perform search when query provided
    def _matches(friend, q, fields):
        q = q.lower()
        if "Name" in fields and q in friend["name"].lower():
            return True
        if "Hometown" in fields and q in friend["hometown"].lower():
            return True
        if "Hobbies" in fields:
            for h in friend["hobbies"]:
                if q in h.lower():
                    return True
        if "Bio" in fields and q in friend["bio"].lower():
            return True
        return False

    if query and query.strip():
        results = [f for f in FRIENDS if _matches(f, query, search_fields)]
        st.markdown(f"**Search results — {len(results)} match(es)**")

        # show each result reference (name, birthday, hometown) with a View button
        for i, friend in enumerate(results):
            r1, r2, r3, r4 = st.columns([3, 2, 3, 1])
            with r1:
                st.markdown(f"**{friend['name']}**")
            with r2:
                st.write(friend["birthday"])
            with r3:
                st.write(friend["hometown"])
            with r4:
                if st.button("View", key=f"view_search_{i}"):
                    st.session_state.selected = FRIENDS.index(friend)
                    st.session_state.show_right = True
            st.markdown("---")

        if not results:
            st.info("No friends match your search.")

    # --- always show currently selected friend's full details below the results / search
    selected = FRIENDS[st.session_state.selected]
    st.subheader(selected["name"])
    st.write(f"**Birthday:** {selected['birthday']}")
    st.write(f"**Hometown:** {selected['hometown']}")
    st.write("**Hobbies:**")
    st.write(", ".join(selected["hobbies"]))
    st.markdown("---")
    st.write("**About**")
    st.write(selected["bio"])

# RIGHT: show full info for a clicked friend (only one at a time)
with col3:
    if st.session_state.get("show_right", False):
        friend = FRIENDS[st.session_state.selected]
        st.header("Friend details")
        st.subheader(friend["name"])
        st.write(f"**Birthday:** {friend['birthday']}")
        st.write(f"**Hometown:** {friend['hometown']}")
        st.write("**Hobbies:**")
        st.write(", ".join(friend["hobbies"]))
        st.markdown("---")
        st.write("**About**")
        st.write(friend["bio"])
        st.markdown("---")
        st.button("Send message", key="send_msg_right")
        st.button("Follow", key="follow_right")
        if st.button("Close", key="close_profile"):
            st.session_state.show_right = False
    else:
        st.header("Profile")
        st.metric("Friends loaded", len(FRIENDS))
        st.markdown("**Quick actions**")
        st.button("Send message", key="send_msg_default")
        st.button("Follow", key="follow_default")
        st.markdown("---")
        st.caption("Demo generated with Raptor mini (Preview)")

# footer / run instructions inside app (helpful during local dev)
st.markdown("---")
st.caption("Run locally: `pip install -r requirements.txt` then `streamlit run app.py`")
