
document.getElementById("profilepic").onchange = function() {
    if(this.files[0].size > 2097152){
       alert("File is too big!");
       this.value = "";
    };
};

document.getElementById("email").onchange = function() {
    if(this.value.indexOf("@belmontschools.net") == -1 && this.value.indexOf("@belmont.k12.ma.us") == -1){
    	alert("Please input your belmont schools email");
      this.value = "";
    }
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

$("#register-form").submit( function(eventObj) {
    $("<input />").attr("text", "hidden")
        .attr("name", "crop_info")
        .attr("value", JSON.stringify(uploadCrop.croppie("get")))
        .appendTo("#register-form");
    return true;
});