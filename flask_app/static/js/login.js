document.addEventListener('htmx:afterRequest', function (event) {
    if (event.detail.failed) {
        console.log(event.detail)
        alert(event.detail.xhr.response);
    }
});