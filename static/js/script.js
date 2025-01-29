$(document).ready(function() {
    $("#add-to-cart-btn").on("click", function(){
        let this_button = $(this);
        let index = this_button.attr("data-index")

        let product_id = $(".product-id-" + index).val();
        let product_pid = $(".product-pid-" + index).val();
        let quantity = $(".product-quantity-" + index).val();
        let product_title = $(".product-title-" + index).val();
        let product_price = $(".current-product-price-" + index).text();
        let product_image = $(".product-image-" + index).val();
        let max_quantity = $(".product-max-quantity-" + index).val();
        let product_status = $(".product-status-" + index).val();

        console.log("qty", quantity);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'qty': quantity,
                'max_qty': max_quantity,
                'title': product_title,
                'price': product_price,
                'image': product_image,
                'product_status': product_status
            },
            dataType: 'json',
            beforeSend: function(){

            },
            success: function(response){
                this_button.prop('disabled', true).text('Item Added To Cart');
                $(".cart-items-count").text(response.totalcartitems);
            }
        });
    });

    $(document).on("click", ".delete-product", function(){
        let product_id = $(this).attr("data-product")
        let this_button = $(this)

        $.ajax({
            url:"/delete-from-cart",
            data: {
                'id': product_id
            },
            dataType: "json",
            beforeSend: function(){
                this_button.prop('disabled', true)
            },
            success: function(response){
                this_button.prop('disabled', false)
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    $(document).on("click", ".refresh-product", function(){
        let product_id = $(this).attr("data-product");
        let this_button = $(this);
        let product_qty = $(".product-qty-" + product_id).val();

        $.ajax({
            url:"/refresh-cart",
            data: {
                'id': product_id,
                'qty': product_qty
            },
            dataType: "json",
            beforeSend: function(){
                this_button.prop('disabled', true)
            },
            success: function(response){
                this_button.prop('disabled', false)
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    $(".checkout-btn").on("click", function(){
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let stripe_public_key = $(".STRIPE_PUBLIC_KEY").val();
        var stripe = Stripe(stripe_public_key);
        var checkoutButton = $(this);
        fetch("/create-checkout-session/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (session) {
                return stripe.redirectToCheckout({ sessionId: session.id  });
            })
            .then(function (result) {
                if (result.error) {
                    alert(result.error.message);
                }
            })
            .catch(function (error) {
                console.error("Error:", error)
            });

    });

    $(".large-img-container").find(".large-img").on("mouseover", function() {
        $(this).css({ transform: "scale(" + $(this).closest('.large-img-container').data("scale") + ")" });
    })
    .on("mouseout", function() {
        $(this).css({ transform: "scale(1)" });
    })
    .on("mousemove", function(e) {
        $(this).css({
            "transform-origin":
            ((e.pageX - $(this).offset().left) / $(this).width()) * 50 +
            "% " +
            ((e.pageY - $(this).offset().top) / $(this).height()) * 50 +
            "%"
        });
    });       
});

// Navbar

function toggle() {
    const toggleButton = document.getElementsByClassName('toggle-button')[0]
    const navbarLinks = document.getElementsByClassName('navbar-links')[0]

    navbarLinks.classList.toggle('active')
}