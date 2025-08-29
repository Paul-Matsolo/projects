# Maritime Dashboard - Deployment Guide

This guide provides multiple deployment options for the Maritime Risk Dashboard.

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended for Data Science)

**Pros:**
- Free hosting
- Perfect for data science applications
- Easy deployment
- Built-in caching and performance optimizations

**Steps:**
1. Install Streamlit: `pip install streamlit`
2. Run locally: `streamlit run streamlit_app.py`
3. Deploy to Streamlit Cloud:
   - Push to GitHub
   - Connect to Streamlit Cloud
   - Deploy automatically

**Requirements:** `requirements_streamlit.txt`

### 2. Docker Deployment

**Pros:**
- Consistent environment
- Easy scaling
- Works on any platform
- Good for production

**Steps:**
1. Build image: `docker build -t maritime-dashboard .`
2. Run container: `docker run -p 8050:8050 maritime-dashboard`
3. Or use docker-compose: `docker-compose up`

**Files:** `Dockerfile`, `docker-compose.yml`

### 3. Heroku

**Pros:**
- Free tier available
- Easy deployment
- Good for small to medium applications

**Steps:**
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: python Main.py
   ```
3. Deploy: `heroku create && git push heroku main`

### 4. Railway

**Pros:**
- Modern platform
- Easy deployment
- Good free tier
- Automatic deployments

**Steps:**
1. Connect GitHub repository
2. Railway will auto-detect Python app
3. Deploy automatically

### 5. Google Cloud Run

**Pros:**
- Serverless
- Pay per use
- Scalable
- Good for production

**Steps:**
1. Build and push to Google Container Registry
2. Deploy to Cloud Run
3. Set environment variables

### 6. AWS Elastic Beanstalk

**Pros:**
- Managed service
- Auto-scaling
- Good for production workloads

**Steps:**
1. Create application
2. Upload code or connect Git
3. Configure environment

## 📁 File Structure

```
maritime-project/
├── Main.py                    # Dash application
├── streamlit_app.py           # Streamlit version
├── data_cleaner.py            # Data processing
├── *.py                       # Chart modules
├── requirements.txt           # Dash dependencies
├── requirements_streamlit.txt # Streamlit dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose
├── pyproject.toml            # Project metadata
└── DEPLOYMENT.md             # This file
```

## 🔧 Local Development

### Dash Version
```bash
pip install -r requirements.txt
python Main.py
```

### Streamlit Version
```bash
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
```

### Docker Version
```bash
docker-compose up
```

## 🌐 Access URLs

- **Dash App**: http://localhost:8050
- **Streamlit App**: http://localhost:8501
- **Docker**: http://localhost:8050

## 📊 Performance Tips

1. **Data Caching**: Both Dash and Streamlit have built-in caching
2. **Lazy Loading**: Load data only when needed
3. **Optimized Queries**: Use efficient pandas operations
4. **Memory Management**: Clear cache periodically

## 🔒 Security Considerations

1. **Environment Variables**: Store sensitive data in env vars
2. **HTTPS**: Use HTTPS in production
3. **Authentication**: Add auth if needed
4. **Rate Limiting**: Implement rate limiting for public deployments

## 📈 Monitoring

1. **Logs**: Monitor application logs
2. **Metrics**: Track performance metrics
3. **Errors**: Set up error tracking
4. **Uptime**: Monitor application availability

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change port in application
   - Kill existing process

2. **Memory Issues**
   - Optimize data loading
   - Use smaller datasets for testing

3. **Import Errors**
   - Check Python version compatibility
   - Install missing dependencies

4. **Docker Issues**
   - Check Docker daemon is running
   - Verify Dockerfile syntax

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review error logs
3. Test locally first
4. Verify all dependencies are installed
