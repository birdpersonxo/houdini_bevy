# houdini_bevy

<p align="center">
  <img src="assets/houdini-icon.png" alt="Houdini Icon" width="33" style="display:inline-block; vertical-align:middle;" />
  <img src="assets/bevy-logo.png" alt="Bevy Icon" width="33" style="display:inline-block; vertical-align:middle; margin-left:8px;" />
</p>

**houdini_bevy** is a Python module and set of Houdini Digital Assets (HDAs) designed to support **interactive level authoring for Bevy projects** inside Houdini.

Currently tools focus on quickly drawing and exporting simple 2D platform geometry, with an emphasis on iteration and ease of use.

## Core Concept
* Houdini is used as a **level-authoring tool**
* Interactive HDAs allow you to **draw 2D rectangles directly in the viewport**
* The resulting data is exported in a format that can be consumed by Bevy via `bevy_hou`

## Usage Overview

1. Install the `houdini_bevy` Python module
2. Load the provided HDAs into Houdini
3. Use the interactive rectangle HDA to draw 2D platforms
4. Export the rectangle data using the Python tools
5. Import the data into Bevy via `bevy_hou`

## Status & Limitations
* Currently supports **rectangles only**
* Intended for 2D platforming use cases
* APIs, HDAs, and export formats are subject to change

## Features
- [x] Draw and export rectangle shapes
- [ ] Export any shapes from houdini as (USD / GLTF)
- [ ] Per-primitive metadata (gameplay tags, layers)
- [ ] Live-reload or tighter Bevy integration

## Relationship to `bevy_hou`

`houdini_bevy` is the **authoring side** of the pipeline.

* Houdini is used to create and edit data
* `bevy_hou` consumes that data at runtime
