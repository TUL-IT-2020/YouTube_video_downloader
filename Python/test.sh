#!/bin/bash
clear
coverage run -m py.test
coverage report -m