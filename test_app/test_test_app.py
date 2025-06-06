#!/usr/bin/env python3
"""
Tests for the SRE learning application
"""

import pytest
import json
from test_app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'timestamp' in data
    assert 'version' in data


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code in [200, 503]  # Can be healthy or degraded
    
    data = json.loads(response.data)
    assert 'status' in data
    assert 'timestamp' in data
    assert 'uptime_seconds' in data


def test_metrics_endpoint(client):
    """Test the metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'requests_total' in data
    assert 'errors_total' in data
    assert 'uptime_seconds' in data
    assert 'status' in data


def test_simulate_error_endpoint(client):
    """Test the error simulation endpoint"""
    response = client.get('/simulate-error')
    assert response.status_code == 500
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'timestamp' in data


def test_load_test_endpoint(client):
    """Test the load test endpoint"""
    response = client.get('/load-test')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'processing_time_seconds' in data
    assert 'timestamp' in data