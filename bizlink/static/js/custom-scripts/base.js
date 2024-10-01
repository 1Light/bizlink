/* Script to Update the Wishlist Count on Every Page */
$(document).ready(function() {
  // Get the initial wishlist count from the rendered HTML
  let initialWishlistCount = parseInt($("#wishlist-count").text(), 10) || 0;
  let initialNotificationCount = parseInt($("#notification-count").text(), 10) || 0;

  updateWishlistCount(initialWishlistCount);
  updateNotificationCount(initialNotificationCount);
});

/* Script for Multistep Signup Form */
const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = 0;

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    formStepsNum++;
    updateFormSteps();
    updateProgressbar();
  });
});

prevBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();
  });
});

function updateFormSteps() {
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
      formStep.classList.remove("form-step-active");
  });

  formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
  progressSteps.forEach((progressStep, idx) => {
    if (idx < formStepsNum + 1) {
      progressStep.classList.add("progress-step-active");
    } else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");

  progress.style.width =
    ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}

/* Script for Closing Error and Success Message Automatically Using Timer */
setTimeout(() => {
  $('.alert').alert('close');
}, 3000); // 3 seconds

// Function to update the wishlist count dynamically
function updateWishlistCount(count) {
  console.log("I am in")
    let wishlistCountElement = $("#wishlist-count");
    if (wishlistCountElement.length) {
        wishlistCountElement.text(count);

          // If count is 0, hide the element; otherwise, show it
        if (count > 0) {
            wishlistCountElement.text(count);
            wishlistCountElement.show(); // Show the count when it's greater than 0
        } else {
            wishlistCountElement.hide(); // Hide the element when count is 0
        }
    }
}

// Handle the click event to toggle wishlist status
$(document).on("click", ".add-to-wishlist", function(event) {
    event.preventDefault();  // Prevent default behavior
    
    let product_id = $(this).attr("data-product-item");
    let heartIcon = $(this).find(".fa-heart"); // Target the heart icon inside the clicked wishlist link

    // Add loading indicator to heart icon (Optional CSS styling)
    heartIcon.addClass("loading");

    // AJAX request to toggle wishlist (add or remove)
    $.ajax({
        url: "/core/owner/home/add-to-wishlist/",
        data: {
            "id": product_id
        },
        dataType: "json",
        success: function(response) {
            // Remove loading indicator
            heartIcon.removeClass("loading");

            // Update all heart icons for the product
            let allHeartIcons = $(".add-to-wishlist[data-product-item='" + product_id + "'] .fa-heart");

            if (response.added === true) {
                allHeartIcons.addClass("green-heart"); // Turn green if added to wishlist
                console.log("Added to wishlist...");
            } else if (response.removed === true) {
                allHeartIcons.removeClass("green-heart"); // Remove green if removed from wishlist
                console.log("Removed from wishlist...");
            }

            // Update the wishlist count with the new value from the server
            updateWishlistCount(response.wishlist_count);

        },
        error: function(xhr, status, error) {
            console.error("An error occurred while processing the request:", error);
            heartIcon.removeClass("loading");

            // Optionally show an alert or notification to the user
            alert("There was an error updating the wishlist. Please try again.");
        }
    });
});
