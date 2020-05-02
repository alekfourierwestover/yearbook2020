
if(urlParams.get("error")){
  $.notify(urlParams.get("error"));
}

document.getElementById("profilepic").onchange = function() {
    if(this.files[0].size > 2097152){
       alert("File is too big!");
       this.value = "";
    };
};


let uploadCrop;
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#profilepic_display').attr('src', e.target.result);
      uploadCrop = $('#profilepic_display').croppie({
        enableExif: true,
        viewport: {
            width: 200,
            height: 200,
            type: 'square'
        },
        boundary: {
            width: 300,
            height: 300
        }
      });
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#profilepic").change(function() {
  readURL(this);
});

$("#edit_picture").submit( function(eventObj) {
    $("<input />").attr("text", "hidden")
        .attr("name", "crop_info")
        .attr("value", JSON.stringify(uploadCrop.croppie("get")))
        .appendTo("#edit_picture");
    return true;
});


function showEdit(which_edit){
  let all_edits = ["#edit_pfp", "#edit_college", "#edit_quote", "#edit_pwd"];
  for(let i in all_edits){
    $(all_edits[i]).css("display", "none");
  }
  $(which_edit).css("display", "block");
}
showEdit("#edit_pfp");

