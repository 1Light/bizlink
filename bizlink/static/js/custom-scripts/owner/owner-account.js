$(document).ready(function() {
    $('#edit-profile-form').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // Get the values from the input fields
        var fullName = $('#full-name').val();
        var mobile = $('#mobile').val();
        var isValid = true; // Flag for form validity
        var errorMessage = ''; // To store error messages

        // Validate full name (only letters allowed)
        if (!/^[a-zA-Z\s]*$/.test(fullName)) {
            errorMessage += 'Full Name must contain only letters and spaces.\n';
            isValid = false;
        }

        // Validate mobile number (only digits allowed)
        if (!/^\d+$/.test(mobile)) {
            errorMessage += 'Mobile Number must contain only digits.\n';
            isValid = false;
        }

        // If the form is valid, proceed with AJAX submission
        if (isValid) {
            // Create a new FormData object from the form
            var formData = new FormData(this);

            // Send the form data via AJAX
            $.ajax({
                url: "/userauth/edit_profile/", // Update with the correct URL for your edit_profile view
                type: "POST",
                data: formData, // Use FormData to include file uploads
                processData: false,
                contentType: false,
                success: function(response) {
                    // Handle the success response
                    alert('Profile updated successfully!');
                    // Optionally refresh the page or update the UI with new data
                },
                error: function(xhr, status, error) {
                    // Handle any errors
                    alert('An error occurred while updating the profile: ' + error);
                }
            });
        } else {
            // Display error messages
            alert(errorMessage);
        }
    });
});

// Function to update the notification count dynamically
function updateNotificationCount(count) {
    // Select the element that displays the notification count in base.html
    let notificationCountElement = $("#notification-count");

    // Check if the notification count element exists before updating it
    if (notificationCountElement.length) {
        // Update the text to the new count
        notificationCountElement.text(count);
        
        // If count is 0, hide the notification count element
        if (count === 0) {
            notificationCountElement.hide();
        } else {
            notificationCountElement.show(); // Show the count when it's greater than 0
        }
    }
}

// Handle the click event to remove notifications
$(document).on("click", ".remove-notification", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let notificationId = $(this).data("notification-id"); // Get the notification ID from the data attribute
    let row = $(this).closest("tr"); // Get the closest row to remove it later

    // AJAX request to remove the notification
    $.ajax({
        url: "/core/owner/account/notification/", // Ensure this matches your URL configuration
        type: "POST",
        data: {
            "id": notificationId,
            "csrfmiddlewaretoken": csrfToken // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the removal was successful
                row.remove();
                // Update the notification count
                updateNotificationCount(response.notification_count);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the notification.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the notification:", error);
            alert("There was an error removing the notification. Please try again.");
        }
    });
});

// Script for Uploading and Previewing the Profile Image
const selectProfileImage = document.querySelector('.select-profile-image-btn');
const profileInputFile = document.querySelector('#profile-file');
const profileImgArea = document.querySelector('.profile-img-area');

if (existingProfileImage && existingProfileImage !== "null") {
    const profileImg = document.createElement('img');
    profileImg.src = existingProfileImage;
    profileImgArea.appendChild(profileImg);
    profileImgArea.classList.add('active', 'image-uploaded');
    profileImgArea.dataset.img = existingProfileImage; 
}

selectProfileImage.addEventListener('click', function () {
    profileInputFile.click();
})

profileInputFile.addEventListener('change', function () {
    const image = this.files[0];
    if (image.size < 2000000) {
        const reader = new FileReader();
        reader.onload = () => {
            const allImg = profileImgArea.querySelectorAll('img');
            allImg.forEach(item => item.remove());
            const imgUrl = reader.result;
            const img = document.createElement('img');
            img.src = imgUrl;
            profileImgArea.appendChild(img);
            profileImgArea.classList.add('active', 'image-uploaded'); 
            profileImgArea.dataset.img = image.name;
        }
        reader.readAsDataURL(image);
    } else {
        alert("Image size must be less than 2MB");
    }
})