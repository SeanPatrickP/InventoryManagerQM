$(function() {
    $('.delete-button').click(delete_item);
    function delete_item() {
        if(this && this.parentNode && this.parentNode.elements && this.parentNode.elements.productIdInput && this.parentNode.elements.productIdInput.value) {
            var id = this.parentNode.elements.productIdInput.value;
            var baseEP = '/inventory/deleteItem/?productId=';
            var endPoint = baseEP.concat(id);
            $.ajax({
                url: endPoint,
                type: 'DELETE',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'deleted' && result.productId) {
                        var idPrefix = "#"
                        id = idPrefix.concat(result.productId)
                        $(id).remove()
                    }
                }
            });
        }
    }

    $('.update-button').click(update_item);
    function update_item() {
        if(this && this.parentNode && this.parentNode.elements && this.parentNode.elements.productIdInput && this.parentNode.elements.productIdInput.value) {
            var id = this.parentNode.elements.productIdInput.value;
            var quantity = this.parentNode.elements.quantityInput.value;
            var price = this.parentNode.elements.priceInput.value;
            var endPoint = '/inventory/updateItem/';
            $.ajax({
                url: endPoint,
                type: 'PUT',
                data : {
                    'productId': id,
                    'price': price,
                    'quantity': quantity,
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                }
            });
        }
    }

    $('.add-button').click(add_item);
    function add_item() {
        if(this && this.parentNode && this.parentNode.elements && this.parentNode.elements.productIdInput && this.parentNode.elements.productIdInput.value) {
            var id = this.parentNode.elements.productIdInput.value;
            var quantity = this.parentNode.elements.quantityInput.value;
            var price = this.parentNode.elements.priceInput.value;
            var description = this.parentNode.elements.descriptionInput.value;
            var endPoint = '/inventory/insertItem/';
            $.ajax({
                url: endPoint,
                type: 'POST',
                data : {
                    'description': description,
                    'productId': id,
                    'price': price,
                    'quantity': quantity,
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'inserted') {
                        var form = $("#addItemForm");
                        form.trigger("reset")
                        var productId = $("#productIdInput");
                        var endPoint = '/inventory/getItemsCount/';

                        productId = $.ajax({
                            url: endPoint,
                            type: 'GET',
                            beforeSend: function(xhr) {
                                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                            },
                            success: function(result) {
                                if(result) {
                                    result = JSON.parse(result)
                                }
                                if(result) {
                                    var productId = $("#productIdInput");
                                    productId.val(result)
                                }
                            }
                        });
                    }
                }
            });
        }
    }

    $('.sell-button').click(sell_item);
    function sell_item() {
        var saleId = $("#saleId");
        if(this && this.parentNode && this.parentNode.elements && this.parentNode.elements.productIdInput && this.parentNode.elements.productIdInput.value && saleId) {
            var id = this.parentNode.elements.productIdInput.value;
            var baseEP = '/inventory/addItemToSell/?productId=';
            var endPoint = baseEP.concat(id);
            endPoint = endPoint.concat('&saleId=');
            endPoint = endPoint.concat(saleId[0].outerText);
            this.parentNode.elements.sellButton.disabled = true;
            $.ajax({
                url: endPoint,
                type: 'GET',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'sold' && result.price) {
                        result = 'Total £ ' + result.price;
                        var total = $("#totalPrice");
                        total.text(result);
                    }
                }
            });
        }
    }

    $('.sell-selected-button').click(sell_selected_items);
    function sell_selected_items() {
        var saleId = $("#saleId");
        if(saleId) {
            endPoint = '/inventory/sellSelected/';
            $.ajax({
                url: endPoint,
                type: 'PUT',
                data : {
                    'saleId': saleId[0].outerText,
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'sold' && result.itemsUpdated) {
                        updatedProducts = result.itemsUpdated
                        updatedProducts.forEach(updateProduct);

                        function updateProduct(item) {
                            var idPrefix = "#"
                            id = idPrefix.concat(item.productId)
                            var quantityField = $(id);
                            quantityField.val(item.quantity)
                        }

                        var sellButton = $("#sellSelected");
                        sellButton.prop('disabled', true)

                        var sellButtons = $("button.sell-button");
                        sellButtons.prop('disabled', true)
                    }
                }
            });
        }
    }
 });
 