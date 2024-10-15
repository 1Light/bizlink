// Function to update the wishlist count dynamically
function updateWishlistCount(count) {
    // Select the element that displays the wishlist count in base.html
    let wishlistCountElement = $("#wishlist-count");

    // Check if the wishlist count element exists before updating it
    if (wishlistCountElement.length) {
        wishlistCountElement.text(count);
    }
}

// Handle the click event to remove items from the wishlist
$(document).on("click", ".remove-from-wishlist", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let productId = $(this).data("product-id"); // Get the product ID from the data attribute
    let row = $(this).closest("tr"); // Get the closest row to remove it later

    // AJAX request to remove the item from the wishlist
    $.ajax({
        url: "/core/wishlist/", // Ensure this matches your URL configuration
        type: "POST",
        data: {
            "id": productId,
            "csrfmiddlewaretoken": csrfToken // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the removal was successful
                row.remove();
                // Update the wishlist count
                updateWishlistCount(response.wishlist_count);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the item from the wishlist.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the item:", error);
            alert("There was an error removing the item from the wishlist. Please try again.");
        }
    });
});