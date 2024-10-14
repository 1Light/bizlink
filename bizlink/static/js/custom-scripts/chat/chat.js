document.addEventListener('DOMContentLoaded', function() {
    const chatDisplay = document.getElementById('chat-display');
    const date_indicator = document.getElementById('date');
    let hideTimeout = null;

    console.log("Hi man");

    // Function to show dateHeader
    function showDateHeader() {
        date_indicator.style.opacity = 1;
    }

    // Function to hide dateHeader
    function hideDateHeader() {
        date_indicator.style.opacity = 0;
    }

    // Function to handle scrolling
    function handleScroll() {
        console.log("Scrolled in chat-display!"); // Check if this logs on scroll
        const messages = document.querySelectorAll('#chat_messages .text-box1, #chat_messages .text-box2');
        let currentVisibleDate = null;

        // Show the date header when scrolling
        showDateHeader();

        // Clear the previous timeout if user continues scrolling
        if (hideTimeout) {
            clearTimeout(hideTimeout);
        }

        // Find the current visible date
        for (let message of messages) {
            const messageRect = message.getBoundingClientRect();
            const displayRect = chatDisplay.getBoundingClientRect();

            if (messageRect.top >= displayRect.top && messageRect.bottom <= displayRect.bottom) {
                const messageDate = message.querySelector('.time').getAttribute('data-date');
                console.log(messageDate);
                currentVisibleDate = messageDate;
                break;
            }
        }

        // Update the dateHeader if we have a visible date
        if (currentVisibleDate) {
            date_indicator.innerText = currentVisibleDate;
        }

        // Set a timeout to hide the dateHeader after 1 second of no scrolling
        hideTimeout = setTimeout(hideDateHeader, 1000);
    }

    // Attach the click listener to test
    chatDisplay.addEventListener('click', function() {
        console.log("Chat display clicked!"); // This should log when you click the chat display
    });

    // Attach the scroll listener
    function attachScrollListener() {
        if (chatDisplay) {
            // Remove existing listener to avoid multiple attachments
            chatDisplay.removeEventListener('scroll', handleScroll);
            // Attach the new listener
            chatDisplay.addEventListener('scroll', handleScroll);
            console.log("Scroll listener attached to chat-display.");
        }
    }

    // Attach listener on page load
    attachScrollListener();

    // Add event listener for HTMX requests
    document.body.addEventListener('htmx:afterSwap', function(event) {
        console.log("HTMX content swapped");
        attachScrollListener();
    });

    // Initially hide the dateHeader
    date_indicator.style.transition = 'opacity 0.3s';  // Smooth fade effect
    hideDateHeader();
});

// Function to scroll to the bottom of the chat display
function scrollToBottom() {
    const container = document.getElementById('chat-display');
    container.scrollTop = container.scrollHeight;
}

// Call the scrollToBottom function to scroll the chat to the bottom
scrollToBottom();
