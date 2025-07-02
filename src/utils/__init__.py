"""
NYC Uber Pickups A/B Testing - Utilities Package
Author: Manav Chopra
Date: July 2024

This package contains utility modules for data loading, preprocessing, and analysis.
"""

from .data_loader import NYCUberDataLoader, load_sample_data, get_data_summary

__all__ = ['NYCUberDataLoader', 'load_sample_data', 'get_data_summary'] 