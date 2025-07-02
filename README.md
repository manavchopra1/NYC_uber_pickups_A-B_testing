# NYC Uber Pickups A/B Testing

**Author**: Manav Chopra  
**Date**: July 2024  
**Project**: Comprehensive A/B Testing Analysis of NYC Uber Pickup Patterns

## 🎯 Project Overview

This project conducts systematic A/B testing on NYC Uber pickup data to understand patterns, optimize operations, and drive business insights. The analysis focuses on three key dimensions: weather impact, temporal patterns, and geographic distribution.

## 📊 A/B Testing Experiments

### 1. **Rainy vs Clear Days** 🌧️☀️
- **Hypothesis**: Uber pickups are significantly higher on rainy days than on clear days
- **Treatment Group**: Rainy days (need to merge with NYC weather data)
- **Control Group**: Clear days
- **Metric**: Mean number of trips per hour/day
- **Test**: Two-sample t-test on daily ride counts
- **Business Relevance**: Helps Uber optimize surge pricing strategies

### 2. **Friday Night Effect** 🎉
- **Hypothesis**: Uber pickups are significantly higher on Friday 6 PM–12 AM compared to other weekday evenings
- **Treatment Group**: Friday evenings (6 PM – 12 AM)
- **Control Group**: Monday to Thursday evenings (6 PM – 12 AM)
- **Metric**: Average pickups per hour
- **Test**: t-test comparing hourly ride counts
- **Business Relevance**: Targeted driver deployment & promotions

### 3. **Manhattan vs Brooklyn Pickup Volume** 🗽
- **Hypothesis**: Pickup volume per square mile is higher in Manhattan than Brooklyn
- **Treatment Group**: Manhattan rides
- **Control Group**: Brooklyn rides
- **Metric**: Pickups per sq. mile or per zip code
- **Test**: t-test or rate comparison
- **Bonus**: Normalize by population or area size
- **Business Relevance**: Regional pricing, driver supply management

## 📁 Project Structure

```
NYC_uber_pickups_A-B_testing/
├── data/
│   ├── raw/           # Original CSV files (~20M records)
│   ├── processed/     # Cleaned and processed data
│   └── external/      # External data (weather, etc.)
├── notebooks/
│   └── 01_EDA_NYC_Uber_Dataset.ipynb  # Exploratory Data Analysis
├── src/
│   ├── analysis/      # A/B testing analysis modules
│   └── utils/
│       └── data_loader.py  # Data loading and preprocessing utilities
├── requirements.txt   # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- Required packages (see `requirements.txt`)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd NYC_uber_pickups_A-B_testing

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook
```

### Data Setup
The dataset contains over 20 million records across multiple ride-sharing services:
- **Uber data**: Monthly files from 2014-2015
- **Other services**: Lyft, Dial7, Carmel, American, etc.
- **Total size**: ~1.7GB of data

## 📈 Current Progress

### ✅ Completed
- [x] Dataset upload and organization
- [x] Exploratory Data Analysis (EDA)
- [x] Data preprocessing utilities
- [x] Feature engineering framework
- [x] Project structure setup

### 🔄 In Progress
- [ ] A/B Test 1: Rainy vs Clear Days (weather data integration needed)
- [ ] A/B Test 2: Friday Night Effect
- [ ] A/B Test 3: Manhattan vs Brooklyn

### 📋 Next Steps
1. Implement statistical testing framework
2. Create bootstrapping functions
3. Merge weather data for Test 1
4. Execute all three A/B tests with significance testing
5. Generate business recommendations

## 🔧 Key Features

- **Comprehensive EDA**: Detailed analysis of temporal and geographic patterns
- **Modular Design**: Reusable components for different A/B tests
- **Statistical Rigor**: Proper hypothesis testing and significance analysis
- **Business Focus**: Clear business impact and recommendations
- **Scalable**: Handles large datasets efficiently

## 📊 Initial Insights

From the EDA phase:
- **Peak hours**: Evening rush hours show highest activity
- **Weekend patterns**: Significantly higher weekend usage
- **Geographic distribution**: Manhattan dominates pickup volume
- **Friday effect**: Preliminary evidence of higher Friday evening activity

## 🎯 Business Impact

### Test 1: Weather Impact
- **Surge Pricing**: Optimize pricing during weather events
- **Driver Allocation**: Pre-position drivers before weather changes
- **Revenue Optimization**: Maximize earnings during high-demand periods

### Test 2: Friday Night Effect
- **Driver Scheduling**: Increase driver supply on Friday evenings
- **Promotional Campaigns**: Target Friday night promotions
- **Capacity Planning**: Optimize fleet allocation

### Test 3: Geographic Distribution
- **Regional Pricing**: Adjust pricing based on demand density
- **Driver Incentives**: Target incentives to underserved areas
- **Market Expansion**: Identify growth opportunities

## 🤝 Contributing

This is a personal project for A/B testing analysis. Feel free to use the code and methodology for your own analyses.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.