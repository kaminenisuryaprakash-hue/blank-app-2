import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title="MBBS Attendance Tracker - Roll 48", page_icon="🏥", layout="wide")

st.title("🏥 Clinical Posting Attendance Tracker")
st.subheader("Batch-C (Roll No: 48) | Target Attendance: 80%")
st.markdown("---")

# Official Schedule Date Ranges for Batch-C (Roll Nos 35-51)[span_0](start_span)[span_0](end_span)
schedule = [
    (date(2026, 10, 14), date(2026, 10, 27), "Obstetrics & Gynaecology"),
    (date(2026, 10, 28), date(2026, 11, 10), "Obstetrics & Gynaecology"),
    (date(2026, 11, 11), date(2026, 11, 24), "General Surgery"),
    (date(2026, 11, 25), date(2026, 12, 8), "General Surgery"),
    (date(2026, 12, 9), date(2026, 12, 22), "General Medicine"),
    (date(2026, 12, 23), date(2027, 1, 5), "General Medicine"),
    (date(2027, 1, 6), date(2027, 1, 19), "Orthopaedics"),
    (date(2027, 1, 20), date(2027, 2, 2), "DVL"),
    (date(2027, 2, 3), date(2027, 2, 16), "Psychiatry"),
    (date(2027, 2, 17), date(2027, 3, 2), "Ophthalmology"),
    (date(2027, 3, 3), date(2027, 3, 16), "Ophthalmology"),
    (date(2027, 3, 17), date(2027, 3, 30), "Ophthalmology"),
    (date(2027, 3, 31), date(2027, 4, 13), "Otorhino-laryngology"),
    (date(2027, 4, 14), date(2027, 4, 27), "Otorhino-laryngology"),
    (date(2027, 4, 28), date(2027, 5, 9), "Community Medicine"),
    # Summer vacation: 10-05-2027 to 23-05-2027[span_1](start_span)[span_1](end_span)
    (date(2027, 5, 24), date(2027, 5, 25), "Community Medicine"),
    (date(2027, 5, 26), date(2027, 6, 8), "Community Medicine"),
    (date(2027, 6, 9), date(2027, 6, 22), "Paediatrics"),
    (date(2027, 6, 23), date(2027, 7, 6), "General Surgery"),
]

subjects_list = [
    "Obstetrics & Gynaecology", "General Surgery", "General Medicine",
    "Orthopaedics", "DVL", "Psychiatry", "Ophthalmology",
    "Otorhino-laryngology", "Community Medicine", "Paediatrics"
]

def get_subject_for_date(d):
    if date(2027, 5, 10) <= d <= date(2027, 5, 23):
        return "Summer Vacation (No Posting)"
    for start, end, subj in schedule:
        if start <= d <= end:
            return subj
    return "No Posting Scheduled"

# Calculate total working days (Mon-Fri) per subject[span_2](start_span)[span_2](end_span)
subject_total_days = {subj: 0 for subj in subjects_list}
for start, end, subj in schedule:
    cur = start
    while cur <= end:
        if not (date(2027, 5, 10) <= cur <= date(2027, 5, 23)):
            if cur.weekday() < 5:  # Monday to Friday
                subject_total_days[subj] += 1
        cur += timedelta(days=1)

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = {}

# Sidebar: Daily Marking
st.sidebar.header("📅 Daily Attendance Log")
log_date = st.sidebar.date_input("Select Date", value=date.today())

active_subject = get_subject_for_date(log_date)
st.sidebar.markdown(f"**Mapped Subject:** `{active_subject}`")

if log_date.weekday() >= 5:
    st.sidebar.warning("⚠️ Weekend (Sat/Sun). Clinical postings are Monday to Friday[span_3](start_span)[span_3](end_span)!")
elif active_subject in ["Summer Vacation (No Posting)", "No Posting Scheduled"]:
    st.sidebar.info("No clinical posting on this date.")
else:
    current_status = st.session_state.attendance_logs.get(str(log_date), "Present")
    status_radio = st.sidebar.radio("Mark Status:", ["Present", "Absent"], index=0 if current_status == "Present" else 1)
    
    if st.sidebar.button("Save Record"):
        st.session_state.attendance_logs[str(log_date)] = status_radio
        st.sidebar.success(f"Saved: {log_date} marked as {status_radio}!")

# Main Dashboard
st.markdown("### 📊 Subject-Wise Attendance Overview (Target: 80%)")

absences = {subj: 0 for subj in subjects_list}
for d_str, status in st.session_state.attendance_logs.items():
    d = datetime.strptime(d_str, "%Y-%m-%d").date()
    subj = get_subject_for_date(d)
    if status == "Absent" and subj in absences:
        absences[subj] += 1

for subject in subjects_list:
    total = subject_total_days[subject]
    attended = total - absences[subject]
    percentage = (attended / total) * 100 if total > 0 else 0
    min_required = int(total * 0.8)

    col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
    with col1:
        st.markdown(f"**{subject}**")
    with col2:
        st.text(f"{attended} / {total} Days")
    with col3:
        st.text(f"{percentage:.1f}%")
    with col4:
        if percentage >= 80:
            st.success("Safe ✅")
        else:
            st.error(f"⚠️ Warning! Need {(min_required - attended)} more days.")

st.markdown("---")
st.markdown("### 📝 Attendance History Log")
if st.session_state.attendance_logs:
    for d_str, status in sorted(st.session_state.attendance_logs.items(), reverse=True):
        d = datetime.strptime(d_str, "%Y-%m-%d").date()
        subj = get_subject_for_date(d)
        color = "green" if status == "Present" else "red"
        st.markdown(f"- **{d_str}** ({subj}): :{color}[**{status}**]")
else:
    st.info("No absence records logged yet. All weekdays are counted as Present by default.")
