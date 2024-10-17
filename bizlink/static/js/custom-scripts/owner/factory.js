// JavaScript function to clear the image field
const clearImageBtn = document.querySelector('#clear-image-btn');

// Attach click event to the "Clear Image" button
clearImageBtn.addEventListener('click', function () {
    clearImage();
});

// Function to clear the selected image and reset the input field
function clearImage() {
    // Clear the file input value
    inputCategoryFile.value = '';

    // Remove the preview image
    const allImg = categoryImgArea.querySelectorAll('img');
    allImg.forEach(item => item.remove());

    // Hide the "Clear Image" button
    clearImageBtn.style.display = 'none';

    // Remove classes and reset dataset
    categoryImgArea.classList.remove('active', 'image-uploaded');
    delete categoryImgArea.dataset.img;
}

/* Script for Uploading and Previewing the Shop Image */

const selectCategoryImage = document.querySelector('.select-category-image-btn');
const inputCategoryFile = document.querySelector('#category-file');
const categoryImgArea = document.querySelector('.category-img-area');

selectCategoryImage.addEventListener('click', function () {
    inputCategoryFile.click();
})

inputCategoryFile.addEventListener('change', function () {
    const image = this.files[0]
    if(image.size < 2000000) {
    const reader = new FileReader();
    reader.onload = ()=> {
        const allImg = categoryImgArea.querySelectorAll('img');
        allImg.forEach(item=> item.remove());
        const imgUrl = reader.result;
        const img = document.createElement('img');
        img.src = imgUrl;
        categoryImgArea.appendChild(img);
        categoryImgArea.classList.add('active', 'image-uploaded'); 
        categoryImgArea.dataset.img = image.name;

        // Show the "Clear Image" button
        clearImageBtn.style.display = 'inline-block';
    }
    reader.readAsDataURL(image);
    } else {
    alert("Image size more than 2MB");
    }
})

///////////////////////////////////////// Product ////////////////////////////////////////
const clearVideoBtn = document.querySelector('#clear-video-btn');

// Attach click event to the "Clear Video" button
clearVideoBtn.addEventListener('click', function () {
    clearVideo();
});

// Function to clear the selected video and reset the input field
function clearVideo() {
    // Clear the file input value
    inputVideo.value = '';

    // Remove the preview video
    const videoContainer = videoArea.querySelector('.video-container');
    if (videoContainer) {
        videoContainer.remove();
    }

    // Hide the "Clear Video" button
    clearVideoBtn.style.display = 'none';

    // Remove classes and reset dataset
    videoArea.classList.remove('active', 'video-uploaded');
    delete videoArea.dataset.video;
}

/* Script for Uploading and Previewing the Video */
const selectVideo = document.querySelector('.select-video-btn');
const inputVideo = document.querySelector('#video-file');
const videoArea = document.querySelector('.video-area');
let videoContainer; // Declare the videoContainer variable here

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

        
        // Show the "Clear Video" button
        clearVideoBtn.style.display = 'inline-block';
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

/* Script for Uploading and Previewing the Shop Image */

const selectImage = document.querySelector('.select-image-btn');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');

selectImage.addEventListener('click', function () {
  inputFile.click();
})

inputFile.addEventListener('change', function () {
  const image = this.files[0]
  if(image.size < 2000000) {
    const reader = new FileReader();
    reader.onload = ()=> {
      const allImg = imgArea.querySelectorAll('img');
      allImg.forEach(item=> item.remove());
      const imgUrl = reader.result;
      const img = document.createElement('img');
      img.src = imgUrl;
      imgArea.appendChild(img);
      imgArea.classList.add('active', 'image-uploaded'); 
      imgArea.dataset.img = image.name;

    }
    reader.readAsDataURL(image);
  } else {
    alert("Image size more than 2MB");
  }
})

///////////////////////////////////////////// More Images ////////////////////////////////////

const addMoreImagesBtn = document.querySelector('#add-more-images-btn');
const moreImageFieldsContainer = document.querySelector('#more-product-image');
let imageCount = 0; // Counter to keep track of the number of image fields added

// Function to create a new image upload field
function createImageUploadField() {
    imageCount++; // Increment the image count

    // Create the new field container
    const newField = document.createElement('div');
    newField.classList.add('field', 'product-image');
    newField.innerHTML = `
        <div class="image-preview-box">
            <input name="image${imageCount}" type="file" id="more-img-file-${imageCount}" accept="image/*" hidden>
            <div class="more-img-area" data-img="hello.jpg">
                <i class="fa-solid fa-cloud-arrow-up"></i>
                <h3>Upload Image</h3>
                <p>Image size must be less than <span>2MB</span></p>
            </div>
        </div>
        <button type="button" class="select-more-image-btn btn btn-success">
            <i class="fa-solid fa-square-plus"></i>
        </button>
        <button type="button" class="delete-more-image-btn btn btn-danger">
            <i class="fa-solid fa-square-minus"></i>
        </button>
    `;

    moreImageFieldsContainer.appendChild(newField); // Append the new field to the container

    // Select newly created elements
    const selectMoreImageBtn = newField.querySelector('.select-more-image-btn');
    const inputFile = newField.querySelector(`#more-img-file-${imageCount}`);
    const imgArea = newField.querySelector('.more-img-area');
    const deleteProductImageBtn = newField.querySelector('.delete-more-image-btn');

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
                imgArea.classList.add('active', 'image-uploaded');
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

//////////////////////////////////// More Videos //////////////////////////////////////////////
const addMoreVideosBtn = document.querySelector('#add-more-videos-btn');
const moreVideoFieldsContainer = document.querySelector('#more-product-video');
let videoCount = 0; // Counter to keep track of the number of video fields added

// Function to create a new video upload field
function createVideoUploadField() {
    videoCount++; // Increment the video count

    // Create the new field container
    const newField = document.createElement('div');
    newField.classList.add('product-video');
    newField.innerHTML = `
        <div class="video-preview-box">
            <input name="video${videoCount}" type="file" id="more-video-file-${videoCount}" accept="video/*" hidden>
            <div class="more-video-area" data-video="no-video">
                <i class="fa-solid fa-cloud-arrow-up"></i>
                <h3>Upload Video</h3>
                <p>Video size must be less than <span>50MB</span></p>
            </div>
            <div class="video-description" style="display: none;">
                <textarea name="video-description-${videoCount}"></textarea>
            </div>
            <button type="button" class="select-more-video-btn btn btn-success">
                <i class="fa-solid fa-square-plus"></i>
            </button>
            <button type="button" class="delete-more-video-btn btn btn-danger">
                <i class="fa-solid fa-square-minus"></i>
            </button>
            <button type="button" class="toggle-description-btn btn btn-info"><i class="fa-solid fa-circle-info"></i></button>
        </div>
    `;

    // Append the new field to the container
    moreVideoFieldsContainer.appendChild(newField);

    // Select the newly created elements
    const selectMoreVideoBtn = newField.querySelector('.select-more-video-btn');
    const inputMoreVideo = newField.querySelector(`#more-video-file-${videoCount}`);
    const moreVideoArea = newField.querySelector('.more-video-area');
    const deleteProductVideoBtn = newField.querySelector('.delete-more-video-btn');
    const toggleDescriptionBtn = newField.querySelector('.toggle-description-btn');
    const videoDescription = newField.querySelector('.video-description');

    // Add event listeners for the new elements
    selectMoreVideoBtn.addEventListener('click', function () {
        inputMoreVideo.click();
    });

    inputMoreVideo.addEventListener('change', function () {
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

            // Show the "Clear Video" button
            clearVideoBtn.style.display = 'inline-block';
        } else {
            alert("Video size exceeds 50MB");
        }
    });

    // Toggle the video description textarea visibility
    toggleDescriptionBtn.addEventListener('click', function () {
        if (videoDescription.style.display === 'none') {
            videoDescription.style.display = 'block';
            
        } else {
            videoDescription.style.display = 'none';
            
        }
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

/* Preventing form submission on reload */

if ( window.history.replaceState ) {
window.history.replaceState( null, null, window.location.href );
}