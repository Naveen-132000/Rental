// JavaScript to add in your script.js file
const bannerWrapper = document.getElementById('banner-wrapper');
const banners = bannerWrapper.getElementsByTagName('img');
let currentIndex = 0;

// Initially hide all images except the first one
for (let i = 1; i < banners.length; i++) {
  banners[i].style.display = 'none';
}

// Function to display the next image in the slideshow
function showNextBanner() {
  banners[currentIndex].style.display = 'none'; // Hide current image
  currentIndex = (currentIndex + 1) % banners.length; // Move to next image
  banners[currentIndex].style.display = 'block'; // Show the next image
}

// Set the interval for changing the images (e.g., every 3 seconds)
setInterval(showNextBanner, 3000);
