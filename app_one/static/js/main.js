$(document).ready(function() {
    // $('#summernote').summernote();
    $('#summernote').summernote({
        toolbar: [
          // [groupName, [list of button]]
          ['style', ['bold', 'italic', 'underline', 'fontsize', 'fontname', 'color']],
          ['para', ['ul', 'ol', 'paragraph', 'height']],
          ['font', ['superscript', 'subscript']],
          ['insert', ['picture', 'video', 'link' , 'table', 'hr']],
          ['misc', ['codeview', 'fullscreen', 'undo', 'redo' ]],
        ]
    });
});




// Hide sidebar if clicked outside of the sidebar
// *****************************************************************
$(document).mouseup(function(e) 
{
    var container = $("#sidebar_container");
    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0) 
    {
        sidebar2.hide()
        sidebar1.show()
    }
});



// On the mobile view: Hide sidebar with menu when link to Note clicked
// *****************************************************************
if($(window).width() <= 420) {
    $('a.sidebar_post_link').click( function(){
        sidebar2.hide()
        sidebar1.show()
    });
}


// On the mobile view: show pop out with Topic creation, need to scrol up to see it. 
// *****************************************************************
if($(window).width() <= 420) {
    $(".sidebar2_title_right").click( function() {
        $(window).scrollTop(0);
    });
}


// CREATE THEME POP OUT 
// *****************************************************************
$('.sidebar2_title_right').click(function(){ 
    $('#popout1').css('display', 'block');
})

$('#close_popout1').click(function(){
    $('#popout1').css('display', 'none');
})


// Show Notes when Topick clicked on the sidebar
// *****************************************************************
let theme_link = $('.theme_link')
let theme_posts = $('.sidebar_all_posts_container')
$('.show_posts_option').click(function(){
    $(this).parent().siblings().toggle();
})


// SIDEBAR HIDE AND SHOW
// *****************************************************************
let sidebar1 = $('.sidebar1')
let sidebar2 = $('.sidebar2')
$('.image_container1').click(function(){
    sidebar1.hide()
    sidebar2.show()
})
$('.image_container2').click(function(){
    sidebar2.hide()
    sidebar1.show()
})


// DROPDOWN NEXT TO PROFILE ICON
// *****************************************************************
let arrow_up =  $("#initials_arrow_up");
let arrow_down =  $("#initials_arrow_down");
$('#nav_right').click(function(){
    $('#drop_menu_container ').toggle(); 
    arrow_down.toggle(function () {
        arrow_down.addClass("display_none");
    }, function () {
        arrow_down.removeClass("display_none");
    });
    arrow_up.toggle(function () {
        arrow_up.addClass("display_block");
    }, function () {
        arrow_up.removeClass("display_block");
    });
})


