# 🚀 Render Deployment Guide - Social Engineering Awareness Program

## 📋 Optimal Render Settings

### 1. **Service Configuration**

#### **Basic Settings**
- **Name**: `social-engineering-awareness` (or your preferred name)
- **Environment**: `Web Service`
- **Region**: Choose closest to your users (e.g., `Oregon (US West)` for US users)
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repository)

#### **Build & Deploy Settings**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100`
- **Auto-Deploy**: ✅ Enabled

### 2. **Environment Variables**

Set these in Render Dashboard → Your Service → Environment:

#### **Required Variables**
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
RENDER=true
```

#### **Database Persistence (CRITICAL)**
```
DATABASE_URL=postgresql://username:password@host:port/database
```
**Important:** Add a PostgreSQL database to your Render service for data persistence!

#### **Optional Variables (Recommended)**
```
ADMIN_EMAIL=admin@mmdc.edu.ph
ADMIN_PASSWORD=your-secure-admin-password
LOG_LEVEL=INFO
```

#### **Email Configuration (if using password reset)**
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 3. **Database Setup (CRITICAL FOR DATA PERSISTENCE)**

#### **Add PostgreSQL Database**
1. **Create Database Service:**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `social-engineering-db`
   - Plan: Free (for testing) or Starter (for production)
   - Region: Same as your web service

2. **Get Database URL:**
   - After creation, go to your database service
   - Copy the "External Database URL"
   - Format: `postgresql://username:password@host:port/database`

3. **Set Environment Variable:**
   - Go to your web service settings
   - Add environment variable: `DATABASE_URL`
   - Value: The PostgreSQL URL from step 2

#### **Why This is Critical:**
- **Without PostgreSQL:** Data gets wiped on every deployment
- **With PostgreSQL:** User accounts, progress, and admin credentials persist
- **Admin Access:** Ensures admin user always exists after deployments

### 4. **Resource Allocation**

#### **Free Tier (Recommended for Testing)**
- **Instance Type**: Free
- **Memory**: 512 MB
- **CPU**: Shared
- **Bandwidth**: 100 GB/month

#### **Paid Tier (Recommended for Production)**
- **Instance Type**: Starter ($7/month)
- **Memory**: 512 MB
- **CPU**: 0.1 CPU
- **Bandwidth**: 100 GB/month

### 4. **Health Check Configuration**

#### **Health Check Settings**
- **Path**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Grace Period**: 60 seconds
- **Max Consecutive Failures**: 3

### 5. **Custom Domain (Optional)**

#### **Domain Configuration**
- **Custom Domain**: `your-domain.com`
- **SSL Certificate**: Auto-provisioned by Render
- **Force HTTPS**: ✅ Enabled

## 🔧 Performance Optimizations

### **Gunicorn Settings Explained**
```bash
gunicorn app:app \
  --bind 0.0.0.0:$PORT \     # Bind to all interfaces on Render's PORT
  --workers 2 \              # 2 worker processes (optimal for 512MB RAM)
  --timeout 120 \            # 2-minute timeout for long operations
  --keep-alive 5 \           # Keep connections alive for 5 seconds
  --max-requests 1000 \      # Restart workers after 1000 requests
  --max-requests-jitter 100  # Add randomness to prevent thundering herd
```

### **Database Optimizations**
- **SQLite with Ephemeral Storage**: Data resets on restart (Render limitation)
- **Connection Pooling**: Configured for optimal performance
- **Pre-ping**: Validates connections before use

### **Security Enhancements**
- **HTTPS Only**: Enforced in production
- **Security Headers**: XSS protection, content type options
- **Session Security**: Secure cookies, HTTP-only, SameSite
- **CSRF Protection**: Enabled for forms

## 📊 Monitoring & Logs

### **Accessing Logs**
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. View real-time logs or download log files

### **Key Metrics to Monitor**
- **Response Time**: Should be < 2 seconds
- **Error Rate**: Should be < 1%
- **Memory Usage**: Should stay under 400MB
- **CPU Usage**: Should be < 80%

### **Health Check Monitoring**
- **Endpoint**: `https://your-app.onrender.com/health`
- **Expected Response**: `{"status": "healthy", "timestamp": "..."}`
- **Monitoring**: Set up alerts for failed health checks

## 🚨 Troubleshooting

### **Common Issues & Solutions**

#### **1. Build Failures**
```bash
# Check if all dependencies are in requirements.txt
pip freeze > requirements.txt
```

#### **2. Runtime Errors**
```bash
# Check logs in Render Dashboard
# Common issues: missing environment variables, database errors
```

#### **3. Performance Issues**
```bash
# Reduce workers if memory issues
--workers 1

# Increase timeout if needed
--timeout 300
```

#### **4. Database Issues**
- **SQLite Limitations**: Data resets on restart
- **Solution**: Consider PostgreSQL for persistent data
- **Migration**: Use Render's PostgreSQL service

### **Debug Mode (Temporary)**
```bash
# Set in environment variables
FLASK_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🔄 Deployment Workflow

### **1. Initial Deployment**
1. Connect GitHub repository
2. Configure environment variables
3. Deploy and test health endpoint
4. Verify all functionality

### **2. Updates & Maintenance**
1. Push changes to `main` branch
2. Render auto-deploys
3. Monitor deployment logs
4. Test critical functionality

### **3. Rollback Strategy**
1. Use Git tags for releases
2. Rollback to previous commit if needed
3. Monitor logs for issues

## 📈 Scaling Considerations

### **When to Upgrade**
- **Memory Usage**: > 400MB consistently
- **Response Time**: > 3 seconds average
- **Error Rate**: > 5%
- **User Load**: > 100 concurrent users

### **Upgrade Path**
1. **Free → Starter**: $7/month
2. **Starter → Standard**: $25/month
3. **Standard → Pro**: $100/month

## 🔐 Security Checklist

### **Pre-Deployment**
- [ ] Strong SECRET_KEY set
- [ ] Admin password changed
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Session security enabled

### **Post-Deployment**
- [ ] Health check working
- [ ] All routes accessible
- [ ] Admin panel secured
- [ ] File uploads working
- [ ] Email functionality tested

## 📞 Support & Resources

### **Render Documentation**
- [Render Docs](https://render.com/docs)
- [Flask Deployment](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)

### **Application Support**
- **Health Check**: `/health`
- **Admin Panel**: `/login` (use admin credentials)
- **Logs**: Render Dashboard → Logs tab

---

**🎯 This configuration provides optimal performance, security, and reliability for your Social Engineering Awareness Program on Render!**
