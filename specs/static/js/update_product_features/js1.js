$(document).on('click', '#save-updated-features', function (){
    let featureNames = [];
    let featureCurrentValues = [];
    let newFeatureValues = []
   $('.feature-name').children('input').each(function () {
       featureNames.push(this.value); // "this" is the current element in the loop
   })
   $('.feature-current-value').children('input').each(function () {
        featureCurrentValues.push(this.value)
    })
   console.log($("#product-category-features-id option:selected").text())
   $('select[name="feature-value"] option:selected').each(function () {
        newFeatureValues.push(this.text)
  })
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');
    let data = {
        features_names: featureNames,
        features_current_values: featureCurrentValues,
        new_feature_values: newFeatureValues,
        product: $(".product").text(),
        csrfmiddlewaretoken: csrftoken
    }
    $.ajaxSetup({ traditional: true });
    $.ajax({
        method: "POST",
        data: data,
        url: '/product-specs/update-product-features-ajax/',
        success: function (data){
            window.location.href = '/product-specs'
        }
    })
})
function removeProduct(){
    $(".search-results").css('display', 'block')
    $(".product-search-ajax").css('display', 'block')
    $(".product-features-update-list").empty()
}
function getProduct(productId, name){
    $(".product-features-update-list").css('display', 'block')
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
        url: "/product-specs/show-product-features-for-update/",
        success: function (data){
            $(".product-features-update-list").append(
                data.result
            )
        }
    })
}
$('select[name="category-validators"]').on('change', function() {
    $(".product").empty()
    $("#search-product-results").empty()
    $(".product-search-ajax").css('display', 'block')
});
$('input[name="search-text"]').on('input', function(){
if(this.value.length == 0){
    $(".search-results").css('display', 'none')
}else{
    $('.product').empty()
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