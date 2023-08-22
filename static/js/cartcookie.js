function removeProductNav(button) {
    var productId = button.getAttribute("data-product-id-nav");
    const row = document.querySelector(`[data-row-id-nav="${productId}"]`);
    if (row) {
      row.remove();
    }

    var cart = Cookies.get("cart");
    cart = cart ? JSON.parse(cart) : {};
    cart["total_price"] -= cart[productId]["sub_total"];
    const totalPriceElement = document.getElementById("totalPriceNav");
    totalPriceElement.textContent = cart["total_price"];
    delete cart[productId];
    Cookies.set("cart", JSON.stringify(cart));
    alert("succes");
  }


function addNewItem(newItemHtml) {
    var container = document.getElementById("cartItemsContainer");
    container.insertAdjacentHTML("beforeend", newItemHtml);
    }
    document.addEventListener("DOMContentLoaded", function () {
    var quantityForms = document.querySelectorAll(".quantityForm");

    quantityForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
        event.preventDefault();

        var productId = form.getAttribute("data-product-id");
        var productName = form.getAttribute("data-product-name");
        var productPrice = Number(form.getAttribute("data-product-price"));
        var productImage = form.getAttribute("data-product-image");
        var quantityInput = form.querySelector("[name=quantity]");
        var quantity = parseInt(quantityInput.value);

        if (!isNaN(quantity) && quantity > 0) {
            var cart = Cookies.get("cart");
            cart = cart ? JSON.parse(cart) : {};

            if (cart[productId]) {
            cart[productId]["quantity"] += quantity;
            cart[productId]["sub_total"] += quantity * productPrice;
            } else {
            cart[productId] = {
                name: productName,
                price: productPrice,
                image: productImage,
                quantity: quantity,
                sub_total: quantity * productPrice,
            };
            cart["total_price"] = 0;
            }

            let totalPrice = 0;

            for (let key in cart) {
            if (key != "total_price") {
                totalPrice += cart[key]["sub_total"];
            }
            }

    //         var newItemHtml = `
    // <div class="cart-bar__item position-relative d-flex" data-row-id-nav="${productId}">
    //             <div class="thumb">
    //                 <img src="${productImage}" alt="image_not_found">
    //             </div>
    //             <div class="content">
    //                 <h4 class="title">
    //                     <a href="">${productName}</a>
    //                 </h4>
    //                 <span class="price">${productPrice}</span>
    //                 <span class="price">${quantity}</span>

    //                 <button
    //                 type="button"
    //                 class="remove"                 
    //                 data-product-id-nav="${productId}"
    //                 onclick="removeProduct(this)"
    //                 >
    //                 <i class="fal fa-times"></i>
    //                 </button>
    //             </div>
    //         </div>
    // `;
    //         addNewItem(newItemHtml);
    //         // let totalPriceElement = document.getElementById("totalPriceNav");
    //         // totalPriceElement.innerHTML = totalPrice;

            cart["total_price"] = totalPrice;
            Cookies.set("cart", JSON.stringify(cart), { expires: 365 });
            alert("Your item has been added!");
        }
        });
    });
    });

  function removeProduct(button) {
    var productId = button.getAttribute("data-product-id");
    const row = document.querySelector(`[data-row-id="${productId}"]`);
    if (row) {
      row.remove();
    }

    var cart = Cookies.get("cart");
    cart = cart ? JSON.parse(cart) : {};
    cart["total_price"] -= cart[productId]["sub_total"];
    let totalPriceElement = document.getElementById("totalPrice");
    totalPriceElement.textContent = cart["total_price"];
    delete cart[productId];
    Cookies.set("cart", JSON.stringify(cart));
    alert("item has been removed!");
  }