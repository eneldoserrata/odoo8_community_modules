$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $('#custom-nav').addClass('affix');
        $('#custom-nav').show();
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $('#custom-nav').removeClass('affix');
        $('#custom-nav').hide();
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
    
});