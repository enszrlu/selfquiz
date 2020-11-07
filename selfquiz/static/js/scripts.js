/*!
    * Start Bootstrap - Creative v6.0.3 (https://startbootstrap.com/themes/creative)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
    */
    (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery); // End of use strict


$('body').on('click', '.next', function() {

    var id = $('.content:visible').data('id');
    var nextId = $('.content:visible').data('id')+1;
    $('[data-id="'+id+'"]').hide();
    $('[data-id="'+nextId+'"]').show();

    if($('.back:hidden').length == 1){
        $('.back').show();
    }

    var checked = false;

    $("input:radio:visible").each(function() {
      var name = $(this).attr("name");
      if ($("input:radio:visible:checked").length != 0) {
        checked = true;
      }
    });
    if (!checked)
    {
      document.getElementById("next").disabled = true;
    }


    if(nextId == $('.end').data('id')){
        var answerElems = document.getElementsByClassName("answer");
        count=answerElems.length;
        correctAnswers=0;
        for (var i=0; i<answerElems.length; i++) {
          if (answerElems[i].type == "radio" && answerElems[i].checked == true){
              correctAnswers++;
          }
        }

        $('#score').text("Your Score: "+correctAnswers+"/"+count);

        $('.content-holder').hide();
        $('.back').hide();
        $('.next').hide();
        $('.end').show();



    }
});

$('body').on('click', '.back', function() {
    var id = $('.content:visible').data('id');
    var prevId = $('.content:visible').data('id')-1;
    $('[data-id="'+id+'"]').hide();
    $('[data-id="'+prevId+'"]').show();

    if(prevId == 0){
        $('.back').hide();
    }
    document.getElementById("next").disabled = false;
});

$('body').on('click', '.edit-previous', function() {
    var prevId = $('.end').data('id')-1;
    $('.end').hide();
    $('.content-holder').show();
    $('[data-id="'+prevId+'"]').show();
    $('.next').show();
    if(prevId != 0){
        $('.back').show();
    }
    document.getElementById("next").disabled = false;
});

$('body').on('click', '.choices', function() {
    document.getElementById("next").disabled = false;
});

$('body').on('click', '.show-answers', function() {
    $('.end').hide();
    $('.answers').show();
});

$('body').on('click', '.question', function() {
  var questions=document.getElementsByClassName("question")
  checkedCount = 0;

  for (var i = 0; i < questions.length; i++) {
    if (questions[i].checked == true) {
      checkedCount++;
    }
  }

  if(checkedCount > 1) {
    document.getElementById("create").disabled = false;
  }
  else {
    document.getElementById("create").disabled = true;
  }

});

$('body').on('click', '.create', function() {
  if (confirm('Are you sure that you want to save this quiz to your database?')) {
    var questions=document.getElementsByClassName("question");

    for (var i = 0; i < questions.length; i++) {
      if (questions[i].checked == true) {
        question_list=document.getElementById("question-list");
        question_list.value = question_list.value + questions[i].value + ",";
      }
    }
    question_list.value = question_list.value.substring(0, question_list.value.length - 1)

    document.getElementById("createQuiz").submit();
    console.log('Quiz is saved to the database.');
  }
  else {
    // Do nothing!
    console.log('Quiz is not saved to the database.');
  }
});

$('body').on('click', '.edit_question', function() {
  var fired_button = "editQuestion"+$(this).val();
  if (confirm('Are you sure that you want to edit this question?')) {
    document.getElementById(fired_button).submit();
    console.log('Question will be editted.');
  }
  else {
    // Do nothing!
    console.log('Question will not be editted');
  }
});

$('body').on('click', '.delete_question', function() {
  var fired_button = "deleteQuestion"+$(this).val();
  if (confirm('Are you sure that you want to delete this question?')) {
    document.getElementById(fired_button).submit();
    console.log('Question will be deleted.');
  }
  else {
    // Do nothing!
    console.log('Question will not be editted');
  }
});

$('body').on('click', '.save_question', function() {
  if (confirm('Are you sure that you want to edit this question?')) {
    document.getElementById("saveEdittedQuestion").submit();
    console.log('Question will be editted.');
  }
  else {
    // Do nothing!
    console.log('Question will not be editted');
  }
});

$('body').on('click', '.quiz', function() {
  var quizes=document.getElementsByClassName("quiz")
  checkedCount = 0;

  if (this.checked == true) {
    for (var i = 0; i < quizes.length; i++) {
      quizes[i].checked = false
    }
    this.checked = true
    document.getElementById("start_quiz").disabled = false;
    document.getElementById("start_quiz").innerText = "Start Selected Quiz";
  }
  else {
    document.getElementById("start_quiz").disabled = false;
    document.getElementById("start_quiz").innerText = "Start Random Quiz";
  }

});

$('body').on('click', '.edit_quiz', function() {
  var fired_button = "editQuiz"+$(this).val();
  if (confirm('Are you sure that you want to edit this quiz?')) {
    document.getElementById(fired_button).submit();
    console.log('Quiz will be editted.');
  }
  else {
    // Do nothing!
    console.log('Quiz will not be editted');
  }
});

$('body').on('click', '.delete_quiz', function() {
  var fired_button = "deleteQuiz"+$(this).val();
  if (confirm('Are you sure that you want to delete this quiz?')) {
    document.getElementById(fired_button).submit();
    console.log('Quiz will be deleted.');
  }
  else {
    // Do nothing!
    console.log('Quiz will not be editted');
  }
});

$('body').on('click', '.share_quiz', function() {
  var fired_button = "shareQuiz"+$(this).val();
  if (confirm('Are you sure that you want to share this quiz with everyone?')) {
    document.getElementById(fired_button).submit();
    console.log('Quiz will be shared.');
  }
  else {
    // Do nothing!
    console.log('Quiz will not be shared');
  }
});

$('body').on('click', '.start_quiz_button', function() {
  var fired_button = "startQuiz"+$(this).val();
  if (confirm('Are you sure that you want to start this quiz?')) {
    document.getElementById(fired_button).submit();
    console.log('Quiz will be started.');
  }
  else {
    // Do nothing!
    console.log('Quiz will not be started.');
  }
});


$('body').on('click', '.start_quiz', function() {
  if (confirm('Are you sure that you want to start this quiz?')) {
    var quizes=document.getElementsByClassName("quiz");

    for (var i = 0; i < quizes.length; i++) {
      if (quizes[i].checked == true) {
        selected_quiz=document.getElementById("selected_quiz");
        selected_quiz.value = quizes[i].value;
        break
      }
    }

    document.getElementById("startQuiz").submit();
    console.log('Quiz will be started.');
  }
  else {
    // Do nothing!
    console.log('No Action.');
  }
});