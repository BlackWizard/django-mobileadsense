Helpers for using Google AdSense for Mobile in a Django app.


USAGE:

1) Add `adsense` into your INSTALLED_APPS:

    INSTALLED_APPS = [..., "adsense", ...]

2) Display an ad:

    from adsense.adsense import adsense

    def view(request):
        adsense_publisher_id = "get-from-google"
        adsense_slot_id = "get-it-from-example-code-at-google"
        ad = adsense(request, adsense_publisher_id, adsense_slot_id, timeout=1, fail_silently=True)
        return HttpResponse(ad)
        
3) Or in a template:

    {% load adsense_tags %}
    
    <p>Fabulous content.</p>
    {% mobileadsense "adsense_publisher_id" "adsense_slot_id" %}

    If no mobile ads avialable or timeout occured at slot showed code from adsense.html template.
