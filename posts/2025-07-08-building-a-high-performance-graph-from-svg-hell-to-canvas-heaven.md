---
title: "Building a High-Performance Graph: From SVG Hell to Canvas Heaven"
slug: "building-a-high-performance-graph-from-svg-hell-to-canvas-heaven"
date: "2025-07-08T08:03:53+00:00"
author: "Anzal Husain Abidi"
description: "A Deep Dive into Rendering Large Networks with React and D3 At its core, our work often revolves around data. But raw data in tables and spreadsheets can only tell us so much. The real magic happens when we can see the relationships hidden within tha..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1751961670939/d63a6cf9-17fa-4d03-8ae5-e0dec3bcbc31.png"
tags:
  - "React"
  - "Browsers"
  - "Rendering"
  - "optimization"
  - "canvas"
  - "JavaScript"
canonical_url: "https://anzal.hashnode.dev/building-a-high-performance-graph-from-svg-hell-to-canvas-heaven"
source: "hashnode"
---

![Building a High-Performance Graph: From SVG Hell to Canvas Heaven](https://cdn.hashnode.com/res/hashnode/image/upload/v1751961670939/d63a6cf9-17fa-4d03-8ae5-e0dec3bcbc31.png)

### A Deep Dive into Rendering Large Networks with React and D3

At its core, our work often revolves around data. But raw data in tables and spreadsheets can only tell us so much. The real magic happens when we can *see* the relationships hidden within that data. This is especially true for network data, where the connections between points are often more important than the points themselves.

Visualizing these networks allows our analysts to spot fraud rings, understand complex system dependencies, and uncover insights that would be impossible to find in a spreadsheet. The tool for this job? A force-directed graph.

However, as we quickly discovered, building a graph that looks good with a handful of test nodes is one thing. Building one that stays fast and usable with real-world, large-scale data is another challenge entirely.

This document chronicles our journey of transforming a sluggish, proof-of-concept graph into a highly performant, feature-rich analysis tool. We'll explore the technical bottlenecks we hit, the architectural decisions we made, and the clever algorithms that saved the day.

## The Tool for the Job: What is D3.js?

Before we dive into the problems, let's talk about the main tool we used: **D3.js (Data-Driven Documents)**.

D3 is not a "charting library" in the traditional sense. It doesn't give you pre-built bar charts or pie charts. Instead, it gives you a powerful set of tools to bind arbitrary data to the Document Object Model (DOM) and then apply data-driven transformations to the document.

In simple terms, you can give D3 an array of numbers and use it to create and style a `<div>` for each number. For graph visualization, we give it an array of nodes and links and use it to create and position SVG elements. Its most powerful feature for our use case is its `forceSimulation` module—a physics engine that can automatically position nodes in a way that is both aesthetically pleasing and analytically insightful.

## The First Attempt: The Simplicity and Deception of SVG

When you start a D3 project, SVG (Scalable Vector Graphics) is the natural choice. It's a web standard, and it integrates perfectly with D3's data-binding paradigm. The logic feels wonderfully direct: for every node in our data, we create a `<circle>` element, and for every link, we create a `<line>` element.

```javascript
// This looks so simple, right?
const svg = d3.select("#graph-container").append("svg");

// Make a line for every link
svg.selectAll("line").data(links).enter().append("line");

// And a circle for every node
svg.selectAll("circle").data(nodes).enter().append("circle");
```

This creates a direct, one-to-one relationship between our data and the DOM.

For a few hundred nodes, this works like a charm! It's crisp, it's interactive (you can attach `onClick` listeners directly to the circles), and you feel like you've built something amazing in just a few lines of code.

The problem is, this simple approach has a hidden, dark side that only reveals itself when you start throwing real, complex data at it.

### The SVG Bottleneck: Why Our Graph Ground to a Halt

Here's the catch: SVG is what's called a **"retained-mode"** system. In simple terms, for every single shape you draw, the browser has to create and keep track of a separate object in the DOM.

Think about it. A graph with 5,000 nodes and 10,000 links means you're creating over **15,000 DOM elements!** This is what our graph looked like—a classic "hairball."

The real trouble starts when the D3 force simulation kicks in. To create that nice, organic layout, the simulation is constantly adjusting the positions of all the nodes. For our SVG graph, that meant:

1. **The Reflow Nightmare:** On every single "tick" of the simulation, we were telling the browser to update the `cx` and `cy` attributes of thousands of circle elements. Every time an element moves, the browser has to do a "reflow"—a super expensive calculation to figure out how that move affects the layout of everything else on the page.
2. **Painting Over and Over:** After the reflow, the browser has to repaint all the changed elements.
3. **Putting it all Together:** Finally, it composites all these freshly painted layers back onto the screen.

Doing all of that, for thousands of elements, hundreds of times per second? The browser's main thread just couldn't keep up. The result was a jumpy, laggy mess that was frustrating to use and made analysis impossible.

## The Fix: Breaking Free with Canvas

To get the performance we needed, we had to break free from the DOM. The HTML5 `<canvas>` element was our escape hatch.

### A Different Way of Thinking: "Immediate-Mode"

Canvas works in **"immediate-mode"**. Think of it like this:

- **SVG is like building with Legos.** Each brick is a distinct object. You can move a brick, change its color, or attach an event listener to it. The model retains the state of every single brick.
- **Canvas is like... well, a canvas!** You're a painter with a brush. You tell the canvas "draw a circle here," and it puts pixels on the screen. The moment it's drawn, the canvas forgets it was a circle. It's just a collection of pixels. It doesn't retain anything.

This "fire-and-forget" approach is the key to its speed.

### The Performance Win

1. **One Element to Rule Them All:** No matter if we have 10 nodes or 10,000, we only ever have *one* `<canvas>` element in the DOM. The browser's layout work is basically zero.
2. **We're in Control of the Rendering:** We let the D3 physics simulation run in the background, constantly updating the `x` and `y` coordinates of our nodes in a simple JavaScript array. Then, in a separate, highly optimized loop using `requestAnimationFrame`, we tell the canvas to redraw the entire scene based on that data.

```cpp
function renderLoop() {
  // 1. Wipe the canvas clean.
  context.clearRect(0, 0, width, height);

  // 2. Loop through our data and paint everything.
  nodes.forEach(node => {
    context.beginPath();
    context.arc(node.x, node.y, 5, 0, 2 * Math.PI);
    context.fill();
  });

  // 3. Tell the browser we're ready for the next paint frame.
  requestAnimationFrame(renderLoop);
}
```

This decouples the physics from the painting and syncs our drawing with the screen's refresh rate. The result? A buttery-smooth 60fps animation, even with a massive number of nodes!

## The Interaction Challenge: How Do You Click on Pixels?

We solved the rendering bottleneck, but created a new problem: **interaction**. The canvas is a dumb pixel buffer. It has no concept of the nodes or edges drawn on it. If a user clicks on the canvas, how do we know *what* they clicked on?

The naive approach is a brute-force search: loop through every node and check if the click coordinates are within its radius. This is an **O(n)** operation, meaning it scales linearly with the number of nodes. For 10,000 nodes, this is far too slow.

### The Hero of Our Story: The Mighty Quadtree

This is where the **Quadtree** becomes our most important tool. A quadtree is a data structure that recursively subdivides a 2D space into four quadrants, allowing for incredibly efficient spatial lookups.

Instead of checking every node, we can find the node under the cursor with **O(log n)** complexity. For 10,000 nodes, this reduces the number of checks from 10,000 to roughly 14.

In our implementation:

1. **Build the Tree:** On every render frame, we build a new quadtree from the latest node positions: `quadtree = d3.quadtree().addAll(nodes)`.
2. **Find the Node:** On a mouse event, we query the tree: `quadtree.find(mouseX, mouseY, searchRadius)`.

This is fast enough to run on every mouse move, enabling smooth tooltips, clicks, and dragging on a canvas with tens of thousands of elements.

## Putting It All Together: A Stable React Architecture

The final piece of the puzzle is ensuring our component is stable within the React ecosystem. A common pitfall is to place the D3 simulation setup inside a standard `useEffect` hook. This causes the entire simulation to be destroyed and recreated whenever a prop changes, leading to the dreaded "jumping" graph.

Our solution uses a two-hook architecture:

1. **One-Time Setup** `useEffect`: This hook runs only once (`useEffect(..., [])`). It is responsible for all the expensive, one-time setup: creating the simulation, appending UI elements, attaching event listeners, and starting the render loop.
2. **Data Update** `useEffect`: This hook runs only when the `dataset` prop changes. It does *not* destroy the simulation. It simply updates the existing simulation with the new data and "reheats" it with `simulation.alpha(1).restart()`.

This separation is the key to preventing the "jumping" and "twitching" issues, as UI interactions and prop changes no longer trigger a full teardown and recreation of the graph visualization.

## Conclusion

By migrating from SVG to Canvas, we traded the convenience of the DOM for raw rendering performance. We then regained interactivity by implementing a Quadtree for efficient spatial lookups. Finally, by carefully structuring our React component, we created a stable, non-rerendering architecture. The result is a feature-rich, highly performant graph visualization tool capable of handling the scale and complexity our data demands.

## Quadtree Implementation from Scratch

While we use D3's built-in Quadtree for its robustness and integration with the D3 ecosystem, understanding how one works from scratch is enlightening. Below is a simplified JavaScript implementation that demonstrates the core principles of insertion and querying.

```javascript
class Point {
    constructor(x, y, data) {
        this.x = x;
        this.y = y;
        this.data = data; // Arbitrary data associated with the point
    }
}

class Rectangle {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
    }

    contains(point) {
        return (
            point.x >= this.x - this.w &&
            point.x < this.x + this.w &&
            point.y >= this.y - this.h &&
            point.y < this.y + this.h
        );
    }

    intersects(range) {
        return !(
            range.x - range.w > this.x + this.w ||
            range.x + range.w < this.x - this.w ||
            range.y - range.h > this.y + this.h ||
            range.y + range.h < this.y - this.h
        );
    }
}

class QuadTree {
    constructor(boundary, capacity) {
        this.boundary = boundary; // A Rectangle object
        this.capacity = capacity; // Max number of points before subdividing
        this.points = [];
        this.divided = false;
    }

    subdivide() {
        const { x, y, w, h } = this.boundary;
        const nw = new Rectangle(x - w / 2, y - h / 2, w / 2, h / 2);
        const ne = new Rectangle(x + w / 2, y - h / 2, w / 2, h / 2);
        const sw = new Rectangle(x - w / 2, y + h / 2, w / 2, h / 2);
        const se = new Rectangle(x + w / 2, y + h / 2, w / 2, h / 2);

        this.northwest = new QuadTree(nw, this.capacity);
        this.northeast = new QuadTree(ne, this.capacity);
        this.southwest = new QuadTree(sw, this.capacity);
        this.southeast = new QuadTree(se, this.capacity);

        this.divided = true;
    }

    insert(point) {
        if (!this.boundary.contains(point)) {
            return false;
        }

        if (this.points.length < this.capacity) {
            this.points.push(point);
            return true;
        } else {
            if (!this.divided) {
                this.subdivide();
            }

            if (this.northeast.insert(point)) return true;
            if (this.northwest.insert(point)) return true;
            if (this.southeast.insert(point)) return true;
            if (this.southwest.insert(point)) return true;
        }
    }

    query(range, found = []) {
        if (!this.boundary.intersects(range)) {
            return found;
        }

        for (let p of this.points) {
            if (range.contains(p)) {
                found.push(p);
            }
        }

        if (this.divided) {
            this.northwest.query(range, found);
            this.northeast.query(range, found);
            this.southwest.query(range, found);
            this.southeast.query(range, found);
        }

        return found;
    }
}
```

## Live Performance Demo

To see the performance difference for yourself, save the code below as a single `.html` file and open it in your browser. It renders the same force-directed graph in a single panel.

Use the controls at the top to switch between "SVG Mode" and "Canvas Mode" and to increase the number of nodes and links. You will quickly see the SVG version's FPS drop dramatically, while the Canvas version remains smooth and interactive

Use the controls at the top to switch between "SVG Mode" and "Canvas Mode" and to increase the number of nodes and links. You will quickly see the SVG version's FPS drop dramatically, while the Canvas version remains smooth and interactive.

```xml
<!DOCTYPE html>
<html>
<head>
    <title>SVG vs. Canvas Performance Demo</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f0f2f5; }
        .controls { padding: 15px; background-color: #fff; border-bottom: 1px solid #ddd; display: flex; align-items: center; gap: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .controls label { font-weight: bold; }
        .controls input[type="number"] { width: 80px; padding: 5px; border: 1px solid #ccc; border-radius: 4px; }
        .controls button { padding: 5px 15px; border: 1px solid #ccc; border-radius: 4px; background-color: #e9e9e9; cursor: pointer; }
        .controls .mode-toggle button.active { background-color: #007bff; color: white; border-color: #007bff; }
        .container { display: flex; width: 100%; height: calc(100vh - 70px); }
        .panel { width: 100%; height: 100%; position: relative; background-color: #fff; }
        .fps-container { position: absolute; top: 10px; right: 10px; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
        .fps { background: rgba(0,0,0,0.5); color: white; padding: 5px 8px; border-radius: 3px; font-family: monospace; }
        .perf-graph { border: 1px solid #ccc; background-color: rgba(255,255,255,0.8); }
        #graph-container { width: 100%; height: 100%; }
        #graph-container > * { width: 100%; height: 100%; display: block; }
        .tooltip { position: absolute; visibility: hidden; background: rgba(0,0,0,0.7); color: white; padding: 4px 8px; border-radius: 3px; pointer-events: none; }
    </style>
</head>
<body>

<div class="controls">
    <div class="mode-toggle">
        <label>Mode:</label>
        <button id="svg-btn" class="active">SVG</button>
        <button id="canvas-btn">Canvas</button>
    </div>
    <label for="nodes">Nodes:</label>
    <input type="number" id="nodes" value="500" min="10" max="20000" step="100">
    <label for="links">Links:</label>
    <input type="number" id="links" value="400" min="10" max="20000" step="100">
    <button id="update">Update Graph</button>
</div>

<div class="container">
    <div class="panel">
        <div id="graph-container"></div>
        <div class="fps-container">
            <div id="fps-display" class="fps">-- FPS</div>
            <canvas id="perf-graph" class="perf-graph" width="200" height="50"></canvas>
        </div>
    </div>
</div>

<script>
    const graphContainer = d3.select("#graph-container");
    const perfCanvas = document.getElementById("perf-graph");
    const perfContext = perfCanvas.getContext("2d");

    let activeSimulation;
    let activeRenderLoopId;
    let currentMode = 'svg';

    const fpsCounter = {
        history: [],
        lastTime: performance.now(),
        frames: 0
    };

    function createData(numNodes, numLinks) {
        const nodes = Array.from({length: numNodes}, (_, i) => ({id: i}));
        const links = Array.from({length: numLinks}, () => ({
            source: Math.floor(Math.random() * numNodes),
            target: Math.floor(Math.random() * numNodes)
        }));
        return { nodes, links };
    }

    function updateFPS() {
        fpsCounter.frames++;
        const time = performance.now();
        if (time >= fpsCounter.lastTime + 1000) {
            const fps = fpsCounter.frames;
            fpsCounter.frames = 0;
            fpsCounter.lastTime = time;
            document.getElementById('fps-display').textContent = `${fps} FPS`;
            fpsCounter.history.push(fps);
            if (fpsCounter.history.length > 100) fpsCounter.history.shift();
        }
        drawPerformanceGraph();
    }

    function drawPerformanceGraph() {
        perfContext.clearRect(0, 0, perfCanvas.width, perfCanvas.height);
        perfContext.fillStyle = "rgba(240, 240, 240, 0.8)";
        perfContext.fillRect(0, 0, perfCanvas.width, perfCanvas.height);

        perfContext.beginPath();
        perfContext.moveTo(0, perfCanvas.height - (60 / 70 * perfCanvas.height));
        perfContext.lineTo(perfCanvas.width, perfCanvas.height - (60 / 70 * perfCanvas.height));
        perfContext.strokeStyle = "rgba(0, 255, 0, 0.5)";
        perfContext.stroke();

        perfContext.beginPath();
        perfContext.moveTo(0, perfCanvas.height);
        fpsCounter.history.forEach((fps, i) => {
            const x = (i / 99) * perfCanvas.width;
            const y = perfCanvas.height - (Math.min(fps, 70) / 70 * perfCanvas.height);
            perfContext.lineTo(x, y);
        });
        perfContext.strokeStyle = "#333";
        perfContext.stroke();
    }

    function cleanup() {
        if (activeSimulation) activeSimulation.stop();
        if (activeRenderLoopId) cancelAnimationFrame(activeRenderLoopId);
        graphContainer.html("");
        fpsCounter.history = [];
        fpsCounter.frames = 0;
        fpsCounter.lastTime = performance.now();
    }

    function runSVG(data, width, height) {
        cleanup();
        const svg = graphContainer.append("svg").attr("width", width).attr("height", height);
        const tooltip = d3.select("body").append("div").attr("class", "tooltip");

        activeSimulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g").selectAll("line").data(data.links).join("line").attr("stroke", "#999").attr("stroke-opacity", 0.6);
        const node = svg.append("g").selectAll("circle").data(data.nodes).join("circle").attr("r", 5).attr("fill", "#333")
            .on("mouseover", (event, d) => {
                tooltip.style("visibility", "visible").text(`Node ${d.id}`);
            })
            .on("mousemove", (event) => {
                tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
            })
            .on("mouseout", () => {
                tooltip.style("visibility", "hidden");
            })
            .call(d3.drag()
                .on("start", (event, d) => {
                    if (!event.active) activeSimulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                })
                .on("drag", (event, d) => {
                    d.fx = event.x;
                    d.fy = event.y;
                })
                .on("end", (event, d) => {
                    if (!event.active) activeSimulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }));

        activeSimulation.on("tick", () => {
            link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
            node.attr("cx", d => d.x).attr("cy", d => d.y);
        });

        function renderLoop() {
            updateFPS();
            activeRenderLoopId = requestAnimationFrame(renderLoop);
        }
        activeRenderLoopId = requestAnimationFrame(renderLoop);
    }

    function runCanvas(data, width, height) {
        cleanup();
        const canvas = graphContainer.append("canvas").attr("width", width).attr("height", height).node();
        const context = canvas.getContext("2d");
        const tooltip = d3.select("body").append("div").attr("class", "tooltip");

        activeSimulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(width / 2, height / 2));

        let quadtree = d3.quadtree().x(d => d.x).y(d => d.y);

        activeSimulation.on("tick", () => {
            quadtree = d3.quadtree().x(d => d.x).y(d => d.y).addAll(data.nodes);
            render();
        });

        function render() {
            context.clearRect(0, 0, width, height);
            context.beginPath();
            data.links.forEach(d => {
                context.moveTo(d.source.x, d.source.y);
                context.lineTo(d.target.x, d.target.y);
            });
            context.strokeStyle = "#999";
            context.stroke();
            context.beginPath();
            data.nodes.forEach(d => {
                context.moveTo(d.x + 5, d.y);
                context.arc(d.x, d.y, 5, 0, 2 * Math.PI);
            });
            context.fillStyle = "#333";
            context.fill();
        }

        d3.select(canvas)
            .on("mousemove", (event) => {
                const [mx, my] = d3.pointer(event);
                const found = quadtree.find(mx, my, 10);
                if (found) {
                    tooltip.style("visibility", "visible").text(`Node ${found.id}`)
                        .style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
                } else {
                    tooltip.style("visibility", "hidden");
                }
            })
            .call(d3.drag()
                .subject((event) => {
                    const [mx, my] = d3.pointer(event, canvas);
                    return quadtree.find(mx, my, 10);
                })
                .on("start", (event) => {
                    if (!event.active) activeSimulation.alphaTarget(0.3).restart();
                    event.subject.fx = event.subject.x;
                    event.subject.fy = event.subject.y;
                })
                .on("drag", (event) => {
                    event.subject.fx = event.x;
                    event.subject.fy = event.y;
                })
                .on("end", (event) => {
                    if (!event.active) activeSimulation.alphaTarget(0);
                    event.subject.fx = null;
                    event.subject.fy = null;
                }));

        function animationLoop() {
            updateFPS();
            activeRenderLoopId = requestAnimationFrame(animationLoop);
        }
        activeRenderLoopId = requestAnimationFrame(animationLoop);
    }

    function updateAll() {
        const numNodes = +document.getElementById('nodes').value;
        const numLinks = +document.getElementById('links').value;
        const data = createData(numNodes, numLinks);

        const panelWidth = document.querySelector('.panel').clientWidth;
        const panelHeight = document.querySelector('.panel').clientHeight;

        if (currentMode === 'svg') {
            runSVG(data, panelWidth, panelHeight);
        } else {
            runCanvas(data, panelWidth, panelHeight);
        }
    }

    document.getElementById('svg-btn').addEventListener('click', () => {
        currentMode = 'svg';
        document.getElementById('svg-btn').classList.add('active');
        document.getElementById('canvas-btn').classList.remove('active');
        updateAll();
    });

    document.getElementById('canvas-btn').addEventListener('click', () => {
        currentMode = 'canvas';
        document.getElementById('canvas-btn').classList.add('active');
        document.getElementById('svg-btn').classList.remove('active');
        updateAll();
    });

    document.getElementById('update').addEventListener('click', updateAll);

    // Initial load
    updateAll();
</script>

</body>
</html>
```
