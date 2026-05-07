import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

input_css = """
        /* Input Controls */
        .input-group { margin-bottom: 16px; }
        .input-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .input-label { font-size: 0.9rem; font-weight: 500; }
        .input-value { font-size: 0.9rem; color: var(--accent-blue); font-weight: bold; background: var(--input-bg); padding: 4px 8px; border-radius: 4px; border: 1px solid var(--border-color); text-align: right; width: 120px;}

        input[type=range] {
            -webkit-appearance: none;
            width: 100%;
            background: transparent;
            margin: 8px 0;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: var(--accent-blue);
            cursor: pointer;
            margin-top: -6px;
        }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 4px;
            cursor: pointer;
            background: var(--border-color);
            border-radius: 2px;
        }

        .radio-group {
            display: flex;
            background: var(--input-bg);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            margin-top: 8px;
        }
        .radio-label {
            flex: 1;
            text-align: center;
            padding: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            border-right: 1px solid var(--border-color);
            transition: background 0.2s;
        }
        .radio-label:last-child { border-right: none; }
        .radio-input { display: none; }
        .radio-input:checked + .radio-label {
            background: var(--accent-blue);
            color: white;
            font-weight: bold;
        }
"""

inputs_html = """
                    <!-- 목표 주택 가격 -->
                    <div class="input-group">
                        <div class="input-header">
                            <label class="input-label" for="target-price">목표 주택 가격 (원)</label>
                            <input type="text" id="target-price-val" class="input-value" value="1,000,000,000" onchange="updateSlider('target-price', this.value)">
                        </div>
                        <input type="range" id="target-price" min="100000000" max="5000000000" step="10000000" value="1000000000" oninput="updateInput('target-price-val', this.value)">
                    </div>

                    <!-- 현재 보유 순자산 -->
                    <div class="input-group">
                        <div class="input-header">
                            <label class="input-label" for="current-net-worth">현재 보유 순자산 (원)</label>
                            <input type="text" id="current-net-worth-val" class="input-value" value="300,000,000" onchange="updateSlider('current-net-worth', this.value)">
                        </div>
                        <input type="range" id="current-net-worth" min="0" max="3000000000" step="10000000" value="300000000" oninput="updateInput('current-net-worth-val', this.value)">
                    </div>

                    <!-- 예상 월 저축액 -->
                    <div class="input-group">
                        <div class="input-header">
                            <label class="input-label" for="monthly-savings">예상 월 저축액 (원)</label>
                            <input type="text" id="monthly-savings-val" class="input-value" value="2,000,000" onchange="updateSlider('monthly-savings', this.value)">
                        </div>
                        <input type="range" id="monthly-savings" min="0" max="10000000" step="100000" value="2000000" oninput="updateInput('monthly-savings-val', this.value)">
                    </div>

                    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 20px 0;">

                    <!-- 현재 거주 형태 -->
                    <div class="input-group">
                        <label class="input-label">현재 거주 형태</label>
                        <div class="radio-group">
                            <input type="radio" id="rent-type-jeonse" name="rent-type" class="radio-input" value="jeonse" checked onchange="toggleRentInputs()">
                            <label for="rent-type-jeonse" class="radio-label">전세</label>

                            <input type="radio" id="rent-type-monthly" name="rent-type" class="radio-input" value="monthly" onchange="toggleRentInputs()">
                            <label for="rent-type-monthly" class="radio-label">월세</label>
                        </div>
                    </div>

                    <!-- 전세 보증금 -->
                    <div class="input-group" id="group-jeonse-deposit">
                        <div class="input-header">
                            <label class="input-label" for="jeonse-deposit">전세 보증금 (원)</label>
                            <input type="text" id="jeonse-deposit-val" class="input-value" value="200,000,000" onchange="updateSlider('jeonse-deposit', this.value)">
                        </div>
                        <input type="range" id="jeonse-deposit" min="0" max="2000000000" step="10000000" value="200000000" oninput="updateInput('jeonse-deposit-val', this.value)">
                    </div>

                    <!-- 월세 보증금 (Hidden by default) -->
                    <div class="input-group" id="group-monthly-deposit" style="display: none;">
                        <div class="input-header">
                            <label class="input-label" for="monthly-deposit">월세 보증금 (원)</label>
                            <input type="text" id="monthly-deposit-val" class="input-value" value="50,000,000" onchange="updateSlider('monthly-deposit', this.value)">
                        </div>
                        <input type="range" id="monthly-deposit" min="0" max="1000000000" step="5000000" value="50000000" oninput="updateInput('monthly-deposit-val', this.value)">
                    </div>

                    <!-- 월세 (Hidden by default) -->
                    <div class="input-group" id="group-monthly-rent" style="display: none;">
                        <div class="input-header">
                            <label class="input-label" for="monthly-rent">월세 (원)</label>
                            <input type="text" id="monthly-rent-val" class="input-value" value="1,000,000" onchange="updateSlider('monthly-rent', this.value)">
                        </div>
                        <input type="range" id="monthly-rent" min="0" max="10000000" step="50000" value="1000000" oninput="updateInput('monthly-rent-val', this.value)">
                    </div>

                    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 20px 0;">

                    <!-- 투자 성향 -->
                    <div class="input-group">
                        <label class="input-label">투자 성향 (수익률 가정)</label>
                        <div class="radio-group">
                            <input type="radio" id="invest-conservative" name="invest-profile" class="radio-input" value="conservative">
                            <label for="invest-conservative" class="radio-label">안정형 (3%)</label>

                            <input type="radio" id="invest-neutral" name="invest-profile" class="radio-input" value="neutral" checked>
                            <label for="invest-neutral" class="radio-label">중립형 (5%)</label>

                            <input type="radio" id="invest-aggressive" name="invest-profile" class="radio-input" value="aggressive">
                            <label for="invest-aggressive" class="radio-label">공격형 (8%)</label>
                        </div>
                    </div>

                    <!-- 분석 기간 -->
                    <div class="input-group">
                        <div class="input-header">
                            <label class="input-label" for="analysis-years">분석 기간 (년)</label>
                            <input type="text" id="analysis-years-val" class="input-value" value="20" onchange="updateSlider('analysis-years', this.value)">
                        </div>
                        <input type="range" id="analysis-years" min="5" max="50" step="1" value="20" oninput="updateInput('analysis-years-val', this.value)">
                    </div>

                    <!-- 시뮬레이션 횟수 -->
                    <div class="input-group">
                        <div class="input-header">
                            <label class="input-label" for="sim-count">시뮬레이션 횟수</label>
                            <input type="text" id="sim-count-val" class="input-value" value="1,000" onchange="updateSlider('sim-count', this.value)">
                        </div>
                        <input type="range" id="sim-count" min="100" max="10000" step="100" value="1000" oninput="updateInput('sim-count-val', this.value)">
                    </div>
"""

script_js = """
    <script>
        function formatNumber(num) {
            return num.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");
        }

        function parseNumber(str) {
            return parseInt(str.replace(/,/g, ''), 10) || 0;
        }

        function updateInput(inputId, value) {
            document.getElementById(inputId).value = formatNumber(value);
        }

        function updateSlider(sliderId, value) {
            let num = parseNumber(value);
            let slider = document.getElementById(sliderId);
            if(num < slider.min) num = slider.min;
            if(num > slider.max) num = slider.max;
            slider.value = num;
            document.getElementById(sliderId + '-val').value = formatNumber(num);
        }

        function toggleRentInputs() {
            const isJeonse = document.getElementById('rent-type-jeonse').checked;
            document.getElementById('group-jeonse-deposit').style.display = isJeonse ? 'block' : 'none';
            document.getElementById('group-monthly-deposit').style.display = isJeonse ? 'none' : 'block';
            document.getElementById('group-monthly-rent').style.display = isJeonse ? 'none' : 'block';
        }

        // Initialize formatting on load
        window.onload = function() {
            const inputs = document.querySelectorAll('input[type=range]');
            inputs.forEach(input => {
                updateInput(input.id + '-val', input.value);
            });
        };
    </script>
"""

# Insert CSS
html = html.replace("</style>", input_css + "\n    </style>")

# Insert HTML inputs
html = html.replace('<p class="text-muted text-sm">입력 폼 영역 (진행 예정)</p>', inputs_html)

# Insert Script
html = html.replace("</body>", script_js + "\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
