from pathlib import Path
import streamlit as st
import subprocess

st.title("AfriPulse AI – Africa Startup Digest")

digest_path = Path(__file__).resolve().parent / "outputs" / "weeklyDigest.md"

if digest_path.exists():
    with open(digest_path, "r", encoding="utf-8") as f:
        digest = f.read()
    st.markdown(digest)
else:
    st.warning("No digest found. Please run `python -m src.main.py` first.")

    if st.button("Generate Weekly Digest Now"):
        with st.spinner("Fetching and summarizing latest Africa startup news..."):
            subprocess.run(["python", "src/main.py"])
        st.success("Digest generated! Please reload the dashboard.")
