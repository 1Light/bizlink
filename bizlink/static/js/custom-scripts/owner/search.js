
/* Script to Automatically Update Searched Products based on Filters  */

$(document).ready(function() {
    $(".loader").hide();

    $(".filter-checkbox, #min-price-input, #max-price-input").on("change", function() { // Listen for changes on checkboxes and price inputs
        console.log("Filter changed!"); 
        let filter_object = {};

        // Build the filter object from the checked checkboxes
        $(".filter-checkbox").each(function(index) {
            let filter_key = $(this).data("filter");
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter="'+filter_key+'"]:checked'))
                .map(function(element) {
                    return element.value;
                });
            console.log(`Filter Key: ${filter_key}, Values: ${filter_object[filter_key]}`);
        });

        // Add min and max price to the filter object
        filter_object.min_price = $("#min-price-input").val(); // Get the value of min price
        filter_object.max_price = $("#max-price-input").val(); // Get the value of max price

        console.log(filter_object); // Debugging to see the filter_object

        // Send the filter_object via AJAX
        $.ajax({
            url: '/core/owner/home/search/filter_searched_product/', // Ensure this URL is correct
            method: 'GET',
            data: filter_object, // Filter object to be sent
            dataType: 'json',
            beforeSend: function() {
                console.log("Sending data...");
                $(".loader").show(); // Show the loader before sending request
            },
            success: function(response) {
                console.log(response);
                console.log("Data filtered successfully...");

                if (response.data) { // Check if response.data exists
                    $("#filtered-product").html(response.data);
                    console.log("Products updated successfully.");
                } else {
                    console.log("No data returned for products.");
                }
            },
            error: function(xhr, status, error) {
                console.log("Error occurred: ", status, error); // Handle errors
            },
            complete: function() {
                $(".loader").hide(); // Hide the loader after the request completes
            }
        });
    });
});

    ///////////////////////////////////////////////////////

/* Script to display Error Messages for the Price Filter */
function validateInputs() {
  // Clear previous error messages
  document.getElementById('min-price-error').style.display = 'none';
  document.getElementById('negative-min-error').style.display = 'none';
  document.getElementById('max-price-error').style.display = 'none';

  const minPrice = parseFloat(document.getElementById('min-price-input').value);
  const maxPrice = parseFloat(document.getElementById('max-price-input').value);
  let isValid = true;

  // Check if min price is negative
  if (minPrice < 0) {
      document.getElementById('negative-min-error').style.display = 'block';
      isValid = false;
  }

  // Check if max price is negative
  if (maxPrice < 0) {
      document.getElementById('max-price-error').style.display = 'block';
      isValid = false;
  }

  // Check if min is greater than max
  if (minPrice > maxPrice) {
      document.getElementById('min-price-error').style.display = 'block';
      isValid = false;
  }

  // Additional logic can go here based on the validation results
  if (isValid) {
      // Logic to filter products based on valid inputs
      console.log("Inputs are valid, proceed with filtering.");
  }
}

// Add event listeners to input fields to validate on input change
document.getElementById('min-price-input').addEventListener('input', validateInputs);
document.getElementById('max-price-input').addEventListener('input', validateInputs);