$(document).on('click', "#create-product-feature", function (){
        let product = $("#product-title").text()
        let category_feature = $("#product-category-features-id option:selected").text()
        let value = $("#product-category-features-choices-id option:selected").text()
        let data = {
            product: product,
            category_feature: category_feature,
            value: value
        }
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            url: '/product-specs/attach-new-product-feature/',
            success: function (data){
                console.log('asdasd')
            }
        })
    })
    function removeProduct(){
        $(".search-results").css('display', 'block')
        $(".product-search-ajax").css('display', 'block')
        $(".product-feature-choices").empty()
        $(".product-feature-choices-values").empty()
    }
    function getProduct(productId, name){
        $('.product').append(
            '<div class="alert alert-info alert-dismissible show" id="product-title" role="alert">' + name +
            '<button type="button" onclick="removeProduct()" ' +
            'class="btn-close" data-bs-dismiss="alert" aria-label="Close">' +
            '</button>' +
            '</div>'
        )
        $(".search-results").css('display', 'none')
        $("#search-product-results").empty()
        $(".product-search-ajax").css('display', 'none')
        $(".product-feature-choices").css('display', 'block')
        $(".product-feature-choices-values").css('display', 'block')
        $('input[name="search-text"]').val("")
        let data = {
            product_id: productId
        }
        $.ajax({
            method: "GET",
            data:data,
            dataType: "json",
            url: "/product-specs/attach-feature/",
            success: function (data){
                $(".product-feature-choices").append(data.features)
            }
        })
    }
    $(document).on('change', 'select[name="product-category-features"]', function (){
        let data = {
            category_id: this.value,
            product_feature_name: $("#product-category-features-id option:selected").text()
        }
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            url: "/product-specs/product-feature/",
            success: function (data){
                $(".product-feature-choices-values").append(data.features)
            }
        })
    })
    $(document).on('change', 'select[name="product-category-features-choices"]', function (){
        $("#create-product-feature").css('display', 'block')
    })
    $('select[name="category-validators"]').on('change', function() {
    $(".product").empty()
    $(".errors").empty()
    $("#search-product-results").empty()
    $(".product-search-ajax").css('display', 'block')
    });
    $('input[name="search-text"]').on('input', function(){
    if(this.value.length == 0){
        $(".search-results").css('display', 'none')
    }else{
        $(".search-results").css('display', 'block')
    }
    $("#search-product-results").empty()
    let data = {
        query: this.value,
        category_id: $('select[name="category-validators"] option').filter(':selected').val()
    }

    $.ajax({
    method: "GET",
    dataType: "json",
    data: data,
    url: "/product-specs/search-product/",
    success: function(data){
        let items = []
        if(data.result.length < 1){
            $('#no-results').css('display', 'block')
        }else{
            $('#no-results').css('display', 'none')
        }
        $.each(data, function (index, value) {
            $.each(value, function (idx, v){
                if($.inArray(v, items) == -1){
                    items.push(v)
                    $('#search-product-results').append(
                        '<li class="list-group-item list-group-item-action" ' +
                        'onclick="getProduct(\'' + v.id + '\', \'' + v.name + '\')" ' +
                        'style="cursor: pointer" id="product-' +
                        v.id + '">'
                        + v.name +
                        ' | ' +
                        v.price +
                        ' руб.' +
                        '</li>')
                        }
                    })
                })
            }
        })
    })