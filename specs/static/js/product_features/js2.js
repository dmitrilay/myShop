$(document).on('click', '#create-validator', function (){
    var catgoryId = $("#category-validators-id").val();
    var featureName = $("#feature-validators-id").val();
    var featureValue = $("#feature-value").val()
    data = {
        category_id: catgoryId,
        feature_name: featureName,
        feature_value: featureValue
    }
    $.ajax({
        method: "GET",
        dataType: "json",
        data:data,
        url: "/product-specs/feature-create/",
        success: function (data){
            if('error' in data){
                $('.errors').append(
                    '<p class="text-center" style="color:red;"><strong>' + data['error'] + '</strong></p>'
                )
            }else{
                console.log('asdasdasdasdasd')
                window.location.href="/product-specs/"
            }
        }
    })
})