const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');
const search = `<<<<<<< HEAD
                let sellBrokerFee = houseVal * costSelling;
                let sellTax = 0;
                if (applyCapGains) {
                    let profit = houseVal - targetPrice - sellBrokerFee;
                    if (profit > 0 && houseVal > 1200000000) {
                        let taxableRatio = (houseVal - 1200000000) / houseVal;
                        sellTax = profit * taxableRatio * 0.20; // Simplified 20%
                    }
                } else {
                     let profit = houseVal - targetPrice - sellBrokerFee;
                     if (profit > 0) sellTax = profit * 0.20;
                }

                let finalBuyNW = hasBought ? (houseVal + buy_Liquid - remainingLoan - sellBrokerFee - sellTax) : (buy_Liquid + currentRentDeposit - currentJeonseLoan);
=======
                let finalSellingCost = calculateSellingCost(targetPrice, houseVal, applyCapGains, costSelling);
                let finalBuyNW = houseVal + buy_Liquid - remainingLoan - finalSellingCost;
>>>>>>> origin/main`;

const replace = `                let finalSellingCost = calculateSellingCost(targetPrice, houseVal, applyCapGains, costSelling);
                let finalBuyNW = hasBought ? (houseVal + buy_Liquid - remainingLoan - finalSellingCost) : (buy_Liquid + currentRentDeposit - currentJeonseLoan);`;

html = html.replace(search, replace);
fs.writeFileSync('index.html', html);
