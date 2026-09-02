document.addEventListener("DOMContentLoaded", function () {

    const paymentForm = document.getElementById("payment-form");
    const payButton = document.getElementById("pay-button");
    const paymentResult = document.getElementById("payment-result");

    function getCSRFToken() {
        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        ).value;
    }

    // Read the selected plan and billing cycle from the URL
    const urlParams = new URLSearchParams(
        window.location.search
    );

    const selectedPlan = urlParams.get("plan");
    const billingCycle =
        urlParams.get("billing") || "monthly";


    // Subscription plan information
    const plans = {

        family: {
            name: "Family Plan",
            monthlyPrice: 3000,
            planId: 2
        },

        senior: {
            name: "Senior Care Plan",
            monthlyPrice: 2500,
            planId: 3
        },

        overseas: {
            name: "Overseas Parent Care Plan",
            monthlyPrice: 3500,
            planId: 4
        }

    };


    // Find the selected plan
    const plan = plans[selectedPlan];


    // Display selected plan
    if (plan) {

        document.getElementById("plan-name").textContent =
            plan.name;

        let price = plan.monthlyPrice;

        // Apply 20% annual discount
        if (billingCycle === "annual") {

            price = price * 12 * 0.8;

        }

        document.getElementById("plan-price").textContent =
            `Rs. ${price.toLocaleString("en-US", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}`;

    }


    // Handle payment form
    paymentForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            // Make sure a valid plan was selected
            if (!plan) {

                showResult(
                    "Invalid subscription plan.",
                    "error"
                );

                return;
            }


            payButton.disabled = true;

            payButton.innerHTML =
                "<span>Processing...</span>";


            // Temporary user ID
            const userId = 1;


            try {

                const response = await fetch(
                    "/payments/fake-payment/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCSRFToken()
                        },

                        body: JSON.stringify({

                            user_id: userId,

                            plan_id: plan.planId,

                            payment_method: "card"

                        })
                    }
                );


                const data =
                    await response.json();


                // Payment successful
                if (response.ok) {

                    showResult(
                        `
                        <strong>
                            Payment Successful!
                        </strong>

                        <br><br>

                        Transaction ID:
                        ${data.transaction_id}

                        <br>

                        Invoice ID:
                        ${data.invoice_id}

                        <br>

                        Amount:
                        Rs. ${data.amount}
                        `,
                        "success"
                    );


                    payButton.innerHTML =
                        "<span>Payment Complete</span>";

                }


                // Payment failed
                else {

                    showResult(
                        data.error ||
                        "Payment failed.",
                        "error"
                    );


                    payButton.disabled = false;

                    payButton.innerHTML =
                        `
                        <span class="lock-icon">
                            🔒
                        </span>

                        <span>
                            Pay Now
                        </span>
                        `;

                }


            }


            // Connection error
            catch (error) {

                console.error(
                    "Payment error:",
                    error
                );


                showResult(
                    "Unable to process payment. Please try again.",
                    "error"
                );


                payButton.disabled = false;

                payButton.innerHTML =
                    `
                    <span class="lock-icon">
                        🔒
                    </span>

                    <span>
                        Pay Now
                    </span>
                    `;

            }

        }
    );


    // Display result message
    function showResult(message, type) {

        paymentResult.innerHTML = message;

        paymentResult.classList.remove(
            "hidden",
            "success",
            "error"
        );

        paymentResult.classList.add(type);

    }

});