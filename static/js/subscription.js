document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("billing-toggle");
    const billingOptions = document.querySelectorAll(".billing-option");
    const toggleCircle = toggle.querySelector(".toggle-circle");

    const monthlyPrices = {
        family: 3000,
        senior: 2500,
        overseas: 3500
    };

    const planCards = document.querySelectorAll(".plan-card");

    let isAnnual = false;

    toggle.addEventListener("click", function () {

        isAnnual = !isAnnual;

        billingOptions[0].classList.toggle(
            "active-billing",
            !isAnnual
        );

        billingOptions[1].classList.toggle(
            "active-billing",
            isAnnual
        );

        if (isAnnual) {

            toggle.style.background = "#178982";
            toggleCircle.style.transform = "translateX(26px)";

        } else {

            toggle.style.background = "#cccccc";
            toggleCircle.style.transform = "translateX(0)";
        }

        planCards.forEach(function (card) {

            const button = card.querySelector(".subscribe-button");

            if (!button) {
                return;
            }

            const plan = button.dataset.plan;

            if (!monthlyPrices[plan]) {
                return;
            }

            const priceElement = card.querySelector(".price");
            const billingElement = card.querySelector(".billing");

            if (isAnnual) {

                const annualPrice =
                    monthlyPrices[plan] * 12 * 0.8;

                priceElement.innerHTML =
                    `<span class="currency">Rs.</span>
                     <span>${annualPrice.toLocaleString()}</span>
                     <span class="per-month">/yr</span>`;

                if (billingElement) {
                    billingElement.textContent =
                        "Billed annually";
                }

            } else {

                priceElement.innerHTML =
                    `<span class="currency">Rs.</span>
                     <span>${monthlyPrices[plan].toLocaleString()}</span>
                     <span class="per-month">/mon</span>`;

                if (billingElement) {
                    billingElement.textContent =
                        "Billed monthly";
                }
            }
        });
    });

   // Subscribe button handling
const subscribeButtons = document.querySelectorAll(
    ".subscribe-button"
);

subscribeButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const plan = button.dataset.plan;

        // Do nothing for the free plan
        if (plan === "free") {
            return;
        }

        const billingCycle = isAnnual
            ? "annual"
            : "monthly";

        const params = new URLSearchParams({
            plan: plan,
            billing: billingCycle
        });

        window.location.href =
            `/payments/?${params.toString()}`;
    });
});
});