with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Already mostly applied dark theme during initial HTML creation.
# Need to make sure inputs look like the image (darker background for inputs, border styling).

css_update = """
        /* Extra styling for a modern dark theme */
        .panel {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .input-value {
            background-color: #1a1a24;
            color: #60a5fa;
            border: 1px solid #3f3f46;
        }
        input[type=range]::-webkit-slider-runnable-track {
            background: #3f3f46;
        }
        .radio-group {
            background-color: #1a1a24;
            border: 1px solid #3f3f46;
        }
        .radio-label {
            border-right: 1px solid #3f3f46;
            color: #a1a1aa;
        }
        .radio-input:checked + .radio-label {
            background: #2563eb;
            color: #ffffff;
        }
"""

html = html.replace("/* Utilities */", css_update + "\n        /* Utilities */")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
