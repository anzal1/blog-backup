---
title: "A Beginner’s Guide to RTSP Streaming with WebSockets Using Node.js and FFmpeg"
slug: "a-beginners-guide-to-rtsp-streaming-with-websockets-using-nodejs-and-ffmpeg"
date: "2024-09-15T10:05:35+00:00"
author: "Anzal Husain Abidi"
description: "Real-Time Streaming Protocol (RTSP) is widely used for controlling media streams in surveillance systems, IP cameras, and more. However, interacting with RTSP streams directly in web applications can be challenging since browsers don’t natively suppo..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1726394619890/c91433e9-2087-4347-994e-390122aa162a.webp"
tags:
  - "Node.js"
  - "streaming"
  - "video"
  - "FFmpeg"
  - "Programming Blogs"
  - "React"
  - "HTML5"
  - "npm"
  - "JavaScript"
canonical_url: "https://anzal.hashnode.dev/a-beginners-guide-to-rtsp-streaming-with-websockets-using-nodejs-and-ffmpeg"
source: "hashnode"
---

![A Beginner’s Guide to RTSP Streaming with WebSockets Using Node.js and FFmpeg](https://cdn.hashnode.com/res/hashnode/image/upload/v1726394619890/c91433e9-2087-4347-994e-390122aa162a.webp)

**Real-Time Streaming Protocol** (RTSP) is widely used for controlling media streams in surveillance systems, IP cameras, and more. However, interacting with RTSP streams directly in web applications can be challenging since browsers don’t natively support this protocol. The good news is that by leveraging **FFmpeg** and **WebSockets**, you can relay RTSP streams to a browser.

In this blog, I’ll walk you through the process of streaming RTSP feeds using Node.js and FFmpeg, as well as packaging this into a Docker container. We’ll also go over how to create an npm package that developers can use to set up their own RTSP-to-WebSocket relay server.

## What is RTSP?

RTSP (Real-Time Streaming Protocol) is a network control protocol designed for use in entertainment and communications systems to control streaming media servers. It establishes and controls media sessions between endpoints and is often used to deliver live feeds, such as from IP cameras.

Unfortunately, modern browsers don’t directly support RTSP, so we need to find a way to relay the RTSP stream to a more browser-friendly format, such as WebSockets or HTTP.

### Why Use FFmpeg?

FFmpeg is a powerful open-source tool that can handle multimedia streams like RTSP. It can transcode, decode, and relay streams in various formats. In this tutorial, FFmpeg will convert the RTSP stream into a format suitable for sending over WebSockets to a browser.

### The Role of WebSockets

WebSockets enable two-way communication between a server and a client over a single, persistent connection. By relaying RTSP streams through WebSockets, we can push the stream data directly to the browser in real time.

---

## Setting Up the Node.js RTSP Stream Relay

### Step 1: Create a Basic Node.js Server

We’ll start by creating a simple Node.js server that will listen for WebSocket connections and relay RTSP streams.

1. **Initialize the Node.js Project**

   First, create a project directory and initialize a new Node.js project:

   ```bash
    mkdir rtsp-stream-relay
    cd rtsp-stream-relay
    npm init -y
   ```
2. **Install Required Dependencies**

   We’ll need to install the following packages:
   - `express`: For creating the server.
   - `cors`: For enabling Cross-Origin Resource Sharing.
   - `rtsp-relay`: A package that simplifies relaying RTSP streams over WebSockets.

Install the required packages:

```bash
    npm install express cors rtsp-relay
```

3. **Set Up the Express Server**

   Create an `index.js` file and add the following code:

   ```javascript
    const cors = require('cors');
    const express = require('express');
    const { proxy } = require('rtsp-relay');

    const app = express();
    app.use(cors());

    const handler = (url) => {
      return proxy({
        additionalFlags: ['-q', '1'],  // Reduce quality for lower bandwidth
        url: url,
        transport: 'tcp',             // Use TCP for stream transport
        verbose: true,                // Print FFmpeg logs
      });
    };

    app.ws('/api/stream', (ws, req) => {
      const url = req.query.url;      // Get RTSP URL from query parameter
      handler(url)(ws, req);          // Proxy RTSP stream via WebSocket
    });

    app.listen(3000, () => {
      console.log('RTSP Stream relay running on port 3000');
    });
   ```

This basic Express server listens for WebSocket connections on `/api/stream`, accepts an RTSP URL as a query parameter, and relays the stream via WebSocket.

### Step 2: Add FFmpeg to Handle RTSP

FFmpeg is responsible for handling the actual RTSP stream. The `rtsp-relay` package internally uses FFmpeg to convert the RTSP stream into a format that can be sent via WebSocket.

The `proxy` function used in the `index.js` file relays the RTSP stream from the specified `url` and transmits it over WebSocket. This is where the stream is processed and relayed efficiently.

---

## Step 3: Packaging the Server with Docker

Next, we’ll containerize the entire application using Docker. This makes it easy to deploy on any platform without worrying about dependencies.

1. **Create a Dockerfile**

   Create a `Dockerfile` to define the container environment:

   ```dockerfile
    FROM ubuntu:22.04

    RUN apt-get update && apt-get install -y ffmpeg

    RUN apt-get install -y curl
    RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    RUN apt-get install -y nodejs

    WORKDIR /app
    COPY package.json yarn.lock ./
    RUN npm install

    COPY . .

    EXPOSE 3000

    CMD ["node", "index.js"]
   ```

This Dockerfile uses an Ubuntu base image, installs FFmpeg and Node.js, and runs the Node.js server on port `3000`.

2. **Build and Run the Docker Image**

   Build the Docker image and run the container:

   ```bash
    docker build -t rtsp-relay-app .
    docker run -p 3000:3000 rtsp-relay-app
   ```

Your RTSP relay server is now running inside the Docker container!

---

## Step 4: Viewing the Stream in a Browser

To consume the WebSocket stream in a browser, you’ll need to use the `MediaSource` API or a video player that supports WebSocket.

### React Example

You can use React to display the video stream:

```jsx
import React, { useEffect, useRef } from "react";

const RTSPStream = ({ streamUrl }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:3000/api/stream?url=${streamUrl}`);
    ws.onmessage = (event) => {
      const video = videoRef.current;
      const mediaSource = new MediaSource();
      video.src = URL.createObjectURL(mediaSource);
      mediaSource.addEventListener("sourceopen", () => {
        const sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E"');
        sourceBuffer.appendBuffer(event.data);
      });
    };
  }, [streamUrl]);

  return <video ref={videoRef} controls autoPlay />;
};

export default RTSPStream;
```

This React component establishes a WebSocket connection and renders the stream in a video element.

## Conclusion

Streaming RTSP feeds to the browser isn’t natively supported, but by using FFmpeg and WebSockets with a Node.js server, you can create a real-time, two-way relay that efficiently delivers RTSP streams to web clients.

With a Dockerized environment and an npm package, this solution becomes even more accessible and portable for any development workflow.
