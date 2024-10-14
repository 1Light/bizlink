/* Script to Update the Wishlist Count on Every Page */
$(document).ready(function() {
  // Get the initial wishlist count from the rendered HTML
  let initialWishlistCount = parseInt($("#wishlist-count").text(), 10) || 0;
  let initialInboxCount = parseInt($("#inbox-count").text(), 10) || 0;
  let initialNotificationCount = parseInt($("#notification-count").text(), 10) || 0;

  console.log("hey")

  updateWishlistCount(initialWishlistCount);
  updateInboxCount(initialInboxCount);
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
        url: "/core/owner/shop/add-to-wishlist/",
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

$(document).ready(function() {
  // Loop through each chat profile on page load
  $(".chat-profile").each(function() {
      let chatGroupId = $(this).data("chat-group-id");
      let unreadCount = parseInt($("#unread-count-" + chatGroupId).text()) || 0;

      // Update the individual count display
      updateIndividualCount(chatGroupId, unreadCount);
  });
});


let currentChatGroupId; // Variable to hold the current chat group ID

// Handle the click event when a chat profile is clicked
$(document).on("click", ".chat-profile", function(event) {
    event.preventDefault();  // Prevent the default behavior

    // Store the chat group ID in the variable
    currentChatGroupId = $(this).data("chat-group-id");
});

// Listen for the HTMX afterSwap event
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Check if the swapped element is the chat window
    if (event.target.id === "chat-window") {
        // Use the stored chatGroupId
        fetchUnreadCount(currentChatGroupId);
    }
});

// Function to fetch and update unread count
function fetchUnreadCount(chatGroupId) {
    $.ajax({
        url: "/chat/unread-count/" + chatGroupId + "/",  // URL to your unread count view
        dataType: "json",
        success: function(response) {
            // Update the unread count in the UI
            let countElement = $("#unread-count-" + chatGroupId);
            let oldUnreadCount = parseInt(countElement.text()) || 0;
            console.log(oldUnreadCount)

            if (countElement.length) {
                countElement.text(response.unread_count);
            }

            updateIndividualCount(chatGroupId, countElement)

            // Update the total unread messages count in the navbar
            let inboxCountElement = $("#inbox-count");
            let currentTotalUnread = parseInt(inboxCountElement.text()) || 0;
            console.log(currentTotalUnread)
            let unreadDiff = oldUnreadCount - response.unread_count; // Calculate the difference
            console.log(unreadDiff)

            // Subtract the difference from the total unread count
            let newTotalUnread = currentTotalUnread - unreadDiff;
            console.log(newTotalUnread)
            // Safely update the total unread count, ensuring it doesn't go negative
            inboxCountElement.text(newTotalUnread >= 0 ? newTotalUnread : 0);

            // Call updateInboxCount only if the new unread count is 0
            if (newTotalUnread === 0) {
                updateInboxCount(newTotalUnread);
            }


        },
        error: function(xhr, status, error) {
            console.error("Error fetching unread count:", error);
        }
    });
}

// Function to update the inbox count dynamically
function updateInboxCount(count) {
  let inboxCountElement = $("#inbox-count");
  if (inboxCountElement.length) {
      inboxCountElement.text(count);

      // If count is 0, hide the element; otherwise, show it
      if (count > 0) {
          inboxCountElement.show(); // Show the count when it's greater than 0
      } else {
          inboxCountElement.hide(); // Hide the element when count is 0
      }
  }
}

function updateIndividualCount(chatGroupId, count) {
  let countElement = $("#unread-count-" + chatGroupId);
  
  if (countElement.length) {
      countElement.text(count);

      // If count is 0, hide the element; otherwise, show it
      if (count > 0) {
          countElement.show();  // Show the count when it's greater than 0
      } else {
          countElement.hide();  // Hide the element when count is 0
      }
  }
}


// Function to update the notification count dynamically
function updateNotificationCount(count) {
  let notificationCountElement = $("#notification-count");
  if (notificationCountElement.length) {
      notificationCountElement.text(count);

      // If count is 0, hide the element; otherwise, show it
      if (count > 0) {
          notificationCountElement.show(); // Show the count when it's greater than 0
      } else {
          notificationCountElement.hide(); // Hide the element when count is 0
      }
  }
}
