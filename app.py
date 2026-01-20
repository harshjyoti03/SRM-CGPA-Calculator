import streamlit as st

st.set_page_config(page_title="SRM CGPA Calculator", layout="centered")

st.title("🎓 SRM CGPA Calculator")
st.caption("Semester-wise | Credit-based | SRM grading system")

GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}

num_semesters = st.number_input(
    "Number of Semesters",
    min_value=1,
    max_value=12,
    step=1
)

overall_weighted_sum = 0
overall_credits = 0
has_fail = False

st.divider()

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
                GRADE_POINTS.keys(),
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
        sgpa = sem_weighted_sum / sem_credits
        st.success(f"SGPA (Semester {sem}): **{sgpa:.2f}**")

        overall_weighted_sum += sem_weighted_sum
        overall_credits += sem_credits

    st.divider()

if st.button("📊 Calculate Final CGPA"):
    if overall_credits > 0:
        cgpa = overall_weighted_sum / overall_credits
        st.success(f"🎯 Overall CGPA: **{cgpa:.2f}**")

        if has_fail:
            st.warning("⚠️ One or more subjects have an F grade. CGPA affected due to arrears.")
    else:
        st.error("Please enter valid subjects and credits.")