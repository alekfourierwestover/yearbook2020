

$.get("/get_uuid", function(uuid){
  $.get("/view_profile", {"uuid": uuid}, function(data){
    let currentCard = $("<div class='face-card' style='height:auto'></div>");
    currentCard.append($(`<img id="img_${uuid}" alt="profile picture missing" src="${pfp_path}/${uuid}.png" onerror="this.onerror=null;this.src='${assets_path}/panda.png';"></img>`));

    let nameText = $("<h2></h2>");
    nameText.text(data.name);
    currentCard.append(nameText);

    let bioText = $("<p></p>");
    bioText.text(data.bio);
    currentCard.append(bioText);
    $("#myprofile").append(currentCard);
  });
});

$.get("/view_my_messages", function(data){
  if(data == "no messages"){
    $.notify("no messages yet");
  }
  else{
    let allCards = $("<ul id='stick'></ul>");
    for(let sender_person in data){
      let currentCard = $("<div class='sticky'></div>");
      currentCard.append($(`<h2>messages from ${sender_person}</h2>`));
      for(let message in data[sender_person]){
	let stickyMessageText = $("<p></p>");
        stickyMessageText.text(`message: ${data[sender_person][message]}`);
        currentCard.append(stickyMessageText);
      }
      let currentSticky = $("<li></li>");
      currentSticky.append(currentCard);
      $("#stick").append(currentSticky);
    }
  }
});
