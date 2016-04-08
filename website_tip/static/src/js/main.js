$(document).ready(function() {
    $('a[data-tipso]').each(function() {
        hook_tipso($(this));
    });
});

function hook_tipso(element) {
    var a = element;

    a.tipso('hide').tipso('destroy');

    if (!a.attr('data-tipso'))
        return;

    var settings = {
        'useTitle': false
    }

    if (a.attr('data-tipso-position'))
        settings['position'] = a.attr('data-tipso-position');
    if (a.attr('data-tipso-background'))
        settings['background'] = a.attr('data-tipso-background');
    if (a.attr('data-tipso-color'))
        settings['color'] = a.attr('data-tipso-color');
    if (a.attr('data-tipso-animationin'))
        settings['animationIn'] = a.attr('data-tipso-animationin');
    if (a.attr('data-tipso-animationout'))
        settings['animationOut'] = a.attr('data-tipso-animationout');

    a.tipso(settings);

    if (a.attr('data-tipso-onload'))
        a.tipso('show');
}