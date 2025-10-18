import streamlit as st
from src.main import summaries_array, digest_md

# st.write("DEBUG: summaries_array", summaries_array)
# st.write("DEBUG: digest_md", digest_md)

if __name__ == "__main__":
    st.title("AfriPulse AI – Africa Startup Digest")

    if summaries_array:
        for i, article in enumerate(summaries_array, 1):
            st.markdown(f"**{i}. [{article['title']}]({article['url']})**")
            st.write(article['summary'])
    else:
        st.warning("No news found. Please check your API key or run -m src.main first.")
