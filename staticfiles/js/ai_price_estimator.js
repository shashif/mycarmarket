/* ==========================================
MyCarMarket
Version: v1.5.5
File: static/js/ai_price_estimator.js
Description: AI Smart Price Estimation Frontend
========================================== */

document.addEventListener("DOMContentLoaded", function () {
    const estimateBtn = document.getElementById("estimate-price-btn");
    const resultBox = document.getElementById("ai-price-result");

    if (!estimateBtn || !resultBox) {
        return;
    }

    estimateBtn.addEventListener("click", function () {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const formData = new FormData();

        const fields = [
            "make",
            "model",
            "year",
            "kilometres",
            "transmission",
            "fuel_type",
            "body_type",
            "condition",
            "state"
        ];

        fields.forEach(function (field) {
            const input = document.getElementById("id_" + field);
            if (input) {
                formData.append(field, input.value);
            }
        });

        resultBox.innerHTML = "Estimating price...";

        fetch("/cars/ai-price-estimate/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                resultBox.innerHTML = data.message;
                return;
            }

            resultBox.innerHTML = `
                <div class="ai-price-card">
                    <h3>AI Smart Price Estimate</h3>
                    <p><strong>Suggested Price:</strong> $${data.suggested_price.toLocaleString()}</p>
                    <p><strong>Fair Range:</strong> $${data.low_price.toLocaleString()} - $${data.high_price.toLocaleString()}</p>
                    <p><strong>Confidence:</strong> ${data.confidence}%</p>
                    <p><strong>Similar Cars Found:</strong> ${data.total_matches}</p>
                    <button type="button" id="use-ai-price-btn">
                        Use This Price
                    </button>
                </div>
            `;

            const useBtn = document.getElementById("use-ai-price-btn");
            const priceInput = document.getElementById("id_price");

            if (useBtn && priceInput) {
                useBtn.addEventListener("click", function () {
                    priceInput.value = data.suggested_price;
                });
            }
        })
        .catch(() => {
            resultBox.innerHTML = "Something went wrong. Please try again.";
        });
    });
});