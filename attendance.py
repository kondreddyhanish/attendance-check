import json
import os
from datetime import datetime

DATA_FILE = "attendance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"subjects": {}, "student_name": "Student"}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def calculate_percentage(attended, total):
    if total == 0:
        return 0
    return round((attended / total) * 100, 2)

def get_status(percentage):
    if percentage >= 75:
        return "✅ Safe"
    elif percentage >= 60:
        return "⚠️ Warning"
    else:
        return "❌ Danger"

def add_subject(data):
    name = input("Enter subject name: ").strip()
    if not name:
        print("Subject name cannot be empty.")
        return
    if name in data["subjects"]:
        print(f"Subject '{name}' already exists.")
        return
    data["subjects"][name] = {"attended": 0, "total": 0, "history": []}
    save_data(data)
    print(f"Subject '{name}' added successfully!")

def mark_attendance(data):
    if not data["subjects"]:
        print("No subjects found. Please add a subject first.")
        return
    print("\nSubjects:")
    subjects = list(data["subjects"].keys())
    for i, s in enumerate(subjects, 1):
        print(f"  {i}. {s}")
    try:
        choice = int(input("Select subject number: ")) - 1
        subject = subjects[choice]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return
    status = input("Mark as (P)resent or (A)bsent: ").strip().upper()
    if status not in ["P", "A"]:
        print("Invalid input. Use P or A.")
        return
    data["subjects"][subject]["total"] += 1
    if status == "P":
        data["subjects"][subject]["attended"] += 1
    data["subjects"][subject]["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "Present" if status == "P" else "Absent"
    })
    save_data(data)
    print(f"Attendance marked as {'Present' if status == 'P' else 'Absent'} for {subject}.")

def view_dashboard(data):
    if not data["subjects"]:
        print("No subjects found.")
        return
    print(f"\n{'='*60}")
    print(f"  📊 ATTENDANCE DASHBOARD — {data['student_name']}")
    print(f"{'='*60}")
    print(f"{'Subject':<20} {'Attended':<10} {'Total':<10} {'%':<10} {'Status'}")
    print(f"{'-'*60}")
    total_attended = 0
    total_classes = 0
    for subject, info in data["subjects"].items():
        pct = calculate_percentage(info["attended"], info["total"])
        status = get_status(pct)
        print(f"{subject:<20} {info['attended']:<10} {info['total']:<10} {pct:<10} {status}")
        total_attended += info["attended"]
        total_classes += info["total"]
    print(f"{'-'*60}")
    overall = calculate_percentage(total_attended, total_classes)
    print(f"{'OVERALL':<20} {total_attended:<10} {total_classes:<10} {overall:<10} {get_status(overall)}")
    print(f"{'='*60}\n")

def classes_needed(data):
    if not data["subjects"]:
        print("No subjects found.")
        return
    print("\n📌 Classes needed to reach 75%:")
    for subject, info in data["subjects"].items():
        attended = info["attended"]
        total = info["total"]
        pct = calculate_percentage(attended, total)
        if pct >= 75:
            print(f"  {subject}: Already at {pct}% ✅")
        else:
            needed = 0
            while calculate_percentage(attended + needed, total + needed) < 75:
                needed += 1
            print(f"  {subject}: Need {needed} more class(es) to reach 75% (currently {pct}%)")

def generate_chart(data):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import numpy as np

        if not data["subjects"]:
            print("No subjects to chart.")
            return

        subjects = list(data["subjects"].keys())
        percentages = [
            calculate_percentage(data["subjects"][s]["attended"], data["subjects"][s]["total"])
            for s in subjects
        ]

        colors = []
        for p in percentages:
            if p >= 75:
                colors.append("#2ecc71")
            elif p >= 60:
                colors.append("#f39c12")
            else:
                colors.append("#e74c3c")

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor("#0f1117")

        # Bar Chart
        ax1 = axes[0]
        ax1.set_facecolor("#1a1d2e")
        bars = ax1.bar(subjects, percentages, color=colors, edgecolor="#2d3250", linewidth=1.5, width=0.5)
        ax1.axhline(y=75, color="#e74c3c", linestyle="--", linewidth=1.5, label="75% Threshold")
        ax1.set_ylim(0, 110)
        ax1.set_title("Attendance by Subject", color="white", fontsize=14, fontweight="bold", pad=15)
        ax1.set_xlabel("Subjects", color="#aaaaaa", fontsize=11)
        ax1.set_ylabel("Attendance %", color="#aaaaaa", fontsize=11)
        ax1.tick_params(colors="white")
        ax1.spines["bottom"].set_color("#2d3250")
        ax1.spines["left"].set_color("#2d3250")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        for bar, pct in zip(bars, percentages):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                     f"{pct}%", ha="center", va="bottom", color="white", fontsize=10, fontweight="bold")
        ax1.legend(facecolor="#1a1d2e", edgecolor="#2d3250", labelcolor="white")
        ax1.set_xticklabels(subjects, rotation=20, ha="right", color="white")

        # Pie Chart — overall breakdown
        ax2 = axes[1]
        ax2.set_facecolor("#1a1d2e")
        total_attended = sum(data["subjects"][s]["attended"] for s in subjects)
        total_classes = sum(data["subjects"][s]["total"] for s in subjects)
        total_absent = total_classes - total_attended
        if total_classes > 0:
            pie_data = [total_attended, total_absent]
            pie_colors = ["#2ecc71", "#e74c3c"]
            wedges, texts, autotexts = ax2.pie(
                pie_data,
                labels=["Present", "Absent"],
                colors=pie_colors,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(edgecolor="#0f1117", linewidth=2)
            )
            for text in texts:
                text.set_color("white")
                text.set_fontsize(12)
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(11)
                autotext.set_fontweight("bold")
        ax2.set_title("Overall Attendance Split", color="white", fontsize=14, fontweight="bold", pad=15)

        plt.suptitle(f"📊 {data['student_name']}'s Attendance Dashboard",
                     color="white", fontsize=16, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig("attendance_chart.png", dpi=150, bbox_inches="tight", facecolor="#0f1117")
        plt.show()
        print("✅ Chart saved as 'attendance_chart.png'")

    except ImportError:
        print("matplotlib not installed. Run: pip install matplotlib")

def set_student_name(data):
    name = input("Enter your name: ").strip()
    if name:
        data["student_name"] = name
        save_data(data)
        print(f"Name set to '{name}'!")

def main():
    data = load_data()
    print(f"\n🎓 Welcome to Student Attendance Tracker!")
    if data["student_name"] == "Student":
        set_student_name(data)

    while True:
        print("\n📋 MENU")
        print("  1. View Dashboard")
        print("  2. Mark Attendance")
        print("  3. Add Subject")
        print("  4. Classes Needed for 75%")
        print("  5. Generate Chart")
        print("  6. Change Student Name")
        print("  7. Exit")
        choice = input("\nChoose option: ").strip()
        if choice == "1":
            view_dashboard(data)
        elif choice == "2":
            mark_attendance(data)
        elif choice == "3":
            add_subject(data)
        elif choice == "4":
            classes_needed(data)
        elif choice == "5":
            generate_chart(data)
        elif choice == "6":
            set_student_name(data)
        elif choice == "7":
            print("👋 Goodbye! Study hard!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
