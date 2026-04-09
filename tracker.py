import os
import pandas as pd


def load_data(emp_file, att_file):
    employees = pd.read_csv(emp_file)
    attendance = pd.read_csv(att_file)
    attendance["date"] = pd.to_datetime(attendance["date"])
    attendance["status"] = attendance["status"].str.strip()
    merged = attendance.merge(employees, on="employee_id", how="left")
    return employees, attendance, merged


def print_header(title):
    print("\n" + "=" * 62)
    print(f"  {title}")
    print("=" * 62)


def print_section(title):
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print(f"{'─' * 55}")


def overview(df, employees):
    print_header("EMPLOYEE ATTENDANCE TRACKER")
    total_days = df["date"].nunique()
    total_employees = employees.shape[0]
    total_present = (df["status"] == "present").sum()
    total_absent = (df["status"] == "absent").sum()
    total_late = (df["status"] == "late").sum()
    total_records = len(df)
    attendance_rate = (total_present / total_records) * 100

    print(f"  {'Tracking Period':<28} {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"  {'Total Employees':<28} {total_employees}")
    print(f"  {'Working Days Tracked':<28} {total_days}")
    print(f"  {'Overall Attendance Rate':<28} {attendance_rate:.1f}%")
    print(f"  {'Present':<28} {total_present}")
    print(f"  {'Absent':<28} {total_absent}")
    print(f"  {'Late':<28} {total_late}")


def employee_summary(df):
    print_section("EMPLOYEE ATTENDANCE SUMMARY")
    summary = df.groupby(["employee_id", "name", "department"]).apply(
        lambda x: pd.Series({
            "present": (x["status"] == "present").sum(),
            "absent": (x["status"] == "absent").sum(),
            "late": (x["status"] == "late").sum(),
            "total": len(x),
        })
    ).reset_index()
    summary["rate"] = (summary["present"] / summary["total"] * 100).round(1)
    summary = summary.sort_values("rate", ascending=False)

    print(f"  {'Name':<25}{'Dept':<15}{'Present':>8}{'Absent':>8}{'Late':>6}{'Rate':>8}")
    print(f"  {'─'*23:<25}{'─'*13:<15}{'─'*6:>8}{'─'*6:>8}{'─'*4:>6}{'─'*6:>8}")
    for _, row in summary.iterrows():
        flag = " ⚠️" if row["rate"] < 75 else ""
        print(f"  {row['name']:<25}{row['department']:<15}{row['present']:>8}{row['absent']:>8}"
              f"{row['late']:>6}{row['rate']:>7.1f}%{flag}")


def daily_attendance(df):
    print_section("DAILY ATTENDANCE RATE")
    daily = df.groupby("date").apply(
        lambda x: round((x["status"] == "present").sum() / len(x) * 100, 1)
    ).reset_index()
    daily.columns = ["date", "rate"]

    for _, row in daily.iterrows():
        bar_len = int(row["rate"] / 5)
        bar = "█" * bar_len
        flag = " ⚠️ LOW" if row["rate"] < 75 else ""
        print(f"  {row['date'].date()}  {bar:<22} {row['rate']:>5.1f}%{flag}")


def absenteeism_alerts(df):
    print_section("ABSENTEEISM ALERTS")
    absences = df[df["status"] == "absent"].groupby(
        ["employee_id", "name"]
    ).size().reset_index(name="absences")
    alerts = absences[absences["absences"] >= 2]

    if alerts.empty:
        print("  ✅ No employees with excessive absences")
    else:
        print("  Employees with 2+ absences:")
        for _, row in alerts.iterrows():
            print(f"  🔴 {row['name']:<25} Absences: {row['absences']}")


def late_arrivals(df):
    print_section("FREQUENT LATE ARRIVALS")
    late = df[df["status"] == "late"].groupby(
        ["employee_id", "name"]
    ).size().reset_index(name="late_count")
    late = late[late["late_count"] >= 2].sort_values("late_count", ascending=False)

    if late.empty:
        print("  ✅ No employees with frequent late arrivals")
    else:
        for _, row in late.iterrows():
            print(f"  🟡 {row['name']:<25} Late arrivals: {row['late_count']}")


def department_summary(df):
    print_section("ATTENDANCE BY DEPARTMENT")
    dept = df.groupby("department").apply(
        lambda x: round((x["status"] == "present").sum() / len(x) * 100, 1)
    ).reset_index()
    dept.columns = ["department", "attendance_rate"]
    dept = dept.sort_values("attendance_rate", ascending=False)

    for _, row in dept.iterrows():
        bar = "█" * int(row["attendance_rate"] / 5)
        print(f"  {row['department']:<20} {bar:<22} {row['attendance_rate']:>5.1f}%")


def export_report(df, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"\n  📁 Report exported to: {output_file}")


def run_tracker(emp_file="data/employees.csv", att_file="data/attendance.csv",
                output_file="output/attendance_report.csv"):
    employees, attendance, merged = load_data(emp_file, att_file)
    overview(merged, employees)
    employee_summary(merged)
    daily_attendance(merged)
    absenteeism_alerts(merged)
    late_arrivals(merged)
    department_summary(merged)
    punctuality_score(merged)
    export_report(merged, output_file)
    print("\n" + "=" * 62)

def punctuality_score(df):
    print_section("PUNCTUALITY SCORE")
    total_days = df["date"].nunique()
    scores = df.groupby(["employee_id", "name"]).apply(
        lambda x: round(
            ((x["status"] == "present").sum() * 100 +
             (x["status"] == "late").sum() * 50) /
            (total_days * 100) * 100, 1
        )
    ).reset_index()
    scores.columns = ["employee_id", "name", "score"]
    scores = scores.sort_values("score", ascending=False)

    for _, row in scores.iterrows():
        bar = "█" * int(row["score"] / 5)
        status = "🌟" if row["score"] >= 90 else "✅" if row["score"] >= 75 else "⚠️ "
        print(f"  {status} {row['name']:<25} {bar:<22} {row['score']:>5.1f}%")

if __name__ == "__main__":
    run_tracker()
