#!/bin/bash

TEST_FILES=(
    test_view.py
    test_model.py
    test_controller.py
)

for i in "${TEST_FILES[@]}"; do
    $PYTHON -m pytest test/$i -vv
done
