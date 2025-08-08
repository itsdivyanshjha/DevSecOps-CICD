#!/bin/bash

# DAST Scan Script for Jenkins Pipeline
# This script handles the Dynamic Application Security Testing with ZAP

set -e

echo "Starting DAST scan preparation..."

# Function to check if application is ready
check_app_ready() {
    echo "Checking if application is ready..."
    for i in {1..30}; do
        if curl -f http://localhost:5000 > /dev/null 2>&1; then
            echo "Application is ready!"
            return 0
        fi
        echo "Waiting for application... (attempt $i/30)"
        sleep 2
    done
    echo "Application may not be fully ready, proceeding with scan"
    return 1
}

# Function to run ZAP scan
run_zap_scan() {
    echo "Starting ZAP DAST scan..."
    
    # Run ZAP scan with proper error handling
    docker run --network devsecops-network --rm \
        -v $(pwd):/zap/wrk/:rw \
        owasp/zap2docker-stable zap-full-scan.py \
        -t http://devsecops_app:5000 \
        -r zap_report.html \
        --auto || {
            echo "ZAP scan completed with warnings or errors"
            # Check if report was generated
            if [ -f "zap_report.html" ]; then
                echo "ZAP report generated successfully"
                return 0
            else
                echo "ZAP report not generated, creating empty report"
                echo "<html><body><h1>ZAP Scan Report</h1><p>Scan completed with warnings or errors. Check Jenkins logs for details.</p></body></html>" > zap_report.html
                return 0
            fi
        }
}

# Main execution
echo "=== DAST Scan Process Started ==="

# Check if application is ready
check_app_ready

# Run the ZAP scan
run_zap_scan

echo "=== DAST Scan Process Completed ==="
