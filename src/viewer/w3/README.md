# 3D Model Viewer

A beautiful web application built with Node.js and Three.js to display 3D models in GLB format.

## Features

- Modern, responsive UI with gradient background
- Interactive 3D controls (rotate, pan, zoom)
- Professional lighting setup with shadows
- Auto-rotation toggle
- Wireframe mode toggle
- Mobile-friendly design
- Real-time rendering with smooth animations

## Installation

1. Install dependencies:
```bash
npm install
```

## Running the Application

1. Start the server:
```bash
npm start
```

2. Open your browser and navigate to:
```
http://localhost:3000
```

## Controls

### Mouse Controls
- **Left click + drag**: Rotate the camera around the model
- **Right click + drag**: Pan the camera
- **Scroll wheel**: Zoom in/out

### UI Controls
- **Reset View**: Reset camera to default position
- **Wireframe**: Toggle wireframe rendering mode
- **Auto Rotate**: Toggle automatic model rotation

## File Structure

```
├── server.js              # Express server
├── package.json           # Project dependencies
├── public/
│   ├── index.html        # Main HTML file
│   └── app.js           # Three.js application logic
├── exported_label.glb    # Your 3D model file
└── README.md            # This file
```

## Customization

### Changing the Model
Replace `exported_label.glb` with your own GLB file and update the path in `public/app.js`:

```javascript
loader.load('/models/your-model.glb', ...)
```

### Modifying the UI
Edit the CSS in `public/index.html` to customize colors, fonts, and layout.

### Adjusting Lighting
Modify the `setupLighting()` function in `public/app.js` to change lighting setup.

## Technical Details

- **Backend**: Node.js with Express
- **Frontend**: Three.js for 3D rendering
- **Model Format**: GLB (GL Binary)
- **Controls**: OrbitControls for camera manipulation
- **Lighting**: Multiple light sources for realistic rendering

## Browser Compatibility

This application works best in modern browsers that support WebGL:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

If the model doesn't load:
1. Check the browser console for errors
2. Ensure the GLB file is in the correct location
3. Verify the file path in `app.js`
4. Make sure your browser supports WebGL

## Development

For development with auto-reload:
```bash
npm run dev
```

This requires `nodemon` to be installed globally or as a dev dependency. 