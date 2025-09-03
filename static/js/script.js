// Declare svgs
const openedIcon = [
            '<path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 ',
            '.708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 ',
            '0 0 1-.708-.708L7.293 8z"/> Menula'
        ].join("");
const closedIcon = [
            '<path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 ',
            '.5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 ',
            '0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5',
            '0 0 1-.5-.5"/> Menule'
        ].join("");
const deleteItem = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"',
    ' class="bi bi-trash-fill toggle-amount" style="opacity: 0.75;" viewBox="0 0 16 16"><path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 ',
    '0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0',
    ' 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1',
    ' .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1',
    ' 0v-7a.5.5 0 0 1 1 0"/></svg>'
].join("");
const reduce = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" ',
    'fill="currentColor" class="bi bi-dash-lg toggle-amount" viewBox="0 0 16 16"><path ',
    'fill-rule="evenodd" d="M2 8a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11A.5.5 0 0 ',
    '1 2 8"/></svg>'
].join("");
const eye = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" ',
    'fill="currentColor" class="bi bi-eye password-toggle" viewBox="0 0 16 16"><path ',
    'd="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 ',
    '13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 ',
    '2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 ',
    '1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 ',
    '0 0 1 1.172 8z"/><path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 ',
    '0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/></svg>'
].join("");
const canceled_eye = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" ',
    'fill="currentColor" class="bi bi-eye-slash password-toggle" viewBox="0 0 16 16">',
    '<path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 ',
    '0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 ',
    '2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 ',
    '1.12-1.465 1.755q-.247.248-.517.486z"/><path d="M11.297 9.176a3.5 ',
    '3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 ',
    '1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 ',
    '2.829"/><path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 ',
    '8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 ',
    '12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 ',
    '8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 ',
    '12 12z"/></svg>'
].join("");
// Declare A.I. conversational elements
const userMessage = '<div class="user-question"><div class="user-message"><p class="text user-message">'
const assistantMessage = '<div class="assistant-message"><p class="text assistant-message">'

/*
Show and hide the navigation bar whenever the 'Menu' button is clicked on portrait mode,
do not hide the navigation bar on landscape mode
*/
// Check for clicks on the 'Menu' button
$("button.menu").click(function () {
    // Check if the navigation bar is showing(display: flex) or if it's hidden(display: none)
    // and change the 'Menu' button's icon accordingly
    if ($("div.links-container").css("display") === "flex") {
        $("svg.menu-icon").html(closedIcon);
    } else {
        $("svg.menu-icon").html(openedIcon);
    }
    // Animate the navigation bar's show/hide process to slide out/in
    $("div.links-container").slideToggle();
})


// If the page orientation changes from landscape to portrait mode
// and the navigation bar is not hidden, hide the navigation bar, and
// if the page orientation changes from portrait to landscape mode and the
// navigation bar is hidden, unhide the navigation bar
var screenOrientation = window.matchMedia("(orientation: portrait)");
screenOrientation.addEventListener("change", detectChange)


function detectChange(portraitState) {
    if (portraitState.matches) {
        $("div.links-container").css("display", "none");
        $("svg.menu-icon").html(closedIcon);
    } else {
        if ($("div.links-container").css("display") === "none") {
            $("div.links-container").css("display", "flex");
        }
    }
}


detectChange(screenOrientation);


// Fade the hero in.
//window.onload(function () {
//    $("div.hero-prompt").fadeOut();
//})

$(document).ready(function () {
    setInterval(function () {$(".hero-body, .hero-actions, h2.home-testifies, div.home-testifies, a.more-testimonies").fadeIn(500)}, 500)
  });



// Show navigation bar only when scrolling up
var currentScroll = window.scrollY || document.documentElement.scrollTop;
window.addEventListener("scroll", function () {
    var lastScroll = currentScroll;
    currentScroll = window.scrollY || document.documentElement.scrollTop;
    if (currentScroll < 0) { // Default all negative values to 0. 
        currentScroll = 0;
    }
    if (currentScroll > lastScroll) {
        $("div.navigation-container").slideUp(333);
    } else if (currentScroll < lastScroll) {
        $("div.navigation-container").slideDown(333);
    }
});


////        Transparent navbar effect
//        if (currentScroll === 0) {
//            if (window.innerWidth > window.innerHeight) {
//              $("div.navigation-container").css("background", "transparent");
//            }
//        } else {
//            $("div.navigation-container").css("background", "#2b3035");
//        }


// // Convert text version to title case
// function toTitleCase(str) {
//     return str.charAt(0).toUpperCase() + str.slice(1);
// }


 


// // Make each design section show or hide their content, also add their emojis
// function activateDesign(design, emoji) {
//     const business_html1 = '<p class="text design-type"><b>▲ ' + emoji + ' ' + toTitleCase(design) + ' Designs</b></p>';
//     const business_html2 = '<p class="text design-type"><b>▼ ' + emoji + ' ' + toTitleCase(design) + ' Designs</b></p>';
//     $("div." + design).click(() => {
//     $("div." + design + "-designs").toggleClass("hidden");
//     if ($("div." + design + "-designs").hasClass("hidden")) {
//         console.log(true)
//         $("div." + design).html(business_html1);
//     } else {
//         console.log(false)
//         $("div." + design).html(business_html2);
//     }
// })
// }


// activateDesign("business", "💼");
// activateDesign("portfolio", "🗂️");
// activateDesign("blog", "📝");
// activateDesign("personal", "👨🏼‍💼");


// Show or hide the 'Must read' full text when the 'more' or 'less' span element is clicked

// var information = $("div.information").html();
// $("div.information").html(information.slice(0, 440) + '<span class="text must-read"> ...more</span>')

// $("div.information").on("click", "span.must-read", function () {
//     if ($(this).text() === " ...more") {
//         $("div.information").html(information.slice(0, -38) + '<span class="text must-read"> less</span>' + information.slice(-39, -1));    
//     } else if ($(this).text() === " less") {
//         $("div.information").html(information.slice(0, 440) + '<span class="text must-read"> ...more</span>')
//     }
// })


// scroll the page to the list of designs on-click
$("span.touch-designs").click(function () {
    document.querySelector("div.design.business").scrollIntoView({behavior: "smooth"})
})







//  Projects page
$("div.business").click(() => {
    $("div.business-designs").toggleClass("hidden");
    if ($("div.business-designs").hasClass("hidden")) {
        $("div.business").html('<p class="text design-type"><b>▲ 1. 🔐 Authentication System</b></p>');
    } else {
        $("div.business").html('<p class="text design-type"><b>▼ 1. 🔐 Authentication System</b></p>');
    }
});
$("div.portfolio").click(() => {
    $("div.portfolio-designs").toggleClass("hidden");
    if ($("div.portfolio-designs").hasClass("hidden")) {
        $("div.portfolio").html('<p class="text design-type"><b>▲ 2. 📤 Picture Upload Manager</b></p>');
    } else {
        $("div.portfolio").html('<p class="text design-type"><b>▼ 2. 📤 Picture Upload Manager</b></p>');
    }
});
$("div.blog").click(() => {
    $("div.blog-designs").toggleClass("hidden");
    if ($("div.blog-designs").hasClass("hidden")) {
        $("div.blog").html('<p class="text design-type"><b>▲ 3. 🛒 E-commerce Platform</b></p>');
    } else {
        $("div.blog").html('<p class="text design-type"><b>▼ 3. 🛒 E-commerce Platform</b></p>');
    }
});
$("div.personal").click(() => {
    $("div.personal-designs").toggleClass("hidden");
    if ($("div.personal-designs").hasClass("hidden")) {
        $("div.personal").html('<p class="text design-type"><b>▲ 4. 🤖 AI-Powered Writing Assistant</b></p>');
    } else {
        $("div.personal").html('<p class="text design-type"><b>▼ 4. 🤖 AI-Powered Writing Assistant</b></p>');
    }
});


// Upload section
$("div.upload-house").click(function () {
    $("input.upload-picture").click();
});

$("input.upload-picture").change(function () {
    if ($("input.upload-picture")[0].files.length > 0) {
        const fileName = $("input.upload-picture")[0].files[0].name;
        $("p.file-name").text(fileName);
        $("p.file-name").css("color", "#FF90BB");
    } else {
        $("p.file-name").text("No file chosen");
    }
});


// Upload Item section
$("div.upload-home").click(function () {
    $("input.upload-photo").click();
});

$("input.upload-photo").change(function () {
    if ($("input.upload-photo")[0].files.length > 0) {
        const fileName = $("input.upload-photo")[0].files[0].name;
        $("p.file-title").text(fileName);
        $("p.file-title").css("color", "#FF90BB");
    } else {
        $("p.file-title").text("No file chosen");
    }
});


// Load store
document.addEventListener("DOMContentLoaded", () => {
    const pageName = document.querySelector('meta[name="page-name"]').getAttribute("content");

    if (pageName === "store" || "cart" || "item" || "checkout" || "orders" || "order") {
        fetch("/load-store/api")
        .then(response => response.json())
        .then(function(data)  {
            document.querySelector("p.item-count").textContent = data["cart_length"];
            document.querySelectorAll("a.item-button").forEach(function(item) {
                const itemId = Number(item.getAttribute("data-item-id"));
                $("div.item-button[data-item-id='" + itemId + "']").removeClass("hidden");
                const currentUserId = Number(item.getAttribute("data-current-user-id"));
                data["product_ids"].forEach(content => {
                    const buyerId = data["buyer_ids"][data["product_ids"].indexOf(itemId)]
                    if (buyerId === currentUserId) {
                        var quantity = 0;
                        data["items_ids"].forEach(item => {
                            if (item === itemId) {
                                quantity++;
                            }
                        })
                        $("div.item-button[data-item-id='" + itemId + "']").addClass("hidden");
                        $("p.item-quantity[data-item-id='" + itemId + "']").text(quantity + " item(s) selected");
                        $("div.quantity-buttons[data-item-id='" + itemId + "']").removeClass("hidden");
                    } else {
                        $("div.item-button[data-item-id='" + itemId + "']").removeClass("hidden");
                    }
                })
            });
        });
    }
})


// add-to-cart
document.querySelectorAll("a.item-button").forEach(function(item) {
    item.addEventListener("click", function(event) {
        event.preventDefault()
        const itemId = Number(item.getAttribute("data-item-id"));
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("/add-to-cart/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "item_id": itemId
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            document.querySelector("p.item-count").textContent = data["cart_length"];
            $("div.item-button[data-item-id='" + itemId + "']").addClass("hidden");
            $("p.item-quantity[data-item-id='" + itemId + "']").text(data["quantity"] + " item(s) selected");
            $("div.quantity-buttons[data-item-id='" + itemId + "']").removeClass("hidden");
            })
        });
    })


// Reduce-quantity buttons for store and cart pages
document.querySelectorAll("a.reduce-quantity").forEach(function(item) {
    item.addEventListener("click", function(event) {
        event.preventDefault()
        const itemId = Number(item.getAttribute("data-item-id"));
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("/reduce-quantity/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "item_id": itemId
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            if (data["quantity"] === 0) {
                $("div.quantity-buttons[data-item-id='" + itemId + "']").addClass("hidden");
                $("div.item-button[data-item-id='" + itemId + "']").removeClass("hidden");
                $("div.cart-item[data-item-id='" + itemId + "']").css("display", "none")
            } else if (data["quantity"] === 1) {
                $("a.reduce-amount[data-item-id='" + itemId + "']").html(deleteItem);
                $("p.item-quantity[data-item-id='" + itemId + "']").text(data["quantity"] + " item(s) selected");
                $("p.item-amount[data-item-id='" + itemId + "']").text(data["quantity"]);
            } else{
                $("p.item-quantity[data-item-id='" + itemId + "']").text(data["quantity"] + " item(s) selected");
                $("p.item-amount[data-item-id='" + itemId + "']").text(data["quantity"]);
            }
            document.querySelector("p.item-count").textContent = data["cart_length"];
            document.querySelector("b.total-price").textContent = data["total_price"].toLocaleString('en-NG', { style: 'currency', currency: 'NGN' });
            if (data["cart_length"] === 0) {
                $("a.checkout-button").css("display", "none");
                $("div.total").css("display", "none");
                $("div.empty-cart").removeClass("hidden")
            }
            $("a.checkout-button").text("Proceed to checkout (" + data["cart_length"] + " items[s])")
        })
    })
});


// Increase-quantity buttons for store and cart pages
document.querySelectorAll("a.increase-quantity").forEach(function(item) {
    item.addEventListener("click", function(event) {
        event.preventDefault()
        const itemId = Number(item.getAttribute("data-item-id"));
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("/increase-quantity/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "item_id": itemId
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            $("p.item-quantity[data-item-id='" + itemId + "'], p.item-amount[data-item-id='" + itemId + "']").text(data["quantity"] + " item(s) selected");
            $("p.item-amount[data-item-id='" + itemId + "']").text(data["quantity"]);
            document.querySelector("p.item-count").textContent = data["cart_length"];
            if (data["quantity"] !== 1) {
                $("a.reduce-amount[data-item-id='" + itemId + "']").html(reduce);
            }
            document.querySelector("b.total-price").textContent = data["total_price"].toLocaleString('en-NG', { style: 'currency', currency: 'NGN' });
            $("a.checkout-button").text("Proceed to checkout (" + data["cart_length"] + " items[s])")
        })
    })
});


// Make every item image on the store home page a button that links to it's information
document.querySelectorAll("img.item-image").forEach(function(item) {
    item.addEventListener("click", function() {
        const itemId = item.getAttribute("data-item-id");
        document.querySelector("a.item-information.id-" + itemId).click();
    })
})


// Load cart page
document.addEventListener("DOMContentLoaded", () => {
    const pageName = document.querySelector('meta[name="page-name"]').getAttribute("content");

    if (pageName === "cart") {
        document.querySelectorAll("a.reduce-amount").forEach(item => {
            const quantity = Number(item.getAttribute("data-quantity"));
            if (quantity === 1) {
                item.innerHTML = deleteItem;
            }
        })
    }
});


// Delete item from cart
document.querySelectorAll("a.delete-item").forEach(item => {
    item.addEventListener("click", function(event) {
        event.preventDefault()
        const itemId = Number(item.getAttribute("data-item-id"));
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("/delete-item/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "item_id": itemId
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            $("div.cart-item[data-item-id='" + itemId + "']").css("display", "none");
            if (data["cart_length"] === 0) {
                $("a.checkout-button").css("display", "none");
                $("div.total").css("display", "none");
                document.querySelector("p.item-count").textContent = data["cart_length"];
                $("div.empty-cart").removeClass("hidden")
            }
        })
    })
});




document.addEventListener("DOMContentLoaded", () => {
    const pageName = document.querySelector('meta[name="page-name"]').getAttribute("content");

    if (pageName === "store" || "cart" || "item" || "checkout" || "orders" || "order") {
        // Reduce count on 'Item' page
        document.querySelector("a.reduce-count").addEventListener("click", function(event) {
            event.preventDefault();
            const itemId = Number(document.querySelector("a.reduce-count").getAttribute("data-item-id"));
            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch("/reduce-quantity/api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": token
                },
                body: JSON.stringify({
                    "item_id": itemId
                })
            })
            .then(response => response.json())
            .then(data => {
                    if (data["quantity"] === 0) {
                        $("div.count-buttons[data-item-id='" + itemId + "']").addClass("hidden");
                        $("a.add-item[data-item-id='" + itemId + "']").removeClass("hidden");
                    } else{
                        $("p.item-size[data-item-id='" + itemId + "']").text(data["quantity"]);
                    }
                    document.querySelector("p.item-count").textContent = data["cart_length"];
            });
        })
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const pageName = document.querySelector('meta[name="page-name"]').getAttribute("content");

    if (pageName === "store" || "cart" || "item" || "checkout" || "orders" || "order") {
        // Increase count on 'Item' page
        document.querySelector("a.increase-count").addEventListener("click", function(event) {
            event.preventDefault()
            const itemId = Number(document.querySelector("a.increase-count").getAttribute("data-item-id"));
            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch("/increase-quantity/api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": token
                },
                body: JSON.stringify({
                    "item_id": itemId
                })
            })
            .then(response => response.json())
            .then(function(data)  {
                $("p.item-size[data-item-id='" + itemId + "']").text(data["quantity"]);
                document.querySelector("p.item-count").textContent = data["cart_length"];
            })
        });
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const pageName = document.querySelector('meta[name="page-name"]').getAttribute("content");

    if (pageName === "store" || "cart" || "item" || "checkout" || "orders" || "order") {
        
        // Add to cart from 'Item' page
        document.querySelector("a.add-item").addEventListener("click", function(event) {
            event.preventDefault()
            const itemId = Number(document.querySelector("a.add-item").getAttribute("data-item-id"));
            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch("/add-to-trolley/api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": token
                },
                body: JSON.stringify({
                    "item_id": itemId
                })
            })
            .then(response => response.json())
            .then(function(data)  {
                $("a.add-item[data-item-id='" + itemId + "']").addClass("hidden");
                $("p.item-size[data-item-id='" + itemId + "']").text(data["quantity"]);
                $("div.count-buttons[data-item-id='" + itemId + "']").removeClass("hidden");
                document.querySelector("p.item-count").textContent = data["cart_length"];
            })
        });
    }
});


// Implement a password visibility toggle
function togglePassword(buttonClass, inputClass) {
    const inputField = document.querySelector("input." + inputClass);
    if (inputField.type === "password") {
        inputField.type = "text";
        $("button." + buttonClass).html(canceled_eye);  // change icon to "hide"
    } else {
        inputField.type = "password";
        $("button." + buttonClass).html(eye);  // change back to "show"
    }
}


// Open the A.I. menu bar on click
document.querySelector("button.ai-menu").addEventListener("click", function() {
    document.querySelector("button.send-button").disabled = true;
    const menu = document.querySelector("div.ai-menu");
    menu.classList.remove("slide-left");
    menu.classList.add("slide-right");
    menu.style.left = 0;
});


function closeNav() {
    document.querySelector("button.send-button").disabled = false;
    const menu = document.querySelector("div.ai-menu");
    menu.classList.remove("slide-right");
    menu.classList.add("slide-left");
    if (window.matchMedia("(orientation: landscape)").matches) {
        setTimeout(() => {
            menu.style.left = "-66vw";
        }, 600)
    } else if (window.matchMedia("(orientation: portrait)").matches) {
        setTimeout(() => {
            menu.style.left = "-66vw";
        }, 300)
    } else {
        setTimeout(() => {
            menu.style.left = "-66vw";
        }, 300)
    }
}


// Close the A.I. menu bar on click (portrait mode only)
document.querySelector("button.close-ai").addEventListener("click", function() {
    closeNav();
});


document.querySelector("form.message-form").addEventListener('submit', function(event) {
    event.preventDefault();
});


// Scroll to last user message
function scrollTolastUserMessage() {
    let elements = document.querySelectorAll('p.user-message');
    if (elements.length > 0) {
    elements[elements.length - 1].scrollIntoView();
    }
}


// Let A.I. Think
function think() {
    const assistantMessage = document.createElement("div");
    assistantMessage.classList.add("assistant-message", "thinking");
    assistantMessage.innerHTML = "<p class='text assistant-message thinking' style='color: #89918C'></p>";
    document.querySelector("div.messages").appendChild(assistantMessage);
    const textArray = [" ●", "●●", "●●●", "●●●●"]
    var itemIndex = 0;
    setInterval(function() {
        document.querySelector("p.assistant-message.thinking").textContent = textArray[itemIndex];
        itemIndex += 1;
        if (itemIndex === 4) {
            itemIndex = 0;
        }
    }, 250)
}


// Send the A.I. a message
document.querySelector("button.send-button").addEventListener("click", function() {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const chatButton = document.querySelector("button.send-button");
    const chatId = Number(chatButton.getAttribute('data-chat-id'));
    if (chatId === 0) {
        const input = document.querySelector("textarea.message-box");
        const message = input.value;
        input.value = "";
        document.querySelector("div.ai-greeting").style.display = "none";
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-question");
        userMessage.innerHTML = "<div class='user-message'><p class='text user-message'>" + message + "</p></div>";
        document.querySelector("div.messages").appendChild(userMessage);
        think();
        fetch("/ping-ai/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "message": message
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            document.querySelector("div.assistant-message.thinking").remove();
            const elementsClass = "assistant-message";
            const assistantMessage = document.createElement("div");
            assistantMessage.classList.add(elementsClass);
            assistantMessage.innerHTML = "<p class='text assistant-message id-" + data["message_id"] + "'></p>";
            document.querySelector("div.messages").appendChild(assistantMessage);
            var typed =  new Typed("p.assistant-message.id-" + data["message_id"], {
            strings: [data["output"]],
            typeSpeed: 5,
            startDelay: 0,
            showCursor: false
            });
            chatButton.setAttribute("data-chat-id", data["chat_id"]);
            const parentElement = document.querySelector('div.ai-menu');
            if (data["no_chats"] === true) {
                const chatsLabel = document.createElement("div");
                chatsLabel.classList.add("text", "chats-label"); 
                chatsLabel.textContent = "Chats";
                parentElement.appendChild(chatsLabel)
            }
            const chat = document.createElement("button");
            chat.classList.add("old-chat");
            chat.setAttribute('data-chat-id', data["chat_id"]);
            chat.textContent = data["chat_title"];
            const referenceChild = document.querySelector('button.old-chat');
            parentElement.insertBefore(chat, referenceChild);
            activateChatButton(chat);
        });
    } else {
        const input = document.querySelector("textarea.message-box");
        const message = input.value;
        input.value = "";
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-question");
        userMessage.innerHTML = "<div class='user-message'><p class='text user-message'>" + message + "</p></div>";
        document.querySelector("div.messages").appendChild(userMessage);
        scrollTolastUserMessage()
        think();
        fetch("/update-ai/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "chat_id": chatId,
                "message": message
            })
        })
        .then(response => response.json())
        .then(function(data)  {
            document.querySelector("div.assistant-message.thinking").remove();
            const elementsClass = "assistant-message";
            const assistantMessage = document.createElement("div");
            assistantMessage.classList.add(elementsClass);
            assistantMessage.innerHTML = "<p class='text assistant-message id-" + data["message_id"] + "'></p>";
            document.querySelector("div.messages").appendChild(assistantMessage);
            var typed =  new Typed("p.assistant-message.id-" + data["message_id"], {
            strings: [data["output"]],
            typeSpeed: 4,
            startDelay: 0,
            showCursor: false
            });
            chatButton.setAttribute("data-chat-id", chatId)
        });
    }
});


// Activate A.I. past-chat's button
function activateChatButton(accessPoint) {
    accessPoint.addEventListener("click", function(event) {
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        document.querySelector("div.ai-greeting").style.display = "none";
        const chatId = Number(accessPoint.getAttribute("data-chat-id"));
        fetch("/open-chat/api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token
        },
        body: JSON.stringify({
            "chat_id": chatId
        })
        })
        .then(response => response.json())
        .then(function(data)  {
            var html = "";
            data["messages"].forEach(function(message) {
                if (message["role"] === "user") {
                    html += userMessage + message["message"] + "</p></div></div>"
                } else if (message["role"] === "model") {
                    html += assistantMessage + message["message"] + "</p></div>"
                }
            });
            document.querySelector("div.messages").innerHTML = html;
            scrollTolastUserMessage()
            const parentElement = document.querySelector('div.ai-menu');
            const referenceChild = document.querySelector('button.old-chat');
            parentElement.insertBefore(event.target, referenceChild);
            closeNav();
            const chatButton = document.querySelector("button.send-button");
            chatButton.setAttribute('data-chat-id', chatId);
        });
    });
}


// Activate all A.I. past-chats' buttons
document.querySelectorAll("button.old-chat").forEach(function(button) {
    activateChatButton(button);
})


// Initiate a new A.I. chat
document.querySelector("button.new-chat").addEventListener("click", function() {
    document.querySelector("button.send-button").setAttribute("data-chat-id", 0);
    document.querySelectorAll("div.user-question").forEach(function(div) {
        div.style.display = "none";
    })
    document.querySelectorAll("div.assistant-message").forEach(function(div) {
        div.style.display = "none";
    })
    
    document.querySelector("div.ai-greeting").style.display = "flex";
    window.scrollTo(0, 0);
    closeNav();
});


