# Golf Ball Label Generator Web App

A modern web application that allows users to generate custom golf ball labels using AI and view them in 3D. This web app integrates your entire pipeline into a user-friendly interface.

## Features

- **AI-Powered Label Generation**: Generate custom golf ball labels using DALL-E 3
- **3D Model Integration**: Automatically apply labels to 3D golf ball models in Blender
- **Web-Based Interface**: Modern, responsive web interface with real-time progress updates
- **Real-Time Updates**: Live progress tracking with WebSocket connections
- **Example Prompts**: Pre-built examples to help users get started
- **System Status**: Automatic dependency checking and status monitoring
- **3D Viewer**: Integrated 3D model viewer with professional controls

## Quick Start

### 1. Prerequisites

Make sure you have the following installed:
- Python 3.8+
- Node.js and npm
- Blender 4.4 (or update the path in `web_app.py`)
- OpenAI API key in `.env` file

### 2. Setup and Run

The easiest way to start the web app is using the startup script:

```bash
python start_web_app.py
```

This will:
- Install all required Python dependencies
- Install Node.js dependencies for the 3D viewer
- Start the web application
- Open the app in your browser

### 3. Access the App

Once running, the web app will be available at:
- **Main App**: http://localhost:5000
- **3D Viewer**: http://localhost:3000 (opens automatically after generation)

## Manual Setup

If you prefer to set up manually:

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies
```bash
cd w3
npm install
cd ..
```

### 3. Start the Web App
```bash
python web_app.py
```

## How to Use

### 1. Generate a Label

1. Open the web app in your browser
2. Enter a description of your desired golf ball label design
3. Click "Generate Label"
4. Watch the real-time progress as the system:
   - Generates the image with DALL-E 3
   - Updates the 3D model in Blender
   - Starts the 3D viewer

### 2. Example Prompts

The app includes helpful example prompts:
- Professional corporate designs
- Vibrant sports-themed labels
- Elegant personal designs

### 3. View Results

After generation completes:
- The 3D viewer opens automatically
- You can rotate, zoom, and inspect your golf ball
- The viewer includes professional controls and lighting

## Architecture

### Web App Components

- **Flask Backend** (`web_app.py`): Handles API requests and pipeline coordination
- **Socket.IO**: Real-time progress updates and status communication
- **HTML Interface** (`templates/index.html`): Modern, responsive user interface
- **Node.js 3D Viewer** (`w3/`): Professional 3D model viewer with Three.js

### Pipeline Integration

The web app integrates your existing pipeline:
1. **Image Generation**: Uses `generate_image_with_dalle.py`
2. **3D Model Update**: Uses `generate_label_glb.py` with Blender
3. **3D Viewer**: Uses the existing `w3` web app

### API Endpoints

- `GET /` - Main web interface
- `GET /api/status` - Get current pipeline status
- `GET /api/check-dependencies` - Check system dependencies
- `POST /api/generate` - Start label generation
- `GET /api/viewer` - Open 3D viewer

## Configuration

### File Paths

Update these paths in `web_app.py` if needed:
```python
IMAGE_PATH = r"C:\Users\Shriansh\Desktop\SPT\Golf Image\3D\image.png"
GLB_OUTPUT_PATH = r"C:\Users\Shriansh\Desktop\SPT\Golf Image\3D\exported_label.glb"
BLEND_FILE = r"C:\Users\Shriansh\Desktop\SPT\Golf Image\3D\Golf.blend"
BLENDER_DIR = r"C:\Program Files\Blender Foundation\Blender 4.4"
```

### Environment Variables

Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Troubleshooting

### Common Issues

1. **Dependencies Not Found**
   - Run `python start_web_app.py` to install dependencies
   - Check that Blender is installed and the path is correct

2. **3D Viewer Not Starting**
   - Ensure Node.js is installed
   - Check that the `w3` directory exists with all files
   - Try running `npm install` in the `w3` directory

3. **Generation Fails**
   - Check your OpenAI API key in `.env`
   - Ensure all required Python scripts exist
   - Check the console for detailed error messages

### Debug Mode

For detailed logging, the web app runs in debug mode by default. Check the console output for detailed information about any issues.

## File Structure

```
3D/
├── web_app.py              # Main Flask web application
├── start_web_app.py        # Startup script
├── templates/
│   └── index.html          # Web interface
├── w3/                     # 3D viewer web app
│   ├── server.js
│   ├── package.json
│   └── public/
├── generate_image_with_dalle.py
├── generate_label_glb.py
├── run_pipeline.py         # Original command-line pipeline
└── requirements.txt
```

## Development

### Adding Features

The web app is built with Flask and Socket.IO, making it easy to extend:

- **New API Endpoints**: Add routes to `web_app.py`
- **UI Improvements**: Modify `templates/index.html`
- **Pipeline Steps**: Add new steps to the `pipeline_worker` function

### Customization

- **Styling**: Modify the CSS in `templates/index.html`
- **Example Prompts**: Update the prompt examples in the HTML
- **Progress Steps**: Modify the progress percentages in `web_app.py`

## Security Notes

- The web app runs on localhost by default
- For production deployment, consider:
  - Using HTTPS
  - Adding authentication
  - Rate limiting
  - Input validation

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure file paths are correct for your system
4. Check that Blender and Node.js are properly installed

The web app provides a complete, user-friendly interface for your golf ball label generation pipeline, making it accessible to users without technical knowledge of the underlying components. 