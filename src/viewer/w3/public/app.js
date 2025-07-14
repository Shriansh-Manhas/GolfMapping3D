// Global variables
let scene, camera, renderer, controls;
let model, mixer;
let clock = new THREE.Clock();
let autoRotate = false;
let wireframeMode = false;

// Initialize the 3D scene
function init() {
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);

    // Create camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(5, 5, 5);

    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    // Add renderer to container
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Add controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 1;
    controls.maxDistance = 50;
    controls.maxPolarAngle = Math.PI;

    // Add lighting
    setupLighting();

    // Load the 3D model
    loadModel();

    // Handle window resize
    window.addEventListener('resize', onWindowResize);

    // Start animation loop
    animate();
}

// Setup lighting for the scene
function setupLighting() {
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    // Directional light (main light)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 50;
    directionalLight.shadow.camera.left = -10;
    directionalLight.shadow.camera.right = 10;
    directionalLight.shadow.camera.top = 10;
    directionalLight.shadow.camera.bottom = -10;
    scene.add(directionalLight);

    // Point light for additional illumination
    const pointLight = new THREE.PointLight(0xffffff, 0.5);
    pointLight.position.set(-10, 10, -10);
    scene.add(pointLight);

    // Hemisphere light for better color balance
    const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3);
    scene.add(hemisphereLight);
}

// Load the 3D model
function loadModel() {
    const loader = new THREE.GLTFLoader();
    
    loader.load(
        '/models/exported_label.glb',
        function (gltf) {
            model = gltf.scene;
            
            // Enable shadows for all meshes
            model.traverse(function (child) {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    
                    // Improve material quality
                    if (child.material) {
                        child.material.needsUpdate = true;
                    }
                }
            });

            // Center and scale the model
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            
            // Center the model
            model.position.sub(center);
            
            // Scale to fit in view
            const maxDim = Math.max(size.x, size.y, size.z);
            const scale = 5 / maxDim;
            model.scale.setScalar(scale);

            scene.add(model);

            // Setup animations if any
            if (gltf.animations && gltf.animations.length) {
                mixer = new THREE.AnimationMixer(model);
                gltf.animations.forEach((clip) => {
                    mixer.clipAction(clip).play();
                });
            }

            // Hide loading screen
            document.getElementById('loading').classList.add('hidden');
            
            console.log('Model loaded successfully!');
        },
        function (xhr) {
            // Progress callback
            const percent = (xhr.loaded / xhr.total) * 100;
            console.log('Loading progress: ' + percent.toFixed(0) + '%');
        },
        function (error) {
            console.error('Error loading model:', error);
            document.getElementById('loading').innerHTML = 
                '<p style="color: #ff6b6b;">Error loading model. Please check the console for details.</p>';
        }
    );
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    // Update controls
    controls.update();

    // Update animations
    if (mixer) {
        mixer.update(delta);
    }

    // Auto rotate if enabled
    if (autoRotate && model) {
        model.rotation.y += 0.01;
    }

    // Render the scene
    renderer.render(scene, camera);
}

// Handle window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Control functions
function resetCamera() {
    camera.position.set(5, 5, 5);
    controls.reset();
}

function toggleWireframe() {
    wireframeMode = !wireframeMode;
    if (model) {
        model.traverse(function (child) {
            if (child.isMesh && child.material) {
                child.material.wireframe = wireframeMode;
            }
        });
    }
}

function toggleAutoRotate() {
    autoRotate = !autoRotate;
    const button = event.target;
    if (autoRotate) {
        button.style.background = 'rgba(255, 255, 255, 0.3)';
    } else {
        button.style.background = 'rgba(255, 255, 255, 0.1)';
    }
}

// Initialize the application
init(); 