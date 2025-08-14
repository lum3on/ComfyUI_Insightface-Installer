/**
 * ComfyUI Insightface Installer - Custom Node Skin
 *
 * This web extension applies a custom background skin to the InsightfaceInstaller node
 * while ensuring text readability and proper widget display.
 *
 * Author: ComfyUI Node Architect
 * Version: 1.0.0
 */

import { app } from "../../scripts/app.js";

// Configuration for the skin
const SKIN_CONFIG = {
    nodeType: "InsightfaceInstaller",
    backgroundVideo: "/extensions/ComfyUI-Insightface-Installer/social_yo9otatara_httpss.mj.run9tOjy1psBZ0_light_hearted_daylight_so_af383426-114f-401f-885b-15b19d88725d_2.mp4",
    opacity: 1.0,
    textShadow: "1px 1px 2px rgba(0,0,0,0.8)",
    borderRadius: "8px",
    overlayColor: "rgba(255,255,255,0.1)"
};

// Load CSS file
function loadCSS() {
    const cssPath = `/extensions/ComfyUI-Insightface-Installer/insightface_skin.css?v=${Date.now()}`;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = cssPath;
    link.id = "insightface-installer-skin-css";

    // Remove existing CSS if present
    const existing = document.getElementById("insightface-installer-skin-css");
    if (existing) {
        existing.remove();
    }

    document.head.appendChild(link);
    console.log("InsightfaceInstaller CSS skin loaded from:", cssPath);
}

// Function to apply node styling
function applyNodeSkin(node) {
    if (!node || node.type !== SKIN_CONFIG.nodeType) return;

    // Apply custom styling to the LiteGraph node
    if (node.canvas && node.canvas.canvas) {
        // Add data attribute for CSS targeting
        const canvas = node.canvas.canvas;
        if (!canvas.hasAttribute("data-insightface-skin")) {
            canvas.setAttribute("data-insightface-skin", "true");
        }
    }

    // Store original drawing functions if not already stored
    if (!node._originalOnDrawBackground) {
        node._originalOnDrawBackground = node.onDrawBackground;
    }
    if (!node._originalOnDrawForeground) {
        node._originalOnDrawForeground = node.onDrawForeground;
    }

    // Draw on background so the image becomes the node chrome (title + body)
    node.onDrawBackground = function(ctx) {
        // First draw our image to cover the full node area
        drawCustomBackground(ctx, this);
        // Then allow original background to add shadows/extra visuals (colors are transparent)
        if (this._originalOnDrawBackground) {
            this._originalOnDrawBackground.call(this, ctx);
        }
    };
}

// Preload the background video
let backgroundVideo = null;
function preloadBackgroundVideo() {
    if (backgroundVideo) return; // Prevent re-initialization
    
    backgroundVideo = document.createElement("video");
    backgroundVideo.muted = true;
    backgroundVideo.loop = true; // Keep for fallback
    backgroundVideo.autoplay = true;
    backgroundVideo.playsInline = true;
    
    let isPlaying = false;
    let errorOccurred = false;

    // --- Seamless Loop ---
    // The 'loop' attribute can be unreliable. This ensures it resets manually.
    backgroundVideo.addEventListener("timeupdate", function() {
        if (this.currentTime >= this.duration - 0.1) {
            this.currentTime = 0;
            if (isPlaying) this.play();
        }
    });

    backgroundVideo.oncanplay = function() {
        if (errorOccurred) return;
        console.log("Background video can play successfully");
        backgroundVideo.play().then(() => {
            isPlaying = true;
        }).catch(e => {
            console.warn("Autoplay was prevented for background video.", e);
        });
    };
    
    backgroundVideo.onerror = function() {
        errorOccurred = true;
        isPlaying = false;
        console.error("Failed to load background video:", SKIN_CONFIG.backgroundVideo);
    };

    backgroundVideo.src = SKIN_CONFIG.backgroundVideo;
    backgroundVideo.load(); // Start loading the video
}

// Function to draw custom background
function drawCustomBackground(ctx, node) {
    if (!ctx || !node || !backgroundVideo || backgroundVideo.readyState < 3) return;

    try {
        ctx.save();

        const nw = node.size[0];
        const nh = node.size[1];
        const vw = backgroundVideo.videoWidth;
        const vh = backgroundVideo.videoHeight;

        if (!vw || !vh || !nw || !nh) {
            ctx.restore();
            return;
        }

        const nodeRatio = nw / nh;
        const videoRatio = vw / vh;
        
        let drawW, drawH;
        if (videoRatio > nodeRatio) {
            drawH = nh;
            drawW = videoRatio * drawH;
        } else {
            drawW = nw;
            drawH = drawW / videoRatio;
        }
        const dx = (nw - drawW) / 2;
        const dy = (nh - drawH) / 2;

        const bleed = 1;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(-bleed, -bleed, nw + 2 * bleed, nh + 2 * bleed, 8);
        } else {
            ctx.rect(-bleed, -bleed, nw + 2 * bleed, nh + 2 * bleed);
        }
        ctx.clip();

        ctx.globalAlpha = SKIN_CONFIG.opacity;
        ctx.drawImage(backgroundVideo, dx, dy, drawW, drawH);

        ctx.globalAlpha = 1.0;
        ctx.fillStyle = "rgba(255, 255, 255, 0.1)"; // Brighten: Light overlay instead of dark
        ctx.fillRect(0, 0, nw, nh);

        ctx.restore();
    } catch (error) {
        console.error("Error drawing video background:", error);
    }
}

// Extension registration
app.registerExtension({
    name: "InsightfaceInstaller.Skin",

    async setup() {
        // Load CSS styles
        loadCSS();

        // Preload background video
        preloadBackgroundVideo();

        console.log("InsightfaceInstaller skin extension loaded");
    },

    async nodeCreated(node) {
        // Check if this is our target node type
        if (node.comfyClass === SKIN_CONFIG.nodeType || node.type === SKIN_CONFIG.nodeType) {
            console.log("Applying skin to node:", node.comfyClass || node.type);

            // Add custom class to the node's element for CSS targeting
            if(node.html) {
                node.html.classList.add("insightface-installer-custom-node");
            }

            node.color = "#2B3B72";
            node.bgcolor = "rgba(0,0,0,0)";  // body fill
            node.title_text_color = node.title_text_color || "#fff";
            node.title_text_font = "16px 'Palace Script MT', 'Times New Roman', serif";

            if (!node._originalOnDrawBackground) {
                node._originalOnDrawBackground = node.onDrawBackground;
            }

            node.onDrawBackground = function(ctx) {
                if (this.flags.collapsed) {
                    if (this._originalOnDrawBackground) {
                        this._originalOnDrawBackground.call(this, ctx);
                    }
                    return;
                }
                drawCustomBackground(ctx, this);
                if (this._originalOnDrawBackground) {
                    this._originalOnDrawBackground.call(this, ctx);
                }
            };

            // Continuous redraw loop for video
            const animationLoop = () => {
                if (node.graph) { // Ensure node is still on canvas
                    node.setDirtyCanvas(true, true);
                    requestAnimationFrame(animationLoop);
                }
            };
            requestAnimationFrame(animationLoop);
        }
    }
});

// Export configuration for potential customization
export { SKIN_CONFIG };
