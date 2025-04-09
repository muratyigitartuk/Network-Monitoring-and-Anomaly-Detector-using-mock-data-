import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
import logging
import joblib
import os
from database.db_connector import get_db
from processors.traffic_analyzer import get_historical_metrics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model file paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
TRAFFIC_MODEL_PATH = os.path.join(MODEL_DIR, "traffic_anomaly_model.joblib")
LATENCY_MODEL_PATH = os.path.join(MODEL_DIR, "latency_anomaly_model.joblib")

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

class AnomalyDetector:
    def __init__(self):
        self.traffic_model = None
        self.latency_model = None
        self.traffic_scaler = None
        self.latency_scaler = None
        self.is_trained = False
        
        # Try to load existing models
        self.load_models()
    
    def load_models(self) -> bool:
        """Load trained models if they exist"""
        try:
            if os.path.exists(TRAFFIC_MODEL_PATH) and os.path.exists(LATENCY_MODEL_PATH):
                self.traffic_model = joblib.load(TRAFFIC_MODEL_PATH)
                self.latency_model = joblib.load(LATENCY_MODEL_PATH)
                self.traffic_scaler = joblib.load(os.path.join(MODEL_DIR, "traffic_scaler.joblib"))
                self.latency_scaler = joblib.load(os.path.join(MODEL_DIR, "latency_scaler.joblib"))
                self.is_trained = True
                logger.info("Loaded existing anomaly detection models")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def save_models(self) -> None:
        """Save trained models"""
        try:
            joblib.dump(self.traffic_model, TRAFFIC_MODEL_PATH)
            joblib.dump(self.latency_model, LATENCY_MODEL_PATH)
            joblib.dump(self.traffic_scaler, os.path.join(MODEL_DIR, "traffic_scaler.joblib"))
            joblib.dump(self.latency_scaler, os.path.join(MODEL_DIR, "latency_scaler.joblib"))
            logger.info("Saved anomaly detection models")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def train(self, metrics: List[Dict[str, Any]]) -> None:
        """Train anomaly detection models on historical data"""
        if not metrics:
            logger.warning("No metrics provided for training")
            return
        
        try:
            # Extract features for traffic model
            traffic_data = np.array([
                [m["incoming_traffic"], m["outgoing_traffic"], m["active_connections"]]
                for m in metrics
            ])
            
            # Extract features for latency model
            latency_data = np.array([
                [m["average_latency"], m["packet_loss"]]
                for m in metrics
            ])
            
            # Scale the data
            self.traffic_scaler = StandardScaler()
            self.latency_scaler = StandardScaler()
            
            traffic_data_scaled = self.traffic_scaler.fit_transform(traffic_data)
            latency_data_scaled = self.latency_scaler.fit_transform(latency_data)
            
            # Train Isolation Forest models
            self.traffic_model = IsolationForest(
                n_estimators=100,
                contamination=0.05,  # Assume 5% of data points are anomalies
                random_state=42
            )
            
            self.latency_model = IsolationForest(
                n_estimators=100,
                contamination=0.05,
                random_state=42
            )
            
            self.traffic_model.fit(traffic_data_scaled)
            self.latency_model.fit(latency_data_scaled)
            
            self.is_trained = True
            
            # Save the models
            self.save_models()
            
            logger.info("Trained anomaly detection models")
        except Exception as e:
            logger.error(f"Error training models: {e}")
            raise
    
    def detect_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies in network metrics"""
        if not self.is_trained:
            logger.warning("Models not trained, cannot detect anomalies")
            return {
                "is_anomaly": False,
                "traffic_anomaly": False,
                "latency_anomaly": False,
                "anomaly_score": 0.0
            }
        
        try:
            # Extract features
            traffic_features = np.array([[
                metrics["incoming_traffic"],
                metrics["outgoing_traffic"],
                metrics["active_connections"]
            ]])
            
            latency_features = np.array([[
                metrics["average_latency"],
                metrics["packet_loss"]
            ]])
            
            # Scale features
            traffic_features_scaled = self.traffic_scaler.transform(traffic_features)
            latency_features_scaled = self.latency_scaler.transform(latency_features)
            
            # Predict anomalies
            traffic_prediction = self.traffic_model.predict(traffic_features_scaled)
            latency_prediction = self.latency_model.predict(latency_features_scaled)
            
            # Get anomaly scores
            traffic_score = self.traffic_model.score_samples(traffic_features_scaled)
            latency_score = self.latency_model.score_samples(latency_features_scaled)
            
            # Determine if anomalies
            traffic_anomaly = traffic_prediction[0] == -1
            latency_anomaly = latency_prediction[0] == -1
            
            # Calculate overall anomaly score
            # Lower score = more anomalous
            overall_score = min(traffic_score[0], latency_score[0])
            
            return {
                "is_anomaly": traffic_anomaly or latency_anomaly,
                "traffic_anomaly": traffic_anomaly,
                "latency_anomaly": latency_anomaly,
                "anomaly_score": float(overall_score),
                "traffic_score": float(traffic_score[0]),
                "latency_score": float(latency_score[0])
            }
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {
                "is_anomaly": False,
                "traffic_anomaly": False,
                "latency_anomaly": False,
                "anomaly_score": 0.0,
                "error": str(e)
            }

# Singleton instance
detector = AnomalyDetector()

def train_anomaly_models(db=None):
    """Train anomaly detection models on historical data"""
    try:
        # Get database session if not provided
        if db is None:
            db = next(get_db())
        
        # Get historical data for the past week
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        metrics = get_historical_metrics(db, start_time, end_time)
        
        if not metrics:
            logger.warning("No historical data available for training")
            return False
        
        # Train models
        detector.train(metrics)
        return True
    except Exception as e:
        logger.error(f"Error training anomaly models: {e}")
        return False

def detect_anomalies(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Detect anomalies in network metrics"""
    return detector.detect_anomalies(metrics)

# Initialize models on import
if not detector.is_trained:
    try:
        train_anomaly_models()
    except Exception as e:
        logger.error(f"Error initializing anomaly models: {e}")

# For testing
if __name__ == "__main__":
    # Generate some test data
    import random
    
    test_metrics = []
    now = datetime.now()
    
    # Generate normal data
    for i in range(100):
        test_metrics.append({
            "timestamp": now - timedelta(minutes=i),
            "incoming_traffic": random.uniform(100, 200),
            "outgoing_traffic": random.uniform(80, 150),
            "active_connections": random.randint(100, 300),
            "average_latency": random.uniform(20, 50),
            "packet_loss": random.uniform(0, 1)
        })
    
    # Add some anomalies
    for i in range(5):
        test_metrics.append({
            "timestamp": now - timedelta(minutes=random.randint(0, 100)),
            "incoming_traffic": random.uniform(500, 1000),  # Much higher traffic
            "outgoing_traffic": random.uniform(400, 800),
            "active_connections": random.randint(800, 1000),
            "average_latency": random.uniform(20, 50),
            "packet_loss": random.uniform(0, 1)
        })
    
    for i in range(5):
        test_metrics.append({
            "timestamp": now - timedelta(minutes=random.randint(0, 100)),
            "incoming_traffic": random.uniform(100, 200),
            "outgoing_traffic": random.uniform(80, 150),
            "active_connections": random.randint(100, 300),
            "average_latency": random.uniform(200, 500),  # Much higher latency
            "packet_loss": random.uniform(5, 10)  # Much higher packet loss
        })
    
    # Train the model
    detector.train(test_metrics)
    
    # Test normal data
    normal_data = {
        "incoming_traffic": 150,
        "outgoing_traffic": 120,
        "active_connections": 200,
        "average_latency": 30,
        "packet_loss": 0.5
    }
    
    # Test traffic anomaly
    traffic_anomaly = {
        "incoming_traffic": 800,
        "outgoing_traffic": 600,
        "active_connections": 900,
        "average_latency": 30,
        "packet_loss": 0.5
    }
    
    # Test latency anomaly
    latency_anomaly = {
        "incoming_traffic": 150,
        "outgoing_traffic": 120,
        "active_connections": 200,
        "average_latency": 300,
        "packet_loss": 8
    }
    
    print("Normal data:", detector.detect_anomalies(normal_data))
    print("Traffic anomaly:", detector.detect_anomalies(traffic_anomaly))
    print("Latency anomaly:", detector.detect_anomalies(latency_anomaly))
