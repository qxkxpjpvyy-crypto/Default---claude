const fs = require('fs');
const path = require('path');

// Extract the function from index.html
const htmlContent = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
const functionMatch = htmlContent.match(/function calculateSellingCost\(buyPrice, sellPrice, hasCapGainsTax, brokerFeeRate = 0\.005\) \{[\s\S]*?return brokerFee \+ capGainsTax;\s*\}/);

if (!functionMatch) {
    console.error('Could not find calculateSellingCost function in index.html');
    process.exit(1);
}

const calculateSellingCostStr = functionMatch[0];
const calculateSellingCost = eval(`(${calculateSellingCostStr})`);

function assertEqual(actual, expected, message) {
    if (Math.abs(actual - expected) > 0.0001) {
        throw new Error(`Test failed: ${message}. Expected ${expected}, but got ${actual}`);
    }
    console.log(`PASS: ${message}`);
}

function runTests() {
    console.log('Running tests for calculateSellingCost...');

    // Scenario 1: No profit, no tax
    // buyPrice: 1B, sellPrice: 1B, hasCapGainsTax: true, brokerFeeRate: 0.005
    // brokerFee = 1B * 0.005 = 5M
    // profit = 1B - 1B - 5M = -5M
    // capGainsTax = 0
    // total = 5M
    assertEqual(calculateSellingCost(1000000000, 1000000000, true, 0.005), 5000000, 'Scenario 1: No profit, no tax');

    // Scenario 2: Profit < 1.2B, exemption applied
    // buyPrice: 800M, sellPrice: 1B, hasCapGainsTax: true, brokerFeeRate: 0.005
    // brokerFee = 1B * 0.005 = 5M
    // profit = 1B - 800M - 5M = 195M
    // capGainsTax = 0 (sellPrice <= 1.2B and hasCapGainsTax is true)
    // total = 5M
    assertEqual(calculateSellingCost(800000000, 1000000000, true, 0.005), 5000000, 'Scenario 2: Profit < 1.2B, exemption applied');

    // Scenario 3: Profit < 1.2B, but exemption NOT applied (hasCapGainsTax = false)
    // buyPrice: 800M, sellPrice: 1B, hasCapGainsTax: false, brokerFeeRate: 0.005
    // brokerFee = 1B * 0.005 = 5M
    // profit = 1B - 800M - 5M = 195M
    // capGainsTax = 195M * 0.20 = 39M
    // total = 5M + 39M = 44M
    assertEqual(calculateSellingCost(800000000, 1000000000, false, 0.005), 44000000, 'Scenario 3: Profit < 1.2B, no exemption');

    // Scenario 4: Sell Price exactly 1.2B, exemption applied
    // buyPrice: 800M, sellPrice: 1.2B, hasCapGainsTax: true, brokerFeeRate: 0.005
    // brokerFee = 1.2B * 0.005 = 6M
    // profit = 1.2B - 800M - 6M = 394M
    // capGainsTax = 0
    // total = 6M
    assertEqual(calculateSellingCost(800000000, 1200000000, true, 0.005), 6000000, 'Scenario 4: Sell Price exactly 1.2B, exemption');

    // Scenario 5: Sell Price > 1.2B, partial exemption
    // buyPrice: 1B, sellPrice: 2B, hasCapGainsTax: true, brokerFeeRate: 0.005
    // brokerFee = 2B * 0.005 = 10M
    // profit = 2B - 1B - 10M = 990M
    // taxableRatio = (2B - 1.2B) / 2B = 0.8B / 2B = 0.4
    // taxableProfit = 990M * 0.4 = 396M
    // capGainsTax = 396M * 0.20 = 79.2M
    // total = 10M + 79.2M = 89.2M
    assertEqual(calculateSellingCost(1000000000, 2000000000, true, 0.005), 89200000, 'Scenario 5: Sell Price > 1.2B, partial exemption');

    // Scenario 6: Sell Price > 1.2B, no exemption
    // buyPrice: 1B, sellPrice: 2B, hasCapGainsTax: false, brokerFeeRate: 0.005
    // brokerFee = 2B * 0.005 = 10M
    // profit = 2B - 1B - 10M = 990M
    // capGainsTax = 990M * 0.20 = 198M
    // total = 10M + 198M = 208M
    assertEqual(calculateSellingCost(1000000000, 2000000000, false, 0.005), 208000000, 'Scenario 6: Sell Price > 1.2B, no exemption');

    // Scenario 7: Custom broker fee rate
    // buyPrice: 800M, sellPrice: 1B, hasCapGainsTax: true, brokerFeeRate: 0.01 (1%)
    // brokerFee = 1B * 0.01 = 10M
    // profit = 1B - 800M - 10M = 190M
    // capGainsTax = 0
    // total = 10M
    assertEqual(calculateSellingCost(800000000, 1000000000, true, 0.01), 10000000, 'Scenario 7: Custom broker fee rate');

    console.log('All tests passed!');
}

try {
    runTests();
} catch (error) {
    console.error(error.message);
    process.exit(1);
}
