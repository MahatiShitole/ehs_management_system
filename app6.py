import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import os
import time
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from datetime import date
import pandas as pd
import streamlit as st
import uuid
from io import BytesIO
from PIL import Image  # pip install pillow
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# Create directories for storing files if they don't exist
BASE_UPLOAD_DIR = "uploads"
INJURY_PHOTOS_DIR = os.path.join(BASE_UPLOAD_DIR, "injury_photos")
FIR_DOCS_DIR = os.path.join(BASE_UPLOAD_DIR, "fir_documents")
MOM_DOCS_DIR = os.path.join(BASE_UPLOAD_DIR, "meeting_minutes")
COST_BILLS_DIR = os.path.join(BASE_UPLOAD_DIR, "cost_bills")

# Create directories if they don't exist
for directory in [BASE_UPLOAD_DIR, INJURY_PHOTOS_DIR, FIR_DOCS_DIR, MOM_DOCS_DIR, COST_BILLS_DIR]:
    os.makedirs(directory, exist_ok=True)


# Set page configuration
st.set_page_config(layout="wide", page_title="EHS Management System")


# Paths for data files
FILE_PATH = "incident_sheet.xlsx"
LOGIN_FILE = "login_data.xlsx"


# Initialize the login data file if it doesn't exist
def initialize_login_file():
    if not os.path.exists(LOGIN_FILE):
        with pd.ExcelWriter(LOGIN_FILE, engine='openpyxl') as writer:
            pd.DataFrame(columns=['Username', 'Login Time']).to_excel(writer, index=False)

# Function to verify login (simple implementation)
def verify_login(username, password):
    # For demonstration, using a simple authentication
    # In production, use a secure authentication method
    valid_users = {
        "mahati": "brainwave",
        "nida": "brainwave",
        "mariyam": "brainwave",
        "siva": "brainwave",
        "rohan": "brainwave"
    }
    
    if username in valid_users and valid_users[username] == password:
        return True
    return False

# Function to log login activity
def log_login(username):
    try:
        df = pd.read_excel(LOGIN_FILE)
    except:
        df = pd.DataFrame(columns=['Username', 'Login Time'])
    
    new_login = pd.DataFrame({
        'Username': [username],
        'Login Time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    df = pd.concat([df, new_login], ignore_index=True)
    df.to_excel(LOGIN_FILE, index=False)

# Initialize files
initialize_login_file()

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# Login Page
if not st.session_state.logged_in:
    
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("EHS Management System")
            st.image("logo1.jpg", width=9000)
            st.subheader("Please Login")
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                login_button = st.form_submit_button("Login")
                
                if login_button:
                    if verify_login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        log_login(username)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")

else:
    # Navigation after login
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.subheader("EHS Management System")
    
    # Navigation buttons
    button_names = [
        "1. Incident", 
        "2. Aspect/Impact", 
        "3. Waste", 
        "4. Audit", 
        "5. HAZOP", 
        "6. Training", 
        "7. Permit", 
        "8. Risk", 
        "9. Occupation Health Care", 
        "10. Carbon Accounting", 
        "11. Consumption in Facility", 
        "12. Conservation in Facility"
    ]
    
    # Create buttons for each option
    for button in button_names:
        button_id = int(button.split(".")[0])
        if st.sidebar.button(button):
            st.session_state.current_page = button_id
            st.rerun()
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_page = None
        st.rerun()
    
    # Display content based on selected page
    if st.session_state.current_page == 1:
        # Your original incident management code starts here
        # Initialize session state variables
        if "incidents" not in st.session_state:
            try:
                df_create = pd.read_excel(FILE_PATH, sheet_name='Create')
                st.session_state.incidents = {
                    row["Incident Number"]: {"status": "Approved"} 
                    for _, row in df_create.iterrows() 
                    if str(row["Incident Number"]) != "nan"
                }
            except:
                st.session_state.incidents = {}

        if "investigation_data" not in st.session_state:
            st.session_state.investigation_data = {}

        if "root_cause_data" not in st.session_state:
            st.session_state.root_cause_data = {}

        def initialize_excel():
            if not os.path.exists(FILE_PATH):
                with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
                    pd.DataFrame().to_excel(writer, sheet_name='Create', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='Approver', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='Injury', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='Investigation', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='RootCause', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='CA_PA', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='Costing', index=False)
                    pd.DataFrame().to_excel(writer, sheet_name='Closure', index=False)

        def generate_fishbone_diagram(cause_type, causes):
            """Generate a fishbone diagram using Plotly"""
            # Create figure
            fig = go.Figure()
            
            # Add main spine (horizontal line)
            fig.add_shape(
                type="line",
                x0=0, y0=0,
                x1=1, y1=0,
                line=dict(color="black", width=3)
            )
            
            # Add incident box at the right
            fig.add_annotation(
                x=1.02, y=0,
                text="Incident",
                showarrow=False,
                font=dict(size=16, color="black"),
                bgcolor="lightblue",
                bordercolor="black",
                borderwidth=2,
                borderpad=6
            )
            
            # Define category positions
            categories = list(causes.keys())
            num_categories = len(categories)
            
            if num_categories > 0:
                spacing = 1.0 / (num_categories + 1)
                
                for i, category in enumerate(categories):
                    pos = (i + 1) * spacing
                    
                    # Add category spine (vertical line)
                    fig.add_shape(
                        type="line",
                        x0=pos, y0=-0.4,
                        x1=pos, y1=0,
                        line=dict(color="black", width=2)
                    )
                    
                    # Add category label
                    fig.add_annotation(
                        x=pos, y=-0.45,
                        text=category,
                        showarrow=False,
                        font=dict(size=14, color="black")
                    )
                    
                    # Add causes for this category
                    cause_list = causes[category]
                    if cause_list:
                        num_causes = len(cause_list)
                        for j, cause in enumerate(cause_list):
                            # Position causes along the category spine
                            cause_y = -0.4 * (j + 1) / (num_causes + 1)
                            
                            # Add cause text
                            fig.add_annotation(
                                x=pos + 0.05, y=cause_y,
                                text=cause,
                                showarrow=False,
                                xanchor="left",
                                font=dict(size=10)
                            )
            
            # Update layout
            fig.update_layout(
                title=f"{cause_type} Root Cause Analysis",
                showlegend=False,
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[-0.1, 1.2]
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[-0.6, 0.6]
                ),
                plot_bgcolor="white",
                height=500
            )
            
            return fig

        initialize_excel()

        st.title("Incident Management System")

        tabs = st.tabs(["Create", "Approver", "Injury", "Investigation", "Root Cause", "CA/PA", "Costing", "Closure", "Report"])

        # Tab 1: Create
        with tabs[0]:
            st.header("Create Incident")
            with st.form("create_form"):
                data = {
                    "Company Name": st.text_input("Company Name"),
                    "Department Name": st.text_input("Department Name"),
                    "Incident Number": st.text_input("Incident Number"),
                    "Incident Location": st.text_input("Incident Location"),
                    "Incident_type": st.selectbox("Incident Type (required)", 
                                                ["Injury", "Near Miss", "Property Damage", 
                                                "Environmental", "Fire", "Security", "Other"]),
                    "No. of Involved Persons": st.number_input("No. of Involved Persons", min_value=0),
                    "Shift (Duty Timings)": st.selectbox("Shift (Duty Timings)", 
                                                        ["", "Morning (6:00 AM - 2:00 PM)", 
                                                        "Afternoon (2:00 PM - 10:00 PM)", 
                                                        "Night (10:00 PM - 6:00 AM)"]),
                    "Description": st.text_area("Description"),
                    "Incident Start Date": st.date_input("Incident Start Date", value=date.today())
                }
                submit = st.form_submit_button("Submit")
                if submit:
                    try:
                        df = pd.read_excel(FILE_PATH, sheet_name='Create')
                    except:
                        df = pd.DataFrame()
                    
                    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                    
                    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name='Create', index=False)
                    
                    # Update session state
                    incident_number = data["Incident Number"]
                    if incident_number:
                        st.session_state.incidents[incident_number] = {"status": "Approved"}
                    
                    st.success("Incident Created Successfully")

        # Tab 2: Approver
        with tabs[1]:
            st.header("Approver")
            try:
                df = pd.read_excel(FILE_PATH, sheet_name='Create')
                if not df.empty:
                    row = st.selectbox("Select Incident to Approve", df.index, key="approver_index_select")
                    edited = st.data_editor(df.loc[[row]], num_rows="dynamic")
                    if st.button("Check & Approve"):
                        df.loc[row] = edited.iloc[0]
                        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            df.to_excel(writer, sheet_name='Create', index=False)
                        st.success("Incident Approved")
                else:
                    st.info("No incidents available for approval.")
            except:
                st.info("No incidents available for approval.")

        # Tab 3: Injury
                
        with tabs[2]:
            st.header("Injury Form")
            with st.form("injury_form"):
                injury_data = {
                    "Emp. Code": st.text_input("Emp. Code", key="injury_emp_code"),
                    "Emp. Name": st.text_input("Emp. Name", key="injury_emp_name"),
                    "Incident Number": st.text_input("Incident Number"),
                    "Injury": st.selectbox("Injury", ["Yes", "No"], key="injury_yesno"),
                    "Injury_status": st.selectbox("Injury Status",
                                        ["None", "Minor", "Major", "Fatal"], key="injury_status"),
                    "Injury Information": st.text_area("Injury Information", key="injury_info_text"),
                    
                    "Investigation": st.text_input("Investigation Status", key="injury_investigation"),
                    "fir_number": st.text_input("FIR Number", key="fir_number"),
                    "fir_date": st.date_input("FIR Date", key="fir_date"),
                    "fir_police_station": st.text_input("Police Station", key="fir_station"),
                    "fir_details": st.text_area("FIR Brief Description", key="fir_details", height=100),
                    "Root Cause": st.text_input("Root Cause", key="injury_root_cause"),
                }
                
                st.subheader("Injured Body Parts")
                body_parts_options = [
                    "Head", "Face", "Eye", "Ear", "Nose", "Mouth", "Neck", "Shoulder", 
                    "Arm", "Elbow", "Wrist", "Hand", "Fingers", "Chest", "Back", "Abdomen", 
                    "Hip", "Leg", "Knee", "Ankle", "Foot", "Toes", "Internal Organs", "Multiple"
                ]
                
                selected_body_parts = st.multiselect("Select Injured Body Parts", 
                                                    body_parts_options,
                                                    default=[], key="body_parts_select")
                
                injury_data["body_parts"] = ", ".join(selected_body_parts) if selected_body_parts else ""
                
                # Add file upload section
                st.subheader("Upload Documents")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Injury Photos**")
                    injury_photos = st.file_uploader("Upload injury photos (if any)", 
                                                    type=["jpg", "jpeg", "png"], 
                                                    accept_multiple_files=True,
                                                    key="injury_photos_upload")
                    
                with col2:
                    st.write("**FIR Document**")
                    fir_doc = st.file_uploader("Upload FIR document (if any)", 
                                            type=["jpg", "jpeg", "png", "pdf"], 
                                            key="fir_doc_upload")
                
                # Single submit button for the form
                if st.form_submit_button("Submit Injury Info"):
                    try:
                        df = pd.read_excel(FILE_PATH, sheet_name='Injury')
                    except:
                        df = pd.DataFrame()
                        
                    # Generate a unique ID for this submission
                    submission_id = str(uuid.uuid4())[:8]
                    injury_data["submission_id"] = submission_id
                    
                    # Save uploaded injury photos
                    injury_photo_paths = []
                    if injury_photos:
                        for i, photo in enumerate(injury_photos):
                            file_ext = os.path.splitext(photo.name)[1]
                            filename = f"{submission_id}_injury_{i}{file_ext}"
                            filepath = os.path.join(INJURY_PHOTOS_DIR, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(photo.getbuffer())
                            
                            injury_photo_paths.append(filepath)
                    
                    injury_data["injury_photos"] = ",".join(injury_photo_paths) if injury_photo_paths else ""
                    
                    # Save uploaded FIR document
                    fir_doc_path = ""
                    if fir_doc:
                        file_ext = os.path.splitext(fir_doc.name)[1]
                        filename = f"{submission_id}_fir{file_ext}"
                        filepath = os.path.join(FIR_DOCS_DIR, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(fir_doc.getbuffer())
                        
                        fir_doc_path = filepath
                    
                    injury_data["fir_doc_path"] = fir_doc_path
                    
                    df = pd.concat([df, pd.DataFrame([injury_data])], ignore_index=True)
                    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name='Injury', index=False)
                    st.success("Injury Data and Documents Saved")

        # Tab 4: Investigation
        with tabs[3]:
            st.header("Investigation")
            
            # Only show approved incidents
            approved_incidents = {k: v for k, v in st.session_state.incidents.items() if v.get("status") == "Approved"}
            
            if not approved_incidents:
                st.info("No approved incidents available for investigation.")
            else:
                selected_incident = st.selectbox("Select Incident", list(approved_incidents.keys()), key="investigation_incident_select")
                
                if selected_incident:
                    # Check if investigation data already exists for this incident
                    if selected_incident in st.session_state.investigation_data:
                        investigation_data = st.session_state.investigation_data[selected_incident]
                    else:
                        # Generate a default investigation ID
                        try:
                            investigation_id = f"{str(selected_incident).split('-')[-1]}"
                        except:
                            investigation_id = f"INV-{selected_incident}"

                        investigation_data = {
                            "investigation_id": investigation_id,
                            "subject": "",
                            "description": "",
                            "start_date": date.today(),
                            "not_applicable": False
                        }
                    
                    # Not Applicable checkbox
                    not_applicable = st.checkbox("Not Applicable", value=investigation_data["not_applicable"], key="investigation_na")
                    
                    if not not_applicable:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            investigation_id = st.text_input("Investigation ID", value=investigation_data["investigation_id"], key="inv_id_input")
                            investigation_subject = st.text_input("Investigation Subject", value=investigation_data["subject"], key="inv_subject_input")
                        
                        with col2:
                            investigation_start_date = st.date_input("Start Date", value=investigation_data["start_date"], key="inv_date_input")
                        
                        investigation_description = st.text_area("Investigation Description", 
                                                                value=investigation_data["description"],
                                                                height=200,
                                                                key="inv_description_input")
                        
                        if st.button("Save Investigation", key="save_investigation_button"):
                            investigation_data = {
                                "investigation_id": investigation_id,
                                "subject": investigation_subject,
                                "description": investigation_description,
                                "start_date": investigation_start_date,
                                "not_applicable": not_applicable
                            }
                            
                            st.session_state.investigation_data[selected_incident] = investigation_data
                            
                            # Save to Excel
                            try:
                                df = pd.read_excel(FILE_PATH, sheet_name='Investigation')
                            except:
                                df = pd.DataFrame()

                            new_row = {
                                "Incident ID": selected_incident,
                                "Investigation ID": investigation_id,
                                "Subject": investigation_subject,
                                "Description": investigation_description,
                                "Start Date": investigation_start_date,
                                "Not Applicable": not_applicable
                            }
                            
                            # Remove old entry if it exists
                            if not df.empty and "Incident ID" in df.columns:
                                df = df[df["Incident ID"] != selected_incident]
                                
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                df.to_excel(writer, sheet_name='Investigation', index=False)
                            
                            st.success("Investigation details saved successfully!")
                    else:
                        investigation_data["not_applicable"] = True
                        st.session_state.investigation_data[selected_incident] = investigation_data
                        st.info("Investigation marked as Not Applicable for this incident.")
                    
                    # View investigation data if applicable
                    if (selected_incident in st.session_state.investigation_data and 
                        not st.session_state.investigation_data[selected_incident]["not_applicable"]):
                        st.subheader("Investigation Details")
                        inv_data = st.session_state.investigation_data[selected_incident]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Investigation ID:** {inv_data['investigation_id']}")
                            st.write(f"**Subject:** {inv_data['subject']}")
                        with col2:
                            st.write(f"**Start Date:** {inv_data['start_date']}")
                        
                        st.write("**Description:**")
                        st.write(inv_data['description'])

        # Tab 5: Root Cause Analysis
        with tabs[4]:
            st.header("Root Cause Analysis")
            
            # Only show incidents with investigation data
            investigated_incidents = {k: v for k, v in st.session_state.incidents.items() 
                                    if k in st.session_state.investigation_data}
            
            if not investigated_incidents:
                st.info("No incidents with investigation data available.")
            else:
                selected_incident = st.selectbox("Select Incident", list(investigated_incidents.keys()), 
                                                key="root_cause_incident_select")
                
                if selected_incident:
                    # Check if root cause data already exists for this incident
                    if selected_incident in st.session_state.root_cause_data:
                        root_cause_data = st.session_state.root_cause_data[selected_incident]
                    else:
                        root_cause_data = {
                            "type": "Internal",
                            "causes": {
                                "People": [],
                                "Process": [],
                                "Equipment": [],
                                "Environment": []
                            }
                        }
                    
                    # Root cause type selection
                    cause_type = st.radio("Root Cause Type", ["Internal", "External"], 
                                        index=0 if root_cause_data["type"] == "Internal" else 1,
                                        key="root_cause_type_radio")
                    
                    st.subheader("Fishbone Diagram Inputs")
                    
                    # Categories based on internal/external type
                    if cause_type == "Internal":
                        categories = ["People", "Process", "Equipment", "Environment"]
                    else:
                        categories = ["External Factors", "Regulatory", "Third-party", "Natural"]
                    
                    # Initialize or update categories in root_cause_data
                    if "causes" not in root_cause_data or set(root_cause_data["causes"].keys()) != set(categories):
                        root_cause_data["causes"] = {category: [] for category in categories}
                    
                    # Input fields for each category
                    for category in categories:
                        st.write(f"**{category} Factors:**")
                        
                        # Display existing causes with delete option
                        if category in root_cause_data["causes"] and root_cause_data["causes"][category]:
                            for i, cause in enumerate(root_cause_data["causes"][category]):
                                col1, col2 = st.columns([5, 1])
                                with col1:
                                    st.text_input(f"{category} Factor {i+1}", 
                                                value=cause, 
                                                key=f"{category}_{i}_{selected_incident}", 
                                                disabled=True)
                                with col2:
                                    if st.button("Delete", key=f"delete_{category}_{i}_{selected_incident}"):
                                        root_cause_data["causes"][category].pop(i)
                                        st.session_state.root_cause_data[selected_incident] = root_cause_data
                                        st.rerun()
                        
                        # Add new cause
                        new_cause = st.text_input(f"Add {category} Factor", key=f"new_{category}_{selected_incident}")
                        if st.button(f"Add to {category}", key=f"add_{category}_{selected_incident}"):
                            if new_cause:
                                if category not in root_cause_data["causes"]:
                                    root_cause_data["causes"][category] = []
                                root_cause_data["causes"][category].append(new_cause)
                                st.session_state.root_cause_data[selected_incident] = root_cause_data
                                st.success(f"Added to {category} factors!")
                                st.rerun()
                    
                    # Generate fishbone diagram if there's data
                    has_causes = False
                    for category_causes in root_cause_data["causes"].values():
                        if category_causes:
                            has_causes = True
                            break
                            
                    if has_causes:
                        st.subheader("Fishbone Analysis Diagram")
                        try:
                            fig = generate_fishbone_diagram(cause_type, root_cause_data["causes"])
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error generating fishbone diagram: {e}")
                    
                    if st.button("Save Root Cause Analysis", key="save_root_cause"):
                        root_cause_data["type"] = cause_type
                        st.session_state.root_cause_data[selected_incident] = root_cause_data
                        
                        # Save to Excel
                        try:
                            df = pd.read_excel(FILE_PATH, sheet_name='RootCause')
                        except:
                            df = pd.DataFrame()
                        
                        # Convert the root cause data to a row format for Excel
                        excel_data = {
                            "Incident ID": selected_incident,
                            "Type": cause_type
                        }
                        
                        # Add all causes as separate columns
                        for category, causes in root_cause_data["causes"].items():
                            for i, cause in enumerate(causes):
                                excel_data[f"{category}_Cause_{i+1}"] = cause
                        
                        # Remove old entry if it exists
                        if not df.empty and "Incident ID" in df.columns:
                            df = df[df["Incident ID"] != selected_incident]
                            
                        df = pd.concat([df, pd.DataFrame([excel_data])], ignore_index=True)
                        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            df.to_excel(writer, sheet_name='RootCause', index=False)
                        
                        st.success("Root cause analysis saved successfully!")

        # Tab 6: CA/PA
                
        with tabs[5]:
            st.header("Corrective / Preventive Action")
            with st.form("capa_form"):
                capa_data = {
                    "Incident Number": st.text_input("Incident Number"),
                    "CA Number": st.text_input("CA Number", value="CA018", key="ca_number"),
                    "Priority": st.selectbox("Priority", ["High", "Medium", "Low"], key="ca_priority"),
                    "Owner ID": st.text_input("Owner ID", key="ca_owner_id"),
                    "Start Date": st.date_input("Start Date", key="ca_start_date"),
                    "End Date": st.date_input("End Date", key="ca_end_date"),
                    "Status": st.selectbox("Status", ["Open", "In Progress", "Closed"], key="ca_status"),
                    "Mail IDs": st.text_input("Mail IDs (Owner, Implementer)", key="ca_email_ids"),
                    "Proposed CA": st.text_area("Proposed CA", key="ca_proposed"),
                    "Implemented CA": st.text_area("Implemented CA", key="ca_implemented"),
                    "Implementer Info": st.text_input("Implementer Info", key="ca_implementer_info"),
                    "Owner Comments": st.text_area("Owner Comments", key="ca_owner_comments"),
                    "Implementer Comments": st.text_area("Implementer Comments", key="ca_implementer_comments")
                }
                
                # Add meeting minutes upload section
                st.subheader("Meeting Documentation")
                mom_doc = st.file_uploader("Upload Minutes of Meeting (if any)", 
                                        type=["jpg", "jpeg", "png", "pdf"], 
                                        accept_multiple_files=True,
                                        key="mom_doc_upload")
                
                # Single submit button for the form
                if st.form_submit_button("Submit CA/PA"):
                    try:
                        df = pd.read_excel(FILE_PATH, sheet_name='CA_PA')
                    except:
                        df = pd.DataFrame()
                    
                    # Generate a unique ID for this submission
                    submission_id = str(uuid.uuid4())[:8]
                    capa_data["submission_id"] = submission_id
                    
                    # Save uploaded meeting minutes
                    mom_doc_paths = []
                    if mom_doc:
                        for i, doc in enumerate(mom_doc):
                            file_ext = os.path.splitext(doc.name)[1]
                            filename = f"{submission_id}_mom_{i}{file_ext}"
                            filepath = os.path.join(MOM_DOCS_DIR, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(doc.getbuffer())
                            
                            mom_doc_paths.append(filepath)
                    
                    capa_data["mom_doc_paths"] = ",".join(mom_doc_paths) if mom_doc_paths else ""
                    
                    df = pd.concat([df, pd.DataFrame([capa_data])], ignore_index=True)
                    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name='CA_PA', index=False)
                    st.success("CA/PA Submitted with Meeting Documentation")

        # Tab 7: Costing
                
        with tabs[6]:
            st.header("Costing")
            with st.form("costing_form"):
                
                fields = [
                    "Medical Bills", "Injury Pay", "Transport", "Compensation", "Man Hours Lost",
                    "Machine Downtime", "Damages", "Implementation Costs", "Miscellaneous"]
                cost_data = {f: st.number_input(f, min_value=0.0, key=f"cost_{f.lower().replace(' ', '_')}") for f in fields}
                total = sum(cost_data.values())
                st.write(f"Total Cost: ₹{total:.2f}")
                cost_data["Total Cost"] = total
                
                # Add bills upload section
                st.subheader("Bills Documentation")
                cost_categories = [
                    "Medical Bills", "Transport Receipts", "Compensation Documents", 
                 "Machine Repair Bills", "Damage Assessment", "Implementation Cost Documents", "Miscellaneous"
                ]

                bill_uploads = {}
                cols = st.columns(2)
                for i, category in enumerate(cost_categories):
                    with cols[i % 2]:
                        bill_uploads[category] = st.file_uploader(
                            f"Upload {category} (if any)", 
                            type=["jpg", "jpeg", "png", "pdf"], 
                            accept_multiple_files=True,
                            key=f"bill_{category.lower().replace(' ', '_')}_upload"
                        )
                
                # Single submit button for the form
                if st.form_submit_button("Save Costing"):
                    try:
                        df = pd.read_excel(FILE_PATH, sheet_name='Costing')
                    except:
                        df = pd.DataFrame()
                    
                    # Generate a unique ID for this submission
                    submission_id = str(uuid.uuid4())[:8]
                    cost_data["submission_id"] = submission_id
                    
                    # Dictionary to store paths for each category
                    bill_doc_paths = {}
                    
                    # Save uploaded bills for each category
                    for category, files in bill_uploads.items():
                        if files:
                            category_paths = []
                            for i, doc in enumerate(files):
                                safe_category = category.lower().replace(' ', '_')
                                file_ext = os.path.splitext(doc.name)[1]
                                filename = f"{submission_id}_{safe_category}_{i}{file_ext}"
                                filepath = os.path.join(COST_BILLS_DIR, filename)
                                
                                with open(filepath, "wb") as f:
                                    f.write(doc.getbuffer())
                                
                                category_paths.append(filepath)
                            
                            bill_doc_paths[category] = ",".join(category_paths)
                    
                    # Add file paths to cost data
                    for category, paths in bill_doc_paths.items():
                        cost_data[f"{category}_docs"] = paths
                    
                    df = pd.concat([df, pd.DataFrame([cost_data])], ignore_index=True)
                    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name='Costing', index=False)
                    st.success("Costing Saved with Supporting Documents")

        # Tab 8: Closure
        with tabs[7]:
            st.header("Closure")
            with st.form("closure_form"):
                closure_data = {
                    "Closure Date": st.date_input("Closure Date", key="closure_date"),
                    "Comments": st.text_area("Comments", key="closure_comments")
                }
                if st.form_submit_button("Submit Closure"):
                    try:
                        df = pd.read_excel(FILE_PATH, sheet_name='Closure')
                    except:
                        df = pd.DataFrame()
                        
                    df = pd.concat([df, pd.DataFrame([closure_data])], ignore_index=True)
                    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name='Closure', index=False)
                    st.success("Closure Submitted")

        # Tab 9: Report
        # Tab 9: Report
        with tabs[8]:
            st.header("Incident Report")
            
            # Individual incident report section
            st.subheader("Individual Incident Report")
            incident_id = st.text_input("Enter Incident Number to Generate Report", key="report_incident_id")
            if incident_id:
                st.subheader("Create")
                try:
                    df_create = pd.read_excel(FILE_PATH, sheet_name='Create')
                    filtered_create = df_create[df_create['Incident Number'] == incident_id]
                    if not filtered_create.empty:
                        st.dataframe(filtered_create)
                    else:
                        st.warning("No matching Create data found")
                except Exception as e:
                    st.warning("No Create data found")

                st.subheader("Injury")
                try:
                    df_injury = pd.read_excel(FILE_PATH, sheet_name='Injury')
                    filtered_injury = df_injury[df_injury['Incident Number'] == incident_id]
                    if not filtered_injury.empty:
                        st.dataframe(filtered_injury)
                    else:
                        st.warning("No matching Injury data found")
                except Exception as e:
                    st.warning("No Injury data found")

                st.subheader("Investigation")
                try:
                    df_investigation = pd.read_excel(FILE_PATH, sheet_name='Investigation')
                    filtered_investigation = df_investigation[
                        (df_investigation['Investigation ID'].astype(str).str.contains(incident_id, na=False)) |
                        (df_investigation['Incident ID'].astype(str) == incident_id)
                    ]
                    if not filtered_investigation.empty:
                        st.dataframe(filtered_investigation)
                    else:
                        st.warning("No matching Investigation data found")
                except Exception as e:
                    st.warning("No Investigation data found")
                    
                st.subheader("Root Cause")
                try:
                    df_root_cause = pd.read_excel(FILE_PATH, sheet_name='RootCause')
                    filtered_root_cause = df_root_cause[df_root_cause['Incident ID'].astype(str) == incident_id]
                    if not filtered_root_cause.empty:
                        st.dataframe(filtered_root_cause)
                    else:
                        st.warning("No matching Root Cause data found")
                except Exception as e:
                    st.warning("No Root Cause data found")

                st.subheader("CA/PA")
                try:
                    df_capa = pd.read_excel(FILE_PATH, sheet_name='CA_PA')
                    filtered_capa = df_capa[df_capa['Incident Number'] == incident_id]
                    if not filtered_capa.empty:
                        st.dataframe(filtered_capa)
                    else:
                        st.warning("No matching CA/PA data found")
                except Exception as e:
                    st.warning("No CA/PA data found")

                st.subheader("Costing")
                try:
                    df_cost = pd.read_excel(FILE_PATH, sheet_name='Costing')
                    st.dataframe(df_cost)
                except Exception as e:
                    st.warning("No Costing data found")

                st.subheader("Closure")
                try:
                    df_close = pd.read_excel(FILE_PATH, sheet_name='Closure')
                    st.dataframe(df_close)
                except Exception as e:
                    st.warning("No Closure data found")
            
            

                
                if incident_id:
                    st.subheader("Edit Incident Details")
                    
                    # Define list of roles authorized to edit
                    authorized_editors = ["mahati", "siva", "rohan"]  # Add all authorized usernames
                    
                    if st.session_state.username in authorized_editors:
                        edit_section = st.selectbox(
                            "Select section to edit:", 
                            ["None", "Create", "Injury", "Investigation", "RootCause", "CA_PA", "Costing", "Closure"]
                        )
                        
                        if edit_section != "None":
                            try:
                                df_to_edit = pd.read_excel(FILE_PATH, sheet_name=edit_section)
                                
                                # Filter data based on incident ID
                                if edit_section == "Create" or edit_section == "Injury" or edit_section == "CA_PA":
                                    filtered_df = df_to_edit[df_to_edit['Incident Number'] == incident_id]
                                elif edit_section == "Investigation" or edit_section == "RootCause":
                                    filtered_df = df_to_edit[df_to_edit['Incident ID'] == incident_id]
                                else:
                                    filtered_df = df_to_edit  # For Costing and Closure which might not have direct ID links
                                
                                if not filtered_df.empty:
                                    st.write(f"Editing {edit_section} data for incident {incident_id}")
                                    
                                    # Use data editor to allow in-place editing
                                    edited_df = st.data_editor(filtered_df, key=f"edit_{edit_section}")
                                    
                                    if st.button(f"Save {edit_section} Changes"):
                                        # Update the main dataframe with edited values
                                        if edit_section == "Create" or edit_section == "Injury" or edit_section == "CA_PA":
                                            df_to_edit.loc[df_to_edit['Incident Number'] == incident_id] = edited_df
                                        elif edit_section == "Investigation" or edit_section == "RootCause":
                                            df_to_edit.loc[df_to_edit['Incident ID'] == incident_id] = edited_df
                                        else:
                                            # For sheets without direct ID linking, replace the entire content
                                            # This is simplified - in a real app, you might want more specific updating
                                            df_to_edit = edited_df
                                        
                                        # Save back to Excel
                                        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                            df_to_edit.to_excel(writer, sheet_name=edit_section, index=False)
                                        
                                        st.success(f"{edit_section} data updated successfully!")
                                        st.rerun()
                                else:
                                    st.warning(f"No {edit_section} data found for this incident ID.")
                            except Exception as e:
                                st.error(f"Error editing data: {e}")
                    else:
                        st.warning("You do not have permission to edit incident details. Please contact an administrator.")



            # Data Visualization Section
            st.header("Data Visualizations")

            # Load data for visualizations
            try:
                df_create = pd.read_excel(FILE_PATH, sheet_name='Create')
                df_injury = pd.read_excel(FILE_PATH, sheet_name='Injury')
                df_cost = pd.read_excel(FILE_PATH, sheet_name='Costing')
                
                # Convert incident date to datetime if available
                if not df_create.empty and 'Incident Start Date' in df_create.columns:
                    df_create['Incident Start Date'] = pd.to_datetime(df_create['Incident Start Date'], errors='coerce')
                    # Filter out rows with invalid dates
                    df_create = df_create.dropna(subset=['Incident Start Date'])
                
                # Create visualizations
                col1, col2 = st.columns(2)
                
                # 1. Total Incidents by Type (Pie Chart)
                with col1:
                    st.subheader("Total Incidents by Type")
                    if not df_create.empty and 'Incident_type' in df_create.columns and df_create['Incident_type'].notna().any():
                        incident_counts = df_create['Incident_type'].value_counts()
                        
                        fig = go.Figure(data=[go.Pie(
                            labels=incident_counts.index,
                            values=incident_counts.values,
                            hole=.3,
                            marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
                        )])
                        
                        fig.update_layout(
                            title="Incident Distribution by Type",
                            height=400,
                            margin=dict(l=10, r=10, t=50, b=10)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No incident type data available")
                
                # 2. Incidents by Severity (Bar Chart)
                with col2:
                    st.subheader("Incidents by Severity")
                    if not df_injury.empty and 'Injury_status' in df_injury.columns and df_injury['Injury_status'].notna().any():
                        # Order severity categories
                        severity_order = ["None", "Minor", "Major", "Fatal"]
                        severity_counts = df_injury['Injury_status'].value_counts().reindex(severity_order, fill_value=0)
                        
                        colors = {
                            'None': '#2ca02c',    # Green
                            'Minor': '#ffbb78',   # Light orange
                            'Major': '#ff7f0e',   # Orange
                            'Fatal': '#d62728'    # Red
                        }
                        
                        bar_colors = [colors.get(severity, '#1f77b4') for severity in severity_counts.index]
                        
                        fig = go.Figure(data=[go.Bar(
                            x=severity_counts.index,
                            y=severity_counts.values,
                            marker_color=bar_colors
                        )])
                        
                        fig.update_layout(
                            title="Incident Severity Distribution",
                            xaxis_title="Severity Level",
                            yaxis_title="Number of Incidents",
                            height=400,
                            margin=dict(l=10, r=10, t=50, b=10)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No severity data available")
                
                # 3. Incident Trends Over Time (Line Chart)
                st.subheader("Incident Trends Over Time")
                if not df_create.empty and 'Incident Start Date' in df_create.columns and df_create['Incident Start Date'].notna().any():
                    try:
                        # Group incidents by month
                        df_create['Month'] = df_create['Incident Start Date'].dt.to_period('M')
                        monthly_incidents = df_create.groupby('Month').size().reset_index(name='Count')
                        monthly_incidents['Month'] = monthly_incidents['Month'].astype(str)
                        
                        # Sort by date to ensure correct timeline
                        monthly_incidents = monthly_incidents.sort_values('Month')
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=monthly_incidents['Month'],
                            y=monthly_incidents['Count'],
                            mode='lines+markers',
                            name='Incidents',
                            line=dict(color='#1f77b4', width=3),
                            marker=dict(size=8)
                        ))
                        
                        fig.update_layout(
                            title="Monthly Incident Trends",
                            xaxis_title="Month",
                            yaxis_title="Number of Incidents",
                            height=400,
                            margin=dict(l=10, r=10, t=50, b=10)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error generating time trend chart: {str(e)}")
                        st.info("Please check that incident dates are in the correct format")
                else:
                    st.info("No incident date data available for trend analysis")
                
                # 4. Cost Breakdown (Horizontal Bar Chart)
                st.subheader("Cost Breakdown Analysis")
                if not df_cost.empty:
                    try:
                        # Select cost columns (excluding non-numeric columns)
                        numeric_cols = df_cost.select_dtypes(include=['int64', 'float64']).columns
                        cost_columns = [col for col in numeric_cols if col != 'Total Cost' and not col.endswith('_docs') 
                                    and not col.endswith('_id') and 'submission' not in col.lower()]
                        
                        if cost_columns:  # Check if we have any valid cost columns
                            # Calculate total for each cost category
                            cost_totals = df_cost[cost_columns].sum().sort_values(ascending=True)
                            
                            # Only proceed if we have valid cost data
                            if not cost_totals.empty and cost_totals.sum() > 0:
                                fig = go.Figure()
                                
                                fig.add_trace(go.Bar(
                                    y=cost_totals.index,
                                    x=cost_totals.values,
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(50, 171, 96, 0.6)',
                                        line=dict(color='rgba(50, 171, 96, 1.0)', width=1)
                                    )
                                ))
                                
                                fig.update_layout(
                                    title="Cost Breakdown by Category",
                                    xaxis_title="Amount (₹)",
                                    yaxis_title="Cost Category",
                                    height=500,
                                    margin=dict(l=10, r=10, t=50, b=10)
                                )
                                
                                # Format x-axis to show currency
                                fig.update_xaxes(tickprefix="₹")
                                
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No cost data available (all values are zero)")
                        else:
                            st.info("No numeric cost columns identified for analysis")
                    except Exception as e:
                        st.error(f"Error in cost analysis: {str(e)}")
                        st.info("Please ensure cost data is properly formatted")
                else:
                    st.info("No cost data available for analysis")
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.info("Please ensure the Excel file exists and contains the required sheets: Create, Injury, and Costing")

        # Add this code inside the section where you handle the aspects/impacts page
# This should be under the condition: if st.session_state.current_page == 2:






























# Then add this function after initialize_aspect_impact_excel()
def save_uploaded_images(files, assessment_number):
    """Save uploaded images to the aspect_images folder with assessment number prefix"""
    if not files:
        return []
    
    # Create directory if it doesn't exist
    image_dir = "aspect_images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    saved_files = []
    for i, file in enumerate(files):
        # Create filename with assessment number, date and index
        today = date.today().strftime("%Y%m%d")
        filename = f"{assessment_number}_{today}_{i+1}.{file.name.split('.')[-1]}"
        file_path = os.path.join(image_dir, filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_files.append(file_path)
    
    return saved_files


if 'current_page' not in st.session_state:
    st.session_state.current_page = 2

if st.session_state.current_page == 2:
    # Aspect/Impact Management Section
    st.title("Aspect/Impact Management System")
    
    # Set file path for the aspect/impact sheet
    ASPECT_IMPACT_FILE = "aspect_impact_sheet.xlsx"
    
    # Initialize Excel file if it doesn't exist
    def initialize_aspect_impact_excel():
        if not os.path.exists(ASPECT_IMPACT_FILE):
            with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl') as writer:
                pd.DataFrame().to_excel(writer, sheet_name='Activity', index=False)
                pd.DataFrame().to_excel(writer, sheet_name='AspectImpact', index=False)
                pd.DataFrame().to_excel(writer, sheet_name='ScoreCard', index=False)
                pd.DataFrame().to_excel(writer, sheet_name='CAPA', index=False)
                pd.DataFrame().to_excel(writer, sheet_name='Report', index=False)
    
    initialize_aspect_impact_excel()
    
    # Function to load existing assessments
    def load_assessments():
        try:
            df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Activity')
            return df
        except Exception as e:
            return pd.DataFrame()
    
    # Create tabs for the Aspect/Impact section
    aspect_tabs = st.tabs(["Activity", "Aspect/Impact", "Score Card", "CA/PA", "Report"])
    
    # Initialize session state for current assessment if not exist
    if "current_assessment_id" not in st.session_state:
        st.session_state.current_assessment_id = None
        
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
        
    # Top section for assessment selection or creation
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Load existing assessments for selection
        existing_assessments = load_assessments()
        if not existing_assessments.empty and 'Aspect/Impact Assessment Number' in existing_assessments.columns:
            assessment_options = ["New Assessment"] + existing_assessments['Aspect/Impact Assessment Number'].dropna().unique().tolist()
            selected_assessment = st.selectbox("Select Assessment", options=assessment_options)
            
            if selected_assessment != "New Assessment":
                st.session_state.current_assessment_id = selected_assessment
                st.session_state.edit_mode = True
            else:
                st.session_state.current_assessment_id = None
                st.session_state.edit_mode = False
        else:
            st.write("No existing assessments found. Create a new one.")
            st.session_state.current_assessment_id = None
            st.session_state.edit_mode = False

    
    # Tab 1: Activity
    with aspect_tabs[0]:
        st.header("Activity")
        
        # Load existing data if in edit mode
        activity_data = {}
        if st.session_state.edit_mode and st.session_state.current_assessment_id:
            try:
                df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Activity')
                filtered_df = df[df['Aspect/Impact Assessment Number'] == st.session_state.current_assessment_id]
                if not filtered_df.empty:
                    activity_data = filtered_df.iloc[0].to_dict()
            except Exception as e:
                st.error(f"Error loading assessment data: {e}")
        
        with st.form("activity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name", 
                                            value=activity_data.get('Company Name', ''))
                
                incident_number = st.text_input("Incident Number", 
                                                value=activity_data.get('Incident Number', ''))
                
                incident_type_options = ["Injury", "Near Miss", "Property Damage", 
                                        "Environmental", "Fire", "Security", "Other"]
                incident_type_default = 0
                if 'Incident Type' in activity_data and activity_data['Incident Type'] in incident_type_options:
                    incident_type_default = incident_type_options.index(activity_data['Incident Type'])
                
                incident_type = st.selectbox("Incident Type", incident_type_options, index=incident_type_default)
                
                # Handle date conversion safely
                if 'Incident Date' in activity_data and activity_data['Incident Date'] is not None:
                    try:
                        incident_date_val = pd.to_datetime(activity_data['Incident Date']).date()
                    except:
                        incident_date_val = date.today()
                else:
                    incident_date_val = date.today()
                
                incident_date = st.date_input("Incident Date", value=incident_date_val)
            
            with col2:
                incident_location = st.text_input("Incident Location", 
                                                 value=activity_data.get('Incident Location', ''))
                
                reported_by_name = st.text_input("Reported By (Name)", 
                                                value=activity_data.get('Reported By Name', ''))
                
                reported_by_id = st.text_input("Reported By (ID)", 
                                              value=activity_data.get('Reported By ID', ''))
                
                reported_by_dept = st.text_input("Reported By (Department)", 
                                                value=activity_data.get('Reported By Department', ''))
            
            incident_description = st.text_area("Incident Description", 
                                               value=activity_data.get('Incident Description', ''),
                                               height=150)
            
            # File uploader for evidence photos
            st.write("Attach Evidence Photos (if any)")
            evidence_photos = st.file_uploader("Upload evidence photos", 
                                              type=["jpg", "jpeg", "png"], 
                                              accept_multiple_files=True)
            
            # Assessment Number - Auto-generate if new, or use existing
            if not st.session_state.edit_mode:
                # Auto-generate a new assessment number
                try:
                    df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Activity')
                    if 'Aspect/Impact Assessment Number' in df.columns and not df.empty:
                        existing_numbers = df['Aspect/Impact Assessment Number'].astype(str).dropna()
                        highest_num = 0
                        for num_str in existing_numbers:
                            try:
                                if num_str.startswith('AI-'):
                                    num = int(num_str.split('-')[1])
                                    highest_num = max(highest_num, num)
                            except:
                                pass
                        assessment_number = f"AI-{highest_num + 1:03d}"
                    else:
                        assessment_number = "AI-001"
                except:
                    assessment_number = "AI-001"
            else:
                assessment_number = st.session_state.current_assessment_id
            
            st.write(f"**Aspect/Impact Assessment Number:** {assessment_number}")
            
            submit_activity = st.form_submit_button("Save Activity Information")
            
            if submit_activity:
                # Save uploaded images
                saved_image_paths = save_uploaded_images(evidence_photos, assessment_number)
                
                # Prepare data for saving
                data = {
                    "Company Name": company_name,
                    "Incident Number": incident_number,
                    "Incident Type": incident_type,
                    "Incident Date": incident_date,
                    "Incident Description": incident_description,
                    "Incident Location": incident_location,
                    "Reported By Name": reported_by_name,
                    "Reported By ID": reported_by_id,
                    "Reported By Department": reported_by_dept,
                    "Aspect/Impact Assessment Number": assessment_number,
                    "Evidence Photos": len(saved_image_paths),  # Store count of photos
                    "Evidence Photo Paths": ",".join(saved_image_paths) if saved_image_paths else ""  # Store image paths
                }
                
                try:
                    # Read existing data or create new DataFrame if file doesn't exist
                    try:
                        df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Activity')
                    except:
                        df = pd.DataFrame()
                    
                    if st.session_state.edit_mode:
                        # Update existing record
                        if not df.empty and 'Aspect/Impact Assessment Number' in df.columns:
                            df = df[df['Aspect/Impact Assessment Number'] != assessment_number]
                    
                    # Add new record
                    new_df = pd.DataFrame([data])
                    df = pd.concat([df, new_df], ignore_index=True)
                    
                    # Save to Excel - Fixed the Excel writer mode
                    with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl', mode='w') as writer:
                        # Load other sheets first
                        sheets_to_keep = ['AspectImpact', 'ScoreCard', 'CAPA', 'Report']
                        sheet_data = {}
                        for sheet in sheets_to_keep:
                            try:
                                sheet_data[sheet] = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name=sheet)
                            except:
                                sheet_data[sheet] = pd.DataFrame()
                                
                        # Write all sheets back
                        df.to_excel(writer, sheet_name='Activity', index=False)
                        for sheet_name, sheet_df in sheet_data.items():
                            sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    st.success(f"Activity information saved with Assessment Number: {assessment_number}")
                    # Update session state with the current assessment ID
                    st.session_state.current_assessment_id = assessment_number
                    st.session_state.edit_mode = True
                    
                except Exception as e:
                    st.error(f"Error saving data: {e}")
    
    # Tab 2: Aspect/Impact
    with aspect_tabs[1]:
        st.header("Aspect/Impact Analysis")
        
        if not st.session_state.current_assessment_id:
            st.warning("Please save Activity information first before proceeding to Aspect/Impact analysis.")
        else:
            # Load existing data if in edit mode
            aspect_impact_data = {}
            if st.session_state.edit_mode:
                try:
                    df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='AspectImpact')
                    filtered_df = df[df['Assessment Number'] == st.session_state.current_assessment_id]
                    if not filtered_df.empty:
                        aspect_impact_data = filtered_df.iloc[0].to_dict()
                except Exception as e:
                    pass
            
            with st.form("aspect_impact_form"):
                st.subheader("Identification of Relevant Aspects")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    human_factors = st.text_area("Human Factors", 
                                               placeholder="E.g., lapse in attention, fatigue",
                                               value=aspect_impact_data.get('Human Factors', ''),
                                               height=100)
                    
                    equipment_factors = st.text_area("Equipment/Material Factors", 
                                                   placeholder="E.g., mechanical breakdown, faulty components",
                                                   value=aspect_impact_data.get('Equipment Factors', ''),
                                                   height=100)
                    
                    procedural_factors = st.text_area("Procedural Factors", 
                                                    placeholder="E.g., deviation from standard operating procedures",
                                                    value=aspect_impact_data.get('Procedural Factors', ''),
                                                    height=100)
                
                with col2:
                    environmental_factors = st.text_area("Environmental Factors", 
                                                      placeholder="E.g., weather conditions, physical environment",
                                                      value=aspect_impact_data.get('Environmental Factors', ''),
                                                      height=100)
                    
                    organizational_factors = st.text_area("Organizational Factors", 
                                                       placeholder="E.g., inadequate supervision, resource shortage",
                                                       value=aspect_impact_data.get('Organizational Factors', ''),
                                                       height=100)
                    
                    external_factors = st.text_area("External Factors", 
                                                  placeholder="E.g., contractor or vendor failures",
                                                  value=aspect_impact_data.get('External Factors', ''),
                                                  height=100)
                
                st.subheader("Impact Evaluation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    safety_impact = st.text_area("Safety", 
                                               placeholder="E.g., Injuries, near misses, fatalities",
                                               value=aspect_impact_data.get('Safety Impact', ''),
                                               height=100)
                    
                    environment_impact = st.text_area("Environment", 
                                                    placeholder="E.g., Pollution, hazardous material release",
                                                    value=aspect_impact_data.get('Environment Impact', ''),
                                                    height=100)
                    
                    operations_impact = st.text_area("Operations", 
                                                   placeholder="E.g., Process disruptions, downtime",
                                                   value=aspect_impact_data.get('Operations Impact', ''),
                                                   height=100)
                
                with col2:
                    financial_impact = st.text_area("Financial", 
                                                  placeholder="E.g., Direct and indirect costs",
                                                  value=aspect_impact_data.get('Financial Impact', ''),
                                                  height=100)
                    
                    reputation_impact = st.text_area("Reputation", 
                                                   placeholder="E.g., Public image, stakeholder trust",
                                                   value=aspect_impact_data.get('Reputation Impact', ''),
                                                   height=100)
                    
                    legal_impact = st.text_area("Legal/Compliance", 
                                              placeholder="E.g., Breach of regulations, penalties",
                                              value=aspect_impact_data.get('Legal Impact', ''),
                                              height=100)
                
                submit_aspect_impact = st.form_submit_button("Save Aspect/Impact Analysis")
                
                if submit_aspect_impact:
                    # Prepare data for saving
                    data = {
                        "Assessment Number": st.session_state.current_assessment_id,
                        "Human Factors": human_factors,
                        "Equipment Factors": equipment_factors,
                        "Procedural Factors": procedural_factors,
                        "Environmental Factors": environmental_factors,
                        "Organizational Factors": organizational_factors,
                        "External Factors": external_factors,
                        "Safety Impact": safety_impact,
                        "Environment Impact": environment_impact,
                        "Operations Impact": operations_impact,
                        "Financial Impact": financial_impact,
                        "Reputation Impact": reputation_impact,
                        "Legal Impact": legal_impact
                    }
                    
                    try:
                        # Load existing data from all sheets
                        sheets_data = {}
                        sheets_to_save = ['Activity', 'AspectImpact', 'ScoreCard', 'CAPA', 'Report']
                        
                        for sheet in sheets_to_save:
                            try:
                                sheets_data[sheet] = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name=sheet)
                            except:
                                sheets_data[sheet] = pd.DataFrame()
                        
                        # Update AspectImpact sheet
                        if not sheets_data['AspectImpact'].empty and 'Assessment Number' in sheets_data['AspectImpact'].columns:
                            sheets_data['AspectImpact'] = sheets_data['AspectImpact'][sheets_data['AspectImpact']['Assessment Number'] != st.session_state.current_assessment_id]
                        
                        # Add new record
                        new_df = pd.DataFrame([data])
                        sheets_data['AspectImpact'] = pd.concat([sheets_data['AspectImpact'], new_df], ignore_index=True)
                        
                        # Save all sheets back to Excel
                        with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl', mode='w') as writer:
                            for sheet_name, sheet_df in sheets_data.items():
                                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        st.success("Aspect/Impact analysis saved successfully!")
                        
                    except Exception as e:
                        st.error(f"Error saving data: {e}")
    
    # Tab 3: Score Card
    with aspect_tabs[2]:
        st.header("Score Card")
        
        if not st.session_state.current_assessment_id:
            st.warning("Please save Activity information first before proceeding to Score Card.")
        else:
            # Load existing data if in edit mode
            score_card_data = {}
            if st.session_state.edit_mode:
                try:
                    df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='ScoreCard')
                    filtered_df = df[df['Assessment Number'] == st.session_state.current_assessment_id]
                    if not filtered_df.empty:
                        score_card_data = filtered_df.iloc[0].to_dict()
                except Exception as e:
                    pass
            
            with st.form("score_card_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Handle NaN values in severity
                    severity_value = 1
                    if 'Severity' in score_card_data and score_card_data['Severity'] is not None:
                        try:
                            if not pd.isna(score_card_data['Severity']):
                                severity_value = int(score_card_data['Severity'])
                        except:
                            pass
                            
                    severity = st.number_input("Severity (S)",
                                              min_value=1, max_value=10, value=severity_value)
                    
                    st.write("**Severity Rating Guide:**")
                    st.write("1-2: Minimal impact")
                    st.write("3-4: Minor impact")
                    st.write("5-6: Moderate impact")
                    st.write("7-8: Major impact")
                    st.write("9-10: Catastrophic impact")
                
                with col2:
                    # Handle NaN values in occurrence
                    occurrence_value = 1
                    if 'Occurrence' in score_card_data and score_card_data['Occurrence'] is not None:
                        try:
                            if not pd.isna(score_card_data['Occurrence']):
                                occurrence_value = int(score_card_data['Occurrence'])
                        except:
                            pass
                            
                    occurrence = st.number_input("Occurrence (O)",
                                                min_value=1, max_value=10, value=occurrence_value)
                    
                    st.write("**Occurrence Rating Guide:**")
                    st.write("1-2: Very unlikely to occur")
                    st.write("3-4: Low probability")
                    st.write("5-6: Moderate probability")
                    st.write("7-8: High probability")
                    st.write("9-10: Almost certain to occur")
                
                with col3:
                    # Handle NaN values in detection
                    detection_value = 1
                    if 'Detection' in score_card_data and score_card_data['Detection'] is not None:
                        try:
                            if not pd.isna(score_card_data['Detection']):
                                detection_value = int(score_card_data['Detection'])
                        except:
                            pass
                            
                    detection = st.number_input("Detection (D)",
                                               min_value=1, max_value=10, value=detection_value)
                    
                    st.write("**Detection Rating Guide:**")
                    st.write("1-2: Very high detection capability")
                    st.write("3-4: High detection capability")
                    st.write("5-6: Moderate detection capability")
                    st.write("7-8: Low detection capability")
                    st.write("9-10: Very low detection capability")
                
                # Calculate RPN
                rpn = severity * occurrence * detection
                
                st.subheader(f"Risk Priority Number (RPN = S × O × D) = {rpn}")
                
                # Risk level based on RPN
                if rpn <= 50:
                    risk_level = "Low Risk"
                    risk_color = "green"
                elif rpn <= 100:
                    risk_level = "Moderate Risk"
                    risk_color = "orange"
                elif rpn <= 200:
                    risk_level = "High Risk"
                    risk_color = "red"
                else:
                    risk_level = "Critical Risk"
                    risk_color = "darkred"
                
                st.markdown(f"<h3 style='color: {risk_color};'>Risk Level: {risk_level}</h3>", unsafe_allow_html=True)
                
                risk_notes = st.text_area("Additional Risk Notes", 
                                         value=score_card_data.get('Risk Notes', ''),
                                         height=100)
                
                submit_score = st.form_submit_button("Save Score Card")
                
                if submit_score:
                    # Prepare data for saving
                    data = {
                        "Assessment Number": st.session_state.current_assessment_id,
                        "Severity": severity,
                        "Occurrence": occurrence,
                        "Detection": detection,
                        "RPN": rpn,
                        "Risk Level": risk_level,
                        "Risk Notes": risk_notes
                    }
                    
                    try:
                        # Load all existing data from all sheets
                        sheets_data = {}
                        sheets_to_save = ['Activity', 'AspectImpact', 'ScoreCard', 'CAPA', 'Report']
                        
                        for sheet in sheets_to_save:
                            try:
                                sheets_data[sheet] = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name=sheet)
                            except:
                                sheets_data[sheet] = pd.DataFrame()
                        
                        # Update ScoreCard sheet
                        if not sheets_data['ScoreCard'].empty and 'Assessment Number' in sheets_data['ScoreCard'].columns:
                            sheets_data['ScoreCard'] = sheets_data['ScoreCard'][sheets_data['ScoreCard']['Assessment Number'] != st.session_state.current_assessment_id]
                        
                        # Add new record
                        new_df = pd.DataFrame([data])
                        sheets_data['ScoreCard'] = pd.concat([sheets_data['ScoreCard'], new_df], ignore_index=True)
                        
                        # Save all sheets back to Excel
                        with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl', mode='w') as writer:
                            for sheet_name, sheet_df in sheets_data.items():
                                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        st.success("Score Card saved successfully!")
                        
                    except Exception as e:
                        st.error(f"Error saving data: {e}")
    
    # Tab 4: CA/PA
    with aspect_tabs[3]:
        st.header("Corrective/Preventive Actions")
        
        if not st.session_state.current_assessment_id:
            st.warning("Please save Activity information first before proceeding to CA/PA.")
        else:
            # Create a container for existing actions
            st.subheader("Existing Actions")
            
            try:
                df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='CAPA')
                filtered_df = df[df['Assessment Number'] == st.session_state.current_assessment_id]
                
                if not filtered_df.empty:
                    display_columns = [col for col in filtered_df.columns if col != 'Assessment Number']
                    if display_columns:  # Make sure there are columns to display
                        st.dataframe(filtered_df[display_columns], use_container_width=True)
                    else:
                        st.info("No existing actions found. Add new actions below.")
                else:
                    st.info("No existing actions found. Add new actions below.")
            except Exception as e:
                st.info("No existing actions found. Add new actions below.")
            
            # Form for adding new action
            st.subheader("Add New Action")
            with st.form("capa_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    action_description = st.text_area("Action Description", height=100)
                    assigned_to = st.text_input("Assigned To")
                    
                with col2:
                    due_date = st.date_input("Due Date")
                    verification_approach = st.selectbox("Verification Approach", 
                                                        ["Audit", "Inspection", "Monitoring", "Testing", "Review", "Other"])
                
                lessons_learned = st.text_area("Lessons Learned", 
                                             placeholder="Key takeaways to strengthen future prevention, response, and resilience",
                                             height=100)
                
                submit_action = st.form_submit_button("Add Action")
                
                if submit_action:
                    # Prepare data for saving
                    data = {
                        "Assessment Number": st.session_state.current_assessment_id,
                        "Action Description": action_description,
                        "Assigned To": assigned_to,
                        "Due Date": due_date,
                        "Verification Approach": verification_approach,
                        "Lessons Learned": lessons_learned,
                        "Status": "Open",
                        "Date Added": date.today()
                    }
                    
                    try:
                        # Load all existing data
                        sheets_data = {}
                        sheets_to_save = ['Activity', 'AspectImpact', 'ScoreCard', 'CAPA', 'Report']
                        
                        for sheet in sheets_to_save:
                            try:
                                sheets_data[sheet] = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name=sheet)
                            except:
                                sheets_data[sheet] = pd.DataFrame()
                        
                        # Add new record to CAPA
                        new_df = pd.DataFrame([data])
                        sheets_data['CAPA'] = pd.concat([sheets_data['CAPA'], new_df], ignore_index=True)
                        
                        # Save all sheets back to Excel
                        with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl', mode='w') as writer:
                            for sheet_name, sheet_df in sheets_data.items():
                                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        st.success("Action added successfully!")
                        st.experimental_rerun()  # Updated from st.rerun() for compatibility
                        
                    except Exception as e:
                        st.error(f"Error saving data: {e}")

                 # Tab 5: Report
    with aspect_tabs[4]:
        st.header("Aspect/Impact Assessment Report")
        
        if not st.session_state.current_assessment_id:
            st.warning("Please save Activity information first to view the report.")
        else:
            try:
                # Initialize DataFrames
                activity_df = pd.DataFrame()
                aspect_impact_df = pd.DataFrame()
                score_card_df = pd.DataFrame()
                capa_df = pd.DataFrame()
                report_df = pd.DataFrame()
                
                # Load all data for the current assessment with error handling
                try:
                    activity_df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Activity')
                except Exception as e:
                    pass
                    
                try:
                    aspect_impact_df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='AspectImpact')
                except Exception as e:
                    pass
                    
                try:
                    score_card_df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='ScoreCard')
                except Exception as e:
                    pass
                    
                try:
                    capa_df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='CAPA')
                except Exception as e:
                    pass
                    
                try:
                    report_df = pd.read_excel(ASPECT_IMPACT_FILE, sheet_name='Report')
                except Exception as e:
                    pass
                
                # Filter data for current assessment - now with safety checks
                current_activity = pd.DataFrame()
                if not activity_df.empty and 'Aspect/Impact Assessment Number' in activity_df.columns:
                    current_activity = activity_df[activity_df['Aspect/Impact Assessment Number'] == st.session_state.current_assessment_id]
                    
                current_aspect_impact = pd.DataFrame()
                if not aspect_impact_df.empty and 'Assessment Number' in aspect_impact_df.columns:
                    current_aspect_impact = aspect_impact_df[aspect_impact_df['Assessment Number'] == st.session_state.current_assessment_id]
                    
                current_score_card = pd.DataFrame()
                if not score_card_df.empty and 'Assessment Number' in score_card_df.columns:
                    current_score_card = score_card_df[score_card_df['Assessment Number'] == st.session_state.current_assessment_id]
                    
                current_capa = pd.DataFrame()
                if not capa_df.empty and 'Assessment Number' in capa_df.columns:
                    current_capa = capa_df[capa_df['Assessment Number'] == st.session_state.current_assessment_id]
                
                # Display report sections
                if not current_activity.empty:
                    st.subheader("Activity Information")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Assessment Number:** {st.session_state.current_assessment_id}")
                        st.write(f"**Company Name:** {current_activity.iloc[0].get('Company Name', 'N/A')}")
                        st.write(f"**Incident Number:** {current_activity.iloc[0].get('Incident Number', 'N/A')}")
                        st.write(f"**Incident Type:** {current_activity.iloc[0].get('Incident Type', 'N/A')}")
                        
                    with col2:
                        st.write(f"**Incident Date:** {current_activity.iloc[0].get('Incident Date', 'N/A')}")
                        st.write(f"**Location:** {current_activity.iloc[0].get('Incident Location', 'N/A')}")
                        st.write(f"**Reported By:** {current_activity.iloc[0].get('Reported By Name', 'N/A')}")
                    
                    st.write(f"**Incident Description:** {current_activity.iloc[0].get('Incident Description', 'N/A')}")
                    
                    # Display associated images if any
                    if 'Evidence Photo Paths' in current_activity.columns and not pd.isna(current_activity.iloc[0].get('Evidence Photo Paths')):
                        photo_paths = str(current_activity.iloc[0]['Evidence Photo Paths']).split(',')
                        if photo_paths and photo_paths[0]:  # Check if there are actual paths
                            st.subheader("Evidence Photos")
                            image_cols = st.columns(min(3, len(photo_paths)))
                            for i, img_path in enumerate(photo_paths):
                                if os.path.exists(img_path):
                                    image_cols[i % 3].image(img_path, caption=f"Photo {i+1}")
                
                if not current_aspect_impact.empty:
                    st.subheader("Aspect/Impact Analysis")
                    
                    with st.expander("View Aspects"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Human Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('Human Factors', 'N/A'))
                            
                            st.write("**Equipment/Material Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('Equipment Factors', 'N/A'))
                            
                            st.write("**Procedural Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('Procedural Factors', 'N/A'))
                        
                        with col2:
                            st.write("**Environmental Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('Environmental Factors', 'N/A'))
                            
                            st.write("**Organizational Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('Organizational Factors', 'N/A'))
                            
                            st.write("**External Factors:**")
                            st.write(current_aspect_impact.iloc[0].get('External Factors', 'N/A'))
                    
                    with st.expander("View Impacts"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Safety Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Safety Impact', 'N/A'))
                            
                            st.write("**Environmental Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Environment Impact', 'N/A'))
                            
                            st.write("**Operational Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Operations Impact', 'N/A'))
                        
                        with col2:
                            st.write("**Financial Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Financial Impact', 'N/A'))
                            
                            st.write("**Reputational Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Reputation Impact', 'N/A'))
                            
                            st.write("**Legal/Compliance Impact:**")
                            st.write(current_aspect_impact.iloc[0].get('Legal Impact', 'N/A'))
                
                if not current_score_card.empty:
                    st.subheader("Risk Assessment")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Severity (S):** {int(current_score_card.iloc[0].get('Severity', 0))}")
                        st.write(f"**Occurrence (O):** {int(current_score_card.iloc[0].get('Occurrence', 0))}")
                        st.write(f"**Detection (D):** {int(current_score_card.iloc[0].get('Detection', 0))}")
                    
                    with col2:
                        # Get RPN and risk level with proper error handling
                        rpn = current_score_card.iloc[0].get('RPN', 0)
                        if pd.isna(rpn):
                            rpn = 0
                            
                        risk_level = current_score_card.iloc[0].get('Risk Level', 'N/A')
                        
                        # Set risk color based on level
                        risk_color = "green"
                        if risk_level == "Moderate Risk":
                            risk_color = "orange"
                        elif risk_level == "High Risk":
                            risk_color = "red"
                        elif risk_level == "Critical Risk":
                            risk_color = "darkred"
                        
                        st.write(f"**Risk Priority Number (RPN):** {int(rpn)}")
                        st.markdown(f"<h4 style='color: {risk_color};'>Risk Level: {risk_level}</h4>", unsafe_allow_html=True)
                    
                    st.write("**Risk Notes:**")
                    st.write(current_score_card.iloc[0].get('Risk Notes', 'N/A'))
                
                if not current_capa.empty:
                    st.subheader("Corrective/Preventive Actions")
                    
                    # Display actions in a table
                    display_columns = [col for col in current_capa.columns if col != 'Assessment Number']
                    st.dataframe(current_capa[display_columns], use_container_width=True)
                    
                    # Show lessons learned summary
                    st.subheader("Lessons Learned Summary")
                    lessons = current_capa['Lessons Learned'].dropna().tolist()
                    if lessons:
                        for i, lesson in enumerate(lessons):
                            st.write(f"{i+1}. {lesson}")
                    else:
                        st.write("No lessons learned have been documented.")
                
                # Report actions
                report_actions = st.expander("Report Actions")
                with report_actions:
                    if st.button("Generate PDF Report"):
                        # This functionality would require additional libraries
                        st.warning("PDF generation feature is not implemented in this version.")
                    
                    # Add option to generate a report summary
                    if st.button("Save Report Summary"):
                        try:
                            # Create a summary of the assessment
                            summary_data = {
                                "Assessment Number": st.session_state.current_assessment_id,
                                "Report Date": date.today(),
                                "Incident Type": current_activity.iloc[0].get('Incident Type', 'N/A') if not current_activity.empty else 'N/A',
                                "Risk Level": current_score_card.iloc[0].get('Risk Level', 'N/A') if not current_score_card.empty else 'N/A',
                                "RPN": current_score_card.iloc[0].get('RPN', 0) if not current_score_card.empty else 0,
                                "Actions Count": len(current_capa) if not current_capa.empty else 0,
                                "Key Findings": "Multiple factors identified" if not current_aspect_impact.empty else "No analysis completed",
                                "Status": "Complete" if not current_activity.empty and not current_aspect_impact.empty and not current_score_card.empty else "Incomplete"
                            }
                            
                            # Save to Report sheet
                            if not report_df.empty and 'Assessment Number' in report_df.columns:
                                report_df = report_df[report_df['Assessment Number'] != st.session_state.current_assessment_id]
                            
                            # Add new record
                            new_df = pd.DataFrame([summary_data])
                            report_df = pd.concat([report_df, new_df], ignore_index=True)
                            
                            # Save all sheets back to Excel
                            sheets_data = {
                                'Activity': activity_df,
                                'AspectImpact': aspect_impact_df,
                                'ScoreCard': score_card_df,
                                'CAPA': capa_df,
                                'Report': report_df
                            }
                            
                            with pd.ExcelWriter(ASPECT_IMPACT_FILE, engine='openpyxl', mode='w') as writer:
                                for sheet_name, sheet_df in sheets_data.items():
                                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                            
                            st.success("Report summary saved successfully!")
                            
                        except Exception as e:
                            st.error(f"Error saving report summary: {e}")
                
            except Exception as e:
                st.error(f"Error loading report data: {e}")