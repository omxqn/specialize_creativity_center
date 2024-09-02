/* 
 ========= main JS documentation ==========================

 * theme name: HealthEase Template
 * version: 1.0
 * description: Workplace Html5 Template
 * author: softivus
 * author url: 
    ==================================================
    sticky navbar
    menu bar toggle 
    sub menu toggle
    pre loader
    back to top
    Current Year
*/

"use strict";
$(document).ready(function () {

    // sticky navbar
    window.addEventListener("scroll", function () {
        document.querySelector('header').classList.toggle('sticky', window.scrollY > 0)
    })

    // menu bar toggle 
    let menuBar = document.getElementsByClassName('menu-bar')[0]
    let menuIcon = document.getElementsByClassName('menu-icon')[0]
    menuIcon.addEventListener('click', function () {
        menuBar.classList.toggle('show-menu')
    })

    // sub menu toggle
    let showSubMenu = document.querySelectorAll('.has-children')
    let subMenu = document.querySelectorAll('.sub-menu')
    let navArrow = document.querySelectorAll('.nav-arrow')
    for (let i = 0; i < showSubMenu.length; i++) {
        showSubMenu[i].addEventListener('click', function () {
            subMenu[i].classList.toggle('show-sub')
            navArrow[i].classList.toggle('rotate-arrow')
        })
    }


    //Preloader
    setTimeout(function () {
        $('#preloader').fadeToggle();
    }, 1000);


    // back to top
    var backToTop = $('#back-to-top');

    $(window).scroll(function () {
        if ($(window).scrollTop() > 300) {
            backToTop.addClass('show-preloader');
        } else {
            backToTop.removeClass('show-preloader');
        }
    });

    backToTop.on('click', function (e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, '300');
    });

    // Current Year
    $(".currentYear").text(new Date().getFullYear());


});