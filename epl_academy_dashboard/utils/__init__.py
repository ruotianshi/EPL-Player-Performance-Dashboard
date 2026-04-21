# utils package
import io
import pandas as pd
import streamlit as st


def excel_download_button(df: pd.DataFrame, filename: str = "data.xlsx", label: str = "⬇ Download Excel"):
    """Render a Streamlit download button that exports *df* as an Excel file."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
