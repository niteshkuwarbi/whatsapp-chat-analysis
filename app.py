# app.py  — Cleaned-up, Professional WhatsApp Chat Analyzer

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor
import helper

# ---------- Page & Theme ----------
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
sns.set_theme(style="whitegrid")
sns.set_palette("Blues_r")

# ---------- Custom Styling ----------
st.markdown(
    """
    <style>
      /* Sidebar */
      [data-testid="stSidebar"] {
        background-color: #111827;
      }
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
      [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, 
      [data-testid="stSidebar"] span {
        color: #F9FAFB !important;
      }
      [data-testid="stSidebar"] [data-testid="stFileUploader"] label,
      [data-testid="stSidebar"] [data-testid="stFileUploader"] div,
      [data-testid="stSidebar"] [data-testid="stFileUploader"] span {
        color: #F9FAFB !important;
        font-weight: 500;
      }

      /* Main page background */
      .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: #F9FAFB;
      }

      /* Section cards */
      .section-card {
        background:#ffffff;
        border-left: 6px solid #1E3A8A;
        border-radius:14px; 
        padding:18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      }
      
      /* Metric cards */
      .metric-card {
        background:#ffffff;
        border:1px solid #e6eaf1;
        border-top: 4px solid #3B82F6;
        border-radius:12px; 
        padding:16px; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
      }

      /* Headings */
      h1, h2, h3, h4 {
        color: #1E3A8A;
      }

      /* Captions / notes */
      .caption, .small-note {
        color:#6B7280; 
        font-size:0.92rem;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Sidebar ----------
st.sidebar.header("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload exported chat (.txt)", type=["txt"])

if uploaded_file is None:
    # ---------- Empty State ----------
    st.title("WhatsApp Chat Analyzer")
    st.write(
        "Upload your exported WhatsApp chat text file to explore timelines, activity patterns, "
        "participant activity, word usage, and emoji trends."
    )

    st.markdown("### What you’ll see")
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown(
            "<div class='section-card'><h4>Timelines</h4>"
            "<div class='caption'>Monthly and daily message volumes to understand overall activity trends.</div></div>",
            unsafe_allow_html=True,
        )
    with colB:
        st.markdown(
            "<div class='section-card'><h4>Activity Maps</h4>"
            "<div class='caption'>Most active days/months and an hour-by-hour heatmap for posting habits.</div></div>",
            unsafe_allow_html=True,
        )
    with colC:
        st.markdown(
            "<div class='section-card'><h4>Participants</h4>"
            "<div class='caption'>Most active users with real, count-based statistics and share of messages.</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("### How to get started")
    st.markdown(
        """
        1) In WhatsApp, open a chat → **More** → **Export chat** → **Without media**  
        2) Upload the exported `.txt` file from the sidebar  
        3) Choose **Overall** or a specific participant and click **Analyze**
        """
    )
    st.markdown("<div class='small-note'>Tip: Larger chats may take a few seconds to parse.</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="background:#F3F4F6; border-left:4px solid #1E3A8A; 
                    padding:12px 16px; border-radius:8px; margin-top:15px;">
            <span style="color:#374151; font-size:0.92rem;">
            <strong>Data privacy notice:</strong>  
            Any uploaded chat file is processed entirely within your active session 
            using transient in-memory structures. No persistent storage, database writes, 
            or external transmissions are performed.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    # ---------- Show File Disclaimer in Sidebar ----------
    st.sidebar.markdown(
        f"""
        <div style="background:#1F2937; border-left:4px solid #3B82F6; 
                    padding:10px 12px; border-radius:6px; margin-top:10px;">
            <span style="color:#F9FAFB; font-size:0.9rem;">
            <strong>File uploaded:</strong> {uploaded_file.name}<br>
            The file is processed within this session using transient memory structures. 
            No persistence, caching, or external transmission occurs.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- Parse & Prepare ----------
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    with st.spinner("Parsing chat..."):
        df = preprocessor.preprocess(data)

    # Build user selector
    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Participant", user_list)
    run = st.sidebar.button("Analyze")

    st.title("Chat Overview")

    # ---------- Show File Disclaimer in Main Dashboard ----------
    st.markdown(
        f"""
        <div style="background:#F3F4F6; border-left:4px solid #1E3A8A; 
                    padding:12px 16px; border-radius:8px; margin-bottom:15px;">
            <span style="font-weight:600; color:#1E3A8A;">File in use:</span> {uploaded_file.name}  
            <br>
            <span style="color:#374151; font-size:0.92rem;">
            All uploaded data is confined to the active runtime environment and processed 
            in-memory for statistical computation. No permanent storage, database writes, 
            or external API calls are performed.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not run:
        st.markdown(
            "<div class='small-note'>Select a participant (or keep Overall) and click <strong>Analyze</strong> to generate the dashboard.</div>",
            unsafe_allow_html=True,
        )

    # ---------- Dashboard ----------
    if run:
        # Overview metrics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.subheader("Summary")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown("<div class='metric-card'><h4>Total Messages</h4>", unsafe_allow_html=True)
            st.metric(label="", value=num_messages)
            st.markdown("</div>", unsafe_allow_html=True)
        with m2:
            st.markdown("<div class='metric-card'><h4>Total Words</h4>", unsafe_allow_html=True)
            st.metric(label="", value=words)
            st.markdown("</div>", unsafe_allow_html=True)
        with m3:
            st.markdown("<div class='metric-card'><h4>Media Shared</h4>", unsafe_allow_html=True)
            st.metric(label="", value=num_media_messages)
            st.markdown("</div>", unsafe_allow_html=True)
        with m4:
            st.markdown("<div class='metric-card'><h4>Links Shared</h4>", unsafe_allow_html=True)
            st.metric(label="", value=num_links)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='small-note'>Reasoning: These are direct counts from the parsed chat. "
            "Media items are detected using WhatsApp’s export marker, and links are found via URL extraction.</div>",
            unsafe_allow_html=True,
        )

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Timelines", "Activity Maps", "Participants", "Text Analysis", "Emojis"]
        )

        # ----- Tab 1: Timelines -----
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Monthly timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline["time"], timeline["message"])
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.markdown("#### Daily timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline["only_date"], daily_timeline["message"])
                plt.xticks(rotation=90)
                st.pyplot(fig)

        # ----- Tab 2: Activity Maps -----
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Most active day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                st.pyplot(fig)
            with c2:
                st.markdown("#### Most active month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)
            st.markdown("#### Weekly activity heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

        # ----- Tab 3: Participants -----
        with tab3:
            if selected_user == "Overall":
                st.markdown("#### Most active users")
                x, new_df = helper.most_busy_users(df)
                c1, c2 = st.columns([2, 1])
                with c1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation=90)
                    st.pyplot(fig)
                with c2:
                    st.dataframe(new_df)
            else:
                st.info("Switch participant to ‘Overall’ in the sidebar to view group-level most active users.")

        # ----- Tab 4: Text Analysis -----
        with tab4:
            st.markdown("#### Word cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

            st.markdown("#### Most common words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            ax.invert_yaxis()
            st.pyplot(fig)

        # ----- Tab 5: Emojis -----
        with tab5:
            emoji_df = helper.emoji_helper(selected_user, df)
            c1, c2 = st.columns([1, 1])
            with c1:
                st.dataframe(emoji_df.rename(columns={0: "Emoji", 1: "Count"}))
            with c2:
                if not emoji_df.empty:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                    st.pyplot(fig)

        # ---------- Methodology ----------
        with st.expander("Methodology details"):
            st.markdown(
                """
                - **Parsing:** Messages are split from the exported text using a date–time pattern, then user and message text are extracted.
                - **Statistics:** Totals are simple counts. Links are detected via URL extraction; media uses WhatsApp's export marker.
                - **Timelines & Activity:** Grouped by date parts (year, month, day name, hour window) to reveal trends and habits.
                - **Participants:** Ranking is by message count; share (%) = user messages ÷ total messages × 100.
                - **Text Analysis:** Removes system messages and media placeholders; applies a Hinglish stopword list before counting.
                """
            )
