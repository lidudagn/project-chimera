#!/bin/bash
echo "=========================================="
echo "Running Project Chimera Test Suite"
echo "=========================================="

echo -e "\n🔧 Unit Tests:"
echo "----------------"
pytest tests/unit/ -v --tb=short 2>&1 | tail -20

echo -e "\n🔗 Integration Tests:"
echo "---------------------"
pytest tests/integration/ -v --tb=short 2>&1 | tail -10

echo -e "\n⚡ Performance Tests:"
echo "----------------------"
pytest tests/performance/ -v --tb=short 2>&1 | tail -15

echo -e "\n🚨 Error & Recovery Tests:"
echo "--------------------------"
pytest tests/error_recovery/ -v --tb=short 2>&1 | tail -10

echo -e "\n👤 HITL Validation Tests:"
echo "--------------------------"
pytest tests/hitl/ -v --tb=short 2>&1 | tail -10

echo -e "\n=========================================="
echo "All Test Categories Complete!"
echo "=========================================="
