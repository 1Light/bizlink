    ///////////////////////////////////////////////////////////////////
    /////////////////////// Products Tab /////////////////////////////
     ///////////////////////////////////////////////////////////////////

let currentProductId = null;
document.addEventListener('DOMContentLoaded', function() {
    const editProductForm = document.getElementById('edit-product-form');

    editProductForm.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget; // Button that triggered the modal

        // Fetch data attributes from the button that was clicked
        currentProductId = button.getAttribute('data-product-id');
        const productName = button.getAttribute('data-product-name');
        const productCategory = button.getAttribute('data-product-category');
        const productPrice = button.getAttribute('data-product-price');
        const productTags = button.getAttribute('data-product-tags');
        const productStockQuantity = button.getAttribute('data-product-stock-quantity');
        const productDescription = button.getAttribute('data-product-description');
        const productSpecification = button.getAttribute('data-product-specification')
        const existingImage = button.getAttribute('data-product-image');
        const existingVideo = button.getAttribute('data-product-video');
        const productVideoDescription = button.getAttribute('data-product-video-description');
        const categorySelect = document.querySelector('select[name="category"]');

        // Loop through the options and select the correct one
        for (let option of categorySelect.options) {
            if (option.text === productCategory) {
                option.selected = true;
                break;
            }
        }

        // Populate the form fields with the selected product's information
        document.querySelector('input[name="name"]').value = productName;
        document.querySelector('input[name="price"]').value = productPrice;
        document.querySelector('input[name="tags"]').value = productTags;
        document.querySelector('input[name="stock_quantity"]').value = productStockQuantity;
        document.querySelector('textarea[name="description"]').value = productDescription;
        document.querySelector('textarea[name="specifications"]').value = productSpecification;
        document.querySelector('textarea[name="video-description"]').value = productVideoDescription;

        displayExistingImage(existingImage)
        displayExistingVideo(existingVideo)

        // Use button instead of this
        const imagesData = button.getAttribute('data-more-product-images');
        const videosData = button.getAttribute('data-more-product-video');

        // Ensure to replace HTML entities before parsing
        const videosArray = JSON.parse(videosData.replace(/&quot;/g, '"'));
        const imagesArray = JSON.parse(imagesData.replace(/&quot;/g, '"'));
        console.log(videosArray)

        // Populate the modal with the product images
        populateProductImagesModal(imagesArray);
        populateProductVideosModal(videosArray);

        const transactionLogIdData = button.getAttribute('data-transaction-log-id');
        const actionData = button.getAttribute('data-action');
        const quantityData = button.getAttribute('data-quantity');
        const timestampData = button.getAttribute('data-timestamp');

        // Ensure to replace HTML entities before parsing
        const transactionLogIdArray = JSON.parse(transactionLogIdData.replace(/&quot;/g, '"'));
        const actionArray = JSON.parse(actionData.replace(/&quot;/g, '"'));
        const quantityArray = JSON.parse(quantityData.replace(/&quot;/g, '"'));
        const timestampArray = JSON.parse(timestampData.replace(/&quot;/g, '"'));

        
        populateTransactionLogs(actionArray, quantityArray, timestampArray, transactionLogIdArray);

        // Set the form's action URL for submission
        const actionUrl = updateProductInfoUrl.replace('dummy_id', currentProductId);
        $('#productUpdateForm').attr('action', actionUrl);

    });
});

/* Script for Uploading and Previewing the Video */
function displayExistingVideo(existingVideo) {
    const selectVideo = document.querySelector('.select-video-btn');
    const inputVideo = document.querySelector('#video-file');
    const videoArea = document.querySelector('.video-area');
    let videoContainer; // Declare the videoContainer variable here

    // If there's an existing video, display it
    if (existingVideo && existingVideo !== "null") {
        videoContainer = document.createElement('div');
        videoContainer.classList.add('video-container');
        const videoPreview = document.createElement('video');
        videoPreview.id = 'video-preview';
        videoPreview.controls = true;

        const source = document.createElement('source');
        source.id = 'video-source';
        source.src = existingVideo; // Set the source to the existing video URL
        source.type = 'video/mp4'; // Set video type

        videoPreview.appendChild(source); // Add source to video
        videoContainer.appendChild(videoPreview);
        videoArea.appendChild(videoContainer); // Append video to the video area
        videoArea.classList.add('active', 'video-uploaded');
    }

    // Handle click event to trigger the file input dialog
    selectVideo.addEventListener('click', function () {
        inputVideo.click();
    });

    // Handle file input change event to preview selected video
    inputVideo.addEventListener('change', function () {
        const selectedVideo = this.files[0]; // Rename 'video' to 'selectedVideo'
        console.log(selectedVideo);

        if (selectedVideo && selectedVideo.size < 50000000) { // Check if video is less than 50MB
            const videoUrl = URL.createObjectURL(selectedVideo);

            // Remove any existing video elements
            const existingContainer = videoArea.querySelector('.video-container');
            if (existingContainer) {
                existingContainer.remove();
            }

            // Create new video element for preview
            const newVideoContainer = document.createElement('div');
            newVideoContainer.classList.add('video-container'); // Correctly reference newVideoContainer
            const newVideo = document.createElement('video'); // Rename this variable to avoid conflict
            newVideo.id = 'video-preview';
            newVideo.controls = true;

            const source = document.createElement('source');
            source.id = 'video-source';
            source.src = videoUrl;
            source.type = selectedVideo.type; // Use the correct variable

            newVideo.appendChild(source); // Append the new source
            newVideoContainer.appendChild(newVideo);
            videoArea.appendChild(newVideoContainer); // Append the new video to the video area
            videoArea.classList.add('active', 'video-uploaded'); // Add active classes

            newVideo.load(); // Load the new video source
        } else {
            alert("Video size exceeds 50MB");
        }
    });

    // Add event listener for all toggle description buttons
document.querySelectorAll('.toggle-description-btn').forEach(button => {
    button.addEventListener('click', function () {
        const videoBox = this.closest('.product-video'); // Find the closest .product-video container
        const descriptionDiv = videoBox.querySelector('.video-description'); // Find the description div within the same container
        
        // Toggle the display of the video description
        const isDescriptionVisible = descriptionDiv.style.display === 'block';
        descriptionDiv.style.display = isDescriptionVisible ? 'none' : 'block';
        
    });
});
}


$(document).on("click", ".delete-product-video", function(event) {
    event.preventDefault(); // Prevent the default button behavior

    console.log("Button clicked for product ID:", currentProductId);
    console.log("CSRF Token:", csrfToken);

    // Get the closest video container that holds the video tag
    const videoContainer = $(this).closest('.video-preview-box').find('.video-container'); // Find the video container inside the video-preview-box
    const videoArea = $(this).closest('.video-preview-box').find('.video-area'); 
    
    // AJAX request to remove the video
    $.ajax({
        url: "/core/owner/home/inventory/delete_product_video/",  // URL to handle video deletion
        type: "POST",
        data: {
            "id": currentProductId,  // Send product ID to identify the product video
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        beforeSend: function(xhr) {
            console.log("Sending AJAX request...");
            console.log("Request Data:", {
                id: currentProductId,
                csrfmiddlewaretoken: csrfToken
            });
        },
        success: function(response) {
            console.log("Response received:", response);
            if (response.success) {
                videoContainer.remove(); // Remove only the video container
                // Reset the video area UI as necessary
                videoArea.classList.remove('video-uploaded'); 
                videoArea.classList.remove('active');
                
            } else {
                // Handle errors from the server
                console.error("Error from server:", response.error);
                alert(response.error || "Error deleting video.");
            }
        },
        error: function(xhr, status, error) {
            console.error("Error occurred while deleting the video:", error);
            console.log("XHR Response:", xhr);
            console.log("Status:", status);
            alert("Error deleting video. Please try again.");
        }
    });
});



/* Script for Uploading and Previewing the Shop Image */
function displayExistingImage(existingImage) {
    const selectImage = document.querySelector('.select-image-btn');
    const inputFile = document.querySelector('#file');
    const imgArea = document.querySelector('.img-area');

    // Clear existing images before displaying the new one
    const existingImages = imgArea.querySelectorAll('img');
    existingImages.forEach(item => item.remove()); // Remove any existing img elements

    if (existingImage && existingImage !== "null") {
        const img = document.createElement('img');
        img.src = existingImage;
        imgArea.appendChild(img);
        imgArea.classList.add('active', 'image-uploaded');

        const filename = existingImage.split('/').pop();
        imgArea.dataset.img = filename; 
    }

    selectImage.addEventListener('click', function () {
        inputFile.click();
    });

    inputFile.addEventListener('change', function () {
        const image = this.files[0];
        if (image.size < 2000000) {
            const reader = new FileReader();
            reader.onload = () => {
                // Clear existing images again to prevent duplicates when a new image is selected
                const allImg = imgArea.querySelectorAll('img');
                allImg.forEach(item => item.remove());
                const imgUrl = reader.result;
                const img = document.createElement('img');
                img.src = imgUrl;
                imgArea.appendChild(img);
                imgArea.classList.add('active', 'image-uploaded');
                imgArea.dataset.img = image.name;
            };
            reader.readAsDataURL(image);
        } else {
            alert("Image size more than 2MB");
        }
    });
}

const addMoreImagesBtn = document.querySelector('#add-more-images-btn');
const moreImageFieldsContainer = document.querySelector('.more-product-image-box');
let imageCount = 0; // Counter to keep track of the number of image fields added

// Function to create a new image upload field
function createImageUploadField() {
    imageCount++; // Increment the image count

    // Create the new field container
    const newField = document.createElement('div');
    newField.classList.add('product-image');
    newField.innerHTML = `
        <div class="image-preview-box">
            <input name="image-${imageCount}" type="file" id="more-img-file-${imageCount}" accept="image/*" hidden>
            <div class="more-img-area" data-img="">
                <i class="fa-solid fa-cloud-arrow-up"></i>
                <h3>Upload Image</h3>
                <p>Image size must be less than <span>2MB</span></p>
            </div>
        </div>
        <button type="button" class="select-more-image-btn btn btn-success" data-id="${imageCount}">
            <i class="fa-solid fa-square-plus"></i>
        </button>
        <button type="button" class="delete-more-product-image btn btn-danger" data-image-id="${imageCount}">
            <i class="fa-solid fa-square-minus"></i>
        </button>
    `;

    moreImageFieldsContainer.appendChild(newField); // Append the new field to the container

    // Select newly created elements
    const selectMoreImageBtn = newField.querySelector('.select-more-image-btn');
    const inputFile = newField.querySelector(`#more-img-file-${imageCount}`);
    const imgArea = newField.querySelector('.more-img-area');
    const deleteProductImageBtn = newField.querySelector('.delete-more-product-image');

    // Add event listeners for the new elements
    selectMoreImageBtn.addEventListener('click', function () {
        inputFile.click();
    });

    inputFile.addEventListener('change', function () {
        const image = this.files[0];
        if (image.size < 2000000) {
            const reader = new FileReader();
            reader.onload = () => {
                const allImg = imgArea.querySelectorAll('img');
                allImg.forEach(item => item.remove());
                const imgUrl = reader.result;
                const img = document.createElement('img');
                img.src = imgUrl;
                imgArea.appendChild(img);
                imgArea.classList.add('active', 'more-image-uploaded');
                imgArea.dataset.img = image.name;
            };
            reader.readAsDataURL(image);
        } else {
            alert("Image size more than 2MB");
        }
    });

    // Event listener to delete the entire video field when the minus button is clicked
    deleteProductImageBtn.addEventListener('click', function () {
        moreImageFieldsContainer.removeChild(newField); // Remove the entire field
    });
}

// Event listener for adding new image upload fields
addMoreImagesBtn.addEventListener('click', function () {
    createImageUploadField();
});

// For more product videos
const addMoreVideosBtn = document.querySelector('#add-more-videos-btn');
const moreVideoFieldsContainer = document.querySelector('.more-product-video-box');
let videoCount = 0; // Initialize the video count

// Function to create a new video upload field
function createVideoUploadField() {
    videoCount++; // Increment the video count

    // Create the new field container
    const newField = document.createElement('div');
    newField.classList.add('product-video');
    newField.innerHTML = `
        <div class="video-preview-box">
            <input name="video-${videoCount}" type="file" id="video-file-${videoCount}" accept="video/*" hidden>
            <div class="video-area" data-video="">
                <i class="fa-solid fa-cloud-arrow-up"></i>
                <h3>Upload Video</h3>
                <p>Video size must be less than <span>50MB</span></p>
            </div>
        </div>
        <button type="button" class="select-video-btn btn btn-success" data-id="${videoCount}">
            <i class="fa-solid fa-square-plus"></i>
        </button>
        <button type="button" class="delete-more-product-video btn btn-danger" data-video-id="${videoCount}">
            <i class="fa-solid fa-square-minus"></i>
        </button>
        <button type="button" class="toggle-description-btn btn btn-info" data-id="${videoCount}"><i class="fa-solid fa-circle-info"></i></button>
        <div class="video-description-container">
            <div class="video-description" style="display: none;">
                <textarea name="video-description-${videoCount}"></textarea>
            </div>
        </div>
    `;

    moreVideoFieldsContainer.appendChild(newField); // Append the new field to the container

    // Select newly created elements
    const selectVideoButton = newField.querySelector('.select-video-btn');
    const inputVideoFile = newField.querySelector(`#video-file-${videoCount}`);
    const moreVideoArea = newField.querySelector('.video-area');
    const deleteProductVideoBtn = newField.querySelector('.delete-more-product-video');

    // Add event listeners for the new elements
    selectVideoButton.addEventListener('click', function () {
        inputVideoFile.click();
    });

    inputVideoFile.addEventListener('change', function () {
        const selectedVideo = this.files[0];
        if (selectedVideo && selectedVideo.size < 50000000) {
            const videoUrl = URL.createObjectURL(selectedVideo);

            // Remove any existing video elements
            const existingContainer = moreVideoArea.querySelector('.video-container');
            if (existingContainer) {
                existingContainer.remove();
            }

            // Create a new video element for preview
            const newVideoContainer = document.createElement('div');
            newVideoContainer.classList.add('video-container');
            const newVideo = document.createElement('video');
            newVideo.id = `video-preview-${videoCount}`;
            newVideo.controls = true;

            const source = document.createElement('source');
            source.id = `video-source-${videoCount}`;
            source.src = videoUrl;
            source.type = selectedVideo.type;

            newVideo.appendChild(source);
            newVideoContainer.appendChild(newVideo);
            moreVideoArea.appendChild(newVideoContainer);
            moreVideoArea.classList.add('active', 'video-uploaded');

            newVideo.load();
        } else {
            alert("Video size exceeds 50MB");
        }
    });

    // Add functionality for toggling video description visibility
    const toggleDescriptionButton = newField.querySelector('.toggle-description-btn');
    toggleDescriptionButton.addEventListener('click', function () {
        const descriptionDiv = newField.querySelector('.video-description');
        const isDescriptionVisible = descriptionDiv.style.display === 'block';
        descriptionDiv.style.display = isDescriptionVisible ? 'none' : 'block';
    });

    // Event listener to delete the entire video field when the minus button is clicked
    deleteProductVideoBtn.addEventListener('click', function () {
        moreVideoFieldsContainer.removeChild(newField); // Remove the entire field
    });
}

// Event listener for adding new video upload fields
addMoreVideosBtn.addEventListener('click', function () {
    createVideoUploadField();
});


// Function to generate image preview boxes within the modal
function populateProductImagesModal(images) {
    const productImagesContainer = document.querySelector('.more-product-image-box'); // Target the container
    productImagesContainer.innerHTML = ''; // Clear previous images

    images.forEach((image) => {
        const { url, mpiId } = image; 

        // Create HTML for each product image div
        const productImageDiv = `
            <div class="product-image" id="product-image-${mpiId}">
                <div class="image-preview-box">
                    <input name="image-${mpiId}" type="file" id="file-${mpiId}" accept="image/*" hidden>
                    <div class="more-img-area" data-img="${url}">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                        <h3>Upload Image</h3>
                        <p>Image size must be less than <span>2MB</span></p>
                    </div>
                </div>
                <button type="button" class="select-more-image-btn btn btn-success" data-id="${mpiId}"><i class="fa-solid fa-square-plus"></i></button>
                <button type="button" class="remove-more-product-image btn btn-danger" data-image-id="${mpiId}"><i class="fa-solid fa-trash"></i></button>
            </div>
        `;

        // Append the new image div to the container
        productImagesContainer.insertAdjacentHTML('beforeend', productImageDiv);

        // Initialize image preview for the newly created image box
        displayMoreExistingImage(url, mpiId);
    });
}

// Function to handle image preview for a specific image box
function displayMoreExistingImage(existingImage, imageId) {
    const selectMoreImage = document.querySelector(`#product-image-${imageId} .select-more-image-btn`);
    const inputMoreFile = document.querySelector(`#file-${imageId}`);
    const moreImgArea = document.querySelector(`#product-image-${imageId} .more-img-area`);

    // If there is an existing image, display it
    if (existingImage && existingImage !== "null") {
        const img = document.createElement('img');
        img.src = existingImage;
        moreImgArea.appendChild(img);
        moreImgArea.classList.add('active', 'more-image-uploaded');
        moreImgArea.dataset.img = existingImage.split('/').pop();
    }

    // Handle file selection and preview
    selectMoreImage.addEventListener('click', function () {
        inputMoreFile.click();
    });

    inputMoreFile.addEventListener('change', function () {
        const image = this.files[0];
        if (image.size < 2000000) { // Check image size < 2MB
            const reader = new FileReader();
            reader.onload = () => {
                // Remove any previous image
                const allImg = moreImgArea.querySelectorAll('img');
                allImg.forEach(item => item.remove());

                // Display new image
                const imgUrl = reader.result;
                const img = document.createElement('img');
                img.src = imgUrl;
                moreImgArea.appendChild(img);
                moreImgArea.classList.add('active', 'more-image-uploaded');
                moreImgArea.dataset.img = image.name;
            };
            reader.readAsDataURL(image);
        } else {
            alert("Image size more than 2MB");
        }
    });
}

// Handle the click event to remove images
$(document).on("click", ".remove-more-product-image", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let imageId = $(this).data("image-id"); // Get the image ID from the data attribute
    console.log(imageId)
    let imageDiv = $(this).closest(".product-image"); // Select the specific image div to remove it later
    console.log(imageDiv)

    // AJAX request to remove the image
    $.ajax({
        url: "/core/owner/home/inventory/delete_more_product_image/",  // Ensure this matches your URL configuration for deleting an image
        type: "POST",
        data: {
            "id": imageId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the image div from the container if the deletion was successful
                imageDiv.remove();
                // Optionally, handle other UI updates here
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the image.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the image:", error);
            alert("There was an error removing the image. Please try again.");
        }
    });
});


// Function to generate video preview boxes within the modal
function populateProductVideosModal(videos) {
    const productVideosContainer = document.querySelector('.more-product-video-box'); // Target the container
    productVideosContainer.innerHTML = ''; // Clear previous videos

    videos.forEach((video) => {
        const { url, moreProductVideoDescription, mpvId } = video; 

        // Create HTML for each product video div
        const productVideoDiv = `
            <div class="product-video" id="product-video-${mpvId}">
                <div class="video-preview-box">
                    <input name="video-${mpvId}" type="file" id="video-file-${mpvId}" accept="video/*" hidden>
                    <div class="video-area" data-video="${url}">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                        <h3>Upload Video</h3>
                        <p>Video size must be less than <span>50MB</span></p>
                        <video id="video-preview-${mpvId}" controls>
                            <source id="video-source-${mpvId}" src="${url}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
                <button type="button" class="select-video-btn btn btn-success" data-id="${mpvId}"><i class="fa-solid fa-square-plus"></i></button>
                <button type="button" class="remove-more-product-video btn btn-danger" data-video-id="${mpvId}"><i class="fa-solid fa-trash"></i></button>
                                    <button type="button" class="toggle-description-btn btn btn-info" data-id="${mpvId}"><i class="fa-solid fa-circle-info"></i></button>
                <div class="video-description-container">
                    <div class="video-description" style="display: none;">
                        <textarea name="video-description-${mpvId}">${moreProductVideoDescription}</textarea>
                    </div>
                </div>
            </div>
        `;

        // Append the new video div to the container
        productVideosContainer.insertAdjacentHTML('beforeend', productVideoDiv);

        // Initialize video preview for the newly created video box
        displayMoreExistingVideo(url, mpvId);
    });

    // Add event listener for toggle description buttons
    const toggleDescriptionButtons = document.querySelectorAll('.toggle-description-btn');
    toggleDescriptionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const videoId = this.getAttribute('data-id');
            const descriptionDiv = document.querySelector(`#product-video-${videoId} .video-description`);
            
            // Toggle the display of the video description
            const isDescriptionVisible = descriptionDiv.style.display === 'block';
            descriptionDiv.style.display = isDescriptionVisible ? 'none' : 'block';
        });
    });
}

// Function to handle video preview for a specific video box
function displayMoreExistingVideo(existingVideo, videoId) {
    const selectVideoButton = document.querySelector(`#product-video-${videoId} .select-video-btn`);
    const inputVideoFile = document.querySelector(`#video-file-${videoId}`);
    const videoArea = document.querySelector(`#product-video-${videoId} .video-area`);

    // If there is an existing video, display it
    if (existingVideo && existingVideo !== "no-video") {
        const videoPreview = document.querySelector(`#video-preview-${videoId}`);
        const videoSource = document.querySelector(`#video-source-${videoId}`);
        videoSource.src = existingVideo;
        videoPreview.load(); // Load the video
        videoArea.classList.add('active', 'video-uploaded');
        videoArea.dataset.video = existingVideo.split('/').pop();
    }

    // Handle file selection and preview
    selectVideoButton.addEventListener('click', function () {
        inputVideoFile.click();
    });

    inputVideoFile.addEventListener('change', function () {
        const videoFile = this.files[0];
        if (videoFile.size < 50000000) { // Check video size < 50MB
            const reader = new FileReader();
            reader.onload = () => {
                // Set the new video source
                const videoPreview = document.querySelector(`#video-preview-${videoId}`);
                const videoSource = document.querySelector(`#video-source-${videoId}`);
                videoSource.src = reader.result;
                videoPreview.load(); // Load the new video
                videoArea.classList.add('active', 'video-uploaded');
                videoArea.dataset.video = videoFile.name; // Update dataset with the video name
            };
            reader.readAsDataURL(videoFile);
        } else {
            alert("Video size exceeds 50MB");
        }
    });
}

// Handle the click event to remove images
$(document).on("click", ".remove-more-product-video", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let videoId = $(this).data("video-id"); // Get the image ID from the data attribute
    let videoDiv = $(this).closest(".product-video"); // Select the specific image div to remove it later

    // AJAX request to remove the image
    $.ajax({
        url: "/core/owner/home/inventory/delete_more_product_video/",  // Ensure this matches your URL configuration for deleting an image
        type: "POST",
        data: {
            "id": videoId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the image div from the container if the deletion was successful
                videoDiv.remove();
                // Optionally, handle other UI updates here
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the image.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the image:", error);
            alert("There was an error removing the image. Please try again.");
        }
    });
});

// Loop through arrays and populate transaction log rows
function populateTransactionLogs(actionArray, quantityArray, timestampArray, transactionLogIdArray) {
    // Ensure arrays have the same length
    if (actionArray.length === quantityArray.length && quantityArray.length === timestampArray.length && transactionLogIdArray.length === actionArray.length) {
        for (let i = 0; i < actionArray.length; i++) {
            addTransactionLog(actionArray[i], quantityArray[i], timestampArray[i], transactionLogIdArray[i]);
        }
    } else {
        console.error("Mismatch in array lengths for actions, quantities, timestamps, and transaction log IDs.");
    }
}


// Function to add a new transaction log row
function addTransactionLog(action, quantity, timestamp, transactionLogId) {

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${action}</td>
        <td>${quantity}</td>
        <td>${timestamp.replace(' at ', '<br>at ')}</td>
     <td><button type="button" class="remove-transaction btn btn-danger" data-transaction-id="${transactionLogId}"><i class="fa-solid fa-trash"></i></button></td>
    `;
    
    // Append the new row to the table body
    document.getElementById('transaction-log-body').appendChild(newRow);
}

// Handle the click event to remove transaction logs
$(document).on("click", ".remove-transaction", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let transactionLogId = $(this).data("transaction-id"); // Get the transaction log ID from the data attribute
    let row = $(this).closest("tr"); // Select the specific transaction log row to remove it later

    // AJAX request to remove the transaction log
    $.ajax({
        url: "/core/owner/home/inventory/delete_transaction_log/",  // Ensure this matches your URL configuration for deleting a transaction log
        type: "POST",
        data: {
            "id": transactionLogId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the deletion was successful
                row.remove();
                // Optionally, you can also handle other UI updates here, like updating a transaction count
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the transaction log.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the transaction log:", error);
            alert("There was an error removing the transaction log. Please try again.");
        }
    });
});


// Function to update the product count
function updateProductCount(count) {
    $("#product-count").text(count);
    if (count == 1) {
        $("#product-count").text('1 product');
    } else {
        $("#product-count").text(count + ' products');
    }
}

// On page load, fetch the current product count
$(document).ready(function() {
    // Assuming the product count is available in the HTML or through an API
    let currentProductCount = $("#product-count").data("initial-count") || 0;  // You may get this from the server or set it in the HTML
    updateProductCount(currentProductCount);
});

// Handle the click event to remove products
$(document).on("click", ".remove-product", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let productId = $(this).data("product-id"); // Get the product ID from the data attribute
    let row = $("#product-row-" + productId); // Select the specific product row to remove it later

    // AJAX request to remove the product
    $.ajax({
        url: "/core/owner/home/inventory/delete_product/",  // Ensure this matches your URL configuration for deleting a product
        type: "POST",
        data: {
            "id": productId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the deletion was successful
                row.remove();
                // Update the product count using the response
                updateProductCount(response.product_count);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the product.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the product:", error);
            alert("There was an error removing the product. Please try again.");
        }
    });
});

// Handle the click event for the Add button
$(document).on("click", ".add-stock", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let quantity = $("#quantity-" + productId).val();  // Get the inputted quantity
    let stockElement = $("#stock-" + productId);  // Select the stock display element

    // AJAX request to update the stock
    $.ajax({
        url: "/core/owner/home/inventory/add_stock/",  // Your backend URL for updating stock
        type: "POST",
        data: {
            "id": productId,
            "quantity": quantity,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the addition was successful
                stockElement.text(response.new_stock);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error updating the stock.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while updating the stock:", error);
            alert("There was an error updating the stock. Please try again.");
        }
    });
});

// Handle the click event for the Sell button
$(document).on("click", ".sell-stock", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let quantity = $("#quantity-" + productId).val();  // Get the inputted quantity
    let stockElement = $("#stock-" + productId);  // Select the stock display element

    // AJAX request to update the stock
    $.ajax({
        url: "/core/owner/home/inventory/sell_stock/",  // Your backend URL for updating stock
        type: "POST",
        data: {
            "id": productId,
            "quantity": quantity,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the addition was successful
                stockElement.text(response.new_stock);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error updating the stock.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while updating the stock:", error);
            alert("There was an error updating the stock. Please try again.");
        }
    });
});

$(document).on("click", ".undo-stock", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let stockElement = $("#stock-" + productId);  // Select the stock display element

    // AJAX request to undo the last transaction
    $.ajax({
        url: "/core/owner/home/inventory/undo_last_transaction/",  // Your backend URL for undoing the last transaction
        type: "POST",
        data: {
            "id": productId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the undo was successful
                stockElement.text(response.new_stock);
            } else {
                alert(response.message || "There was an error undoing the last transaction.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while undoing the last transaction:", error);
            console.error("XHR Status:", status);  // Log the status of the XHR request
            console.error("XHR Response:", xhr.responseText);  // Log the full response text
            alert("There was an error undoing the last transaction. Please try again.");
        }
    });
});

    ///////////////////////////////////////////////////////////////////
    /////////////////////// Categories Tab /////////////////////////////
     ///////////////////////////////////////////////////////////////////
     $(document).ready(function() {
        $('#categoryUpdateForm').on('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
    
            var formData = new FormData(this); // Create a FormData object from the form
    
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'), // Get the form action URL
                data: formData,
                contentType: false, // Important: prevent jQuery from overriding the content type
                processData: false, // Important: prevent jQuery from processing the data
                success: function(response) {
                    if (response.success) {
                        // Display success message (you can customize this part)
                        alert(response.message);
                         $('#edit-category-form').modal('hide'); 
                        // Optionally, refresh the product list or redirect if necessary
                        // location.reload(); // Uncomment to reload the page
                    } else {
                        // Handle form validation errors
                        $.each(response.errors, function(field, messages) {
                            // Find the field and display the errors
                            var errorDiv = $('#' + field + '-error'); // Assuming you have error divs with IDs like 'fieldname-error'
                            if (errorDiv.length) {
                                errorDiv.text(messages.join(', ')); // Show the errors
                            }
                        });
                    }
                },
                error: function(xhr, status, error) {
                    // Handle any errors that occur during the AJAX request
                    alert('An error occurred while updating the product. Please try again.');
                }
            });
        });
    });

// Function to update the category count
function updateCategoryCount(count) {
    $("#category-count").text(count);
    if (count == 1) {
        $("#category-count").text('1 category');
    } else {
        $("#category-count").text(count + ' categories');
    }
}

// On page load, fetch the current category count
$(document).ready(function() {
    // Assuming the category count is available in the HTML or through an API
    let currentCategoryCount = $("#category-count").data("initial-count") || 0;  // You may get this from the server or set it in the HTML
    updateCategoryCount(currentCategoryCount);
});

// Handle the click event to remove products
$(document).on("click", ".remove-category", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let categoryId = $(this).data("category-id"); // Get the product ID from the data attribute
    let row = $("#category-row-" + categoryId); // Select the specific product row to remove it later

    // AJAX request to remove the product
    $.ajax({
        url: "/core/owner/home/inventory/delete_category/",  // Ensure this matches your URL configuration for deleting a product
        type: "POST",
        data: {
            "id": categoryId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the deletion was successful
                row.remove();
                // Update the category count using the response
                updateCategoryCount(response.category_count);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the category.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the category:", error);
            alert("There was an error removing the category. Please try again.");
        }
    });
});

// Handle the click event to remove products
$(document).on("click", ".remove-product-categoryModal", function(event) {
    event.preventDefault(); // Prevent the default link behavior

    let productId = $(this).data("product-id"); // Get the product ID from the data attribute
    let row = $("#categoryModal-product-row-" + productId); // Select the specific product row to remove it later

    // AJAX request to remove the product
    $.ajax({
        url: "/core/owner/home/inventory/delete_product/",  // Ensure this matches your URL configuration for deleting a product
        type: "POST",
        data: {
            "id": productId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Remove the row from the table if the deletion was successful
                row.remove();
                // Update the product count using the response
                updateProductCount(response.product_count);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error removing the product.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing the product:", error);
            alert("There was an error removing the product. Please try again.");
        }
    });
});

let currentCategoryId = null;
document.addEventListener('DOMContentLoaded', function() {
    const editCategoryForm = document.getElementById('edit-category-form');

    editCategoryForm.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget; // Button that triggered the modal

        // Fetch data attributes from the button that was clicked
        currentCategoryId = button.getAttribute('data-category-id');
        const categoryName = button.getAttribute('data-category-name');
        const categoryDescription = button.getAttribute('data-category-description');
        const existingCategoryImage = button.getAttribute('data-category-image');

        console.log(categoryName)
        console.log(categoryDescription)

        // Populate the form fields with the selected product's information
        editCategoryForm.querySelector('input[name="name"]').value = categoryName;
        editCategoryForm.querySelector('textarea[name="description"]').value = categoryDescription;

        displayExistingCategoryImage(existingCategoryImage)

        // Make an AJAX request to fetch products for the selected category
        fetch(`/core/owner/home/inventory/category_inventory_view/${currentCategoryId}/`)
        .then(response => response.json()) // Convert the response to JSON
        .then(data => {
            // Clear the existing table rows
            const tableBody = document.querySelector('#product-table tbody');
            tableBody.innerHTML = '';

            if (data.products.length > 0) {
                // Loop through products and populate the table with your specified format
                data.products.forEach(product => {
                    const row = `
                        <tr id="categoryModal-product-row-${product.productId}">
                            <td>
                                ${product.name}
                            </td>
                            <td>${product.price}</td>
                            <td>
                                ${new Date(product.created_at).toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' })}<br>
                                at ${new Date(product.created_at).toLocaleTimeString("en-US", { hour: 'numeric', minute: 'numeric', hour12: true })}
                            </td>
                            <td id="categoryModal-stock-${product.productId}">${product.stock_quantity}</td>
                            <td class="quantity">
                                <input type="number" min="1" value="1" id="categoryModal-quantity-${product.productId}" name="quantity" oninput="validity.valid||(value='');"/>
                            </td>
                            <td class="btns">
                                <div class="add-and-sell">
                                    <button class="add-stock-categoryModal" data-product-id="${product.productId}">Add</button>
                                    <button class="sell-stock-categoryModal" data-product-id="${product.productId}">Sell</button>
                                </div>
                                <div class="undo">
                                    <button class="undo-stock-categoryModal" data-product-id="${product.productId}">Undo</button>
                            </div>                                            
                            </td>
                            <td>
                                <a href="#" class="remove-product-categoryModal" data-product-id="${product.productId}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            } else {
                // If no products available, display a message
                tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No products available.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });

        // Set the form's action URL for submission
        const actionUrl = updateCategoryInfoUrl.replace('dummy_id', currentCategoryId);
        $('#categoryUpdateForm').attr('action', actionUrl);

    });
});

/* Script for Uploading and Previewing the Shop Image */
function displayExistingCategoryImage(existingImage) {
    console.log(existingImage);

    const selectCategoryImage = document.querySelector('.select-category-image-btn');
    const inputCategoryFile = document.querySelector('#category-file');
    const categoryImgArea = document.querySelector('.category-img-area');

    // Clear existing images before displaying the new one
    const existingImages = categoryImgArea.querySelectorAll('img');
    existingImages.forEach(item => item.remove()); // Remove any existing img elements

    if (existingImage && existingImage !== "null") {
        const img = document.createElement('img');
        img.src = existingImage;
        categoryImgArea.appendChild(img);
        categoryImgArea.classList.add('active', 'image-uploaded');

        const filename = existingImage.split('/').pop();
        categoryImgArea.dataset.img = filename; 
    }

    selectCategoryImage.addEventListener('click', function () {
        inputCategoryFile.click();
    });

    inputCategoryFile.addEventListener('change', function () {
        const image = this.files[0];
        if (image.size < 2000000) {
            const reader = new FileReader();
            reader.onload = () => {
                // Clear existing images again to prevent duplicates when a new image is selected
                const allImg = categoryImgArea.querySelectorAll('img');
                allImg.forEach(item => item.remove());
                const imgUrl = reader.result;
                const img = document.createElement('img');
                img.src = imgUrl;
                categoryImgArea.appendChild(img);
                categoryImgArea.classList.add('active', 'image-uploaded'); 
                categoryImgArea.dataset.img = image.name;
            };
            reader.readAsDataURL(image);
        } else {
            alert("Image size more than 2MB");
        }
    });
}

// Handle the click event for the Add button
$(document).on("click", ".add-stock-categoryModal", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let quantity = $("#categoryModal-quantity-" + productId).val();  // Get the inputted quantity
    let stockElement = $("#categoryModal-stock-" + productId);  // Select the stock display element

    // AJAX request to update the stock
    $.ajax({
        url: "/core/owner/home/inventory/add_stock/",  // Your backend URL for updating stock
        type: "POST",
        data: {
            "id": productId,
            "quantity": quantity,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the addition was successful
                stockElement.text(response.new_stock);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error updating the stock.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while updating the stock:", error);
            alert("There was an error updating the stock. Please try again.");
        }
    });
});

// Handle the click event for the Sell button
$(document).on("click", ".sell-stock-categoryModal", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let quantity = $("#categoryModal-quantity-" + productId).val();  // Get the inputted quantity
    let stockElement = $("#categoryModal-stock-" + productId);  // Select the stock display element

    // AJAX request to update the stock
    $.ajax({
        url: "/core/owner/home/inventory/sell_stock/",  // Your backend URL for updating stock
        type: "POST",
        data: {
            "id": productId,
            "quantity": quantity,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the addition was successful
                stockElement.text(response.new_stock);
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error updating the stock.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while updating the stock:", error);
            alert("There was an error updating the stock. Please try again.");
        }
    });
});

$(document).on("click", ".undo-stock-categoryModal", function(event) {
    event.preventDefault();  // Prevent the default button behavior

    let productId = $(this).data("product-id");  // Get the product ID from the data attribute
    let stockElement = $("#categoryModal-stock-" + productId);  // Select the stock display element

    // AJAX request to undo the last transaction
    $.ajax({
        url: "/core/owner/home/inventory/undo_last_transaction/",  // Your backend URL for undoing the last transaction
        type: "POST",
        data: {
            "id": productId,
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Update the stock value in the DOM if the undo was successful
                stockElement.text(response.new_stock);
            } else {
                alert(response.message || "There was an error undoing the last transaction.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while undoing the last transaction:", error);
            console.error("XHR Status:", status);  // Log the status of the XHR request
            console.error("XHR Response:", xhr.responseText);  // Log the full response text
            alert("There was an error undoing the last transaction. Please try again.");
        }
    });
});

$(document).on("click", ".delete-category-image", function(event) {
    event.preventDefault(); // Prevent the default button behavior

    const imgElement = $(this).closest('.category-image').find('.category-img-area img');
    const categoryImageArea = $(this).closest('.category-image').find('.category-img-area');
    
    // AJAX request to remove the video
    $.ajax({
        url: "/core/owner/home/inventory/delete_category_image/",  // URL to handle video deletion
        type: "POST",
        data: {
            "id": currentCategoryId,  // Send product ID to identify the product video
            "csrfmiddlewaretoken": csrfToken  // Include CSRF token for Django
        },
        dataType: "json",
        beforeSend: function(xhr) {
            console.log("Sending AJAX request...");
            console.log("Request Data:", {
                id: currentCategoryId,
                csrfmiddlewaretoken: csrfToken
            });
        },
        success: function(response) {
            console.log("Response received:", response);
            if (response.success) {
                imgElement.remove(); // Remove only the video container
                // Reset the video area UI as necessary
                categoryImageArea.attr('data-img', '');
                categoryImageArea.classList.remove('active');
                categoryImageArea.classList.remove('image-uploaded'); 
                
            } else {
                // Handle errors from the server
                console.error("Error from server:", response.error);
                alert(response.error || "Error deleting video.");
            }
        },
        error: function(xhr, status, error) {
            console.error("Error occurred while deleting the video:", error);
            console.log("XHR Response:", xhr);
            console.log("Status:", status);
            alert("Error deleting video. Please try again.");
        }
    });
});

// Handle the click event for the Products tab
$(document).on("click", "#nav-products-tab", function(event) {
    event.preventDefault();  // Prevent default behavior

    // AJAX request to retrieve the updated stock quantities
    $.ajax({
        url: "/core/owner/home/inventory/get_updated_stock/",  // Your backend URL to retrieve updated stock
        type: "GET",
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Loop through each product and update the stock quantity
                response.products.forEach(function(product) {
                    // Find the corresponding stock element and update its value
                    let stockElement = $("#stock-" + product.productId);
                    if (stockElement.length) {
                        stockElement.text(product.stock_quantity);  // Update the displayed stock
                    }
                });
            } else {
                // Handle any errors returned by the server
                alert(response.error || "There was an error retrieving the stock information.");
            }
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while retrieving the stock:", error);
            alert("There was an error retrieving the stock information. Please try again.");
        }
    });
});

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }