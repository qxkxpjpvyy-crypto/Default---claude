with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

summary_html = """
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--input-bg); padding: 12px; border-radius: 8px;">
                            <span class="text-sm">구매가 유리할 확률</span>
                            <span id="prob-buy-better" style="font-size: 1.5rem; font-weight: bold; color: var(--accent-blue);">--%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--input-bg); padding: 12px; border-radius: 8px;">
                            <span class="text-sm">중앙값(Median) 순자산 (구매)</span>
                            <span id="median-buy" style="font-size: 1.25rem; font-weight: bold;">--원</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--input-bg); padding: 12px; border-radius: 8px;">
                            <span class="text-sm">중앙값(Median) 순자산 (임대)</span>
                            <span id="median-rent" style="font-size: 1.25rem; font-weight: bold;">--원</span>
                        </div>
                    </div>
"""

charts_html = """
                    <div style="position: relative; width: 100%; height: 300px; background: var(--input-bg); border-radius: 8px; overflow: hidden; padding: 10px;">
                        <canvas id="dist-chart"></canvas>
                        <div style="position: absolute; top: 10px; left: 10px; font-size: 0.8rem; font-weight: bold;">구매 우위 차액 분포 (원)</div>
                    </div>
                    <div style="position: relative; width: 100%; height: 300px; background: var(--input-bg); border-radius: 8px; overflow: hidden; padding: 10px;">
                        <canvas id="quant-chart"></canvas>
                        <div style="position: absolute; top: 10px; left: 10px; font-size: 0.8rem; font-weight: bold;">구매 우위 분위수 분석 (원)</div>
                    </div>
"""

script_charts = """
        // --- Output & Canvas Charting ---
        function getQuantile(sortedArr, q) {
            const pos = (sortedArr.length - 1) * q;
            const base = Math.floor(pos);
            const rest = pos - base;
            if (sortedArr[base + 1] !== undefined) {
                return sortedArr[base] + rest * (sortedArr[base + 1] - sortedArr[base]);
            } else {
                return sortedArr[base];
            }
        }

        function updateSummary(results) {
            let buyBetterCount = results.differences.filter(d => d > 0).length;
            let prob = (buyBetterCount / results.differences.length) * 100;
            document.getElementById('prob-buy-better').innerText = prob.toFixed(1) + "%";

            let medianBuy = getQuantile(results.buyFinalNW, 0.5);
            let medianRent = getQuantile(results.rentFinalNW, 0.5);

            document.getElementById('median-buy').innerText = formatMoney(medianBuy);
            document.getElementById('median-rent').innerText = formatMoney(medianRent);
        }

        function drawCharts(results) {
            drawHistogram(results.differences, 'dist-chart');
            drawQuantileBarChart(results.differences, 'quant-chart');
        }

        function drawHistogram(data, canvasId) {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');

            // Handle resizing
            const rect = canvas.parentElement.getBoundingClientRect();
            canvas.width = rect.width - 20;
            canvas.height = rect.height - 20;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const bins = 40;
            const min = data[0];
            const max = data[data.length - 1];
            const range = max - min;
            const binSize = range / bins;

            let frequencies = new Array(bins).fill(0);
            for (let val of data) {
                let binIndex = Math.floor((val - min) / binSize);
                if (binIndex >= bins) binIndex = bins - 1;
                frequencies[binIndex]++;
            }

            const maxFreq = Math.max(...frequencies);
            const pad = 30;
            const w = canvas.width - (pad * 2);
            const h = canvas.height - (pad * 2);

            // Draw zero line if it exists within range
            if (min < 0 && max > 0) {
                let zeroX = pad + ((0 - min) / range) * w;
                ctx.beginPath();
                ctx.setLineDash([5, 5]);
                ctx.moveTo(zeroX, pad);
                ctx.lineTo(zeroX, canvas.height - pad);
                ctx.strokeStyle = '#666';
                ctx.stroke();
                ctx.setLineDash([]);
            }

            // Draw bars
            for (let i = 0; i < bins; i++) {
                let barH = (frequencies[i] / maxFreq) * h;
                let x = pad + (i / bins) * w;
                let y = canvas.height - pad - barH;

                let binCenter = min + (i + 0.5) * binSize;

                // Color gradient based on positive/negative
                if (binCenter > 0) {
                    ctx.fillStyle = `rgba(59, 130, 246, ${Math.max(0.3, barH/h)})`; // blue
                } else {
                    ctx.fillStyle = `rgba(16, 185, 129, ${Math.max(0.3, barH/h)})`; // green/teal (matches image)
                }

                ctx.fillRect(x, y, w / bins - 1, barH);
            }

            // X Axis Labels
            ctx.fillStyle = '#a0a0a0';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(formatMoney(min), pad, canvas.height - 10);
            ctx.fillText(formatMoney(max), canvas.width - pad, canvas.height - 10);
            if (min < 0 && max > 0) {
                ctx.fillText("0원", pad + ((0 - min) / range) * w, canvas.height - 10);
            }
        }

        function drawQuantileBarChart(data, canvasId) {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');

            const rect = canvas.parentElement.getBoundingClientRect();
            canvas.width = rect.width - 20;
            canvas.height = rect.height - 20;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const q10 = getQuantile(data, 0.1);
            const q25 = getQuantile(data, 0.25);
            const q50 = getQuantile(data, 0.50);
            const mean = data.reduce((a, b) => a + b, 0) / data.length;
            const q75 = getQuantile(data, 0.75);
            const q90 = getQuantile(data, 0.90);

            const labels = ['P10', 'P25', '중앙값', '평균', 'P75', 'P90'];
            const values = [q10, q25, q50, mean, q75, q90];

            const padX = 50;
            const padY = 30;
            const w = canvas.width - padX * 2;
            const h = canvas.height - padY * 2;

            const min = Math.min(...values, -100000000); // ensure some negative space
            const max = Math.max(...values, 100000000);
            const range = max - min;

            let zeroX = padX + ((0 - min) / range) * w;

            // Draw zero line
            ctx.beginPath();
            ctx.setLineDash([5, 5]);
            ctx.moveTo(zeroX, padY);
            ctx.lineTo(zeroX, canvas.height - padY);
            ctx.strokeStyle = '#666';
            ctx.stroke();
            ctx.setLineDash([]);

            // Draw bars
            const barHeight = (h / values.length) * 0.6;
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';

            for (let i = 0; i < values.length; i++) {
                let val = values[i];
                let y = padY + (i + 0.5) * (h / values.length);

                ctx.fillStyle = '#a0a0a0';
                ctx.fillText(labels[i], padX - 10, y);

                let barW = Math.abs((val / range) * w);
                let x = val < 0 ? zeroX - barW : zeroX;

                if (val > 0) {
                    ctx.fillStyle = '#3b82f6'; // blue
                } else {
                    ctx.fillStyle = '#ef4444'; // red
                }

                ctx.fillRect(x, y - barHeight / 2, barW, barHeight);
            }

            // X Axis
            ctx.fillStyle = '#a0a0a0';
            ctx.textAlign = 'center';
            ctx.fillText(formatMoney(min), padX, canvas.height - 10);
            ctx.fillText(formatMoney(max), canvas.width - padX, canvas.height - 10);
            ctx.fillText("0원", zeroX, canvas.height - 10);
        }

        // Add event listeners to redraw on input change
        document.addEventListener('DOMContentLoaded', () => {
            const inputs = document.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('change', runSimulation);
                if (input.type === 'range') {
                    input.addEventListener('input', runSimulation);
                }
            });
            // Initial run
            setTimeout(runSimulation, 100);

            window.addEventListener('resize', runSimulation);
        });
"""

html = html.replace('<p class="text-muted text-sm">결과 요약 영역 (진행 예정)</p>', summary_html)

html = html.replace("""                    <div style="height: 300px; background: var(--input-bg); border-radius: 8px; display: flex; align-items: center; justify-content: center;" class="text-muted text-sm">
                        분포 차트 영역
                    </div>
                    <div style="height: 300px; background: var(--input-bg); border-radius: 8px; display: flex; align-items: center; justify-content: center;" class="text-muted text-sm">
                        분위수 분석 차트 영역
                    </div>""", charts_html)

html = html.replace("// Initialize formatting on load", script_charts + "\n        // Initialize formatting on load")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
