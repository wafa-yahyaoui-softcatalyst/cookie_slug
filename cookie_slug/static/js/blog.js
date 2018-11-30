$(function () {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});


// A $( document ).ready() block.
$(document).ready(function () {
    console.log("ready!");
    //display_post();
    display_list_posts();
    // Submit post on submit
    $("#FormUpdatePost").on('submit', function (event) {
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        update_post();

    });


// AJAX for displaying post
 function display_post() {
        console.log("create post is working!") // sanity check
        var pk = window.location.pathname.split("/")[2]
        var url_action = "/post/".concat(pk, "/edit/ajax/")

        $.ajax({
            url: url_action, // the endpoint
            type: "GET", // http method
            dataType: "json",

            // handle a successful response
            success: function (json) {
                var title = json.title
                var post_text = json.text
                $("#post_title").text(title)
                $("#post_text").text(post_text)
                console.log(post_text)
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };



// AJAX for updating post
    function update_post() {
        console.log("Update Post is working!") // sanity check
        var form = document.forms.namedItem("FormUpdatePostName");
        var formData = $(form).serializeArray();
        var post = window.location.pathname.split("/")[2]
        var url_action = "/post/".concat(post, "/edit/ajax/")
         console.log(formData);
        console.log(url_action)
        $.ajax({
            url: url_action, // the endpoint
            type: "POST", // http method
            data: formData, // data sent with the post request

            // handle a successful response
            success: function (json) {
                console.log("success"); // another sanity check
                $("#ModalDismissButton").click();
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // AJAX for displaying  list of posts
 function display_list_posts() {
        console.log("display list of posts is working!") // sanity check
        $.ajax({
            url: '/', // the endpoint
            type: "GET", // http method
            dataType: "json",

            // handle a successful response
            success: function (json) {
                var posts = []
                json.forEach(function (post) {
                    var post_bloc = "<div class='post'><div class='date'>".concat(post.published_date,
                         "</div><h2><a href= '/post/",
                        post.pk,
                        "'>",
                        post.title,
                         "</a></h2 ><a class='btn btn-default btn-lg' onclick='ClickButtonDelete(this);' data-toggle='modal'  data-target='#DeleteModal' name='",
                        post.pk,
                        "'><span class='glyphicon glyphicon-remove'></span></a><p>",
                        post.text,
                        "</p>")

                    posts.push(post_bloc)

                })
                $("#PostsList").html(posts)
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

 // AJAX for deleting a post


     $("#ModalDeleteButton").click(function(){
         console.log($("#DeleteButton"))
         console.log($('input[name="csrfmiddlewaretoken"]').attr('value'))

        $.ajax({
            url: "/post/delete/".concat(this.name, "/"), // the endpoint
            type: "POST", // http method
            data:{pk:this.name,
            csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').attr('value')},
            // handle a successful response
            success: function (json) {
                console.log(json)
                console.log("success"); // another sanity check
                display_list_posts();
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });


//setInterval(display_post, 2000);
});

 function ClickButtonDelete(element) {
         console.log("clicked")
     console.log(element.name)
    $("#ModalDeleteButton").attr("name",element.name)}


