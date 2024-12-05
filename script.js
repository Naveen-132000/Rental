let slideIndex = 0;
showSlides();

// Automatic Slideshow
function showSlides() {
    let slides = document.getElementsByClassName("slide");
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    slides[slideIndex - 1].style.display = "block";  
    setTimeout(showSlides, 3000); // Change image every 3 seconds
}

// Manual Slide Control
function changeSlide(n) {
    slideIndex += n;
    let slides = document.getElementsByClassName("slide");
    if (slideIndex > slides.length) {slideIndex = 1}
    if (slideIndex < 1) {slideIndex = slides.length}
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slides[slideIndex - 1].style.display = "block";  
}
let secondarySlideIndex = 0;
showSecondarySlides(secondarySlideIndex);

function changeSecondarySlide(n) {
    showSecondarySlides(secondarySlideIndex += n);
}

function showSecondarySlides(n) {
    const slides = document.getElementsByClassName("secondary-slide");
    const maxVisible = 4;
    if (n > slides.length - maxVisible) { secondarySlideIndex = 0; }
    if (n < 0) { secondarySlideIndex = slides.length - maxVisible; }

    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (let i = secondarySlideIndex; i < secondarySlideIndex + maxVisible; i++) {
        slides[i].style.display = "block";
    }
}

function openModal() {
  document.getElementById("termsModal").style.display = "block";
}

function closeModal() {
  document.getElementById("termsModal").style.display = "none";
}

window.onclick = function(event) {
  if (event.target == document.getElementById("termsModal")) {
    closeModal();
  }
}

function filterCars() {
  const searchInput = document.getElementById('carSearch').value.toLowerCase();
  const cards = document.getElementsByClassName('range__card');
  
  for (let card of cards) {
      const title = card.querySelector('h2').textContent.toLowerCase();
      const details = card.querySelectorAll('p');
      let text = title;
      details.forEach(p => text += ' ' + p.textContent.toLowerCase());
      
      if (text.includes(searchInput)) {
          card.style.display = "block";
      } else {
          card.style.display = "none";
      }
  }
}
