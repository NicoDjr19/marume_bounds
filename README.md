# Marume Bounds

**Mathematical bounds that make Bézier curve intersection 20x faster and robotics collision detection 2x faster.**

## Results

| Application | Speedup |
|-------------|---------|
| Graphics (Bézier Curves) | **20.37x** |
| Robotics Collision Detection | **2.03x** |

## Run the Demos

```bash
pip install numpy matplotlib scipy
python bezier_demo.py
python robotics_demo.py

## Mobile/Embedded Performance Results

| Scenario | Speedup |
|----------|---------|
| Font Outline (TrueType) | **12.04x** |
| UI Easing (iOS/Android) | **3.16x** |
| SVG Path Rendering | **32.17x** |
| NURBS Surface (3D) | **10.39x** |
| Real Font Glyph | **11.53x** |
| Complex Animation | **17.34x** |

**Average speedup: 14.44x**

### Key Insights
- No numpy required (pure C/embedded ready)
- Works on real-world mobile scenarios
- Translates to ~11% battery savings on smartphones

### Run the Tests Yourself
```bash
python mobile_embedded_test.py