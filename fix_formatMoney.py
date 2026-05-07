with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the formatMoney function
old_func = """        function formatMoney(amount) {
            const eok = Math.floor(amount / 100000000);
            const man = Math.floor((Math.abs(amount) % 100000000) / 10000);
            if (eok === 0) return man + "만";
            return eok + "억 " + (man > 0 ? man + "만" : "");
        }"""

new_func = """        function formatMoney(amount) {
            const isNegative = amount < 0;
            const absAmount = Math.abs(amount);
            const eok = Math.floor(absAmount / 100000000);
            const man = Math.floor((absAmount % 100000000) / 10000);

            let result = "";
            if (eok === 0) {
                result = man + "만";
            } else {
                result = eok + "억 " + (man > 0 ? man + "만" : "");
            }

            return (isNegative ? "-" : "") + result;
        }"""

if old_func in html:
    html = html.replace(old_func, new_func)
else:
    print("Could not find old formatMoney function.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
