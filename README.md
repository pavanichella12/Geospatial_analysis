# 🔥 Advanced Wildfire Analysis Dashboard

A comprehensive geospatial analysis project using USFS wildfire data to demonstrate advanced data science and geospatial analysis skills.

## 🎯 Project Overview

This project showcases advanced geospatial analysis capabilities using real USFS wildfire data, featuring interactive visualizations, spatial analysis, and comprehensive insights into wildfire patterns across the United States.

## 🚀 Key Features

### 📊 Advanced Analysis
- **Fire Severity Analysis**: Large fires, mega fires, and statistical breakdowns
- **Temporal Trends**: Yearly fire patterns and acreage analysis
- **Spatial Distribution**: Interactive maps with all wildfire locations
- **Cause Analysis**: Natural vs human causes with detailed breakdowns
- **Geographic Insights**: State-wise analysis and geographic patterns

### 🗺️ Interactive Visualizations
- **Interactive Maps**: Filter by year, fire size, and sample size
- **Pie Charts**: Fire causes and category distributions
- **Line Charts**: Temporal trends and fire patterns
- **Bar Charts**: Geographic and cause-based distributions
- **Heatmaps**: Cause vs size relationships

### 🎛️ Advanced Controls
- **Sample Size Control**: Adjust map performance (100-10,000 points)
- **Fire Size Filters**: Small, Medium, Large, Very Large, Mega fires
- **Year Filters**: Filter by specific years or view all data
- **Real-time Updates**: Dynamic filtering and visualization

## 📁 Project Structure

```
wildfire/
├── advanced_wildfire_analysis.py    # Main application
├── requirements.txt                  # Python dependencies
├── secrets.toml                     # AWS credentials (local only)
├── README.md                        # Project documentation
├── PROJECT_SUMMARY.md               # Technical summary
├── CLOUD_DEPLOYMENT_SETUP.md       # Deployment guide
├── .streamlit/                      # Streamlit configuration
├── data/                           # Data directory (gitignored)
└── wildfire_env/                   # Python virtual environment
```

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **GeoPandas**: Geospatial data handling
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Boto3**: AWS S3 integration
- **AWS S3**: Cloud data storage

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wildfire
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv wildfire_env
   source wildfire_env/bin/activate  # On Windows: wildfire_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   - Create `.streamlit/secrets.toml` with your AWS credentials
   - Or use the provided `secrets.toml` for testing

5. **Run the application**
   ```bash
   streamlit run advanced_wildfire_analysis.py
   ```

6. **Access the dashboard**
   - Open http://localhost:8501 in your browser

### Cloud Deployment

See `CLOUD_DEPLOYMENT_SETUP.md` for detailed deployment instructions to Streamlit Cloud.

## 📊 Analysis Sections

### 🔥 Advanced Overview
- Key metrics and statistics
- Fire severity analysis
- Temporal trends with line charts
- Advanced insights and patterns

### 🔥 Advanced Causes Analysis
- Fire causes distribution (pie charts)
- Cause categories (Natural vs Human)
- Detailed cause breakdown table
- Cause vs size heatmap analysis

### 🗺️ Advanced Spatial Analysis
- Interactive fire map with all data points
- Geographic distribution analysis
- Spatial filtering controls
- Geographic insights and patterns

## 🎯 Key Insights

- **Data Coverage**: Nationwide USFS wildfire data
- **Temporal Range**: Historical wildfire records
- **Spatial Coverage**: All US states with wildfire activity
- **Analysis Depth**: Fire causes, sizes, geographic patterns
- **Interactive Features**: Real-time filtering and visualization

## 📈 Performance Features

- **Caching**: Optimized data loading with Streamlit caching
- **Sampling**: Configurable sample sizes for map performance
- **Filtering**: Real-time data filtering without reloading
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Configuration

### AWS S3 Setup
The application loads wildfire data from AWS S3. Configure your credentials in `.streamlit/secrets.toml`:

```toml
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET_NAME = "your_bucket_name"
S3_OBJECT_KEY = "your_file_path"
```

### Streamlit Configuration
Custom configuration in `.streamlit/config.toml`:
- Server settings
- Browser options
- Performance optimizations

## 📚 Documentation

- **README.md**: Project overview and setup
- **PROJECT_SUMMARY.md**: Technical implementation details
- **CLOUD_DEPLOYMENT_SETUP.md**: Deployment instructions

## 🤝 Contributing

This project demonstrates advanced geospatial analysis skills for portfolio purposes. The code is well-documented and follows best practices for maintainability and scalability.

## 📄 License

This project is for educational and portfolio purposes, showcasing geospatial analysis and data science skills.

---

**Built with ❤️ for advanced geospatial analysis and data visualization** 