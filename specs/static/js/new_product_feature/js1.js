//------------------------------------    
// Создает запрос на создание характеристик для товара
//------------------------------------
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

//------------------------------------
//Если удаляем товар то нужно очистить и скрыть поля
//------------------------------------
function removeProduct(){
    $(".search-results").css('display', 'block')
    $(".product-search-ajax").css('display', 'block')
    $(".product-feature-choices").empty()
    $(".product-feature-choices-values").empty()
}

//------------------------------------    
//Выбор продукта после динамического поиска
//------------------------------------
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
            // alert(data['features'])
            
            var option
            let json = JSON.parse (data['features']);
            for (key in json){
                if (json.hasOwnProperty(key)) {
                    option += `<option value="${json[key][0]}">${json[key][1]}</option>`
                }
            }
            let html =`
                <select class="form-select" name="product-category-features" id="product-category-features-id" aria-label="Default select example">
                    <option selected>---</option>${option}</select>`
            

            $(".product-feature-choices").append(html)
        }
    })
}

//------------------------------------
// Вывод Значения для характеристики
//------------------------------------
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
            var option
            let json = JSON.parse (data['features']);
            for (key in json){
                if (json.hasOwnProperty(key)) {
                    option += `<option value="${json[key][0]}">${json[key][1]}</option>`
                }
            }
            let html =`<select class="form-select" name="product-category-features-choices" id="product-category-features-choices-id" aria-label="Default select example">
            <option selected>---</option>${option}</select>`
            $(".product-feature-choices-values").append(html)
        }
    })
})

//------------------------------------
// 
//------------------------------------ 
$(document).on('change', 'select[name="product-category-features-choices"]', function (){
    $("#create-product-feature").css('display', 'block')
})

$('select[name="category-validators"]').on('change', function() {
$(".product").empty()
$(".errors").empty()
$("#search-product-results").empty()
$(".product-search-ajax").css('display', 'block')
});
    
