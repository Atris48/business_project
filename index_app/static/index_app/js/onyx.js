
/*-----------------------------------------------------------
* Template Name    : Onyx | Responsive One Page HTML Template
* Author           : Retrina Group
* Version          : 1.0.0
* Created          : August 2020
* File Description : Main js file of the template
*------------------------------------------------------------
*/

// repeated variables
var $window = $(window);
var $root = $('html, body');

$(document).ready(function () {

    "use strict";
    
    colorScheme();
    colorSchemeTwo();
    sideBarToggler();
    tabBar();
    teamMember();
    testimonialsSlider();
    testimonialsSlider2();
    testimonialsSlider3();
    logoSlider();
    headerSticky();
    headerNavbar();
});

$window.on("load", (function() {
    $("#onyx-preloader").addClass("loaded");

        if ($("#onyx-preloader").hasClass("loaded")) {
            $("#onyx-preloader").delay(900).queue(function () {
                $(this).remove();
            });
        }
    portfolioIsotope();
    headerSticky();

}));
$window.on('scroll', function () {
    headerSticky();
    returnToTop();
    skills();
    countUp();
    
    
});
/*-----------------------------------------------------------------------------
                                   FUNCTIONS
-----------------------------------------------------------------------------*/

/*-------------------------
        Color Scheme
-------------------------*/
function colorScheme(){
    $('.color-scheme').on("click",function() {
        $("body").toggleClass('onyx-dark');
        $('.color-scheme').removeClass('d-none').addClass('d-inline-block');
        $(this).removeClass('d-inline-block').addClass('d-none');
    });
}
/*-------------------------
        Color Scheme 02
-------------------------*/
function colorSchemeTwo(){
    $('.color-scheme').on("click",function() {
        $(".homepage-03").toggleClass('onyx-dark');
        $('.color-scheme').removeClass('d-none').addClass('d-inline-block');
        $(this).removeClass('d-inline-block').addClass('d-none');
    });
}
/*-------------------------
        HEADER STICKY
-------------------------*/
function headerSticky(){

    "use strict";

    if ($window.scrollTop() > 1) {
        $('.top-header-area').addClass('d-none');
        $('#header').addClass('header-sticky');
    } else {
        $('.top-header-area').removeClass('d-none');
        $('#header').removeClass('header-sticky');
    }
}
/*-------------------------
        HEADER NAVBAR
-------------------------*/
function headerNavbar(){

    "use strict";

    $('.navbar-toggler').on('click', function(){
        $('#header').toggleClass('header-bg');
    })
}
/*--------------------------
       RETURN TO TOP
--------------------------*/
function returnToTop() {
    var $returnToTop = $('.return-to-top');
    if ($window.scrollTop() > 150) {
        $returnToTop.addClass('show');
    } else {
        $returnToTop.removeClass('show');
    }
    $returnToTop.on("click",function() {
        $root.stop().animate({
            scrollTop: 0
        }, 1500);
    });
}
/*----------------------------
        Sidebar toggler
----------------------------*/
function sideBarToggler(){
    $('.sidebar-toggler').on('click', function(){
        $('.property-sidebar-sticky ').toggleClass('show');
        $(this).toggleClass('open');
        //$('html, body').toggleClass('fix-hidden');
    });
    $('.report-property-button').on('click', function(){
        $('.report-property-form').toggleClass('open');
    });
}
/*-------------------------
        About Tabs
-------------------------*/
function tabBar(){
    var tabNavItem = $('.tab-boxes .nav-item');
    tabNavItem.on('click', function(){
        tabNavItem.removeClass('active');
        $(this).addClass('active')
    });
    $('#two-tab, #three-tab').on({
        mouseenter: function () {
            $('#one-tab').addClass('grey-color');
        },
        mouseleave: function () {
            $('#one-tab').removeClass('grey-color');
        }
    });
    $('#one-tab, #three-tab').on({
        mouseenter: function () {
            $('#two-tab').addClass('grey-color');
        },
        mouseleave: function () {
            $('#two-tab').removeClass('grey-color');
        }
    });
    $('#two-tab, #one-tab').on({
        mouseenter: function () {
            $('#three-tab').addClass('grey-color');
        },
        mouseleave: function () {
            $('#three-tab').removeClass('grey-color');
        }
    });
}
/*-------------------------
          Skills
-------------------------*/
function skills() {

    "use strict";

    var scroll = $window.scrollTop();
    var skillsDiv = $('.skill-box');
    if(skillsDiv.length > 0){
        var winH = $window.height(),
            skillsT = skillsDiv.offset().top;
        if (scroll + winH > skillsT) {
            $('.skillbar').each(function () {
                $(this).find('.skillbar-bar').animate({
                    width: $(this).attr('data-percent')
                }, 6000);
            });
        }
    }
}
/*-------------------------
            Count up
-------------------------*/
  function countUp() {

    "use strict";

    var scroll = $window.scrollTop();
    var countId = $('.counted');
    if (countId.length){
        var winH = $window.height(),
            countOffset = countId.offset().top;
        if (scroll + winH > countOffset) {
            $('.timer').countTo();
            $('.count-number').removeClass('timer');
        }
    }
}
/*-------------------------
    Team Swiper Js
-------------------------*/
function teamMember() {

    "use strict";

var swiper = new Swiper('.team-member .swiper-container', {
    spaceBetween: 16,
    slidesPerView: 2,
    centeredSlides: true,
    loop: true,
    freeMode: true,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        
        360: {
            centeredSlides: false,
            slidesPerView: 1,
            spaceBetween: 30,
        },
        991: {
            centeredSlides: false,
            slidesPerView: 3,
            spaceBetween: 30,
        },
    }
});
}
/*-------------------------
Testimonial swiper js
-------------------------*/
function testimonialsSlider() {

    "use strict";
    
    var fswiper = new Swiper('#testimonial .swiper-container', {
        spaceBetween: 16,
        loop: true,
        autoplay: false,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
}
/*-------------------------
Testimonial 02 swiper js
-------------------------*/
function testimonialsSlider2() {

    "use strict";
    
    var fswiper = new Swiper('#testimonial2 .swiper-container', {
        spaceBetween: 16,
        loop: true,
        autoplay: false,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            500: {
                spaceBetween: 30,
            },
            776: {
                centeredSlides: false,
                slidesPerView: 2,
                spaceBetween: 30,
            },
            1200: {
                centeredSlides: false,
                slidesPerView: 3,
                spaceBetween: 30,
            },
        }
    });
}
/*-------------------------
Testimonial 03 swiper js
-------------------------*/
function testimonialsSlider3() {

    "use strict";
    
    var fswiper = new Swiper('#testimonial3 .swiper-container', {
        spaceBetween: 16,
        loop: true,
        autoplay: false,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            500: {
                spaceBetween: 30,
            },
            1200: {
                centeredSlides: false,
                slidesPerView: 2,
                spaceBetween: 30,
            }
        }
    });
}
/*-------------------------
    Logo  Swiper Js
-------------------------*/
function logoSlider() {

    "use strict";

    var swiper = new Swiper('.logo-box .swiper-container', {
        spaceBetween: 16,
        slidesPerView: 2,
        centeredSlides: true,
        loop: true,
        freeMode: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            500: {
                spaceBetween: 30,
            },
            768: {
                centeredSlides: false,
                slidesPerView: 4,
                spaceBetween: 30,
            },
        }
    });

}
/*-------------------------
        ISOTOPE JS
-------------------------*/
function portfolioIsotope() {

    "use strict";

    var $container = $('.portfolio-items');
    var $filter = $('#portfolio-filter');
    $container.isotope({
        filter: '*',
        layoutMode: 'masonry',
        originLeft: false,
        animationOptions: {
            duration: 750,
            easing: 'linear'
        }
    });
    $filter.find('a').on("click",function() {
        var selector = $(this).attr('data-filter');
        $filter.find('a').removeClass('active');
        $(this).addClass('active');
        $container.isotope({
            filter: selector,
            animationOptions: {
                animationDuration: 750,
                easing: 'linear',
                queue: false,
                touchSensitivity: 2,
            }
        });
        return false;
    });
}
/*-------------------------
     AJAX CONTACT FORM
-------------------------*/
function validateEmail(email) {

    "use strict";

    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function sendEmail() {

    "use strict";

    var name     = $('#name').val();
    var family   = $('#family').val();
    var email    = $('#email').val();
    var phone    = $('#subject').val();
    var comments = $('#comments').val();

    if(!name){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('نام خود را وارد کنید.');
    }else if(!family){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('نام خانوادگی خود را وارد کنید.');
    }else if(!email){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('ایمیل خود را وارد کنید.');
    } else if(!validateEmail(email)){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('ایمیل معتبر نیست.');
    } else if(!phone){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('تلفن خود را وارد کنید.');
    }else if(!comments){
        $('#message').toast('show').addClass('bg-danger').removeClass('bg-success');
        $('.toast-body').html('متن پیام خود را وارد کنید.');
    }else {
        $.ajax({
            type: 'POST',
            data: $("#contactForm").serialize(),
            url:  "sendEmail.php",
            beforeSend: function() {
                $('#submit-btn').html('<span class="spinner-border spinner-border-sm"></span> Loading..');
            },
            success: function(data) {
                $('#submit-btn').html('Submit');
                var myObj = JSON.parse(data);
                if(myObj['status']=='پیغام'){
                    $('#message').toast('show').addClass('bg-success').removeClass('bg-danger bg-warning');
                    $('.toast-body').html('<strong>'+ myObj['status'] +' : </strong> '+ myObj['message']);
                }else if(myObj['status']=='خطا'){
                    $('#message').toast('show').addClass('bg-danger').removeClass('bg-success bg-warning');
                    $('.toast-body').html('<strong>'+ myObj['status'] +' : </strong> '+ myObj['message']);
                }else if(myObj['status']=='هشدار'){
                    $('#message').toast('show').addClass('bg-warning').removeClass('bg-success bg-danger');
                    $('.toast-body').html('<strong>'+ myObj['status'] +' : </strong> '+ myObj['message']);
                }
            },
            error: function(xhr) {
                $('#submit-btn').html('Submit');
                $('#message').toast('show').addClass('bg-danger').removeClass('bg-success bg-warning');
                $('.toast-body').html('<strong> خطا : </strong> مشکلی پیش آمده است. لطفا بعدا امتحان کنید.');
            },
        });
    }
}


