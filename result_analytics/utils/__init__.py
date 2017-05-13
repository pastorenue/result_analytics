# General non-specific utility functions.

def is_ajax(request):
    """
    Check if the supplied request is an AJAX request.

    Since FILEs can't be uploaded using the browser's XMLHttpRequest object, most libraries use a hidden
    <iframe> to handle file uploads.

    It's presently not possible to set custom headers when POST-ing from an iframe, so Django's
    `HttpRequest.is_ajax` method doesn't work for iframes (since it checks for the presence of the
    'X-Requested-With' header).

    To work around this, we pass a hidden 'X-Requested-With' parameter, set to 'XMLHttpRequest', and test
    for that, in addition to the custom header.
    """
    return request.is_ajax() or \
        ('X-Requested-With' in request.POST and request.POST['X-Requested-With'] == 'ScriptedIFrame')
    