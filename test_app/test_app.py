#!/usr/bin/env python3
"""
Simple Flask application for SRE learning
Demonstrates basic monitoring, health checks, and metrics
"""

from flask import Flask, jsonify, request
import time
import random
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Simple in-memory metrics store
metrics = {
    "requests_total": 0,
    "errors_total": 0,
    "start_time": time.time(),
    "status": "healthy"
}


@app.route('/')
def home():
    """Main endpoint"""
    metrics["requests_total"] += 1
    logger.info(f"Request to / from {request.remote_addr}")
    
    return jsonify({
        "message": "Hello from SRE Learning App!",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    metrics["requests_total"] += 1
    
    # Simulate occasional health issues for learning
    if random.random() < 0.1:  # 10% chance of reporting unhealthy
        metrics["status"] = "degraded"
        return jsonify({
            "status": "degraded",
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": "down",
                "cache": "ok"
            }
        }), 503
    
    metrics["status"] = "healthy"
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": time.time() - metrics["start_time"],
        "checks": {
            "database": "ok",
            "cache": "ok"
        }
    })


@app.route('/metrics')
def get_metrics():
    """Prometheus-style metrics endpoint"""
    metrics["requests_total"] += 1
    
    uptime = time.time() - metrics["start_time"]
    
    return jsonify({
        "requests_total": metrics["requests_total"],
        "errors_total": metrics["errors_total"],
        "uptime_seconds": uptime,
        "status": metrics["status"],
        "memory_usage_mb": random.randint(50, 150),  # Simulated
        "cpu_usage_percent": random.randint(5, 25)   # Simulated
    })


@app.route('/simulate-error')
def simulate_error():
    """Endpoint to simulate errors for testing monitoring"""
    metrics["requests_total"] += 1
    metrics["errors_total"] += 1
    
    logger.error("Simulated error occurred")
    
    return jsonify({
        "error": "Simulated error for testing",
        "timestamp": datetime.now().isoformat(),
        "error_code": 500
    }), 500


@app.route('/load-test')
def load_test():
    """Endpoint to simulate load for testing"""
    metrics["requests_total"] += 1
    
    # Simulate some processing time
    processing_time = random.uniform(0.1, 2.0)
    time.sleep(processing_time)
    
    return jsonify({
        "message": "Load test completed",
        "processing_time_seconds": processing_time,
        "timestamp": datetime.now().isoformat()
    })


if __name__ == '__main__':
    logger.info("Starting SRE Learning Application")
    app.run(host='0.0.0.0', port=5000, debug=False)