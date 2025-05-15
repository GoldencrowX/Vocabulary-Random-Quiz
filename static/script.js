document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("user_input");
    input.focus();

    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            this.form.submit();
        }
    });
});
