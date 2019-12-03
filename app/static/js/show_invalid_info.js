/**
 * Created by YM on 2017/1/11.
 */
function show_invalid_info(tag1,tag2,info) {
    $(tag1).removeClass("hide");
    $(tag2)[0].innerHTML = info;
    setTimeout(function () {
        $(tag1).addClass("hide")
    }, 3000);
}

function preview_picture(event) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $(event.data).attr("src", e.target.result);
        $(event.data).css("display", "block");
    };
    reader.readAsDataURL(this.files[0]);
}

function hide_validate_info(ele) {
    $(ele)[0].innerHTML = "";
}