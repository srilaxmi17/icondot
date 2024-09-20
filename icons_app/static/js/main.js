(function ($) {
    "use strict";
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    // Dropdown on mouse hover
    // document.addEventListener('DOMContentLoaded', function() {
    //     const dropdownBtn = document.querySelector('.dropdown-btn');
    //     const dropdownContent = document.querySelector('.dropdown-content');
    
    //     dropdownBtn.addEventListener('onclick', function() {
    //         dropdownContent.classList.toggle('show');
    //     });
    
    //     window.onclick = function(event) {
    //         if (!event.target.matches('.dropdown-btn')) {
    //             if (dropdownContent.classList.contains('show')) {
    //                 dropdownContent.classList.remove('show');
    //             }
    //         }
    //     };
    // });

    // const $dropdown = $(".dropdown");
    // const $dropdownToggle = $(".dropdown-toggle");
    // const $dropdownMenu = $(".dropdown-menu");
    // const showClass = "show";
    
    // $(window).on("load resize", function() {
    //     if (this.matchMedia("(min-width: 992px)").matches) {
    //         $dropdown.hover(
    //         function() {
    //             const $this = $(this);
    //             $this.addClass(showClass);
    //             $this.find($dropdownToggle).attr("aria-expanded", "true");
    //             $this.find($dropdownMenu).addClass(showClass);
    //         },
    //         function() {
    //             const $this = $(this);
    //             $this.removeClass(showClass);
    //             $this.find($dropdownToggle).attr("aria-expanded", "false");
    //             $this.find($dropdownMenu).removeClass(showClass);
    //         }
    //         );
    //     } else {
    //         $dropdown.off("mouseenter mouseleave");
    //     }
    // });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    function search() {
        const searchText = document.getElementById('searchText').value.trim();
        highlightText(searchText);
    }
    
    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: true,
        loop: true,
        center: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 45,
        dots: false,
        loop: true,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:4
            },
            768:{
                items:6
            },
            992:{
                items:8
            }
        }
    });
    
})(jQuery);

// function highlightText(query) {
//     const content = document.body.innerHTML;
//     const regex = new RegExp(query, 'gi');

//     const highlightedContent = content.replace(regex, '<span class="highlight">$&</span>');
//     document.body.innerHTML = highlightedContent;
// } 

function highlightSearch(event) {
    event.preventDefault();
    
    // Get the search text
    var searchTextElement = document.getElementById('searchText');
    console.log("Search Text Element:", searchTextElement); // Debugging statement
    var searchText = searchTextElement.value.trim().toLowerCase();
    console.log("Search Text:", searchText); // Debugging statement

    // Clear previous highlights
    clearHighlights(document.body);

    if (searchText) {
        // Highlight all occurrences of the search text
        highlightText(document.body, searchText);
    }
}

// exam cnotifications

const slider = document.querySelector(".items");
const slides = document.querySelectorAll(".item");
const button = document.querySelectorAll(".button");

let current = 0;
let prev = -1;
let next = 1;

for (let i = 0; i < button.length; i++) {
    button[i].addEventListener("click", () => i == 0 ? gotoPrev() : gotoNext());
}

const gotoPrev = () => current > 0 ? gotoNum(current - 1) : gotoNum(slides.length - 1);

const gotoNext = () => current < slides.length ? gotoNum(current + 1) : gotoNum(0);

const gotoNum = number => {
    current = number;
    prev = current - 1;
    next = current + 1;

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
        slides[i].classList.remove("prev");
        slides[i].classList.remove("next");
    }

    if (next == slides.length + 1) {
        next = 0;
    }

    if (prev == -1) {
        prev = -1;
    }

    slides[current].classList.add("active");
    slides[prev].classList.add("prev");
    slides[next].classList.add("next");
}





document.addEventListener('DOMContentLoaded', function() {
    var showPopupBtn = document.getElementById('showPopupBtn');
    var popup = document.getElementById('popup2');
    var closePopup = document.querySelector('#popup2 .close');

    // Show the popup
    if (showPopupBtn) {
        showPopupBtn.addEventListener('click', function(event) {
            event.preventDefault();
            popup.style.display = 'block';
        });
    }

    // Close the popup
    if (closePopup) {
        closePopup.addEventListener('click', function(event) {
            event.preventDefault();
            popup.style.display = 'none';
        });
    }
});





document.addEventListener('DOMContentLoaded', () => {
    const heartIcon = document.getElementById('heart-icon');
    const clickCountElement = document.getElementById('click-count');
    
    let clickCount = 0;
    
    heartIcon.addEventListener('click', () => {
        heartIcon.classList.toggle('clicked');
        clickCount++;
        clickCountElement.textContent = clickCount;
    });
});







$('.click').click(function() {
	if ($('span').hasClass("fa-heart")) {
			$('.click').removeClass('active')
		setTimeout(function() {
			$('.click').removeClass('active-2')
		}, 30)
			$('.click').removeClass('active-3')
		setTimeout(function() {
			$('span').removeClass('fa-heart')
			$('span').addClass('fa-heart-o')
		}, 15)
	} else {
		$('.click').addClass('active')
		$('.click').addClass('active-2')
		setTimeout(function() {
			$('span').addClass('fa-heart')
			$('span').removeClass('fa-heart-o')
		}, 150)
		setTimeout(function() {
			$('.click').addClass('active-3')
		}, 150)
		$('.info').addClass('info-tog')
		setTimeout(function(){
			$('.info').removeClass('info-tog')
		},1000)
	}
})