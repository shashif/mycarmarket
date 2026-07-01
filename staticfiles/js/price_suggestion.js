/* ==========================================
MyCarMarket
Version: v1.5.6
File: static/js/price_suggestion.js
Description: Professional AI Smart Price Estimation AJAX
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    const smartPriceBox = document.getElementById("smartPriceBox");
    const smartPriceLoading = document.getElementById("smartPriceLoading");
    const smartPriceResult = document.getElementById("smartPriceResult");
    const smartPriceError = document.getElementById("smartPriceError");

    const smartPriceMin = document.getElementById("smartPriceMin");
    const smartPriceMax = document.getElementById("smartPriceMax");
    const smartPriceRecommended = document.getElementById("smartPriceRecommended");
    const smartPriceCount = document.getElementById("smartPriceCount");
    const smartPriceStars = document.getElementById("smartPriceStars");
    const smartPriceConfidence = document.getElementById("smartPriceConfidence");
    const useSuggestedPriceBtn = document.getElementById("useSuggestedPriceBtn");

    const makeField = document.getElementById("id_make");
    const modelField = document.getElementById("id_model");
    const yearField = document.getElementById("id_year");
    const kilometresField = document.getElementById("id_kilometres");
    const transmissionField = document.getElementById("id_transmission");
    const fuelField = document.getElementById("id_fuel_type");
    const stateField = document.getElementById("id_state");
    const priceField = document.getElementById("id_price");

    let latestRecommendedPrice = null;
    let timer = null;
    let controller = null;

    if (!smartPriceBox) {
        return;
    }

    function getFieldValue(field) {
        return field ? field.value.trim() : "";
    }

    function hasMinimumData() {
        return (
            getFieldValue(makeField) &&
            getFieldValue(modelField) &&
            getFieldValue(yearField)
        );
    }

    function formatNumber(value) {
        return Number(value || 0).toLocaleString("en-AU");
    }

    function hideBox() {
        smartPriceBox.style.display = "none";
    }

    function showLoading() {
        smartPriceBox.style.display = "block";
        smartPriceLoading.style.display = "block";
        smartPriceResult.style.display = "none";
        smartPriceError.style.display = "none";
    }

    function showResult(data) {
        latestRecommendedPrice = data.recommended;

        smartPriceBox.style.display = "block";
        smartPriceLoading.style.display = "none";
        smartPriceError.style.display = "none";
        smartPriceResult.style.display = "block";

        smartPriceMin.innerText = formatNumber(data.min);
        smartPriceMax.innerText = formatNumber(data.max);
        smartPriceRecommended.innerText = formatNumber(data.recommended);
        smartPriceCount.innerText = data.count || 0;

        smartPriceStars.innerText = "★".repeat(data.stars || 1);
        smartPriceConfidence.innerText =
            (data.confidence || "Low") + " Confidence";

        if (data.fallback_label) {
            smartPriceConfidence.innerText +=
                " • Based on " + data.fallback_label;
        }
    }

    function showError(message) {
        latestRecommendedPrice = null;

        smartPriceBox.style.display = "block";
        smartPriceLoading.style.display = "none";
        smartPriceResult.style.display = "none";
        smartPriceError.style.display = "block";
        smartPriceError.innerText = message;
    }

    function fetchPriceSuggestion() {
        if (!hasMinimumData()) {
            hideBox();
            return;
        }

        if (!window.PRICE_SUGGESTION_API_URL) {
            showError("Price suggestion is not available right now.");
            return;
        }

        if (controller) {
            controller.abort();
        }

        controller = new AbortController();

        showLoading();

        const params = new URLSearchParams({
            make: getFieldValue(makeField),
            model: getFieldValue(modelField),
            year: getFieldValue(yearField),
            odometer: getFieldValue(kilometresField),
            transmission: getFieldValue(transmissionField),
            fuel_type: getFieldValue(fuelField),
            state: getFieldValue(stateField),
        });

        fetch(window.PRICE_SUGGESTION_API_URL + "?" + params.toString(), {
            signal: controller.signal
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Network error");
                }

                return response.json();
            })
            .then(function (data) {
                if (data.success) {
                    showResult(data);
                } else {
                    showError(
                        data.message ||
                        "No approved vehicle price data available yet."
                    );
                }
            })
            .catch(function (error) {
                if (error.name === "AbortError") {
                    return;
                }

                showError("Unable to load price suggestion right now.");
            });
    }

    function schedulePriceSuggestion() {
        clearTimeout(timer);

        timer = setTimeout(function () {
            fetchPriceSuggestion();
        }, 500);
    }

    [
        makeField,
        modelField,
        yearField,
        kilometresField,
        transmissionField,
        fuelField,
        stateField,
    ].forEach(function (field) {
        if (field) {
            field.addEventListener("input", schedulePriceSuggestion);
            field.addEventListener("change", schedulePriceSuggestion);
        }
    });

    if (useSuggestedPriceBtn && priceField) {
        useSuggestedPriceBtn.addEventListener("click", function () {
            if (latestRecommendedPrice) {
                priceField.value = latestRecommendedPrice;
                priceField.focus();
            }
        });
    }

    fetchPriceSuggestion();

});