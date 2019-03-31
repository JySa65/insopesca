from django.http import HttpResponse


def alert(msg):
    return HttpResponse(
        f"""<script>
            alert("{msg}");
            window.close();
        </script>"""
    )
