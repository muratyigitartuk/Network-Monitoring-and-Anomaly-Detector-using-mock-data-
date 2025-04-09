# Network Anomaly Monitor and Detection System

![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=flat-square&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0.2-3178C6?style=flat-square&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3.3-38B2AC?style=flat-square&logo=tailwind-css)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

A comprehensive network monitoring and anomaly detection system that provides real-time visibility into network traffic, detects unusual patterns, and alerts on potential security threats. This tool is designed for network administrators, security professionals, and IT teams who need to maintain network health and security.

> **Note:** This project is actively under development. The current version provides a functional dashboard with mock data generation. Python environment dependencies need to be installed manually.

## 📸 Dashboard Screenshots

### Main Dashboard (Dark Mode)
![Main Dashboard](screenshots/dashboard-dark.png)
*The main dashboard provides at-a-glance metrics for network performance monitoring*

### Network Topology Visualization
![Network Topology](screenshots/network-topology.png)
*Interactive network topology map showing device connections and status*

### Dashboard Customization
![Dashboard Customization](screenshots/dashboard-customization.png)
*Extensive customization options for layout, widgets, and appearance*

### Network Health Analysis
![Network Health](screenshots/network-health.png)
*Comprehensive health scoring with anomaly detection*

### Alerting System
![Alerting System](screenshots/alerting-system.png)
*Real-time alerts with configurable thresholds and notification channels*

### System Overview
![System Overview](screenshots/system-overview.png)
*Recent events, top connections, and system resource monitoring*

### Trend Analysis & Forecasting
![Trend Analysis](screenshots/trend-analysis.png)
*Advanced trend analysis with predictive forecasting for capacity planning*

## 🌟 Features

### 🔍 Real-time Network Monitoring
- Traffic visualization (incoming/outgoing) with real-time metrics
- Protocol distribution analysis (TCP/UDP) with percentage breakdown
- Port traffic monitoring with bandwidth usage tracking
- Top source and destination IP tracking with geographic information
- Latency and packet loss measurement with threshold alerts
- Active connections tracking with status indicators

### 🧠 Anomaly Detection
- Machine learning-based anomaly detection
- Statistical pattern analysis
- Customizable alert thresholds
- Historical data comparison
- Adaptive baseline establishment
- Anomaly classification

### 🌐 Network Visualization
- Interactive network topology map with device categorization (Router, Switch, Server, PC, Mobile)
- Color-coded status indicators (Active, Warning, Critical)
- Drag and zoom functionality for exploring complex networks
- Device connection visualization with relationship mapping
- Real-time connection status updates
- Device type identification with custom icons

### 🔒 Security Features
- User authentication and authorization
- Role-based access control
- Secure API endpoints
- Alert management system
- Audit logging

### 📊 Data Management
- Historical data storage and retrieval
- Data export capabilities (CSV, JSON)
- Customizable time ranges
- Advanced filtering options
- Data retention policies
- Aggregation for long-term storage

## 🏗️ Architecture

The system consists of two main components working together to provide a complete network monitoring solution:

```
/
├── backend/               # Python backend code
│   ├── api/              # API endpoints and models
│   ├── collectors/       # Network data collection
│   ├── database/         # Database models and connection
│   ├── processors/       # Data processing and analysis
│   └── main.py           # Application entry point
├── src/                  # React frontend code
│   ├── components/       # UI components
│   ├── context/          # React context providers
│   ├── services/         # API services
│   ├── types/            # TypeScript type definitions
│   └── utils/            # Utility functions
└── public/               # Static assets
```

### Backend (Python)

- **FastAPI**: High-performance API framework for building the REST API endpoints
- **Scapy**: Network packet capture and analysis for real-time traffic monitoring
- **SQLAlchemy**: Database ORM for efficient data storage and retrieval
- **scikit-learn/TensorFlow**: Machine learning libraries for anomaly detection
- **WebSockets**: Real-time data streaming to the frontend
- **Pandas/NumPy**: Data processing and analysis
- **Redis**: Optional caching for improved performance

### Frontend (React)

- **React**: UI framework for building the user interface
- **TypeScript**: Type-safe JavaScript for improved code quality
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Recharts**: Data visualization library for charts and graphs
- **vis.js**: Network topology visualization for interactive network maps
- **React Query**: Data fetching, caching, and state management
- **React Grid Layout**: Customizable dashboard layouts

## 🚀 Getting Started

### Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Python packages** - The following key packages are required:
  - `fastapi`: API framework
  - `uvicorn`: ASGI server
  - `sqlalchemy`: Database ORM
  - `scapy`: Network packet capture (optional, mock data will be used if not available)
  - `python-dotenv`: Environment variable management
- **PostgreSQL** (optional, SQLite works for development) - [Download](https://www.postgresql.org/download/)

### Quick Start

The easiest way to get started is to use our setup scripts:

```bash
# On Windows
setup_environment.bat
run_all.bat
```

This will install all required dependencies and start both the backend and frontend servers.

### Manual Setup

#### Backend Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file and update the SECRET_KEY with a secure random string

# Run the backend server
python run.py
# Or alternatively
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Security Notes

- The `.env` file contains sensitive information and is excluded from version control
- Always change the `SECRET_KEY` in the `.env` file to a secure random string
- Database files (*.db) are also excluded from version control to protect any collected data

#### Frontend Setup

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```

### Docker Setup

For a containerized setup, you can use Docker:

```bash
# Build and start the containers
cd backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

## 🔐 Authentication

The system uses JWT-based authentication with role-based access control:

- **Default credentials**:
  - Username: `admin`
  - Password: `password`

- **Available roles**:
  - `admin`: Full access to all features
  - `analyst`: Can view data and manage alerts
  - `user`: Read-only access to dashboards

## 📊 Dashboard Features

The dashboard provides a comprehensive view of your network:

- **Overview Panel**: Shows key metrics at a glance including incoming/outgoing traffic, active connections, latency, and packet loss
- **Traffic Charts**: Real-time and historical traffic visualization with customizable time ranges
- **Protocol Distribution**: Detailed breakdown of TCP/UDP traffic with percentage analysis
- **Network Health Score**: Comprehensive health analysis with availability, performance, and reliability metrics
- **Anomaly Detection**: Intelligent detection of unusual patterns with severity classification
- **Alert Management**: View, acknowledge, and resolve alerts with configurable thresholds
- **Network Topology**: Interactive visualization of network devices and connections
- **Trend Analysis**: Advanced forecasting with capacity planning recommendations
- **System Information**: Real-time monitoring of CPU, memory, disk, and network resources
- **Recent Events**: Timeline of network events with status indicators
- **Top Connections**: Bandwidth usage breakdown by domain and service type
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Customization Options**: Extensive layout, widget, and appearance settings

## 📚 API Documentation

Comprehensive API documentation is automatically generated and available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

The documentation includes all endpoints, request/response models, and authentication requirements.

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   - The application will attempt to run with mock data if certain dependencies are missing.
   - Install the required dependencies using `pip install -r backend/requirements.txt`.

2. **Port Already in Use**:
   - If port 8000 is already in use, you can change the port in the `.env` file.
   - If port 5173 is already in use, Vite will automatically try to use the next available port.

3. **Database Issues**:
   - The application uses SQLite by default, which should work without additional setup.
   - If you encounter database issues, the application will fall back to using an in-memory database.

4. **Network Capture Issues**:
   - Packet capture requires administrative privileges and the Scapy library.
   - If Scapy is not available or lacks permissions, the application will use mock data.

5. **Dashboard Customization**:
   - If dashboard customization settings aren't persisting, check browser local storage permissions.
   - Some widgets may require specific data sources to be available.
   - Theme colors can be selected from the color palette in the customization panel.

6. **Chart Rendering Issues**:
   - If charts appear blank, try adjusting the time range or refreshing the dashboard.
   - For performance issues with long time ranges, the application automatically samples data points.

### Getting Help

If you encounter any issues not covered here, please:

1. Check the logs in the terminal windows for error messages
2. Open an issue on GitHub with details about your environment and the problem

## 📋 Future Enhancements

We plan to add the following features in future releases:

- Enhanced machine learning models for more accurate anomaly detection
- Support for SNMP monitoring and network device discovery
- Syslog collection and analysis
- Mobile application for on-the-go monitoring
- Expanded notification services beyond the current Email, Slack, and SMS options
- Advanced reporting capabilities with scheduled report generation
- Integration with popular security tools and SIEM systems
- Enhanced capacity planning with automated recommendations
- Geographic traffic mapping and visualization
- Advanced filtering options for network events and alerts
- Custom dashboard builder with drag-and-drop interface
- API integrations with third-party network management tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Scapy](https://scapy.net/) for packet capture capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [React](https://reactjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Recharts](https://recharts.org/) for data visualization
- [vis.js](https://visjs.org/) for network visualization
- [scikit-learn](https://scikit-learn.org/) for machine learning algorithms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
