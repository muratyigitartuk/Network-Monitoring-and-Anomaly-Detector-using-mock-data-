# Network Anomaly Monitor and Detection System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0.1-000000?style=flat-square&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=flat-square&logo=javascript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3.3-38B2AC?style=flat-square&logo=tailwind-css)
![Chart.js](https://img.shields.io/badge/Chart.js-3.9.1-FF6384?style=flat-square&logo=chart-dot-js)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

A comprehensive network monitoring and anomaly detection system that provides real-time visibility into network traffic, detects unusual patterns, and alerts on potential security threats. This tool is designed for network administrators, security professionals, and IT teams who need to maintain network health and security.

> **Note:** This project is actively under development. The current version provides a functional dashboard with mock data generation. Python environment dependencies need to be installed manually.

## 📸 Dashboard Screenshots

### Dashboard Overview
![Dashboard Overview](screenshots/dashboard-overview.png)

### Network Topology
![Network Topology](screenshots/network-topology.png)

### Dashboard Customization
![Dashboard Customization](screenshots/dashboard-customization.png)

### Network Health Analysis
![Network Health Analysis](screenshots/network-health-analysis.png)

### Alerting System
![Alerting System](screenshots/alerting-system.png)

### System Information
![System Information](screenshots/system-information.png)

### Trend Analysis & Forecasting
![Trend Analysis](screenshots/trend-analysis.png)

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
│   ├── static/           # Static files (HTML, CSS, JS)
│   ├── templates/        # HTML templates
│   ├── app.py            # Flask application entry point
│   └── requirements.txt  # Python dependencies
└── screenshots/          # Dashboard screenshots
```

### Backend (Python)

- **Flask**: Lightweight web framework for serving the application
- **Chart.js**: JavaScript library for interactive charts and data visualization
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **JavaScript**: Client-side interactivity and data processing
- **HTML/CSS**: Frontend structure and styling

### Features

- **Real-time Monitoring**: Track network traffic, latency, and packet loss
- **Interactive Dashboard**: Visualize network performance with dynamic charts
- **Network Topology**: Interactive visualization of network structure
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Customization**: Adjust dashboard layout and appearance
- **Responsive Design**: Works on desktop and mobile devices
- **Mock Data Generation**: Realistic network data patterns for demonstration

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** - [Download](https://www.python.org/downloads/)
- **Python packages** - The following key packages are required:
  - `flask`: Web framework
  - `werkzeug`: WSGI utility library
  - `jinja2`: Template engine
  - `markupsafe`: String handling
- **Web Browser** - Chrome, Firefox, or Edge recommended

### Quick Start

```bash
# Clone the repository
git clone https://github.com/muratyigitartuk/Network-Monitoring-and-Anomaly-Detector-using-mock-data-
cd Network-Monitoring-and-Anomaly-Detector-using-mock-data-

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to `http://localhost:8000` to view the dashboard.

### Manual Setup

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

# Run the application
python app.py
```

The application will be available at `http://localhost:8000`.

## 📊 Dashboard Features

The dashboard provides a comprehensive view of your network:

- **Metric Cards**: Shows key metrics at a glance including incoming/outgoing traffic, active connections, latency, and packet loss
- **Traffic Charts**: Real-time and historical traffic visualization with customizable time ranges
- **Latency & Packet Loss**: Monitor network performance metrics over time
- **Protocol Distribution**: Breakdown of network traffic by protocol
- **Bandwidth Usage**: Track bandwidth consumption by time period
- **Network Topology**: Interactive visualization of network devices and connections
- **Network Health Analysis**: Comprehensive health score with performance metrics
- **Trend Analysis**: Forecasting with historical data comparison
- **Anomaly Detection**: Identification of unusual patterns with severity classification
- **Alert Management**: View and manage network alerts
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Customization Options**: Adjust dashboard layout and appearance

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   - Install the required dependencies using `pip install -r backend/requirements.txt`.

2. **Port Already in Use**:
   - If port 8000 is already in use, you can change the port in the Flask app configuration.

3. **Chart Rendering Issues**:
   - If charts appear blank, try refreshing the dashboard.
   - For performance issues with long time ranges (24h), the application automatically samples data points.

4. **Dashboard Customization**:
   - If dashboard customization settings aren't persisting, check browser local storage permissions.
   - Theme colors can be selected from the color palette in the customization panel.

### Getting Help

If you encounter any issues not covered here, please:

1. Check the logs in the terminal window for error messages
2. Open an issue on GitHub with details about your environment and the problem

## 📋 Future Enhancements

Planned features for future releases:

- Real network data collection instead of mock data
- Enhanced anomaly detection algorithms
- Additional chart types and visualizations
- Improved network topology visualization
- User authentication and multi-user support
- Alert notification system (email, SMS)
- Mobile-responsive design improvements
- Data export capabilities (CSV, JSON)
- Historical data storage and analysis
- Geographic traffic mapping and visualization
- Custom dashboard layouts with drag-and-drop interface
- Integration with network monitoring tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Chart.js](https://www.chartjs.org/) for data visualization
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Font Awesome](https://fontawesome.com/) for icons
- [D3.js](https://d3js.org/) for network topology visualization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
