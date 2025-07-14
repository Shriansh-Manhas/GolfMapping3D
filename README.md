# Golf Ball Label 3D Generator

A complete pipeline for generating custom golf ball labels using DALL-E image generation, Blender 3D modeling, and web-based 3D viewing.

## Project Structure

```
3D/
├── src/                    # Source code
│   ├── web_app/           # Flask web application
│   │   ├── web_app.py     # Main Flask app
│   │   ├── requirements.txt
│   │   ├── templates/     # HTML templates
│   │   └── static/        # Static assets (CSS, JS)
│   ├── pipeline/          # Pipeline scripts
│   │   └── run_pipeline.py
│   ├── blender/           # Blender-related scripts
│   │   ├── generate_label_glb.py
│   │   ├── async_blend.py
│   │   └── Blender Init
│   ├── viewer/            # 3D viewer components
│   │   ├── test_viewer.py
│   │   └── w3/           # Node.js web viewer
│   └── tools/             # Utility scripts
│       └── fix_npm_path.py
├── assets/                # Static assets
│   ├── models/           # 3D models (GLB files)
│   ├── images/           # Generated images
│   └── blend_files/      # Blender files
├── scripts/              # Standalone scripts
│   ├── generate_image_with_dalle.py
│   └── start_web_app.py
├── docs/                 # Documentation
└── .gitignore
```

## Quick Start

1. **Generate an image with DALL-E:**
   ```bash
   python scripts/generate_image_with_dalle.py
   ```

2. **Start the web application:**
   ```bash
   python scripts/start_web_app.py
   ```

3. **Run the complete pipeline:**
   ```bash
   python src/pipeline/run_pipeline.py
   ```

## Features

- **DALL-E Integration**: Generate custom golf ball label images using OpenAI's DALL-E
- **Blender Automation**: Automatic 3D model generation and GLB export
- **Web Viewer**: Modern 3D viewer with drag-and-drop support
- **Real-time Pipeline**: Watch for image changes and automatically rebuild 3D models
- **Professional UI**: Clean, modern web interface with progress tracking

## Requirements

- Python 3.8+
- Blender 4.4+
- Node.js (for 3D viewer)
- OpenAI API key

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r src/web_app/requirements.txt
   ```

2. Install Node.js dependencies:
   ```bash
   cd src/viewer/w3
   npm install
   ```

## Usage

The project provides multiple entry points:

- **Web App**: Complete web interface for the entire pipeline
- **Standalone Scripts**: Individual components for specific tasks
- **Pipeline**: Automated end-to-end processing

See individual README files in each directory for detailed usage instructions. 