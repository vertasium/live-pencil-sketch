# Live Pencil Sketch 🎨

Transform your photos into beautiful animated line art sketches with AI-powered edge detection!

![Live Pencil Sketch Demo](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)

## ✨ Features

- **Advanced Edge Detection**: Multi-method edge detection (Canny + Sobel) with intelligent noise removal
- **Smooth Animation**: Beautiful pencil drawing animation with optimized speed
- **Smart Processing**: 
  - Non-Local Means denoising
  - Bilateral filtering
  - Connected component analysis
  - Aspect ratio & density filtering
- **Professional Output**: Clean, detailed sketches with continuous strokes

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/live-pencil-sketch.git
   cd live-pencil-sketch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🌐 Deploy to Web

### Option 1: Deploy to Render (Recommended - FREE)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/live-pencil-sketch.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free
   - Click "Create Web Service"

### Option 2: Deploy to Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

### Option 3: Deploy to Heroku

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

## 📁 Project Structure

```
live-pencil-sketch/
├── app.py                 # Flask backend with edge detection
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── runtime.txt           # Python version
├── templates/
│   └── index.html        # Frontend with animation
├── static/
│   └── pencil_icon.png   # Pencil cursor icon
└── README.md
```

## 🛠️ Technical Details

### Edge Detection Algorithm

1. **Pre-processing**
   - Non-Local Means Denoising (h=8)
   - Bilateral Filter (d=7, sigma=60)

2. **Edge Detection**
   - Canny (thresholds: 15-50)
   - Sobel (threshold: 35)
   - Combined output

3. **Noise Removal**
   - Connected component analysis
   - Aspect ratio filtering (<100)
   - Density analysis (>0.05)
   - Isolation analysis (20px margin)

4. **Morphological Enhancement**
   - Closing (2 iterations)
   - Opening (1 iteration)
   - Dilation for visibility

5. **Vectorization**
   - Adaptive epsilon (0.001-0.005×)
   - Bezier curve smoothing
   - Optimized path generation

### Animation System

- **Duration**: 500-2000ms (based on path length)
- **Sequential drawing**: Long paths (>100px)
- **Batched drawing**: Small paths (<80px, max 2 parallel)
- **Stroke dasharray** animation for smooth effect

## 🔧 Configuration

### Adjust Animation Speed

Edit `templates/index.html`, line ~290:

```javascript
// Slower: increase multiplier and max duration
const duration = Math.min(3000, Math.max(800, pathLength * 3));

// Faster: decrease multiplier and max duration  
const duration = Math.min(1500, Math.max(300, pathLength * 1.5));
```

### Adjust Edge Sensitivity

Edit `app.py`:

```python
# More edges (line ~35):
edges = cv2.Canny(smooth, threshold1=10, threshold2=40)

# Fewer edges (line ~35):
edges = cv2.Canny(smooth, threshold1=25, threshold2=70)
```

## 📦 Dependencies

- Flask 2.0+
- OpenCV 4.5+
- NumPy 1.21+
- SciPy 1.7+

## 🎯 Performance

- **Processing Time**: 2-5 seconds (depending on image size)
- **Max Image Size**: 800px width (auto-resized)
- **Supported Formats**: JPG, PNG, GIF, WebP

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 👤 Author

**Abhishek**

---

**⭐ Star this repo if you found it useful!**
