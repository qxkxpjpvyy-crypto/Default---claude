with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

regs_css = """
        /* Checkbox Toggles for Regulations */
        .toggle-group {
            display: flex;
            align-items: flex-start;
            margin-bottom: 16px;
            padding: 12px;
            background: var(--input-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        .toggle-input {
            margin-top: 4px;
            margin-right: 12px;
            width: 16px;
            height: 16px;
            accent-color: var(--accent-blue);
        }
        .toggle-content { flex: 1; }
        .toggle-title { font-weight: 500; font-size: 0.95rem; margin-bottom: 4px; }
        .toggle-desc { font-size: 0.8rem; color: var(--text-muted); }
        .citation {
            font-size: 0.75rem;
            color: var(--accent-green);
            margin-top: 4px;
            display: inline-block;
        }
"""

regs_html = """
                    <!-- LTV/DSR 규제 -->
                    <div class="toggle-group">
                        <input type="checkbox" id="reg-ltv" class="toggle-input" checked>
                        <div class="toggle-content">
                            <label for="reg-ltv" class="toggle-title">LTV / DSR 대출 규제 적용</label>
                            <div class="toggle-desc">무주택자 LTV 70%, DSR 40% 한도 적용하여 최대 대출 가능액을 제한합니다.</div>
                            <div class="citation">근거: 금융위원회 은행업감독규정 제79조</div>
                        </div>
                    </div>

                    <!-- 취득세 다주택자 중과 -->
                    <div class="toggle-group">
                        <input type="checkbox" id="reg-acq-tax" class="toggle-input" checked>
                        <div class="toggle-content">
                            <label for="reg-acq-tax" class="toggle-title">취득세 누진세율 적용</label>
                            <div class="toggle-desc">주택 가액에 따라 1~3%의 누진 취득세율 및 지방교육세를 적용합니다.</div>
                            <div class="citation">근거: 지방세법 제11조 (부동산 취득의 세율)</div>
                        </div>
                    </div>

                    <!-- 종합부동산세 -->
                    <div class="toggle-group">
                        <input type="checkbox" id="reg-property-tax" class="toggle-input" checked>
                        <div class="toggle-content">
                            <label for="reg-property-tax" class="toggle-title">재산세 및 종합부동산세 (보유세) 적용</label>
                            <div class="toggle-desc">공시가격(시세의 70% 가정)을 기준으로 매년 재산세 및 종부세(12억 초과분)를 공제합니다.</div>
                            <div class="citation">근거: 종합부동산세법 제8조 및 지방세법 제111조</div>
                        </div>
                    </div>

                    <!-- 1세대 1주택 비과세 -->
                    <div class="toggle-group">
                        <input type="checkbox" id="reg-cap-gains" class="toggle-input" checked>
                        <div class="toggle-content">
                            <label for="reg-cap-gains" class="toggle-title">1세대 1주택 양도소득세 비과세 적용</label>
                            <div class="toggle-desc">매도 시 실거래가 12억 이하 양도세 비과세, 12억 초과분에 한해 과세합니다 (보유/거주 요건 충족 가정).</div>
                            <div class="citation">근거: 소득세법 제89조 (비과세 양도소득)</div>
                        </div>
                    </div>
"""

# Insert CSS
html = html.replace("/* Input Controls */", regs_css + "\n        /* Input Controls */")

# Insert HTML regs
html = html.replace('<p class="text-muted text-sm">한국 부동산 규제 옵션 영역 (진행 예정)</p>', regs_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
