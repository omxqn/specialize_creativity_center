
/* 
 ========= main JS documentation ==========================

 * theme name: HealthEase Template
 * version: 1.0
 * description: Workplace Html5 Template
 * author: softivus
 * author url: 
    ==================================================
    Magnific Popup video
    testimonials swiper
    news swiper
    testimonials swiper 2
    disorder swiper
    disorder swiper 2
    Odometer
*/

"use strict";
$(document).ready(function () {

  /* Magnific Popup video */
  if (document.querySelector(".popupvideo") !== null) {
    $(".popupvideo").magnificPopup({
      disableOn: 300,
      type: "iframe",
      mainClass: "mfp-fade",
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false,
    });
  }

  // testimonials swiper
  var testimonialsSwiper = new Swiper(".testimonials-swiper", {
    slidesPerView: 1,
    spaceBetween: 24,
    loop: true,
    autoplay: {
      delay: 4500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".ts-swiper-next",
      prevEl: ".ts-swiper-prev",
    },
    pagination: {
      el: ".ts-pagination",
      clickable: true,
    },

    breakpoints: {
      575: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      767: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
      992: {
        slidesPerView: 4,
        spaceBetween: 24,
      },
    },
  });

  // news swiper
  var newsSwiper = new Swiper(".news-swiper", {
    slidesPerView: 1,
    spaceBetween: 24,
    loop: true,
    autoplay: {
      delay: 4500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".news-swiper-next",
      prevEl: ".news-swiper-prev",
    },
    pagination: {
      el: ".news-pagination",
      clickable: true,
    },

    breakpoints: {
      575: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
    },
  });


  // testimonials swiper 2
  var tsSwiper2 = new Swiper(".ts-swiper-2", {
    slidesPerView: 1,
    spaceBetween: 24,
    loop: true,
    autoplay: {
      delay: 4500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".ts-swiper-2-next",
      prevEl: ".ts-swiper-2-prev",
    },

    breakpoints: {
      575: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
    },
  });

  // disorder swiper
  var disorderSwiper = new Swiper(".disorder-swiper", {
    slidesPerView: 1,
    spaceBetween: 24,
    loop: true,
    autoplay: {
      delay: 4500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".disorder-next",
      prevEl: ".disorder-prev",
    },
    breakpoints: {
      575: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      768: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
      1199: {
        slidesPerView: 4,
        spaceBetween: 24,
      },
    },
  });

  // disorder swiper 2
  var disorderSwiper2 = new Swiper(".disorder-swiper-2", {
    slidesPerView: 1,
    spaceBetween: 24,
    loop: true,
    autoplay: {
      delay: 4500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".disorder-2-next",
      prevEl: ".disorder-2-prev",
    },
    breakpoints: {
      575: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      768: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
      1199: {
        slidesPerView: 4,
        spaceBetween: 24,
      },
    },
  });

  // wow js
  new WOW().init();

  // Odometer
  $(".odometer-item").each(function () {
    $(this).isInViewport(function (status) {
      if (status === "entered") {
        for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
          var el = document.querySelectorAll(".odometer")[i];
          el.innerHTML = el.getAttribute("data-odometer-final");
        }
      }
    });
  });


});