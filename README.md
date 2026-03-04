
# Multi-Domain IT Intelligence Platform (Module CST1510)

## Overview

The **Multi-Domain IT Intelligence Platform** is a comprehensive web-based dashboard designed to centralize the management of IT operations, cybersecurity incidents, datasets, and AI-assisted support. Built using **Python** and **Streamlit**, the platform provides an intuitive interface for monitoring, analyzing, and managing critical IT intelligence through interactive dashboards and secure user authentication.

The platform integrates multiple functional domains into a single application, allowing users to manage IT tickets, monitor cyber incidents, maintain dataset metadata, and interact with an AI-powered chat assistant. Its modular architecture ensures scalability, maintainability, and future extensibility.

---

## Key Features

### Authentication & Security
- Secure user registration and login using **bcrypt** password hashing
- Strong password validation (uppercase, lowercase, number, special character)
- Session-based authentication and access control
- Account management:
  - Update credentials
  - Delete account with confirmation

### Dashboards
- **Cyber Incident Dashboard** with severity tracking and analytics
- **IT Ticket Dashboard** with prioritization and resolution metrics
- **Metadata Dashboard** for dataset inventory and governance
- **AI Chat Assistant** powered by OpenAI GPT for contextual help

---

## System Architecture

The IT Intelligence Platform follows a **modular three-tier architecture**:

### Presentation Layer
- Streamlit dashboards for user interaction and data visualization

### Application Layer
- Python modules handling business logic, validation, and workflows

### Data Layer
- SQLite relational database for persistent data storage

This clear separation of concerns improves maintainability, scalability, and extensibility.

---

## Security & Data Flow

### Core Security Design
- Passwords are hashed using **bcrypt** with salt
- No plain-text passwords are stored
- Session validation is required for all protected resources
- API keys are stored securely in `.streamlit/secrets.toml`

### Data Flow Security

**Registration Flow:**
```
Password → bcrypt hash → Database storage
```

**Login Flow:**
```
Input password → bcrypt verification → Session creation
```

**Data Access Flow:**
```
Session validation → Database queries → Filtered results
```
---

## Installation

### Option 1: Installation Using VS Code (Recommended)

1. Open **Visual Studio Code**
2. Click **File → Open Folder**
3. Open the project root directory

4. Open the integrated terminal:
   - **View → Terminal** or `Ctrl + ``

5. Create a virtual environment:
```bash
python -m venv venv
```

6. Select Python Interpreter:
- Press `Ctrl + Shift + P`
- Search **Python: Select Interpreter**
- Choose the interpreter from `venv`

7. Activate the virtual environment:
```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

8. Install dependencies:
```bash
pip install -r Requirements.txt
```

9. Run the application:
```bash
streamlit run home.py
```

10. Configure secrets in `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

---

### Option 2: Installation Using Command Line

```bash
# Clone the repository
git clone https://github.com/your-username/it-intelligence-platform.git
cd it-intelligence-platform

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r Requirements.txt

# Run application
streamlit run home.py
```

---

## Usage

1. Register or log in using secure credentials
2. Navigate dashboards using the sidebar
3. Manage:
   - IT tickets
   - Cybersecurity incidents
   - Dataset metadata
4. Use the **AI Chat Assistant** for guidance and contextual support

> All dashboards support filtering, analytics, and full CRUD operations.
> Data is stored in SQLite and updated in real time.

---

## Troubleshooting

- Ensure **Python 3.9+** is installed
- Verify all dependencies are installed correctly
- Check SQLite database file path and permissions
- Confirm OpenAI API key is set in `secrets.toml`
- Restart Streamlit after configuration changes

---

## Project Structure

```
CM2_M0107IS1_CSTIS10/
├── app/                          # Core application modules
│   ├── __pycache__/              # Python cache
│   ├── db.py                     # Database connection management
│   ├── incidence.py              # Cyber incident logic
│   ├── metadata.py               # Dataset metadata logic
│   ├── schema.py                 # Database schema
│   ├── ticket.py                 # IT ticket logic
│   └── user.py                   # User authentication
├── pages/                        # Streamlit dashboards
│   ├── chat.py                   # AI Chat Assistant
│   ├── Cyber_Incident.py         # Cyber Incident Dashboard
│   ├── It_Ticket.py              # IT Ticket Dashboard
│   └── Meta_Data.py              # Metadata Dashboard
├── DATA/                         # Data storage
│   ├── intelligence_platform.db  # SQLite database
│   ├── cyber_incidents.csv       # Sample data
│   ├── datasets_metadata.csv     # Sample metadata
│   └── it_tickets.csv            # Sample tickets
├── .streamlit/                   # Streamlit configuration
│   └── secrets.toml              # API keys
├── application.py                # Authentication workflows
├── db_operation.py               # Data migration utilities
├── home.py                       # Main entry point
├── main.py                       # CLI utilities
├── test.py                       # Testing
├── README.md                     # Documentation
├── Requirements.txt              # Dependencies
└── .gitignore                    # Ignored files
```

---

## Learning Outcomes

This project demonstrates:
- Full-stack Python development with Streamlit
- Secure authentication and session management
- SQLite database design and integration
- Data visualization and dashboard development
- Modular architecture and documentation best practices

---

## Conclusion

The **IT Intelligence Platform** provides a secure, scalable, and user-friendly solution for managing IT operations, cybersecurity incidents, and data assets. Its modular design and robust security implementation make it suitable for enterprise, academic, and portfolio use, with strong potential for future enhancements such as automation, advanced analytics, and third-party integrations.

---

## Acknowledgments

- **Streamlit** — Web application framework
- **OpenAI** — GPT integration
- **bcrypt** — Secure password hashing
- **Pandas** — Data manipulation and analytics
- **Python Community** — Documentation and open-source support

---

> Project for Module **CST1510**
