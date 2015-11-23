/**
 * Created by Nightsuki on 2015/11/23.
 */

$('.pjax').click(function () {
    $('body').animate({
        scrollTop: 0
    })
});

$(document).ready(function () {
    $('body').materialScrollTop({
        revealElement: 'header',
        revealPosition: 'bottom'
    });
    $(".post-content").find('a[href^="http"]').each(function () {
        $(this).attr('target', '_blank');
    });
});

$(document).on('pjax:start', function () {
    $('.mdl-progress').show();
});

$(document).on('pjax:end', function () {
    $('.mdl-progress').hide();
});

// Pjax
$(document).pjax('.pjax', '.container');