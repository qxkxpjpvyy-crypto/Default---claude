with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

script_js = """
        // --- Monte Carlo Simulation Engine ---

        // Box-Muller transform for standard normal distribution
        function randomNormal() {
            let u = 0, v = 0;
            while(u === 0) u = Math.random();
            while(v === 0) v = Math.random();
            return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
        }

        // Get value from inputs
        function getVal(id) {
            return parseInt(document.getElementById(id).value, 10);
        }

        // Tax calculation logic
        function calculateTaxesAndCosts(price, isBuying, hasAcqTax, hasCapGainsTax) {
            let costs = 0;

            // 1. Acquisition Tax (취득세)
            if (isBuying && hasAcqTax) {
                let rate = 0.01; // Base 1% under 600m
                if (price > 900000000) rate = 0.03; // Over 900m is 3%
                else if (price > 600000000) rate = 0.01 + ((price - 600000000) / 300000000) * 0.02; // Linear scale
                costs += price * rate;
                costs += price * 0.002; // Local education tax (approx)
            }

            return costs;
        }

        function calculateYearlyHoldingCost(price, hasPropertyTax) {
            if (!hasPropertyTax) return 0;
            let assessedValue = price * 0.7; // 공시가격 현실화율 70% 가정
            let tax = 0;

            // 재산세 (Property Tax) - Simplified
            tax += assessedValue * 0.002;

            // 종합부동산세 (Comprehensive Real Estate Tax) - Simplified for 1 house > 1.2B
            if (assessedValue > 1200000000) {
                tax += (assessedValue - 1200000000) * 0.005; // Base rate
            }
            return tax;
        }

        function calculateSellingCost(buyPrice, sellPrice, hasCapGainsTax) {
            let brokerFee = sellPrice * 0.005; // 중개수수료 0.5% 가정
            let profit = sellPrice - buyPrice - brokerFee;
            let capGainsTax = 0;

            if (profit > 0 && hasCapGainsTax) {
                // 1세대 1주택 12억 이하 비과세 적용
                if (sellPrice > 1200000000) {
                    let taxableRatio = (sellPrice - 1200000000) / sellPrice;
                    let taxableProfit = profit * taxableRatio;
                    // 장기보유특별공제 및 기본공제 등 간소화하여 단일세율 20% 가정
                    capGainsTax = taxableProfit * 0.20;
                }
            } else if (profit > 0 && !hasCapGainsTax) {
                capGainsTax = profit * 0.20; // 비과세 미적용시
            }

            return brokerFee + capGainsTax;
        }

        function runSimulation() {
            // Inputs
            const targetPrice = getVal('target-price');
            const currentNW = getVal('current-net-worth');
            const monthlySavings = getVal('monthly-savings');

            const isJeonse = document.getElementById('rent-type-jeonse').checked;
            const rentDeposit = isJeonse ? getVal('jeonse-deposit') : getVal('monthly-deposit');
            const monthlyRent = isJeonse ? 0 : getVal('monthly-rent');

            // Investment profile
            let investProfile = document.querySelector('input[name="invest-profile"]:checked').value;
            let expectedMarketReturn = 0.05; // Neutral
            let marketVol = 0.10;
            if (investProfile === 'conservative') { expectedMarketReturn = 0.03; marketVol = 0.05; }
            if (investProfile === 'aggressive') { expectedMarketReturn = 0.08; marketVol = 0.15; }

            // Regulations
            const applyLTV = document.getElementById('reg-ltv').checked;
            const applyAcqTax = document.getElementById('reg-acq-tax').checked;
            const applyPropTax = document.getElementById('reg-property-tax').checked;
            const applyCapGains = document.getElementById('reg-cap-gains').checked;

            const years = getVal('analysis-years');
            const simCount = getVal('sim-count');

            // Assumptions for Housing Market
            const expectedHouseReturn = 0.03; // Long term housing appreciation
            const houseVol = 0.07;
            const expectedRentInflation = 0.02;

            // Loan Logic
            const mortgageRate = 0.045; // Fixed 4.5% assumption

            let results = {
                buyFinalNW: [],
                rentFinalNW: [],
                differences: [] // Buy - Rent
            };

            for (let s = 0; s < simCount; s++) {
                // --- BUY SCENARIO ---
                let buy_NW = currentNW;
                let loanAmount = targetPrice - buy_NW;

                // Regulation: LTV/DSR limit
                if (applyLTV) {
                    let maxLTV = targetPrice * 0.7;
                    if (loanAmount > maxLTV) {
                        loanAmount = maxLTV; // Need more cash to buy, but let's assume they buy a cheaper house or find cash.
                        // For simplicity in this calculator: If they can't afford it due to LTV, the simulation just maxes the loan and assumes they scrounge up the rest.
                    }
                }

                if (loanAmount < 0) loanAmount = 0;

                let houseVal = targetPrice;
                let buy_Liquid = buy_NW - (targetPrice - loanAmount) - calculateTaxesAndCosts(targetPrice, true, applyAcqTax, applyCapGains);

                // Amortization assumption (interest only for simplicity, principal paid at end)
                let yearlyMortgageInterest = loanAmount * mortgageRate;

                // --- RENT SCENARIO ---
                let rent_NW = currentNW;
                let currentRentDeposit = rentDeposit;
                let currentMonthlyRent = monthlyRent;
                let rent_Liquid = rent_NW - currentRentDeposit;

                // Year by year simulation
                for (let y = 0; y < years; y++) {
                    // Random shocks
                    let houseShock = randomNormal() * houseVol;
                    let marketShock = randomNormal() * marketVol;

                    // BUY
                    houseVal *= (1 + expectedHouseReturn + houseShock);
                    buy_Liquid = buy_Liquid * (1 + expectedMarketReturn + marketShock);
                    buy_Liquid += (monthlySavings * 12);
                    buy_Liquid -= yearlyMortgageInterest;
                    buy_Liquid -= calculateYearlyHoldingCost(houseVal, applyPropTax);

                    // RENT
                    rent_Liquid = rent_Liquid * (1 + expectedMarketReturn + marketShock);
                    rent_Liquid += (monthlySavings * 12);
                    rent_Liquid -= (currentMonthlyRent * 12);

                    // Rent inflation every 2 years (typical Korean contract)
                    if (y % 2 === 1) {
                        let inflation = 1 + expectedRentInflation * 2;
                        let extraDeposit = currentRentDeposit * (inflation - 1);
                        rent_Liquid -= extraDeposit; // pay more deposit from liquid
                        currentRentDeposit *= inflation;
                        currentMonthlyRent *= inflation;
                    }
                }

                // End of simulation liquidation
                let buySellingCost = calculateSellingCost(targetPrice, houseVal, applyCapGains);
                let finalBuyNW = houseVal + buy_Liquid - loanAmount - buySellingCost;
                let finalRentNW = currentRentDeposit + rent_Liquid;

                results.buyFinalNW.push(finalBuyNW);
                results.rentFinalNW.push(finalRentNW);
                results.differences.push(finalBuyNW - finalRentNW);
            }

            results.buyFinalNW.sort((a,b) => a-b);
            results.rentFinalNW.sort((a,b) => a-b);
            results.differences.sort((a,b) => a-b);

            drawCharts(results);
            updateSummary(results);
        }

        function formatMoney(amount) {
            const eok = Math.floor(amount / 100000000);
            const man = Math.floor((Math.abs(amount) % 100000000) / 10000);
            if (eok === 0) return man + "만";
            return eok + "억 " + (man > 0 ? man + "만" : "");
        }
"""

html = html.replace("// Initialize formatting on load", script_js + "\n        // Initialize formatting on load")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
