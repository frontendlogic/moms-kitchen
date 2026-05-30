// This is a placeholder for your JavaScript code.
// You can add more interactive features here.

// Example: A simple function to log a message when the page loads.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Food website loaded!');
});


document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".hero-slider .slides img");
    let prev = document.querySelector(".hero-slider .prev");
    let next = document.querySelector(".hero-slider .next");
    let dotsContainer = document.querySelector(".hero-slider .dots");

    let currentIndex = 0;
    let slideInterval;

    // Create dots
    slides.forEach((_, index) => {
        let dot = document.createElement("span");
        dot.addEventListener("click", () => showSlide(index));
        dotsContainer.appendChild(dot);
    });

    let dots = dotsContainer.querySelectorAll("span");

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        dots.forEach(dot => dot.classList.remove("active"));

        slides[index].classList.add("active");
        dots[index].classList.add("active");

        currentIndex = index;
    }

    function nextSlide() {
        let index = (currentIndex + 1) % slides.length;
        showSlide(index);
    }

    function prevSlide() {
        let index = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(index);
    }

    prev.addEventListener("click", prevSlide);
    next.addEventListener("click", nextSlide);

    // Auto-play
    function startAutoPlay() {
        slideInterval = setInterval(nextSlide, 3000);
    }

    function stopAutoPlay() {
        clearInterval(slideInterval);
    }

    document.querySelector(".hero-slider").addEventListener("mouseenter", stopAutoPlay);
    document.querySelector(".hero-slider").addEventListener("mouseleave", startAutoPlay);

    // Init
    showSlide(0);
    startAutoPlay();
});

/// 
document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelector('.slides');
    const slideImages = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    let currentIndex = 0;
    const totalSlides = slideImages.length;

    // Function to update the slide position
    function updateSlide() {
        const offset = -currentIndex * 100;
        slides.style.transform = `translateX(${offset}%)`;
    }

    // Event listener for the "next" button
    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlide();
    });

    // Event listener for the "previous" button
    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlide();
    });
});



// Add this in a <script> block at the end of your <body> tag
// or in a separate .js file

document.addEventListener('DOMContentLoaded', () => {

    const indianCuisineCard = document.getElementById('indian-cuisine-card');
    const optionsContainer = document.getElementById('indian-cuisine-options');

    // Define the list of sub-cuisines
    const subCuisines = ['punjabi', 'sindhi', 'gujrati', 'south indian', 'marvadi', 'bihari', 'bendoli', 'himachali'];

    // Function to generate the radio buttons and append them to the container
    const generateRadioButtons = () => {
        let htmlContent = '<form id="indian-sub-cuisine-form">';
        subCuisines.forEach(cuisine => {
            // Create a sanitized ID for the input
            const inputId = `cuisine-${cuisine.toLowerCase().replace(/\s/g, '-')}`;
            htmlContent += `
                <label for="${inputId}">
                    <input type="radio" id="${inputId}" name="sub-cuisine" value="${cuisine}">
                    ${cuisine.charAt(0).toUpperCase() + cuisine.slice(1)}
                </label>
            `;
        });
        htmlContent += '</form>';
        optionsContainer.innerHTML = htmlContent;
    };

    // Add a click event listener to the Indian Cuisine card
    indianCuisineCard.addEventListener('click', () => {
        // Check if the options are already visible
        const isVisible = optionsContainer.classList.contains('active');

        // If visible, hide them. If hidden, generate and show them.
        if (isVisible) {
            optionsContainer.classList.remove('active');
            optionsContainer.innerHTML = ''; // Clear the content
        } else {
            generateRadioButtons();
            optionsContainer.classList.add('active');
        }
    });

});


<!-- 🔄 Background Slider Script -->

    let slides = document.querySelectorAll('.bg-slide');
    let currentSlide = 0;

    function showNextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }

    setInterval(showNextSlide, 4000);



    //Cuisitions
const modal = document.getElementById('cuisineModal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const cuisineForm = document.getElementById('cuisineForm');
    const uploadForm = document.getElementById('uploadForm');

    // Open modal
    openBtn.addEventListener('click', () => { modal.style.display = 'block'; });

    // Close modal
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });

    // Submit upload form only if a cuisine type is selected
    cuisineForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedCuisine = document.querySelector('input[name="cuisine_type"]:checked');
        if (!selectedCuisine) {
            alert("Please select a cuisine type!");
            return;
        }

        // Add cuisine type to main form as hidden input
        let input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'cuisine_type';
        input.value = selectedCuisine.value;
        uploadForm.appendChild(input);

        // Submit the main form
        uploadForm.submit();
    });


// ✅ Menu open/close
function openMenu() {
  document.getElementById("menuModal").style.display = "flex";
}
function closeMenu() {
  document.getElementById("menuModal").style.display = "none";
}

// ✅ Cuisine Filtering
const radios = document.querySelectorAll('input[name="cuisine"]');
const dishes = document.querySelectorAll('.dish');
radios.forEach(radio => {
  radio.addEventListener('change', () => {
    const cuisine = radio.value;
    dishes.forEach(dish => {
      if (cuisine === 'all' || dish.classList.contains(cuisine)) {
        dish.style.display = 'block';
      } else {
        dish.style.display = 'none';
      }
    });
  });
});

// ✅ Recipe Modal
const recipeModal = document.getElementById('recipeModal');
const modalImg = document.getElementById('modalImg');
const modalTitle = document.getElementById('modalTitle');
const modalDesc = document.getElementById('modalDesc');
const modalVideo = document.getElementById('modalVideo');
const modalVideoSrc = document.getElementById('modalVideoSrc');

dishes.forEach(dish => {
  dish.addEventListener('click', () => {
    modalImg.src = dish.dataset.img;
    modalTitle.textContent = dish.dataset.title;
    modalDesc.textContent = dish.dataset.desc;
    modalVideoSrc.src = dish.dataset.video;
    modalVideo.load();
    recipeModal.style.display = 'flex';
  });
});

function closeRecipeModal() {
  recipeModal.style.display = 'none';
  modalVideo.pause();
}

window.onclick = function(event) {
  if (event.target == recipeModal) {
    closeRecipeModal();
  }
}











