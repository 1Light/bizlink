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

/* Script for Uploading and Previewing an Image */
const selectImage = document.querySelector('.select-image-btn');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');

if (existingImage && existingImage !== "null") {
  const img = document.createElement('img');
  img.src = existingImage;
  imgArea.appendChild(img);
  imgArea.classList.add('active', 'image-uploaded');
  imgArea.dataset.img = existingImage; 
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

/* nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn */
/* nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn */
/* nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn */

/* Script for Popovers */

document.addEventListener('DOMContentLoaded', function () {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

    popoverTriggerList.forEach(function (popoverTriggerEl) {
        var contentId = popoverTriggerEl.getAttribute('data-bs-content');
        var contentElement = document.querySelector(contentId);

        var popover = new bootstrap.Popover(popoverTriggerEl, {
            content: function() {
                var clone = contentElement.cloneNode(true);
                clone.style.display = 'block'; // Ensure the cloned element is visible
                return clone.innerHTML;
            },
            html: true,
            sanitize: false,
            trigger: 'manual' // Use manual trigger for more control
        });

        popoverTriggerEl.addEventListener('click', function () {
            var popoverInstance = bootstrap.Popover.getInstance(popoverTriggerEl);
            if (popoverInstance) {
                if (popoverInstance._popper) {
                    // If popover is already shown, hide it
                    popoverInstance.hide();
                } else {
                    // Otherwise, show it
                    popoverInstance.show();
                }
            }
        });
    });
});






