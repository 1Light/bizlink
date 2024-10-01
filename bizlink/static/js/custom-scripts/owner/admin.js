$(document).ready(function() {
    const addedPlatforms = new Set();

    // Function to fetch and display existing social media URLs
    function loadExistingSocialMedia() {
        $.ajax({
            type: 'GET',
            url: '/userauth/manage_social_media/',  // Adjust URL to your view
            success: function(data) {
                data.forEach(function(entry) {
                    addSocialMediaInput(entry.platform, entry.url);
                });
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    }

    // Function to add social media input
    function addSocialMediaInput(platform, url) {
        if (platform && !addedPlatforms.has(platform)) {
            addedPlatforms.add(platform);

            const label = $('<label>').text(`Enter your ${platform.charAt(0).toUpperCase() + platform.slice(1)} URL:`);
            const input = $('<input>', {
                type: 'url',
                name: `${platform}_url`,
                class: 'form-control social-media-input',
                placeholder: `Enter your ${platform} URL`,
                value: url // Populate with existing URL
            });

            const removeButton = $('<button>', {
                type: 'button',
                class: 'remove-social-media',
                css: { border: 'none', cursor: 'pointer' }
              }).html('<i class="fa-solid fa-trash"></i>');

            // Create a wrapper div for the input and remove button
            const inputWrapper = $('<div>', { class: 'input-wrapper' }).append(input, removeButton);

            const wrapperDiv = $('<div>', { class: 'form-row' }).append(label, inputWrapper);
            $('.url-collection-box').append(wrapperDiv);  // Update to target the correct class

            // Remove button click event
            removeButton.on('click', function() {
                $(this).closest('.form-row').remove();
                addedPlatforms.delete(platform); // Remove from the set
                // Send delete request
                $.ajax({
                    type: 'POST',
                    url: '{% url "userauth:manage_social_media" %}',  // Adjust URL to your view
                    data: {
                        'platform': platform,
                        'action': 'delete',  // Specify action
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function(xhr) {
                        alert(xhr.responseJSON.error);
                    }
                });
            });
        }
    }

    // Load existing social media URLs on page load
    loadExistingSocialMedia();

    $('#id_platform').on('change', function() {
        const selectedPlatform = $(this).val();
        // Check if a platform is selected and not already added
        if (selectedPlatform) {
            addSocialMediaInput(selectedPlatform, '');
        }
    });

    $('#save-social-media').on('click', function() {
        const socialMediaData = [];
        $('.url-collection-box .form-row').each(function() {  // Update to target the correct class
            const platform = $(this).find('input').attr('name').split('_')[0];
            const url = $(this).find('input').val();

            if (platform && url) {
                socialMediaData.push({ platform: platform, url: url });
            }
        });

        socialMediaData.forEach(function(data) {
            $.ajax({
                type: 'POST',
                url: '{% url "userauth:manage_social_media" %}',  // Adjust URL to your view
                data: {
                    'platform': data.platform,
                    'url': data.url,
                    'action': 'save',  // Specify action
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(response) {
                    alert(response.message);
                },
                error: function(xhr) {
                    alert(xhr.responseJSON.error);
                }
            });
        });
    });
});

/* Script for Uploading and Previewing the Shop Image on Admin Site */
const selectImage = document.querySelector('.select-image-btn');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');

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

// Script for Uploading and Previewing Feature Image on the Admin Site
const selectFeatureImageBtn = document.querySelector('.select-feature-image-btn');
const inputFeatureFile = document.querySelector('#feature-file');
const featureImgArea = document.querySelector('.feature-img-area');

selectFeatureImageBtn.addEventListener('click', function () {
  inputFeatureFile.click();
});

inputFeatureFile.addEventListener('change', function () {
  const featureImage = this.files[0];
  if(featureImage.size < 2000000) {
    const reader = new FileReader();
    reader.onload = () => {
      const allFeatureImages = featureImgArea.querySelectorAll('img');
      allFeatureImages.forEach(item => item.remove());
      const featureImgUrl = reader.result;
      const featureImg = document.createElement('img');
      featureImg.src = featureImgUrl;
      featureImgArea.appendChild(featureImg);
      featureImgArea.classList.add('active', 'image-uploaded'); 
      featureImgArea.dataset.img = featureImage.name;
    };
    reader.readAsDataURL(featureImage);
  } else {
    alert("Image size must be less than 2MB");
  }
});

/* Script to display the Items in the Featured Products */
document.addEventListener('DOMContentLoaded', function () {
    const addFeaturedBtn = document.getElementById('add-featured-btn');
  
    addFeaturedBtn.addEventListener('click', function () {
      // Collect all checked checkboxes
      const selectedProducts = Array.from(document.querySelectorAll('input[name="featured-products"]:checked'))
        .map(input => input.value); // Extract the item IDs
  
      if (selectedProducts.length > 0) {
        fetch('/core/owner/home/admin/add_featured_product/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
          },
          body: JSON.stringify({ product_ids: selectedProducts })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Products added to featured products!');
            location.reload(); // Reload the page to reflect changes
          } else {
            alert('Failed to add products to featured products.');
          }
        });
      } else {
        alert('Please select at least one item to feature.');
      }
    });
  
    // Function to get CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  
  /* Script to delete the Items in the Featured Products section */
  document.addEventListener('DOMContentLoaded', function () {
    const deleteFeaturedBtn = document.getElementById('delete-featured-btn');
  
    deleteFeaturedBtn.addEventListener('click', function () {
      // Collect all checked checkboxes
      const selectedProducts = Array.from(document.querySelectorAll('input[name="featured-product-ids"]:checked'))
        .map(input => input.value); // Extract the item IDs
  
      if (selectedProducts.length > 0) {
        fetch('/core/owner/home/admin/delete_featured_product/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
          },
          body: JSON.stringify({ product_ids: selectedProducts })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Selected featured products have been deleted!');
            location.reload(); // Reload the page to reflect changes
          } else {
            alert('Failed to delete featured products: ' + data.message);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');
        });
      } else {
        alert('Please select at least one item to delete.');
      }
    });
  
    // Function to get CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  
  
  /* Script to display the Items in the New Arrivals Section */
  document.addEventListener('DOMContentLoaded', function () {
    const addNewArrivalBtn = document.getElementById('add-new-arrival-btn');
  
    addNewArrivalBtn.addEventListener('click', function () {
      // Collect all checked checkboxes
      const selectedProducts = Array.from(document.querySelectorAll('input[name="new-arrivals"]:checked'))
        .map(input => input.value); // Extract the item IDs
  
      if (selectedProducts.length > 0) {
        fetch('/core/owner/home/admin/add_new_arrival/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
          },
          body: JSON.stringify({ product_ids: selectedProducts })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Products added to new arrivals!');
            location.reload(); // Reload the page to reflect changes
          } else {
            alert('Failed to add products to new arrivals.');
          }
        });
      } else {
        alert('Please select at least one product for new arrival.');
      }
    });
  
    // Function to get CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  
  /* Script to delete the Items in the New Arrival section */
  document.addEventListener('DOMContentLoaded', function () {
    const deleteFeaturedBtn = document.getElementById('delete-new-arrival-btn');
  
    deleteFeaturedBtn.addEventListener('click', function () {
      // Collect all checked checkboxes
      const selectedProducts = Array.from(document.querySelectorAll('input[name="new-arrival-ids"]:checked'))
        .map(input => input.value); // Extract the item IDs
  
      if (selectedProducts.length > 0) {
        fetch('/core/owner/home/admin/delete_new_arrival/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
          },
          body: JSON.stringify({ product_ids: selectedProducts })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Selected new arrivals have been deleted!');
            location.reload(); // Reload the page to reflect changes
          } else {
            alert('Failed to new arrivals: ' + data.message);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');
        });
      } else {
        alert('Please select at least one item to delete.');
      }
    });
  
    // Function to get CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  
  /* Preventing form submission on reload */
  
  if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }