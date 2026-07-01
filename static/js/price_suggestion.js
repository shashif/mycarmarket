/* ==========================================
MyCarMarket
Version: v1.4.6
File: static/js/price_suggestion.js
Description: Smart Price Suggestion AJAX for Seller Form
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

    if (!smartPriceBox) {
        console.log("Smart Price Guide box not found.");
        return;
    }

    function getFieldValue(field) {
        if (!field) {
            return "";
        }

        return field.value.trim();
    }

    function hasMinimumData() {
        return (
            getFieldValue(makeField) &&
            getFieldValue(modelField) &&
            getFieldValue(yearField)
        );
    }

    function formatNumber(value) {
        return Number(value).toLocaleString("en-AU");
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
        smartPriceCount.innerText = data.count;

        smartPriceStars.innerText = "★".repeat(data.stars);
        smartPriceConfidence.innerText = data.confidence + " Confidence";
    }

    function showError(message) {
        smartPriceBox.style.display = "block";
        smartPriceLoading.style.display = "none";
        smartPriceResult.style.display = "none";
        smartPriceError.style.display = "block";
        smartPriceError.innerText = message;
    }

    function fetchPriceSuggestion() {
        if (!hasMinimumData()) {
            return;
        }

        if (!window.PRICE_SUGGESTION_API_URL) {
            showError("Price suggestion API URL missing.");
            return;
        }

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

        fetch(window.PRICE_SUGGESTION_API_URL + "?" + params.toString())
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.success) {
                    showResult(data);
                } else {
                    showError(data.message || "No price suggestion available yet.");
                }
            })
            .catch(function () {
                showError("Unable to load price suggestion right now.");
            });
    }

    function schedulePriceSuggestion() {
        clearTimeout(timer);

        timer = setTimeout(function () {
            fetchPriceSuggestion();
        }, 600);
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
            field.addEventListener("change", schedulePriceSuggestion);
            field.addEventListener("keyup", schedulePriceSuggestion);
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