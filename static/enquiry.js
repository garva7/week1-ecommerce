$(document).ready(function () {
    $("#enquiryModal").on("show.bs.modal", function () {
        $("#enquiry-form")[0].reset();
        $("#enquiry-alert").addClass("d-none").html("");
        $(".form-control, .form-select").removeClass("is-invalid");
        $(".invalid-feedback").text("");
    });

    $("#enquiry-submit").on("click", function () {
        if (validateEnquiry()) {
            submitEnquiry();
        }
    });

    function validateEnquiry() {
        let valid = true;

        $(".form-control, .form-select").removeClass("is-invalid");
        $(".invalid-feedback").text("");

        const name = $("#enq-name").val().trim();
        if (!name) {
            showError("enq-name", "err-name", "Name is required.");
            valid = false;
        }

        const email = $("#enq-email").val().trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            showError("enq-email", "err-email", "Email is required.");
            valid = false;
        } else if (!emailRegex.test(email)) {
            showError("enq-email", "err-email", "Enter a valid email address.");
            valid = false;
        }

        const phone = $("#enq-phone").val().trim();
        const phoneRegex = /^[0-9]{10}$/;
        if (!phone) {
            showError("enq-phone", "err-phone", "Phone number is required.");
            valid = false;
        } else if (!phoneRegex.test(phone)) {
            showError("enq-phone", "err-phone", "Enter a valid 10-digit phone number.");
            valid = false;
        }

        const type = $("#enq-type").val();
        if (!type) {
            showError("enq-type", "err-type", "Please select an enquiry type.");
            valid = false;
        }

        const desc = $("#enq-description").val().trim();
        if (!desc) {
            showError("enq-description", "err-description", "Description is required.");
            valid = false;
        } else if (desc.length < 10) {
            showError("enq-description", "err-description", "Description must be at least 10 characters.");
            valid = false;
        }

        return valid;
    }

    function showError(fieldId, errorId, message) {
        $("#" + fieldId).addClass("is-invalid");
        $("#" + errorId).text(message);
    }

    function submitEnquiry() {
        const data = {
            name: $("#enq-name").val().trim(),
            email: $("#enq-email").val().trim(),
            phone: $("#enq-phone").val().trim(),
            type: $("#enq-type").val(),
            description: $("#enq-description").val().trim()
        };

        $.ajax({
            url: "/enquiry",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (response) {
                showAlert("success", response.message || "Enquiry submitted successfully!");
                $("#enquiry-form")[0].reset();
            },
            error: function () {
                showAlert("danger", "Something went wrong. Please try again.");
            }
        });
    }

    function showAlert(type, message) {
        $("#enquiry-alert")
            .removeClass("d-none alert-success alert-danger")
            .addClass("alert alert-" + type)
            .html(message);
    }

});