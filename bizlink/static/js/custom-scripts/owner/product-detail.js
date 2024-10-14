
/////////////////////////////////////////////////////////////////////////////


    const carousel = document.getElementById('carouselExample');
const mainImage = document.getElementById('main-image');

carousel.addEventListener('slid.bs.carousel', function () {
    const activeItem = carousel.querySelector('.carousel-item.active');
    const newImageUrl = activeItem.getAttribute('data-img');
    mainImage.src = newImageUrl;
});

    /////////////////////////////////////////////////////////////////////////////

function playMainVideo(icon) {
    var video = document.getElementById('main-video');
    video.style.pointerEvents = 'auto'; // Enable pointer events for the video
    video.controls = true; // Show controls
    video.play();
    icon.style.display = 'none'; // Hide the icon

    // Handle video pause
    video.onpause = function() {
        icon.style.display = 'block'; // Show the icon again
        video.style.pointerEvents = 'none'; // Disable pointer events again
        video.controls = false; // Hide controls
    };
}

function playMoreVideo(icon, videoId) {
    var video = document.getElementById(videoId);
    video.style.pointerEvents = 'auto'; // Enable pointer events for the video
    video.controls = true; // Show controls
    video.play();
    icon.style.display = 'none'; // Hide the icon

    // Handle video pause
    video.onpause = function() {
        icon.style.display = 'block'; // Show the icon again
        video.style.pointerEvents = 'none'; // Disable pointer events again
        video.controls = false; // Hide controls
    };
}

    /////////////////////////////////////////////////////////////////////////////

// JavaScript to toggle the display of the discount form
document.getElementById("clock-icon").addEventListener("click", function() {
    const discountForm = document.getElementById("discount-form");
    if (discountForm.style.display === "none" || discountForm.style.display === "") {
        discountForm.style.display = "block";  // Show the discount form
    } else {
        discountForm.style.display = "none";  // Hide the discount form
    }
});

    /////////////////////////////////////////////////////////////////////////////

// Apply discount form submission
document.getElementById('discount-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const newPrice = document.getElementById('new-price').value;
    const discountUntil = document.getElementById('discount-time').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log("New Price:", newPrice);
    console.log("Discount Until:", discountUntil);

    const data = {
        'new_price': newPrice,
        'discount_until': discountUntil
    };

    fetch(`/core/owner/home/product/apply-discount/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            console.log("Discount until date:", discountUntil); // Debugging line

            // Dynamically inject the countdown timer into the page
            const discountSection = document.getElementById('discount-section'); // Assuming you have a section with this ID for discounts
            discountSection.innerHTML = `
                <div class="discount-timer">
                    <table id="countdown">
                        <tr id="countdown-timer">
                            <td><span id="days">0</span></td>
                            <td><span id="hours">0</span></td>
                            <td><span id="minutes">0</span></td>
                            <td><span id="seconds">0</span></td>
                        </tr>
                        <tr id="countdown-labels">
                            <td><span>d</span></td>
                            <td><span>hr</span></td>
                            <td><span>min</span></td>
                            <td><span>sec</span></td>
                        </tr>
                    </table>                        
                    <button id="delete-discount-button" data-product-id="${productId}">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            `;

            startCountdown(discountUntil, productId); // Start countdown if discount applied

            // Attach event listener to the delete button
            document.getElementById('delete-discount-button').addEventListener('click', function() {
                const productId = this.getAttribute('data-product-id');
                deleteDiscount(productId);
            });

        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

let countdownInterval;

function startCountdown(discountEndTime, productId) {
    const countdownDisplay = document.getElementById('countdownDisplay');
    const discountEndTimeMs = new Date(discountEndTime).getTime();

    console.log("Countdown starting for:", discountEndTime, "Time in ms:", discountEndTimeMs); // Debugging line

    // Check if the date is valid
    if (isNaN(discountEndTimeMs)) {
        countdownDisplay.textContent = 'Invalid discount end time.';
        return;
    }

    // Clear any existing interval
    clearInterval(countdownInterval);

    countdownInterval = setInterval(function() {
        const now = new Date().getTime();
        const duration = discountEndTimeMs - now;

        // Calculate duration in days, hours, minutes, and seconds
        const seconds = Math.floor(duration / 1000);
        const minutes = Math.floor((seconds % 3600) / 60);
        const hours = Math.floor(seconds / 3600);
        const days = Math.floor(hours / 24);

        // Update the countdown spans in the table
        if (duration > 0) {
            document.getElementById('days').textContent = days;
            document.getElementById('hours').textContent = hours % 24;
            document.getElementById('minutes').textContent = minutes;
            document.getElementById('seconds').textContent = seconds % 60;
        } else {
            document.getElementById('days').textContent = 0;
            document.getElementById('hours').textContent = 0;
            document.getElementById('minutes').textContent = 0;
            document.getElementById('seconds').textContent = 0;

            clearInterval(countdownInterval); // Stop the interval

            console.log("Countdown has ended")
            deleteDiscount(productId, true); // Call the delete function when countdown ends
        }

    }, 1000); // Update every second
}

function deleteDiscount(productId, hasDiscountEnded) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Check if the deletion is triggered by the countdown ending
    if (!hasDiscountEnded) {
        // Only ask for confirmation if not from countdown
        if (confirm('Do you want to delete this discount?')) {
            proceedToDelete();
        }
    } else {
        // Directly proceed to delete if called from countdown
        proceedToDelete();
    }

    function proceedToDelete() {
        console.log(`/core/owner/home/product/delete-discount/${productId}/?has_discount_ended=${hasDiscountEnded}`);
        fetch(`/core/owner/home/product/delete-discount/${productId}/?has_discount_ended=${hasDiscountEnded}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();  // Refresh the page to update the UI
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

// Event listener for the delete button
document.getElementById('delete-discount-button').addEventListener('click', function() {
    const productId = this.getAttribute('data-product-id');
    deleteDiscount(productId);
});

// Start countdown on page load if there's an existing discount
document.addEventListener("DOMContentLoaded", function() {
 // Use Django template filter to format
    if (existingDiscountEndTime) {
        startCountdown(existingDiscountEndTime, productId); // Start countdown if discount exists
    } else {
        console.log('No active discount found.');
    }
});

    /////////////////////////////////////////////////////////////////////////////

// Assuming you have a variable or method to check the user's role
 // This could be set by the server-side framework

 if (userType === 'business_owner') {
    // Remove the 'hidden' class to make the button visible
    document.getElementById('delete-discount-button').classList.remove('hidden');
}

// The rest of your countdown and discount logic


