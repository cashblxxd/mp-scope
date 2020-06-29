
$(function () {
    
    
    function visibility(item){
        item.css({
          "visibility":"visible",
        }).animate({"opacity": "1"},600);
      }

      function hideVisibility(item){
        item.css({
          "visibility":"hidden",
        }).animate({"opacity": "0"},600);
      }

    $(".submit-button").click(function(){
        visibility($("#successScreen"));
    })
$("#settings-close").click(function(){
    hideVisibility($(".accounts__settings"))
    hideVisibility($(".accounts__settings-list"))
    hideVisibility($(".accounts__settings-heading"))
    $("#settings-open").animate({
        'color':'#767676'
    },300,'easeInOutQuint')
})
$("#settings-open").click(function(){
    visibility($(".accounts__settings"))
    visibility($(".accounts__settings-list"))
    visibility($(".accounts__settings-heading"))
    $("#settings-open").animate({
        'color':'#14B2F3'
    },300,'easeInOutQuint')
})
    $(".ok-button").click(function(){
        hideVisibility($("#successScreen"));
    })

    $("#accounts__main-hover-2").mouseover(function(){
        $(".accounts__main-line-active").animate({
            "left":"540px",
        },300,'easeInOutQuint')
    });

    $("#accounts__main-hover-2").mouseleave(function(){
        $(".accounts__main-line-active").attr('style','left:382px');
    });


    $("#accounts__main-hover-one").mouseover(function(){
        $(".accounts__main-line-active").animate({
            "left":"382px",
        },300,'easeInOutQuint')
    });

    $("#accounts__main-hover-one").mouseleave(function(){
        $(".accounts__main-line-active").attr('style','left:540px');
    });

$(".accounts__header-search__input").on('change', 'input', function() {

    $(".accounts__header-search__icon").animate({"color": "#14B2F3"},200);

})





    $(".alert").delay(4000).queue(function (next) { 
        $(this).fadeOut(600, function () {
            $(this).remove();
        });
        next(); 
      });






    function checkRegistration() {
        if (formValidReg.email && formValidReg.password && formValidReg.repeatpassword && formValidReg.checked) {
          $('#regButton').removeAttr('disabled');
        } else {
          $('#regButton').attr('disabled', true); 
        }
      }
    
      var formValidReg = {
          email:false,
          password:false,
          repeatpassword:false,
          checked:false

         
      };
    
        $("#email").on('input', function() {
          var email = $(this).val(); // Assign input value to a variable
          
          // Function to assign message to paragraph tag
          function msg(body) {
              $('#email-feedback').text(body).show();
            };
          
            // Function to hide paragraph tag
            function hide() {
              $('#email-feedback').hide();
            };
        
    
          // Check if e-mail value is at least 1 character
          if (email.length < 1) {
            msg('Это поле обязательно'); // Assign error message to DOM.
            formValidReg.email = false; // Set input as invalid
            checkRegistration(); // Perform validation check
          } else {
            hide(); // Hide previous error message
            formValidReg.email = true; // Set input as valid
    
            checkRegistration(); // Perform validation check
            var testExp = new RegExp(/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/); // Regular Expression to test against e-mail value
            // Check if e-mail value passes regular expression test
            if (!testExp.test(email)) {
              msg('Неверный формат почты'); // Return custom error message
              formValidReg.email = false; // Set input as invalid

              checkRegistration(); // Perform validation check
            } else {
              hide(); // Hide previous error messages
              formValidReg.email = true; // Set input as invalid
              checkRegistration(); // Perform validation check
            
            }
          }
    
    
      });
    
      $('#password').on('input', function() {
        var password = $(this).val(); // Assign input value to a variable
      
        // Function to assign message to paragraph tag
        function msg(body) {
            $('#password-feedback').text(body).show(0);
          };
        
          // Function to hide paragraph tag
          function hide() {
            $('#password-feedback').hide(0);
          };
      
        // Check if e-mail value is at least 1 character
        if (password.length < 1) {
          msg('Это поле обязательно'); // Assign error message to DOM.
          formValidReg.password = false; // Set input as invalid

          checkRegistration(); // Perform validation check
        }
           else {
            hide(); // Hide previous error messages
            formValidReg.password = true; // Set input as invalid
      
            checkRegistration(); // Perform validation check
            // Check if e-mail value meets length requirements
            if (password.length < 8) {
        
              msg('Должно быть 8 символов'); // Return custom error message to DOM
              formValidReg.password = false; // Set input as invalid
              checkRegistration(); // Perform validation check
            
            } else {
              hide(); // Hide previous error message
              formValidReg.password = true; // Set input as valid
      
              checkRegistration(); // Perform validation check
            }
           }        
      });



      $('#repeatpassword').on('input', function() {
        var repeartpassword = $(this).val(); // Assign input value to a variable
        var password = $('#password').val();
        // Function to assign message to paragraph tag
        function msg(body) {
            $('#repeatpassword-feedback').text(body).delay(100).show(200);
          };
        
          // Function to hide paragraph tag
          function hide() {
            $('#repeatpassword-feedback').delay(100).hide(0);
          };
      
        // Check if e-mail value is at least 1 character
        if (repeartpassword != password) {
          msg('Пароли не совпадают'); // Assign error message to DOM.
          formValidReg.repeatpassword = false; // Set input as invalid

          checkRegistration(); // Perform validation check
        }
           else {
            hide();
            formValidReg.repeatpassword = true; 
 

            checkRegistration(); 

        
          }

  });




  $('#checkbox').change(function()
  {
    if ($(this).is(':checked')) {
        formValidReg.checked = true; 
        checkRegistration(); 
    }
    else{
        formValidReg.checked = false; 
        checkRegistration(); 
    }
  });






});
  




















