# 🎓 Student Attendance Tracker

A Python-based CLI app to track, calculate, and visualize student attendance subject-wise — with a full dashboard and charts!

---

## 🚀 Features

- ✅ Add multiple subjects
- 📅 Mark daily attendance (Present/Absent)
- 📊 View attendance dashboard with percentage & status
- ⚠️ Get warned when attendance drops below 75%
- 🔢 Calculate how many classes needed to reach 75%
- 📈 Generate bar + pie charts using matplotlib
- 💾 Data saved locally in JSON (persists between sessions)

---

## 📦 Requirements

- Python 3.7+
- matplotlib

Install dependencies:
```bash
pip install matplotlib
```

---

## ▶️ How to Run

```bash
python attendance.py
```

---

## 🗂️ Project Structure

```
attendance_app/
├── attendance.py        # Main application
├── attendance_data.json # Auto-generated data file
├── attendance_chart.png # Auto-generated chart
└── README.md
```

---

## 📊 Dashboard Preview

```
============================================================
  📊 ATTENDANCE DASHBOARD — Rahul
============================================================
Subject              Attended   Total      %          Status
------------------------------------------------------------
Mathematics          18         22         81.82      ✅ Safe
Physics              14         22         63.64      ⚠️ Warning
Chemistry            10         22         45.45      ❌ Danger
------------------------------------------------------------
OVERALL              42         66         63.64      ⚠️ Warning
============================================================
```

---

## 🧠 Status Legend

| Percentage | Status |
|------------|--------|
| ≥ 75%      | ✅ Safe |
| 60% – 74%  | ⚠️ Warning |
| < 60%      | ❌ Danger |

---

## 🛠️ Future Ideas

- [ ] GUI version using Tkinter
- [ ] Export report as PDF
- [ ] Web version using Flask
- [ ] Timetable integration

---

## 👨‍💻 Author

Built with ❤️ using Python
