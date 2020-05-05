let sendToUUID = urlParams.get("sendto");
$.get("/view_profile", {"uuid": sendToUUID}, function(data){
    let currentCard = $("<div class='face-card' style='height: auto'></div>");
    currentCard.append($(`<img id="img_${data.name}" alt="profile picture missing" src="${pfp_path}/${sendToUUID}.png" onerror="this.onerror=null;this.src='${assets_path}/panda.png';"></img>`));

    let nameText = $(`<h2></h2>`);
    nameText.text(data.name);
    currentCard.append(nameText);
    let bioText = $("<p></p>");
    bioText.text(data.bio);
    currentCard.append(bioText);
    $("#sendto_person_profile").append(currentCard);
});

function send_message(){
  $.post("/send_message", {
  "sendto": urlParams.get("sendto"),
  "message": $("#message").val()
  }, (data)=>{
    window.location.href = data;
  });
}

function send_request(){
  $.post("/send_request", {
  "sendto": urlParams.get("sendto")}, (data)=>{
    window.location.href = data;
  });
}

