from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from scipy import ndimage

app = Flask(__name__)

# ============================================================================
# ADVANCED OPTIMIZED SKETCH ALGORITHM
# Removes random lines while preserving all features
# ============================================================================

def create_advanced_sketch(img):
    """
    ADVANCED OPTIMIZATION:
    - Complete edge detection
    - Intelligent noise removal (removes random lines)
    - Preserves all important features
    """
    
    # --- STAGE 1: OPTIMIZED PRE-PROCESSING ---
    print("  [1/6] Optimized preprocessing...")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Non-Local Means Denoising for texture smoothing
    denoised = cv2.fastNlMeansDenoising(gray, None, h=8, templateWindowSize=7, searchWindowSize=21)
    
    # Light bilateral filter
    smooth = cv2.bilateralFilter(denoised, d=7, sigmaColor=60, sigmaSpace=60)
    
    # --- STAGE 2: MULTI-METHOD EDGE DETECTION ---
    print("  [2/6] Multi-method edge detection...")
    
    # METHOD 1: Canny with balanced thresholds
    canny = cv2.Canny(smooth, threshold1=15, threshold2=50, apertureSize=3)
    
    # METHOD 2: Sobel
    sobelx = cv2.Sobel(smooth, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(smooth, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobelx**2 + sobely**2)
    sobel = np.uint8(sobel / sobel.max() * 255)
    _, sobel_binary = cv2.threshold(sobel, 35, 255, cv2.THRESH_BINARY)
    
    # COMBINE edge methods
    combined_edges = np.maximum(canny, sobel_binary)
    
    # Invert for white background
    edges_inv = 255 - combined_edges
    
    # --- STAGE 3: ADVANCED FILTERING (Remove Random Lines) ---
    print("  [3/6] Advanced filtering (removing random lines)...")
    
    # Find all blobs
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        255 - edges_inv, connectivity=8
    )
    
    # Analyze image density for context
    height, width = edges_inv.shape
    image_area = height * width
    
    clean_mask = np.zeros_like(edges_inv)
    kept_blobs = 0
    removed_random = 0
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], \
                     stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        
        # INTELLIGENT FILTERING CRITERIA
        
        # 1. Remove very tiny specks
        if area < 10:
            removed_random += 1
            continue
        
        # 2. Check aspect ratio - remove extremely thin isolated lines
        aspect_ratio = max(w, h) / (min(w, h) + 1)
        
        # 3. Check density - calculate how "filled" the bounding box is
        density = area / (w * h)
        
        # 4. Check if line is too isolated (random noise tends to be isolated)
        # Extract region around blob
        margin = 20
        y1 = max(0, y - margin)
        y2 = min(height, y + h + margin)
        x1 = max(0, x - margin)
        x2 = min(width, x + w + margin)
        
        region = 255 - edges_inv[y1:y2, x1:x2]
        region_pixels = np.sum(region > 0)
        blob_pixels = area
        neighbor_pixels = region_pixels - blob_pixels
        
        # If blob is very isolated (few neighbors), it might be noise
        isolation_ratio = neighbor_pixels / (blob_pixels + 1)
        
        # DECISION LOGIC
        keep_blob = True
        
        # Remove if: very thin AND very isolated
        if aspect_ratio > 80 and isolation_ratio < 0.3 and area < 100:
            keep_blob = False  # Random thin line
            removed_random += 1
        
        # Remove if: extremely thin thread
        elif aspect_ratio > 150 and area < 200:
            keep_blob = False  # Thread-like noise
            removed_random += 1
        
        # Remove if: very low density (sparse pixels in bbox)
        elif density < 0.05 and area < 50:
            keep_blob = False  # Sparse noise
            removed_random += 1
        
        if keep_blob:
            clean_mask[labels == i] = 255
            kept_blobs += 1
    
    print(f"       Removed {removed_random} random lines, kept {kept_blobs} features")
    
    # --- STAGE 4: MORPHOLOGICAL ENHANCEMENT ---
    print("  [4/6] Line enhancement...")
    
    # Close small gaps
    kernel_close = np.ones((2, 2), np.uint8)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    
    # Remove small artifacts created by closing
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel_open, iterations=1)
    
    # --- STAGE 5: SECONDARY CLEANUP ---
    print("  [5/6] Secondary cleanup...")
    
    # One more connected components pass
    num_labels2, labels2, stats2, _ = cv2.connectedComponentsWithStats(
        clean_mask, connectivity=8
    )
    
    final_mask = np.zeros_like(clean_mask)
    
    for i in range(1, num_labels2):
        area = stats2[i, cv2.CC_STAT_AREA]
        if area > 12:  # Remove very small artifacts
            final_mask[labels2 == i] = 255
    
    # --- STAGE 6: FINAL POLISH ---
    print("  [6/6] Final polish...")
    
    # Slight dilation for visibility
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    final_mask = cv2.dilate(final_mask, kernel_dilate, iterations=1)
    
    # Convert back to black lines on white
    final_sketch = cv2.bitwise_not(final_mask)
    
    print("  ✅ Advanced sketch complete!")
    return final_sketch

def vectorize_sketch(binary_sketch):
    """
    Convert sketch to SVG with ACCURATE continuous strokes
    Uses advanced curve-fitting for smooth, natural lines
    """
    print("  📐 Converting to accurate SVG paths...")
    
    # Find contours with improved approximation algorithm
    contours, _ = cv2.findContours(
        255 - binary_sketch,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_TC89_KCOS  # Better curve approximation
    )
    
    svg_paths = []
    total_points = 0
    
    for contour in contours:
        # Skip very small contours
        if len(contour) < 4:
            continue
        
        # Calculate perimeter for adaptive epsilon
        perimeter = cv2.arcLength(contour, closed=False)
        
        # Very small perimeter = likely noise or artifact
        if perimeter < 10:
            continue
        
        # Adaptive epsilon based on perimeter
        # Smaller epsilon for larger contours (more detail)
        if perimeter > 200:
            epsilon = 0.001 * perimeter  # Very detailed
        elif perimeter > 100:
            epsilon = 0.002 * perimeter  # Detailed
        elif perimeter > 50:
            epsilon = 0.003 * perimeter  # Moderate
        else:
            epsilon = 0.005 * perimeter  # Simplified
        
        # Apply Douglas-Peucker algorithm
        approx = cv2.approxPolyDP(contour, epsilon, closed=False)
        
        # Need at least 2 points for a line
        if len(approx) < 2:
            continue
        
        # Convert to simple array
        points = approx.reshape(-1, 2)
        total_points += len(points)
        
        # Create smooth SVG path
        if len(points) == 2:
            # Simple line
            x1, y1 = points[0]
            x2, y2 = points[1]
            path = f'M {x1} {y1} L {x2} {y2}'
        
        elif len(points) == 3:
            # Three points - use quadratic Bezier
            x1, y1 = points[0]
            cx, cy = points[1]
            x2, y2 = points[2]
            path = f'M {x1} {y1} Q {cx} {cy} {x2} {y2}'
        
        else:
            # Multiple points - create smooth curve
            path_parts = [f'M {points[0][0]} {points[0][1]}']
            
            # Use quadratic Bezier curves for smoothness
            i = 1
            while i < len(points) - 1:
                # Control point
                cx, cy = points[i]
                
                # End point (midpoint to next, or final point)
                if i + 1 < len(points) - 1:
                    # Midpoint between current and next
                    ex = (points[i][0] + points[i + 1][0]) // 2
                    ey = (points[i][1] + points[i + 1][1]) // 2
                else:
                    # Final point
                    ex, ey = points[i + 1]
                
                path_parts.append(f'Q {cx} {cy} {ex} {ey}')
                i += 1
            
            # Add final point if needed
            if i == len(points) - 1:
                path_parts.append(f'L {points[-1][0]} {points[-1][1]}')
            
            path = ' '.join(path_parts)
        
        svg_paths.append(path)
    
    print(f"  ✅ Generated {len(svg_paths)} smooth paths ({total_points} points)")
    return svg_paths

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        print("\n" + "=" * 60)
        print("PROCESSING IMAGE - ADVANCED MODE")
        print("=" * 60)
        
        # Resize if needed
        height, width = img.shape[:2]
        max_width = 800
        
        if width > max_width:
            scale = max_width / width
            new_width = max_width
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height),
                           interpolation=cv2.INTER_LANCZOS4)
            print(f"Resized to {new_width}x{new_height}")
        
        height, width = img.shape[:2]
        
        # Create advanced sketch
        sketch = create_advanced_sketch(img)
        
        # Measure coverage
        total_pixels = sketch.shape[0] * sketch.shape[1]
        black_pixels = np.sum(sketch == 0)
        coverage = (black_pixels / total_pixels) * 100
        
        # Vectorize
        svg_paths = vectorize_sketch(sketch)
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETE!")
        print(f"   Coverage: {coverage:.1f}%")
        print(f"   Paths: {len(svg_paths)}")
        print("=" * 60 + "\n")
        
        svg_data = {
            'width': width,
            'height': height,
            'viewBox': f'0 0 {width} {height}',
            'paths': svg_paths,
            'method': f'Advanced Clean ({coverage:.1f}%)'
        }
        
        return jsonify(svg_data)
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎨 LIVE PENCIL SKETCH - ADVANCED EDITION")
    print("=" * 60)
    print("Advanced Intelligent Filtering:")
    print("  • Non-Local Means + Bilateral denoising")
    print("  • Dual edge detection (Canny + Sobel)")
    print("  • Intelligent noise removal:")
    print("    - Aspect ratio analysis (removes thin threads)")
    print("    - Density analysis (removes sparse noise)")
    print("    - Isolation analysis (removes lonely lines)")
    print("    - Context-aware decision making")
    print("  • Morphological enhancement")
    print("  • Multi-pass cleanup")
    print("")
    print("Result: Complete sketches WITHOUT random lines")
    print("=" * 60)
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Disable debug in production
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"📍 Server: http://0.0.0.0:{port}")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
