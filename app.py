import streamlit as st
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
import os

st.set_page_config(page_title="SRM CGPA Calculator", layout="centered")

st.title("🎓 SRM CGPA Calculator")
st.caption("Semester-wise | SGPA Graph | PDF Download | SRM grading system")

# SRM grade mapping
GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}

# Number of semesters
num_semesters = st.number_input(
    "Number of Semesters",
    min_value=1,
    max_value=12,
    step=1
)

semester_sgpa = []
has_fail = False
overall_weighted_sum = 0
overall_credits = 0

st.divider()

# ---------------- INPUT SECTION ----------------
for sem in range(1, num_semesters + 1):
    st.subheader(f"📘 Semester {sem}")

    num_subjects = st.number_input(
        f"Number of subjects (Semester {sem})",
        min_value=1,
        max_value=10,
        step=1,
        key=f"subjects_{sem}"
    )

    sem_weighted_sum = 0
    sem_credits = 0

    for sub in range(1, num_subjects + 1):
        col1, col2 = st.columns(2)

        with col1:
            grade = st.selectbox(
                f"Grade (Subject {sub})",
                list(GRADE_POINTS.keys()),
                key=f"grade_{sem}_{sub}"
            )

        with col2:
            credit = st.number_input(
                f"Credits (Subject {sub})",
                min_value=1,
                max_value=10,
                step=1,
                key=f"credit_{sem}_{sub}"
            )

        if grade == "F":
            has_fail = True

        sem_weighted_sum += GRADE_POINTS[grade] * credit
        sem_credits += credit

    if sem_credits > 0:
        sgpa = round(sem_weighted_sum / sem_credits, 2)
        semester_sgpa.append(sgpa)

        st.success(f"SGPA (Semester {sem}): **{sgpa}**")

        overall_weighted_sum += sem_weighted_sum
        overall_credits += sem_credits

    st.divider()

# ---------------- RESULT SECTION ----------------
if st.button("📊 Calculate Final CGPA"):
    if overall_credits == 0:
        st.error("Please enter valid subjects and credits.")
    else:
        cgpa = round(overall_weighted_sum / overall_credits, 2)
        st.success(f"🎯 Overall CGPA: **{cgpa}**")

        if has_fail:
            st.warning("⚠️ One or more subjects have F grade. CGPA affected due to arrears.")

        # ---------- GRAPH: BAR + LINE ----------
        st.subheader("📊 Semester-wise SGPA Analysis")

        semesters = list(range(1, len(semester_sgpa) + 1))

        fig, ax = plt.subplots()
        ax.bar(semesters, semester_sgpa, alpha=0.7, label="SGPA")
        ax.plot(semesters, semester_sgpa, marker='o', linewidth=2, label="Trend")

        ax.set_xlabel("Semester")
        ax.set_ylabel("SGPA")
        ax.set_title("Semester-wise SGPA (Bar + Trend Line)")
        ax.set_xticks(semesters)
        ax.legend()

        st.pyplot(fig)

        # ---------- SAVE GRAPH AS IMAGE ----------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as graph_img:
            fig.savefig(graph_img.name, bbox_inches="tight")
            graph_path = graph_img.name

        plt.close(fig)

        # ---------- PDF DOWNLOAD ----------
        st.subheader("📄 Download Result as PDF")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            c = canvas.Canvas(tmp_pdf.name, pagesize=A4)
            width, height = A4

            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "SRM CGPA Report")

            # Text content
            c.setFont("Helvetica", 12)
            y = height - 100

            for i, sgpa in enumerate(semester_sgpa, start=1):
                c.drawString(50, y, f"Semester {i} SGPA: {sgpa}")
                y -= 18

            y -= 10
            c.drawString(50, y, f"Overall CGPA: {cgpa}")

            if has_fail:
                y -= 20
                c.setFillColorRGB(1, 0, 0)
                c.drawString(50, y, "Warning: F grade detected (arrears present)")
                c.setFillColorRGB(0, 0, 0)

            # ---------- ADD GRAPH TO PDF ----------
            y -= 40
            img_width = width - 100
            img_height = 250

            c.drawImage(
                ImageReader(graph_path),
                50,
                y - img_height,
                width=img_width,
                height=img_height,
                preserveAspectRatio=True
            )

            c.save()

            with open(tmp_pdf.name, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=f,
                    file_name="SRM_CGPA_Report.pdf",
                    mime="application/pdf"
                )

        # Cleanup temp graph file
        os.remove(graph_path)
