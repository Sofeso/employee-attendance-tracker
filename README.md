# Employee Attendance Tracker

A Python CLI tool to track employee attendance, flag absences, late arrivals and generate department reports.

## Features
- Overall attendance rate overview
- Per-employee attendance summary with alerts
- Daily attendance rate with visual bars
- Absenteeism alerts for employees with 2+ absences
- Frequent late arrival detection
- Department-level attendance breakdown

## Requirements
- Python 3.x
- pandas

## Installation
\\\ash
pip install pandas
\\\

## Usage
\\\ash
python tracker.py
\\\

## Data Format
**employees.csv**: employee_id, name, department, role
**attendance.csv**: date, employee_id, check_in, check_out, status

## Contributing
1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request
