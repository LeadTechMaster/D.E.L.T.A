# 🧪 D.E.L.T.A 2 Demo Instructions

**How to test the new UI components with real backend data**

---

## 🚀 **Quick Start**

### **Step 1: Start Backend API Server**

Open a PowerShell window:
```powershell
cd backend
node real_api_server_final.js
```

You should see:
```
🚀 D.E.L.T.A 2 REAL API Server running on port 8001
✅ REAL API INTEGRATION ONLY - NO MOCK DATA
🌐 Available at: http://localhost:8001
📊 APIs: Census, Google Places, SerpAPI, Mapbox
```

---

### **Step 2: Start Frontend Demo**

Open **another** PowerShell window:
```powershell
cd frontend
npm run dev
```

You should see:
```
VITE ready in X ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

### **Step 3: Open Demo Page**

**Option A - Demo Page (Recommended):**
Open your browser to:
```
http://localhost:5173/demo.html
```

**Option B - Original App:**
```
http://localhost:5173/
```
(This still has the old UI with Material-UI)

---

## ✅ **What to Test**

### **1. SearchBar Component**
- **Location**: Top center of the page
- **Try it**:
  - Type "94103" (ZIP code) → See autocomplete suggestions
  - Type "San Francisco" → See location suggestions
  - Type "Seattle, WA" → See location suggestions
  - Click any suggestion → See coordinates displayed below

**Expected**: 
- ✅ Search input with glassmorphism design
- ✅ Cyan glow on focus
- ✅ Autocomplete dropdown appears
- ✅ ZIP codes are detected and handled specially
- ✅ Selected location displays below the map placeholder

---

### **2. FloatingMenu Component**
- **Location**: Left side, top of page
- **Try it**:
  - Hover over each icon → See tooltips
  - Click "Demographics" icon (Users) → Opens Demographics panel
  - Click other icons → Shows "Coming Soon" placeholder

**Expected**:
- ✅ 5 menu items in horizontal bar
- ✅ Icons with hover effects (cyan glow)
- ✅ Tooltips with descriptions
- ✅ Active state highlighting

**Menu Items**:
1. 👥 Demographics (working!)
2. 📍 Points of Interest (placeholder)
3. 🏢 Administrative (placeholder)
4. 💾 Custom Metrics (placeholder)
5. 📈 Demand Research (placeholder)

---

### **3. DemographicsPanel Component** ⭐
- **Location**: Right side panel (slides in when opened)
- **Try it**:
  1. Search for "94103" in SearchBar
  2. Click Demographics icon in FloatingMenu
  3. Watch panel slide in from right
  4. See **REAL Census data** loading

**Expected**:
- ✅ Panel slides in smoothly
- ✅ Loading spinner appears
- ✅ Real data populates from backend:
  - Population: 42,319
  - Median Income: $98,237
  - Median Home Value: $987,654
  - Housing Units: (varies)
- ✅ Age distribution bars
- ✅ Housing statistics
- ✅ Data source attribution at bottom

**Try Different ZIP Codes**:
- 94103 (San Francisco)
- 98101 (Seattle)
- 10001 (New York)
- 90210 (Beverly Hills)
- 60601 (Chicago)

---

## 🔍 **Debug Info**

Bottom-left corner shows:
- Active Panel: Which panel is open
- Selected ZIP: Current ZIP code
- Backend URL: API server status
- Connection status: Whether data is loading

---

## 🎨 **UI Features to Notice**

1. **Glassmorphism Design**:
   - Semi-transparent backgrounds with blur
   - Borders with subtle glow
   - Hover effects with color transitions

2. **Color Scheme**:
   - Background: Dark blue-black (#0a0a0a)
   - Primary accent: Cyan (#00bcd4)
   - Borders: Dark blue-gray (#2d3548)
   - Text: White and light gray

3. **Animations**:
   - Panel slide-in from right
   - Icon glow on hover
   - Search bar focus glow
   - Loading spinners

---

## 🐛 **Troubleshooting**

### **Issue: "Failed to fetch"**
**Solution**: Make sure backend is running on port 8001
```powershell
# Check if backend is running
curl http://localhost:8001/api/v1/status
```

### **Issue: "401 Unauthorized" (Mapbox)**
**Solution**: Mapbox token is already configured, but if you see this:
- Check `frontend/src/config/mapbox.ts`
- Token should be: `pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4...`

### **Issue: No suggestions in SearchBar**
**Solution**: 
- Check browser console for errors
- Verify Mapbox token is correct
- Try typing at least 3 characters

### **Issue: Demographics panel shows error**
**Solution**:
- Try a different ZIP code
- Check if backend API is responding:
  ```
  curl http://localhost:8001/api/v1/zipcode/demographics?zipcode=94103
  ```

---

## 📊 **Backend API Endpoints Being Used**

The demo uses these **REAL** backend endpoints:

1. **Mapbox Geocoding** (in SearchBar):
   ```
   https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json
   ```

2. **Census Demographics** (in DemographicsPanel):
   ```
   http://localhost:8001/api/v1/zipcode/demographics?zipcode=94103
   ```

3. **Census Age Distribution**:
   ```
   http://localhost:8001/api/v1/zipcode/age-distribution?zipcode=94103
   ```

4. **Census Housing Data**:
   ```
   http://localhost:8001/api/v1/zipcode/housing?zipcode=94103
   ```

---

## ✅ **Success Criteria**

You should see:
- ✅ SearchBar loads and accepts input
- ✅ Autocomplete suggestions appear when typing
- ✅ FloatingMenu icons are visible and hoverable
- ✅ Demographics icon opens the panel
- ✅ Demographics panel shows **real data** from Census API
- ✅ Age distribution bars display percentages
- ✅ All animations and transitions are smooth
- ✅ No console errors (check browser DevTools)

---

## 🎯 **What's Next**

After testing, we'll continue building:
1. ✅ Points of Interest Panel (Google Places API)
2. ✅ Map Toolbar component
3. ✅ Map tools (draw, measure, travel time)
4. ✅ Additional data panels

---

## 📝 **Notes**

- Demo page is separate from original app (won't break existing code)
- All components use Tailwind CSS (new design system)
- Backend has 20 working endpoints ready to use
- Original app still accessible at `http://localhost:5173/`

---

**ENJOY THE DEMO!** 🎉

If you see any issues or have questions, check the browser console for error messages.

