# ehs_management_system
Environment, Health, and Safety (EHS) Management System built with Streamlit. 

# EHS Management System

*A comprehensive web application for managing environmental health and safety incidents, conducting investigations, performing root cause analyses, and implementing corrective actions.*

---

## Overview

The **EHS (Environment, Health, and Safety) Management System** is a **Streamlit-based web application** designed to help organizations track and manage safety-related incidents, document injuries, analyze environmental impacts, assess risks, and implement corrective actions. This system provides a **user-friendly interface** with comprehensive **reporting and analytics** capabilities.

---

## Features

### Core Modules

1. **Incident Management**

   * Create and document incidents
   * Incident approval workflow
   * Comprehensive incident tracking

2. **Aspect/Impact Analysis**

   * Identify contributing factors
   * Evaluate impacts across multiple domains
   * Document environmental consequences

3. **Injury Documentation**

   * Record employee injury details
   * Document body parts affected
   * Upload injury photos and FIR documents

4. **Investigation**

   * Create and manage investigation records
   * Track investigation progress
   * Link investigations to incidents

5. **Root Cause Analysis**

   * Interactive fishbone diagram generation
   * Internal and external cause categorization
   * Cause and effect visualization

6. **Risk Assessment**

   * Evaluate risks using Severity-Occurrence-Detection (SOD) methodology
   * Automatic risk level calculation
   * Standardized risk evaluation

7. **Corrective/Preventive Actions (CA/PA)**

   * Define and track corrective actions
   * Assign owners and implementers
   * Upload meeting minutes and supporting documents
   * Track due dates and verification methods

8. **Costing**

   * Track incident-related costs
   * Document financial impacts
   * Upload supporting bills and receipts

9. **Closure**

   * Document incident closure
   * Record closure date and comments

10. **Waste Management**

11. **Audit Management**

12. **HAZOP Studies**

13. **Training Records**

14. **Permit Management**

15. **Occupation Health Care**

16. **Carbon Accounting**

17. **Resource Consumption & Conservation**

---

### Additional Functionality

* **Data Visualization**

  * Pie charts for incident distribution
  * Bar charts for severity analysis
  * Line charts for incident trends
  * Cost breakdown analysis

* **File Management**

  * Structured file storage system
  * Support for multiple file formats
  * Organized directories for different document types

* **Admin Functions**

  * User management
  * Data editing capabilities

* **Reporting**

  * Generate comprehensive incident reports
  * Visual analytics and dashboards
  * Incident trends and statistics

---

## System Architecture

### Directory Structure

```
EHS_Management_System/
├── main.py
├── app.py
├── logo1.jpg
├── incident_sheet.xlsx
├── aspect_impact_sheet.xlsx
├── login_data.xlsx
├── requirements.txt
├── uploads/
│   ├── injury_photos/
│   ├── fir_documents/
│   ├── meeting_minutes/
│   ├── cost_bills/
│   └── aspect_images/
```

---

### Data Storage

The system uses **Excel files** for data storage:

* `incident_sheet.xlsx` – Main incident data:

  * `Create` – Incident creation
  * `Approver` – Approval status
  * `Injury` – Injury-related information
  * `Investigation` – Investigation details
  * `RootCause` – Root cause data
  * `CA_PA` – Corrective/Preventive actions
  * `Costing` – Financial impact
  * `Closure` – Closure information

* `aspect_impact_sheet.xlsx` – Aspect/Impact data:

  * `Activity` – Basic incident info
  * `AspectImpact` – Factors and impacts
  * `ScoreCard` – Risk assessment
  * `CAPA` – Corrective actions
  * `Report` – Summaries

* `login_data.xlsx` – Logs user login activity

---

### File Storage

Uploaded files are stored in structured directories:

* `uploads/injury_photos/` – Injury documentation images
* `uploads/fir_documents/` – FIR-related documents
* `uploads/meeting_minutes/` – Meeting files
* `uploads/cost_bills/` – Receipts and bills
* `uploads/aspect_images/` – Aspect/impact evidence

---

## Installation

1. **Install Required Libraries**

   ```bash
   pip install streamlit pandas openpyxl plotly Pillow uuid datetime
   ```

2. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ehs-management-system.git
   cd ehs-management-system
   ```

3. **Run the Application**

   ```bash
   streamlit run main.py
   ```

---

## User Guide

### Login

Use provided credentials:

* **Username:** `mahati`, `nida`, `mariyam`, `siva`, `rohan`
* **Password:** `brainwave`

---

### Navigation

Use the sidebar to access modules:

1. Incident
2. Aspect/Impact
3. Waste
4. Audit
5. HAZOP
6. Training
7. Permit
8. Risk
9. Occupation Health Care
10. Carbon Accounting
11. Consumption in Facility
12. Conservation in Facility

---

## Module Descriptions

### Incident Management

* **Create Incident:** Fill in the "Create" tab
* **Approval:** Go to "Approver" tab > Select > "Check & Approve"
* **Injury Documentation:** Add injury details, upload files
* **Investigation:** Link and manage investigations
* **Root Cause Analysis:** Use fishbone diagram tool
* **CA/PA:** Define actions and assign responsibilities
* **Costing:** Upload bills/receipts for tracking
* **Closure:** Final incident comments and closure date

---

### Aspect/Impact Management

1. **New Assessment**

   * Choose "New Assessment"
   * Fill Activity form
   * Upload photos
   * Click "Save Activity Information"

2. **Complete Assessment**

   * Navigate tabs: Activity, Aspect/Impact, Score Card, CA/PA, Report

3. **Edit Assessment**

   * Select from dropdown
   * Update required fields
   * Save changes via form buttons

---

## Reporting

* View reports by entering incident number
* Analyze through charts and dashboards
* Track incident trends
* Assess cost distribution

---

## Authorization Levels

* **All users:** Can view data
* **Specific users (mahati, siva, rohan):** Can edit data

---

## Technical Details

* Built with **Streamlit**
* Uses **Pandas** for data manipulation
* **Plotly** for interactive charts
* **UUID** for unique ID generation
* File storage with organized structure

---

## Security Features

* Password-based login
* Session management
* Activity logging

---

## Future Enhancements

* Database integration (replace Excel)
* Email notifications (CA/PA updates)
* Mobile app support
* Advanced reporting
* Integration with other EHS systems


