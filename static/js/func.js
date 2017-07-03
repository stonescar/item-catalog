$(document).ready(function() {
    window.setTimeout(function() {
        $(".alert-dismissible").slideUp();
    }, 3000);
});

function validateForm(type) {
    if (type == "del") {
        if ($("#confirm").prop("checked") == false) {
            $(".checkbox").wrap("<div class='has-error'></div>");
            $(".checkbox").append("<b><-- Check this checkbox to confirm</b>");
            return false;
        }
    } else {
        name = $("#name").val();
        if (name == "") {
            $("#name-group").addClass("has-error");
            if (type == "new") {
                $("#err-mess").show().html("Name is required");
            } else if (type == "edit") {
                $("#err-mess").show().html("Name cannot be empty");
            }
            return false;   
        }
    }
}